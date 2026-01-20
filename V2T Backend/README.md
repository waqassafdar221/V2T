# V2T Backend

A FastAPI backend service with complete authentication system and GPT-5.1-Codex-Max enabled for all clients.

## Features

- ✅ **User Authentication System**
  - User registration with OTP email verification
  - Login with username or email
  - JWT token-based authentication
  - Password hashing with bcrypt
  - Role-based user types (Student, Teacher, Others)

- ✅ **FastAPI Framework**
- ✅ **GPT-5.1-Codex-Max AI Integration**
- ✅ **SQLite Database with SQLAlchemy ORM**
- ✅ **Environment-based Configuration**
- ✅ **CORS Support**
- ✅ **Automatic API Documentation (Swagger/ReDoc)**

## Setup

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Configure Environment

```bash
cp .env.example .env
# Edit .env and configure your settings
```

**Important environment variables:**
- `SECRET_KEY` - Change this to a secure random string
- `OPENAI_API_KEY` - Your OpenAI API key (if using GPT features)
- `SMTP_*` - **Email server settings for sending OTP emails** (see [EMAIL_SETUP.md](EMAIL_SETUP.md))

**For Email OTP Delivery:** Configure SMTP settings in `.env` to send real emails. If not configured, OTPs will be printed to console. See [EMAIL_SETUP.md](EMAIL_SETUP.md) for detailed setup instructions.

### 3. Run the Server

```bash
# Activate virtual environment
source venv/bin/activate

# Start the server
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

The server will start at `http://localhost:8000`

## API Endpoints

### Authentication Endpoints

#### 1. **POST /auth/signup** - Register New User
Create a new user account and receive OTP via email.

**Request Body:**
```json
{
  "name": "John Doe",
  "username": "johndoe",
  "email": "john@example.com",
  "role": "Student",
  "password": "securepassword123"
}
```

**Role Options:** `Student`, `Teacher`, `Others`

**Response:**
```json
{
  "message": "User registered successfully. Please check your email for OTP verification.",
  "email": "john@example.com",
  "username": "johndoe"
}
```

#### 2. **POST /auth/verify-otp** - Verify Email with OTP
Verify your email address using the OTP sent during registration.

**Request Body:**
```json
{
  "email": "john@example.com",
  "otp": "123456"
}
```

**Response:**
```json
{
  "message": "Email verified successfully. You can now login.",
  "verified": true
}
```

#### 3. **POST /auth/login** - User Login
Login with username or email and password.

**Request Body:**
```json
{
  "username_or_email": "johndoe",
  "password": "securepassword123"
}
```

