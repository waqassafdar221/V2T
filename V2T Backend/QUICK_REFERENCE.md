# V2T Backend - Quick Reference Card

## 🚀 Start/Stop Commands

```bash
# Start all services
./start_servers.sh

# Stop all services
./stop_servers.sh

# Check status
redis-cli ping                    # Redis
curl http://localhost:8000/      # FastAPI
ps aux | grep celery             # Celery
```

## 🌐 Access URLs

| Service | URL |
|---------|-----|
| API | http://localhost:8000 |
| Swagger Docs | http://localhost:8000/docs |
| ReDoc | http://localhost:8000/redoc |

## 📡 API Endpoints Cheat Sheet

### Authentication
```bash
# Signup
POST /auth/signup
Body: {"name":"...", "username":"...", "email":"...", "password":"...", "role":"Student"}

# Verify OTP
POST /auth/verify-otp
Body: {"email":"...", "otp":"123456"}

# Login
POST /auth/login
Body: {"username_or_email":"...", "password":"..."}
Response: {"access_token": "eyJ...", "token_type": "bearer"}

# Resend OTP
POST /auth/resend-otp?email=user@example.com
```

### Video Processing (Requires JWT Token)
```bash
# Upload Video
POST /video/upload
Headers: Authorization: Bearer <token>
Body: multipart/form-data with "file" field

# Check Status
GET /video/status/{video_id}
Headers: Authorization: Bearer <token>

# Get Results
GET /video/results/{video_id}
Headers: Authorization: Bearer <token>

# List Videos
GET /video/list
Headers: Authorization: Bearer <token>

# Delete Video
DELETE /video/delete/{video_id}
Headers: Authorization: Bearer <token>

# Export to Text File
GET /video/export/{video_id}/text
Headers: Authorization: Bearer <token>

# Export to PDF
GET /video/export/{video_id}/pdf
Headers: Authorization: Bearer <token>
```

## 🧪 Quick Test

```bash
# Complete authentication flow
curl -X POST http://localhost:8000/auth/signup \
  -H "Content-Type: application/json" \
  -d '{"name":"Test","username":"test","email":"test@example.com","password":"pass123","role":"Student"}'

curl -X POST http://localhost:8000/auth/login \
  -H "Content-Type: application/json" \
  -d '{"username_or_email":"test","password":"pass123"}' \
  | jq -r '.access_token'

# Video upload (replace TOKEN)
curl -X POST http://localhost:8000/video/upload \
  -H "Authorization: Bearer TOKEN" \
  -F "file=@video.mp4"
```

## 📂 Important Directories

```
uploads/videos/    # Uploaded videos
uploads/frames/    # Extracted frames (temp)
logs/             # Application logs
venv/             # Python virtual environment
```

## 📝 Log Files

```bash
# View logs
tail -f logs/fastapi.log    # FastAPI server
tail -f logs/celery.log     # Celery worker

# Clear logs
> logs/fastapi.log
> logs/celery.log
```

## 🔧 Troubleshooting

```bash
# Port already in use
lsof -i :8000
kill -9 $(lsof -t -i:8000)

# Celery not processing
pkill -f celery
celery -A app.tasks.video_tasks worker --loglevel=info

# Redis connection failed
brew services restart redis

# Reset database
rm v2t.db
# Restart server to recreate
```

## 🔑 Environment Variables (.env)

```ini
# Must configure
SECRET_KEY=your-secret-key
SMTP_HOST=smtp.gmail.com
SMTP_USER=your-email@gmail.com
SMTP_PASSWORD=your-app-password

# Optional tuning
FRAME_EXTRACTION_INTERVAL=1       # Frames per second
MAX_VIDEO_SIZE_MB=500            # Max upload size
YOLO_CONFIDENCE_THRESHOLD=0.5    # Detection threshold
```

## 📊 Processing Time Estimates

| Video Length | Frames (1fps) | Processing Time |
|-------------|---------------|-----------------|
| 30 seconds | 30 | ~10-20 seconds |
| 60 seconds | 60 | ~20-40 seconds |
| 2 minutes | 120 | ~40-80 seconds |
| 5 minutes | 300 | ~100-200 seconds |

## 🎯 Supported Video Formats

- ✅ MP4 (.mp4)
- ✅ AVI (.avi)
- ✅ MOV (.mov)
- ✅ MKV (.mkv)

## 📚 Documentation Files

- **README.md** - Main setup guide
- **VIDEO_PROCESSING_GUIDE.md** - Video processing details
- **EMAIL_SETUP.md** - Email configuration
- **API_REFERENCE.md** - API documentation
- **SYSTEM_STATUS.md** - Current system status
- **DEPLOYMENT_CHECKLIST.md** - Deployment guide

## 🧰 Useful Commands

```bash
# Virtual environment
source venv/bin/activate          # Activate
deactivate                        # Deactivate

# Dependencies
pip install -r requirements.txt   # Install packages
pip freeze > requirements.txt     # Update requirements

# Database
sqlite3 v2t.db ".tables"         # List tables
sqlite3 v2t.db "SELECT * FROM videos;" # Query

# Testing
python test_video_api.py         # Run test suite
```

## 🔐 Security Notes

- ⚠️ Change `SECRET_KEY` in production
- ⚠️ Use app passwords for email (not main password)
- ⚠️ Enable HTTPS in production
- ⚠️ Don't commit `.env` file to git
- ⚠️ Regularly update dependencies

## 💡 Tips

1. Use Swagger UI (http://localhost:8000/docs) for easy API testing
2. Monitor Celery logs during video processing
3. Clean uploads directory periodically
4. Keep backup of `.env` file
5. Test with small videos first

---

**Quick Start**: `./start_servers.sh` → Open http://localhost:8000/docs → Start testing!
