# V2T Backend

A comprehensive FastAPI backend service with authentication, email verification, and advanced video-to-text extraction capabilities using YOLO object detection and Tesseract OCR.

## Features

- ✅ **User Authentication System**
  - User registration with OTP email verification
  - Login with username or email
  - JWT token-based authentication
  - Password hashing with bcrypt
  - Role-based user types (Student, Teacher, Others)

- ✅ **Video-to-Text Extraction System**
  - Video upload with validation (.mp4, .avi, .mov, .mkv)
  - Automatic frame extraction using FFmpeg
  - YOLOv8 object detection on video frames
  - Tesseract OCR for text extraction
  - Asynchronous processing with Celery + Redis
  - Real-time status tracking
  - Complete results API with detected objects and extracted text
  - **Export to PDF and Text files** with formatted results

- ✅ **FastAPI Framework**
- ✅ **GPT-5.1-Codex-Max AI Integration**
- ✅ **SQLite Database with SQLAlchemy ORM**
- ✅ **Environment-based Configuration**
- ✅ **CORS Support**
- ✅ **Automatic API Documentation (Swagger/ReDoc)**
- ✅ **Email Service (SMTP)**

## Quick Start

### Prerequisites

- Python 3.12+
- FFmpeg (for video processing)
- Tesseract OCR (for text extraction)
- Redis (for async task queue)

### One-Command Setup

```bash
# Clone and setup
git clone <repository-url>
cd "V2T Backend"

# Install system dependencies (macOS)
brew install ffmpeg tesseract redis

# Create virtual environment and install Python packages
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# Configure environment
cp .env.example .env
# Edit .env with your settings

# Start all services
./start_servers.sh
```

Access the API at:
- **API**: http://localhost:8000
- **Swagger Docs**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

## Detailed Setup

### 1. Install System Dependencies

**macOS:**
```bash
brew install ffmpeg tesseract redis
```

**Ubuntu/Debian:**
```bash
sudo apt update
sudo apt install ffmpeg tesseract-ocr redis-server
```

**Verify installations:**
```bash
ffmpeg -version
tesseract --version
redis-cli ping  # Should return PONG
```

### 2. Install Python Dependencies

```bash
# Activate virtual environment
source venv/bin/activate

# Install all packages
pip install -r requirements.txt
```

This installs:
- FastAPI, Uvicorn (web framework)
- SQLAlchemy, databases (database)
- PyTorch, Ultralytics (YOLO)
- OpenCV, Pytesseract (image processing)
- Celery, Redis (async tasks)
- And more...

### 3. Configure Environment

```bash
cp .env.example .env
# Edit .env and configure your settings
```

