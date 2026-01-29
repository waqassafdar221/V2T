# V2T API Integration Guide

## Overview
This document describes the complete API integration between the V2T Frontend (Next.js) and Backend (FastAPI).

## Architecture

### Frontend Stack
- **Framework**: Next.js 14 with TypeScript
- **HTTP Client**: Axios
- **Styling**: CSS Modules
- **State Management**: React Hooks

### Backend Stack
- **Framework**: FastAPI
- **Database**: PostgreSQL with SQLAlchemy
- **Authentication**: JWT tokens
- **Task Queue**: Celery with Redis
- **AI/ML**: YOLOv8 for object detection, Tesseract for OCR

## API Base URL
```
Development: http://localhost:8000
Production: Configure in .env.local
```

## Authentication Flow

### 1. Signup
**Endpoint**: `POST /auth/signup`

**Request**:
```json
{
  "name": "John Doe",
  "username": "johndoe",
  "email": "john@example.com",
  "password": "securepassword123",
  "role": "STUDENT"
}
```

**Response**:
```json
{
  "message": "User registered successfully. Please check your email for OTP verification.",
  "email": "john@example.com",
  "username": "johndoe"
}
```

### 2. Verify OTP
**Endpoint**: `POST /auth/verify-otp`

**Request**:
```json
{
  "email": "john@example.com",
  "otp": "123456"
}
```

**Response**:
```json
{
  "message": "Email verified successfully. You can now login.",
  "verified": true
}
```

### 3. Login
**Endpoint**: `POST /auth/login`

**Request**:
```json
{
  "username_or_email": "johndoe",
  "password": "securepassword123"
}
```

**Response**:
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer",
  "user": {
    "id": 1,
    "name": "John Doe",
    "username": "johndoe",
    "email": "john@example.com",
    "role": "STUDENT",
    "is_verified": true
  }
}
```

### 4. Resend OTP
**Endpoint**: `POST /auth/resend-otp?email=john@example.com`

**Response**:
```json
{
  "message": "OTP has been resent to your email",
  "email": "john@example.com"
}
```

## Video Processing Flow

### 1. Upload Video
**Endpoint**: `POST /video/upload`

**Headers**:
```
Authorization: Bearer <token>
Content-Type: multipart/form-data
```

**Request**: Form data with file field

**Response**:
```json
{
  "video_id": "123bcc8b-0cbc-401f-ad32-2a3a937f7bb0",
  "filename": "sample_video.mp4",
  "file_size": 15728640,
  "status": "UPLOADED",
  "message": "Video uploaded successfully. Processing started in background."
}
```

### 2. Check Processing Status
**Endpoint**: `GET /video/status/{video_id}`

**Headers**:
```
Authorization: Bearer <token>
```

**Response**:
```json
{
  "video_id": "123bcc8b-0cbc-401f-ad32-2a3a937f7bb0",
  "status": "PROCESSING",
  "progress": 50,
  "message": "Processing video frames and extracting data",
  "error_message": null
}
```

**Status Values**:
- `UPLOADED`: Video uploaded, waiting to be processed
- `PROCESSING`: Currently processing
- `COMPLETED`: Processing finished successfully
- `FAILED`: Processing encountered an error

### 3. Get Processing Results
**Endpoint**: `GET /video/results/{video_id}`

**Headers**:
```
Authorization: Bearer <token>
```

**Response**:
```json
{
  "video_id": "123bcc8b-0cbc-401f-ad32-2a3a937f7bb0",
  "filename": "sample_video.mp4",
  "status": "COMPLETED",
  "duration": 30.5,
  "fps": 30.0,
  "total_frames": 915,
  "detected_objects": [
    {
      "frame_number": 0,
      "timestamp": 0.0,
      "object_class": "person",
      "confidence": 0.95,
      "bbox": {
        "x1": 100,
        "y1": 150,
        "x2": 300,
        "y2": 450
      }
    }
  ],
  "extracted_texts": [
    {
      "frame_number": 10,
      "timestamp": 0.33,
      "text": "Welcome to V2T",
      "confidence": 0.92
    }
  ],
  "created_at": "2026-01-20T10:30:00Z",
  "completed_at": "2026-01-20T10:35:00Z"
}
```

### 4. Export Results
**Endpoints**:
- `GET /video/export/{video_id}/txt` - Text format
- `GET /video/export/{video_id}/json` - JSON format
- `GET /video/export/{video_id}/csv` - CSV format
- `GET /video/export/{video_id}/pdf` - PDF format

**Headers**:
```
Authorization: Bearer <token>
```

**Response**: File download

### 5. List Videos
**Endpoint**: `GET /video/list?skip=0&limit=100&status_filter=COMPLETED`

**Headers**:
```
Authorization: Bearer <token>
```

**Response**:
```json
{
  "total": 5,
  "videos": [
    {
      "video_id": "123bcc8b-0cbc-401f-ad32-2a3a937f7bb0",
      "filename": "sample_video.mp4",
      "status": "COMPLETED",
      "created_at": "2026-01-20T10:30:00Z",
      "completed_at": "2026-01-20T10:35:00Z"
    }
  ]
}
```

### 6. Delete Video
**Endpoint**: `DELETE /video/delete/{video_id}`

**Headers**:
```
Authorization: Bearer <token>
```

**Response**:
```json
{
  "message": "Video and all associated data deleted successfully",
  "video_id": "123bcc8b-0cbc-401f-ad32-2a3a937f7bb0"
}
```

## Frontend Pages

### 1. Authentication Pages
- `/auth/login` - Login page
- `/auth/signup` - Registration page
- `/auth/verify-otp` - OTP verification page

### 2. Dashboard Pages
- `/dashboard` - Main dashboard with video upload
- `/dashboard/video/[videoId]` - Video processing status and results

### 3. Landing Page
- `/` - Homepage with hero, team, and contact sections

## API Client (`lib/api.ts`)

The frontend uses a centralized API client with:
- Automatic JWT token injection
- Response/error interceptors
- Type-safe interfaces
- Automatic redirect on 401 errors

### Usage Example

```typescript
import { authAPI, videoAPI } from '@/lib/api';

