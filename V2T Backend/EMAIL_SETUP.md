# Email Configuration Guide

## Overview
The V2T Backend now supports sending OTP verification emails via SMTP. If SMTP is not configured, OTPs will be printed to the console as a fallback.

## SMTP Configuration

### Option 1: Gmail (Recommended for Testing)

1. **Enable 2-Factor Authentication** on your Google Account
2. **Generate App Password:**
   - Go to https://myaccount.google.com/apppasswords
   - Select "Mail" and your device
   - Copy the 16-character password

3. **Update `.env` file:**
```env
SMTP_HOST=smtp.gmail.com
SMTP_PORT=587
SMTP_USER=your-email@gmail.com
SMTP_PASSWORD=your-16-char-app-password
```

### Option 2: Outlook/Hotmail

```env
SMTP_HOST=smtp-mail.outlook.com
SMTP_PORT=587
SMTP_USER=your-email@outlook.com
SMTP_PASSWORD=your-password
```

### Option 3: SendGrid (Production Recommended)

1. Create account at https://sendgrid.com
2. Generate API key
3. Configure:

```env
SMTP_HOST=smtp.sendgrid.net
SMTP_PORT=587
SMTP_USER=apikey
SMTP_PASSWORD=your-sendgrid-api-key
```

### Option 4: Amazon SES (Production)

```env
SMTP_HOST=email-smtp.us-east-1.amazonaws.com
SMTP_PORT=587
SMTP_USER=your-aws-access-key
SMTP_PASSWORD=your-aws-secret-key
```

## Testing Email Configuration

### 1. Update your `.env` file
```bash
cp .env.example .env
# Edit .env with your SMTP settings
```

### 2. Restart the server
```bash
cd "/Users/waqassafdar/V2T/V2T Backend"
source venv/bin/activate
uvicorn main:app --reload
```

### 3. Test signup endpoint
```bash
curl -X POST "http://localhost:8000/auth/signup" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Test User",
    "username": "testuser",
    "email": "your-test-email@gmail.com",
    "role": "Student",
    "password": "password123"
  }'
```

### 4. Check your email inbox
- You should receive a professionally formatted email with the OTP
- If SMTP fails, check the console for the OTP as fallback

## Email Template Features

The OTP email includes:
- ✅ Professional HTML design with styling
- ✅ Clear OTP display with large, easy-to-read font
- ✅ Expiration time reminder
- ✅ Responsive layout
- ✅ Plain text fallback for email clients that don't support HTML

## Troubleshooting

### "Authentication failed"
- Verify your SMTP credentials
- For Gmail, ensure you're using an App Password, not your regular password
- Check if 2FA is enabled (required for Gmail)

### "Connection timeout"
- Check your firewall settings
- Verify the SMTP host and port
- Try port 465 for SSL or port 587 for TLS

### "Email not received"
- Check spam/junk folder
- Verify the recipient email address
- Check server logs for error messages

### "SMTP not configured" message
- The app will fall back to console logging
- Check terminal output for the OTP code
- This is normal in development mode

## Security Best Practices

1. **Never commit SMTP credentials** to version control
2. **Use environment variables** for sensitive data
3. **Use App Passwords** instead of real passwords for Gmail
4. **Enable 2FA** on email accounts
5. **Use dedicated email service** (SendGrid, AWS SES) for production
6. **Monitor email sending** for abuse

## Production Recommendations

For production environments:

1. **Use a dedicated email service:**
   - SendGrid (12,000 free emails/month)
   - AWS SES (very cost-effective)
   - Mailgun (flexible pricing)

2. **Set up SPF and DKIM records** to improve deliverability

3. **Monitor bounce rates** and email reputation

4. **Implement rate limiting** to prevent abuse

5. **Add unsubscribe links** for marketing emails (not needed for OTP)

## Current Configuration

The system automatically detects SMTP configuration:
- ✅ **SMTP Configured:** Sends real emails
- ⚠️ **SMTP Not Configured:** Falls back to console logging

No code changes needed - just update your `.env` file!
