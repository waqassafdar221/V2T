import random
import string
from datetime import datetime, timedelta
from typing import Optional
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from app.core.config import settings


class EmailService:
    """Service for sending emails and managing OTP codes."""
    
    @staticmethod
    def generate_otp(length: int = 6) -> str:
        """Generate a random OTP code."""
        return ''.join(random.choices(string.digits, k=length))
    
    @staticmethod
    async def send_otp_email(email: str, otp: str, name: str) -> bool:
        """
        Send OTP verification email via SMTP.
        
        Falls back to console logging if SMTP is not configured.
        """
        try:
            # Check if SMTP is configured
            if settings.smtp_host and settings.smtp_user and settings.smtp_password:
                # Send actual email
                msg = MIMEMultipart('alternative')
                msg['From'] = settings.smtp_user
                msg['To'] = email
                msg['Subject'] = f"{settings.app_name} - Email Verification"
                
                # Create HTML email body
                html_body = f'''
                <html>
                <head>
                    <style>
                        body {{ font-family: Arial, sans-serif; line-height: 1.6; color: #333; }}
                        .container {{ max-width: 600px; margin: 0 auto; padding: 20px; }}
                        .header {{ background-color: #4CAF50; color: white; padding: 20px; text-align: center; }}
                        .content {{ background-color: #f9f9f9; padding: 30px; border-radius: 5px; margin-top: 20px; }}
                        .otp-code {{ font-size: 32px; font-weight: bold; color: #4CAF50; text-align: center; 
                                     padding: 20px; background-color: #fff; border: 2px dashed #4CAF50; 
                                     border-radius: 5px; margin: 20px 0; letter-spacing: 5px; }}
                        .footer {{ text-align: center; margin-top: 20px; color: #666; font-size: 12px; }}
                    </style>
                </head>
                <body>
                    <div class="container">
                        <div class="header">
                            <h1>{settings.app_name}</h1>
                        </div>
                        <div class="content">
                            <h2>Welcome, {name}!</h2>
                            <p>Thank you for signing up. To complete your registration, please verify your email address.</p>
                            <p>Your verification code is:</p>
                            <div class="otp-code">{otp}</div>
                            <p><strong>This code will expire in {settings.otp_expire_minutes} minutes.</strong></p>
                            <p>If you didn't request this code, please ignore this email.</p>
                        </div>
                        <div class="footer">
                            <p>This is an automated message, please do not reply.</p>
                        </div>
                    </div>
                </body>
                </html>
                '''
                
                # Create plain text version as fallback
                text_body = f'''
                Welcome to {settings.app_name}!
                
                Hello {name},
                
                Your verification code is: {otp}
                
                This code will expire in {settings.otp_expire_minutes} minutes.
                
                If you didn't request this code, please ignore this email.
                '''
                
                # Attach both plain text and HTML versions
                msg.attach(MIMEText(text_body, 'plain'))
                msg.attach(MIMEText(html_body, 'html'))
                
                # Send email via SMTP
                with smtplib.SMTP(settings.smtp_host, settings.smtp_port) as server:
                    server.starttls()
                    server.login(settings.smtp_user, settings.smtp_password)
                    server.send_message(msg)
                
                print(f"✅ OTP email sent successfully to {email}")
                return True
            else:
                # Fall back to console logging if SMTP not configured
                print(f"\n{'='*60}")
                print(f"📧 OTP Email for {name} ({email})")
                print(f"{'='*60}")
                print(f"Your OTP code is: {otp}")
                print(f"This code will expire in {settings.otp_expire_minutes} minutes")
                print(f"{'='*60}")
                print(f"⚠️  SMTP not configured - Email sent to console only")
                print(f"{'='*60}\n")
                return True
                
        except Exception as e:
            print(f"❌ Error sending email: {str(e)}")
            # Still log to console as fallback
            print(f"\n{'='*60}")
            print(f"📧 OTP Email for {name} ({email}) - FALLBACK")
            print(f"{'='*60}")
            print(f"Your OTP code is: {otp}")
            print(f"This code will expire in {settings.otp_expire_minutes} minutes")
            print(f"{'='*60}\n")
            return False
    
    @staticmethod
    def get_otp_expiry() -> datetime:
        """Get OTP expiry datetime."""
        return datetime.utcnow() + timedelta(minutes=settings.otp_expire_minutes)
