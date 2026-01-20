from fastapi import APIRouter, HTTPException, Depends, status
from sqlalchemy.orm import Session
from datetime import datetime
from app.core.database import get_db
from app.core.security import get_password_hash, verify_password, create_access_token
from app.models.user import User, OTPCode, UserSignup, VerifyOTP, UserLogin, Token, UserResponse
from app.services.email import EmailService

router = APIRouter(prefix="/auth", tags=["Authentication"])


@router.post("/signup", status_code=status.HTTP_201_CREATED)
async def signup(user_data: UserSignup, db: Session = Depends(get_db)):
    """
    Register a new user and send OTP to email for verification.
    
    Steps:
    1. Check if username or email already exists
    2. Create user account (unverified)
    3. Generate and send OTP to email
    """
    # Check if username already exists
    existing_user = db.query(User).filter(
        (User.username == user_data.username) | (User.email == user_data.email)
    ).first()
    
    if existing_user:
        if existing_user.username == user_data.username:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Username already registered"
            )
        else:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Email already registered"
            )
    
    # Create new user
    hashed_password = get_password_hash(user_data.password)
    new_user = User(
        name=user_data.name,
        username=user_data.username,
        email=user_data.email,
        role=user_data.role.value,
        hashed_password=hashed_password,
        is_verified=False
    )
    
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    
    # Generate OTP
    otp = EmailService.generate_otp()
    otp_expiry = EmailService.get_otp_expiry()
    
    # Store OTP in database
    otp_record = OTPCode(
        email=user_data.email,
        code=otp,
        expires_at=otp_expiry,
        is_used=False
    )
    db.add(otp_record)
    db.commit()
    
    # Send OTP email
    await EmailService.send_otp_email(user_data.email, otp, user_data.name)
    
    return {
        "message": "User registered successfully. Please check your email for OTP verification.",
        "email": user_data.email,
        "username": user_data.username
    }


@router.post("/verify-otp")
async def verify_otp(verify_data: VerifyOTP, db: Session = Depends(get_db)):
    """
    Verify OTP and activate user account.
    """
    # Find the most recent unused OTP for this email
    otp_record = db.query(OTPCode).filter(
        OTPCode.email == verify_data.email,
        OTPCode.code == verify_data.otp,
        OTPCode.is_used == False
    ).order_by(OTPCode.created_at.desc()).first()
    
    if not otp_record:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid OTP code"
        )
    
    # Check if OTP has expired
    if datetime.utcnow() > otp_record.expires_at:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="OTP code has expired. Please request a new one."
        )
    
    # Mark OTP as used
    otp_record.is_used = True
    
    # Activate user account
    user = db.query(User).filter(User.email == verify_data.email).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    
    user.is_verified = True
    db.commit()
    
    return {
        "message": "Email verified successfully. You can now login.",
        "verified": True
    }


@router.post("/login", response_model=Token)
async def login(login_data: UserLogin, db: Session = Depends(get_db)):
    """
    Login with username/email and password.
    
    Returns JWT access token upon successful authentication.
    """
    # Find user by username or email
    user = db.query(User).filter(
        (User.username == login_data.username_or_email) | 
        (User.email == login_data.username_or_email)
    ).first()
    
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username/email or password",
            headers={"WWW-Authenticate": "Bearer"}
        )
    
    # Verify password
    if not verify_password(login_data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username/email or password",
            headers={"WWW-Authenticate": "Bearer"}
        )
    
    # Check if user is verified
    if not user.is_verified:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Please verify your email first. Check your inbox for OTP."
        )
    
    # Create access token
    access_token = create_access_token(data={"sub": user.username})
    
    user_response = UserResponse.from_orm(user)
    
    return Token(
        access_token=access_token,
        token_type="bearer",
        user=user_response
    )


@router.post("/resend-otp")
async def resend_otp(email: str, db: Session = Depends(get_db)):
    """
    Resend OTP to user's email.
    """
    # Check if user exists
    user = db.query(User).filter(User.email == email).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    
    if user.is_verified:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User is already verified"
        )
    
    # Mark previous OTPs as used
    db.query(OTPCode).filter(
        OTPCode.email == email,
        OTPCode.is_used == False
    ).update({"is_used": True})
    
    # Generate new OTP
    otp = EmailService.generate_otp()
    otp_expiry = EmailService.get_otp_expiry()
    
    # Store new OTP
    otp_record = OTPCode(
        email=email,
        code=otp,
        expires_at=otp_expiry,
        is_used=False
    )
    db.add(otp_record)
    db.commit()
    
    # Send OTP email
    await EmailService.send_otp_email(email, otp, user.name)
    
    return {
        "message": "OTP has been resent to your email",
        "email": email
    }