**Response:**
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer",
  "user": {
    "id": 1,
    "name": "John Doe",
    "username": "johndoe",
    "email": "john@example.com",
    "role": "Student",
    "is_verified": true,
    "created_at": "2026-01-20T10:30:00"
  }
}
```

#### 4. **POST /auth/resend-otp** - Resend OTP
Request a new OTP if the previous one expired.

**Query Parameter:**
- `email` - User's email address

**Response:**
```json
{
  "message": "OTP has been resent to your email",
  "email": "john@example.com"
}
```

### General Endpoints

- `GET /` - Root endpoint with app info
- `GET /health` - Health check endpoint
- `POST /api/generate` - Generate AI response using GPT-5.1-Codex-Max
- `GET /api/config` - Get current AI configuration

### API Documentation

Once the server is running, visit:
- **Swagger UI:** http://localhost:8000/docs
- **ReDoc:** http://localhost:8000/redoc

## Configuration

The application uses environment variables for configuration. Key settings in `.env`:

### Application Settings
```env
APP_NAME="V2T Backend"
DEBUG=True
HOST=0.0.0.0
PORT=8000
```

### Database
```env
DATABASE_URL=sqlite:///./v2t.db
```

### Security / Authentication
```env
SECRET_KEY=your-secret-key-change-this-in-production
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=1440
OTP_EXPIRE_MINUTES=10
```

### Email Configuration (Optional)
For production, configure SMTP settings to send actual emails:
```env
SMTP_HOST=smtp.gmail.com
SMTP_PORT=587
SMTP_USER=your-email@gmail.com
SMTP_PASSWORD=your-app-password
```

**Note:** In development, OTPs are printed to the console.

### GPT-5.1-Codex-Max
```env
ENABLE_GPT_5_1_CODEX_MAX=True
GPT_MODEL=gpt-5.1-codex-max
OPENAI_API_KEY=your_openai_api_key_here
```

## Project Structure

```
V2T Backend/
├── app/
│   ├── api/
│   │   ├── auth.py          # Authentication routes
│   │   └── routes.py        # General API routes
│   ├── core/
│   │   ├── config.py        # Configuration settings
│   │   ├── database.py      # Database setup
│   │   └── security.py      # Password hashing & JWT
│   ├── models/
│   │   └── user.py          # User & OTP database models
│   ├── services/
│   │   └── email.py         # Email service for OTP
│   └── __init__.py
├── main.py                   # FastAPI application entry point
├── requirements.txt          # Python dependencies
├── .env.example             # Example environment variables
├── .gitignore
├── v2t.db                   # SQLite database (created automatically)
└── README.md
```

## Authentication Flow

1. **User Registration:**
   - User submits registration form with name, username, email, role, and password
   - System creates unverified user account
   - System generates 6-digit OTP
   - OTP is sent to user's email (printed to console in development)
   - OTP expires in 10 minutes

2. **Email Verification:**
   - User enters OTP received via email
   - System validates OTP and expiration
   - User account is marked as verified

3. **User Login:**
   - User provides username/email and password
   - System verifies credentials
   - System checks if user is verified
   - System generates JWT access token (valid for 24 hours)
   - Token is returned to client

4. **Authenticated Requests:**
   - Client includes JWT token in Authorization header
   - Format: `Authorization: Bearer <token>`
   - Protected endpoints validate token

## Database Schema

### Users Table
- `id` - Primary key
- `name` - User's full name
- `username` - Unique username
- `email` - Unique email address
- `role` - User role (Student/Teacher/Others)
- `hashed_password` - Bcrypt hashed password
- `is_verified` - Email verification status
- `created_at` - Account creation timestamp
- `updated_at` - Last update timestamp

### OTP Codes Table
- `id` - Primary key
- `email` - Associated email address
- `code` - 6-digit OTP code
- `created_at` - OTP generation time
- `expires_at` - OTP expiration time
- `is_used` - Whether OTP has been used

## Security Features

- **Password Hashing:** Bcrypt algorithm with salt
- **JWT Tokens:** Signed with HS256 algorithm
- **Token Expiration:** Configurable (default 24 hours)
- **OTP Expiration:** Configurable (default 10 minutes)
- **Email Verification:** Required before login
- **CORS Protection:** Configurable allowed origins

## Development Notes

### OTP Email in Development
In development mode, OTPs are printed to the console instead of being sent via email. Look for output like:

```
============================================================
📧 OTP Email for John Doe (john@example.com)
============================================================
Your OTP code is: 123456
This code will expire in 10 minutes
============================================================
```

### Production Email Setup
For production, configure SMTP settings in `.env` and uncomment the email sending code in `app/services/email.py`.

## GPT-5.1-Codex-Max Integration

This backend is configured to use GPT-5.1-Codex-Max for all client requests. The feature is enabled by default and can be toggled via the `ENABLE_GPT_5_1_CODEX_MAX` environment variable.

## Testing with cURL

### Register a new user:
```bash
curl -X POST "http://localhost:8000/auth/signup" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "John Doe",
    "username": "johndoe",
    "email": "john@example.com",
    "role": "Student",
    "password": "password123"
  }'
```

### Verify OTP:
```bash
curl -X POST "http://localhost:8000/auth/verify-otp" \
  -H "Content-Type: application/json" \
  -d '{
    "email": "john@example.com",
    "otp": "123456"
  }'
```

### Login:
```bash
curl -X POST "http://localhost:8000/auth/login" \
  -H "Content-Type: application/json" \
  -d '{
    "username_or_email": "johndoe",
    "password": "password123"
  }'
```

## License

MIT License
