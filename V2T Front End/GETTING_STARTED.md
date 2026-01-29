# V2T Quick Start Guide

## Prerequisites
- Node.js 18+ and npm
- Python 3.9+
- PostgreSQL database
- Redis server
- SMTP email account (Gmail recommended)

## Backend Setup

### 1. Install Dependencies
```bash
cd "V2T Backend"
pip install -r requirements.txt
```

### 2. Configure Environment
Create a `.env` file in the backend directory:
```env
# Database
DATABASE_URL=postgresql://username:password@localhost/v2t_db

# Security
SECRET_KEY=your-very-secret-key-change-this
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30

# Celery
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

# CORS
CORS_ORIGINS=http://localhost:3000,http://localhost:3001
```

### 3. Create Database
```bash
# Connect to PostgreSQL
psql -U postgres

# Create database
CREATE DATABASE v2t_db;
\q
```

### 4. Initialize Database Tables
```bash
# The tables will be created automatically on first run
python -c "from app.core.database import create_tables; create_tables()"
```

### 5. Start Backend Services
```bash
# Option 1: Use the provided script
./start_servers.sh

# Option 2: Start services manually
# Terminal 1 - FastAPI server
uvicorn main:app --reload --port 8000

# Terminal 2 - Celery worker
celery -A app.core.celery_app worker --loglevel=info
```

Backend will be available at `http://localhost:8000`

## Frontend Setup

### 1. Install Dependencies
```bash
cd "V2T Front End"
npm install
```

### 2. Configure Environment
Create a `.env.local` file in the frontend directory:
```env
NEXT_PUBLIC_API_URL=http://localhost:8000
NEXT_PUBLIC_APP_NAME=V2T - Video to Text
```

### 3. Start Development Server
```bash
npm run dev
```

Frontend will be available at `http://localhost:3000`

## Testing the Application

### 1. Access the Application
Open your browser and navigate to `http://localhost:3000`

### 2. Create an Account
- Click "Sign Up" in the header
- Fill in your details:
  - Full Name
  - Username
  - Email (must be a real email to receive OTP)
  - Role (Student/Instructor/Admin)
  - Password (min 8 characters)
- Click "Sign Up"

### 3. Verify Email
- Check your email inbox for OTP code
- Enter the 6-digit OTP code
- Click "Verify Email"

### 4. Login
- Enter your username/email and password
- Click "Sign In"
- You'll be redirected to the dashboard

### 5. Upload a Video
- Click "Click to select video file" or drag & drop
- Select a video file (MP4, AVI, MOV, MKV, FLV, WMV)
- Maximum file size: 500MB
- Click "Upload and Process Video"

### 6. Monitor Processing
- You'll be automatically redirected to the video status page
- The page will auto-refresh every 3 seconds
- Watch the progress bar as processing happens
- Status stages:
  - UPLOADED → PROCESSING → COMPLETED

### 7. View Results
Once processing is complete, you'll see:
- **Processing Summary**: Filename, total frames, objects detected, texts extracted, FPS, duration
- **Detected Objects**: List of objects found with confidence scores
- **Extracted Texts**: List of text found in video frames

### 8. Export Results
Click any export button to download results:
- 📄 Export as TXT - Plain text format
- 📊 Export as JSON - Structured JSON data
- 📈 Export as CSV - Spreadsheet format

### 9. Delete Video
- Click the "🗑️ Delete Video" button
- Confirm deletion
- All video data and files will be removed

## API Documentation

Once the backend is running, access interactive API documentation:
- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

## Common Issues & Solutions

### Backend Issues

**Issue**: `ModuleNotFoundError`
```bash
Solution: Install missing package
pip install <missing-package>
```

**Issue**: Database connection error
```bash
Solution: Verify PostgreSQL is running and credentials are correct
# Check PostgreSQL status
sudo service postgresql status
# Or on macOS
brew services list
```

**Issue**: Redis connection error
```bash
Solution: Start Redis server
# Ubuntu/Debian
sudo service redis-server start
# macOS
brew services start redis
```

**Issue**: Email not sending
```bash
Solution: 
1. Use app-specific password for Gmail
2. Enable less secure app access or use OAuth2
3. Check SMTP credentials in .env
```

### Frontend Issues

**Issue**: `CORS error`
```bash
Solution: Add frontend URL to CORS_ORIGINS in backend .env
CORS_ORIGINS=http://localhost:3000
```

**Issue**: `Network Error` or `401 Unauthorized`
```bash
Solution: 
1. Check backend is running on port 8000
2. Verify NEXT_PUBLIC_API_URL in .env.local
3. Check if token is stored in localStorage
```

**Issue**: Pages not loading
```bash
Solution: Clear browser cache and localStorage
localStorage.clear()
```

## Development Tips

### Hot Reload
Both backend and frontend support hot reload:
- **Backend**: Changes to Python files reload automatically
- **Frontend**: Changes to React/TypeScript files reload automatically

### Viewing Logs
```bash
# Backend logs
tail -f logs/app.log

# Celery worker logs
# Visible in the celery terminal window
```

### Database Inspection
```bash
# Connect to database
psql -U postgres -d v2t_db

# View tables
\dt

# View users
SELECT * FROM users;

# View videos
SELECT * FROM videos;
```

### Testing Endpoints
Use the Swagger UI or curl:
```bash
# Test signup
curl -X POST http://localhost:8000/auth/signup \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Test User",
    "username": "testuser",
    "email": "test@example.com",
    "password": "password123",
    "role": "STUDENT"
  }'

# Test login
curl -X POST http://localhost:8000/auth/login \
  -H "Content-Type: application/json" \
  -d '{
    "username_or_email": "testuser",
    "password": "password123"
  }'
```

## Production Deployment

### Backend Deployment
1. Set production environment variables
2. Use production WSGI server (gunicorn/uvicorn)
3. Configure reverse proxy (nginx)
4. Enable HTTPS
5. Set up monitoring and logging

### Frontend Deployment
```bash
# Build for production
npm run build

# Start production server
npm start
```

Or deploy to Vercel:
```bash
vercel deploy
```

## Additional Resources
- [API Integration Guide](./API_INTEGRATION.md)
- [Backend Documentation](../V2T%20Backend/README.md)
- [Frontend Documentation](./README.md)

## Support
For issues or questions, check:
1. Backend logs in `./logs` directory
2. Browser console for frontend errors
3. PostgreSQL and Redis service status
4. Environment variable configuration
