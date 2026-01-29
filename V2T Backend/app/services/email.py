import random
import string
from datetime import datetime, timedelta
from typing import Optional
import smtplib
import os
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.image import MIMEImage
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
                msg = MIMEMultipart('related')
                msg['From'] = settings.smtp_user
                msg['To'] = email
                msg['Subject'] = f"{settings.app_name} - Email Verification"
                
                # Create alternative part for text and HTML
                msg_alternative = MIMEMultipart('alternative')
                msg.attach(msg_alternative)
                
                # Create HTML email body with logo
                html_body = f'''
                <html>
                <head>
                    <style>
                        body {{ font-family: Arial, sans-serif; line-height: 1.6; color: #333; }}
                        .container {{ max-width: 600px; margin: 0 auto; padding: 20px; }}
                        .header {{ background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); 
                                   color: white; padding: 30px 20px; text-align: center; border-radius: 8px 8px 0 0; }}
                        .logo {{ max-width: 150px; height: auto; margin-bottom: 15px; }}
                        .content {{ background-color: #f9f9f9; padding: 30px; border-radius: 0 0 8px 8px; }}
                        .otp-code {{ font-size: 32px; font-weight: bold; color: #667eea; text-align: center; 
                                     padding: 20px; background-color: #fff; border: 2px dashed #667eea; 
                                     border-radius: 5px; margin: 20px 0; letter-spacing: 5px; }}
                        .footer {{ text-align: center; margin-top: 20px; color: #666; font-size: 12px; }}
                        .highlight {{ color: #764ba2; font-weight: bold; }}
                    </style>
                </head>
                <body>
                    <div class="container">
                        <div class="header">
                            <img src="cid:logo" alt="{settings.app_name} Logo" class="logo">
                            <h1>{settings.app_name}</h1>
                        </div>
                        <div class="content">
                            <h2>Welcome, {name}!</h2>
                            <p>Thank you for signing up. To complete your registration, please verify your email address.</p>
                            <p>Your verification code is:</p>
                            <div class="otp-code">{otp}</div>
                            <p><strong>This code will expire in <span class="highlight">{settings.otp_expire_minutes} minutes</span>.</strong></p>
                            <p>If you didn't request this code, please ignore this email.</p>
                        </div>
                        <div class="footer">
                            <p>This is an automated message, please do not reply.</p>
                            <p>&copy; 2026 {settings.app_name}. All rights reserved.</p>
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
                msg_alternative.attach(MIMEText(text_body, 'plain'))
                msg_alternative.attach(MIMEText(html_body, 'html'))
                
                # Attach logo image
                logo_path = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), 'Assets', 'logo.png')
                if os.path.exists(logo_path):
                    with open(logo_path, 'rb') as img_file:
                        img = MIMEImage(img_file.read())
                        img.add_header('Content-ID', '<logo>')
                        img.add_header('Content-Disposition', 'inline', filename='logo.png')
                        msg.attach(img)
                
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