// Login
const response = await authAPI.login({
  username_or_email: 'johndoe',
  password: 'password123'
});
localStorage.setItem('token', response.data.access_token);

// Upload video
const file = document.getElementById('file-input').files[0];
const uploadResponse = await videoAPI.upload(file);

// Get status
const statusResponse = await videoAPI.getStatus(uploadResponse.data.video_id);

// Get results
const resultsResponse = await videoAPI.getResults(uploadResponse.data.video_id);

// Export
await videoAPI.exportResults(videoId, 'json');
```

## Environment Variables

### Frontend (.env.local)
```env
NEXT_PUBLIC_API_URL=http://localhost:8000
NEXT_PUBLIC_APP_NAME=V2T - Video to Text
```

### Backend (.env)
```env
DATABASE_URL=postgresql://user:password@localhost/v2t_db
SECRET_KEY=your-secret-key-here
CELERY_BROKER_URL=redis://localhost:6379/0
CELERY_RESULT_BACKEND=redis://localhost:6379/0

# Email Configuration
SMTP_HOST=smtp.gmail.com
SMTP_PORT=587
SMTP_USER=your-email@gmail.com
SMTP_PASSWORD=your-app-password
SMTP_FROM=noreply@v2t.com

# Storage
VIDEO_UPLOAD_DIR=./uploads/videos
VIDEO_FRAMES_DIR=./uploads/frames
EXPORT_DIR=./uploads/exports
```

## Error Handling

### Standard Error Response
```json
{
  "detail": "Error message description"
}
```

### Common HTTP Status Codes
- `200 OK` - Success
- `201 Created` - Resource created
- `400 Bad Request` - Validation error
- `401 Unauthorized` - Missing or invalid token
- `403 Forbidden` - User not verified
- `404 Not Found` - Resource not found
- `500 Internal Server Error` - Server error

## Security

### JWT Token Storage
Tokens are stored in `localStorage`:
```typescript
localStorage.setItem('token', access_token);
localStorage.setItem('user', JSON.stringify(user));
```

### Protected Routes
All video endpoints require authentication via JWT token in header:
```
Authorization: Bearer <token>
```

### File Upload Validation
- **Allowed formats**: MP4, AVI, MOV, MKV, FLV, WMV
- **Max file size**: 500MB
- Validated on both client and server

## Running the Application

### Backend
```bash
cd "V2T Backend"

# Install dependencies
pip install -r requirements.txt

# Start backend services
./start_servers.sh

# Or manually:
uvicorn main:app --reload --port 8000
celery -A app.core.celery_app worker --loglevel=info
```

### Frontend
```bash
cd "V2T Front End"

# Install dependencies
npm install

# Start development server
npm run dev
```

The frontend will be available at `http://localhost:3000` and backend at `http://localhost:8000`.

## Testing the Integration

1. **Start Backend**: Run `./start_servers.sh` in backend directory
2. **Start Frontend**: Run `npm run dev` in frontend directory
3. **Navigate to**: `http://localhost:3000`
4. **Sign Up**: Create a new account
5. **Verify Email**: Check email for OTP and verify
6. **Login**: Login with credentials
7. **Upload Video**: Upload a video file in dashboard
8. **View Results**: Monitor processing and view results
9. **Export**: Download results in desired format

## API Documentation

Full interactive API documentation is available at:
- **Swagger UI**: `http://localhost:8000/docs`
- **ReDoc**: `http://localhost:8000/redoc`

## Support

For issues or questions:
- Check backend logs in `./logs` directory
- Review frontend console for client-side errors
- Ensure all services (PostgreSQL, Redis, Celery) are running
- Verify environment variables are correctly set