**Important environment variables:**
- `SECRET_KEY` - Change this to a secure random string
- `OPENAI_API_KEY` - Your OpenAI API key (if using GPT features)
- `SMTP_*` - **Email server settings for sending OTP emails** (see [EMAIL_SETUP.md](EMAIL_SETUP.md))
- `REDIS_URL` - Redis connection URL (default: redis://localhost:6379/0)
- `VIDEO_UPLOAD_DIR` - Directory for uploaded videos (default: ./uploads/videos)
- `FRAME_EXTRACTION_INTERVAL` - Seconds between frame extractions (default: 1)

**For Email OTP Delivery:** Configure SMTP settings in `.env` to send real emails. If not configured, OTPs will be printed to console. See [EMAIL_SETUP.md](EMAIL_SETUP.md) for detailed setup instructions.

### 4. Start Services

**Option A: Automated (Recommended)**
```bash
./start_servers.sh
```

This starts:
1. Redis (message broker)
2. Celery worker (async video processing)
3. FastAPI server (API endpoints)

**Option B: Manual**

Terminal 1 - Redis:
```bash
redis-server
# or as background service
brew services start redis  # macOS
sudo systemctl start redis  # Linux
```

Terminal 2 - Celery Worker:
```bash
cd "V2T Backend"
source venv/bin/activate
celery -A app.tasks.video_tasks worker --loglevel=info
```

Terminal 3 - FastAPI Server:
```bash
cd "V2T Backend"
source venv/bin/activate
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

### 5. Stop Services

```bash
./stop_servers.sh
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

**Example:** `POST /auth/resend-otp?email=john@example.com`

**Response:**
```json
{
  "message": "OTP resent successfully. Please check your email."
}
```

---

### Video Processing Endpoints

> 📘 **Detailed Documentation**: See [VIDEO_PROCESSING_GUIDE.md](VIDEO_PROCESSING_GUIDE.md) for comprehensive guide including workflows, troubleshooting, and advanced usage.

#### 1. **POST /video/upload** - Upload Video for Processing
Upload a video file for automatic frame extraction, object detection, and text extraction.

**Request:**
- **Content-Type**: multipart/form-data
- **Authorization**: Bearer token required
- **Body**: 
  - `file`: Video file (.mp4, .avi, .mov, .mkv)
  - Max size: 500MB (configurable)

**cURL Example:**
```bash
# Get token first
TOKEN=$(curl -X POST "http://localhost:8000/auth/login" \
  -H "Content-Type: application/json" \
  -d '{"username_or_email": "johndoe", "password": "securepassword123"}' \
  | jq -r '.access_token')

# Upload video
curl -X POST "http://localhost:8000/video/upload" \
  -H "Authorization: Bearer $TOKEN" \
  -F "file=@sample_video.mp4"
```

**Response:**
```json
{
  "video_id": 1,
  "message": "Video uploaded successfully. Processing started.",
  "status": "pending"
}
```

#### 2. **GET /video/status/{video_id}** - Check Processing Status
Get current processing status and progress of a video.

**Authorization**: Bearer token required

**Response:**
```json
{
  "video_id": 1,
  "status": "processing",
  "progress": 65,
  "created_at": "2026-01-20T10:30:00"
}
```

**Status Values:**
- `pending`: Queued for processing
- `processing`: Currently extracting frames and analyzing
- `completed`: All processing finished
- `failed`: Error occurred during processing

#### 3. **GET /video/results/{video_id}** - Get Processing Results
Retrieve complete results including detected objects and extracted text.

**Authorization**: Bearer token required

**Response:**
```json
{
  "video_id": 1,
  "status": "completed",
  "file_path": "uploads/videos/video_1_20260120_103000.mp4",
  "detected_objects": [
    {
      "id": 1,
      "label": "person",
      "confidence": 0.95,
      "bbox_x": 120,
      "bbox_y": 200,
      "bbox_width": 100,
      "bbox_height": 300,
      "frame_number": 10
    },
    {
      "id": 2,
      "label": "car",
      "confidence": 0.87,
      "bbox_x": 450,
      "bbox_y": 150,
      "bbox_width": 200,
      "bbox_height": 150,
      "frame_number": 25
    }
  ],
  "extracted_texts": [
    {
      "id": 1,
      "text": "Welcome to the presentation",
      "confidence": 0.92,
      "frame_number": 5
    },
    {
      "id": 2,
      "text": "Contact: support@example.com",
      "confidence": 0.88,
      "frame_number": 120
    }
  ],
  "created_at": "2026-01-20T10:30:00",
  "updated_at": "2026-01-20T10:32:15"
}
```

#### 4. **GET /video/list** - List All User Videos
Get list of all videos uploaded by the authenticated user.

**Authorization**: Bearer token required

**Response:**
```json
{
  "videos": [
    {
      "video_id": 1,
      "filename": "presentation.mp4",
      "status": "completed",
      "created_at": "2026-01-20T10:30:00"
    },
    {
      "video_id": 2,
      "filename": "lecture.mp4",
      "status": "processing",
      "created_at": "2026-01-20T11:15:00"
    }
  ],
  "total": 2
}
```

#### 5. **DELETE /video/delete/{video_id}** - Delete Video
Delete a video and all associated data (frames, detections, texts).

**Authorization**: Bearer token required

**Response:**
```json
{
  "message": "Video deleted successfully"
}
```

#### 6. **GET /video/export/{video_id}/text** - Export Results as Text File
Download video processing results as a formatted text file.

**Authorization**: Bearer token required

**Response:** Downloads `.txt` file containing:
- Video information
- Detected objects with details
- Extracted text entries
- Summary statistics

**Example:**
```bash
curl -X GET "http://localhost:8000/video/export/{video_id}/text" \
  -H "Authorization: Bearer $TOKEN" \
  -o "results.txt"
```

#### 7. **GET /video/export/{video_id}/pdf** - Export Results as PDF
Download video processing results as a professionally formatted PDF.

**Authorization**: Bearer token required

**Response:** Downloads `.pdf` file with:
- Professional formatting and tables
- Video metadata
- Detected objects table
- Extracted text table
- Summary with visualizations

**Example:**
```bash
curl -X GET "http://localhost:8000/video/export/{video_id}/pdf" \
  -H "Authorization: Bearer $TOKEN" \
  -o "results.pdf"
```

> 📘 **Detailed Export Guide**: See [VIDEO_EXPORT_GUIDE.md](VIDEO_EXPORT_GUIDE.md) for complete export documentation

---

## Video Processing Workflow

```
1. User uploads video → API validates and saves file
                     ↓
2. Celery task queued → Status: "pending"
                     ↓
3. FFmpeg extracts frames → Status: "processing" (20%)
                     ↓
4. YOLO detects objects → Status: "processing" (60%)
                     ↓
5. Tesseract extracts text → Status: "processing" (90%)
                     ↓
6. Results saved to DB → Status: "completed" (100%)
                     ↓
7. User retrieves results via API
```

**Processing Time Estimate:**
- 60-second video with 1 frame/sec = 60 frames
- Frame extraction: ~5 seconds
- YOLO processing: ~3-6 seconds
- OCR processing: ~12-30 seconds
- **Total**: ~20-40 seconds

---

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
