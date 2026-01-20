# V2T Backend - System Status & Setup Summary

## ✅ Current Status

**All systems operational and ready to use!**

### Services Running
- ✅ **Redis**: Running on port 6379 (brew services)
- ✅ **Celery Worker**: Processing video tasks (PID: Check with `ps aux | grep celery`)
- ✅ **FastAPI Server**: Running on http://localhost:8000

### System Dependencies Installed
- ✅ **FFmpeg 8.0.1**: Video frame extraction
- ✅ **Tesseract 5.5.1**: OCR text extraction
- ✅ **Redis 8.4.0**: Message broker for Celery
- ✅ **Python 3.12**: Application runtime

### Python Packages Installed
- ✅ **FastAPI & Uvicorn**: Web framework
- ✅ **PyTorch 2.9.1**: Deep learning framework
- ✅ **Ultralytics 8.4.6**: YOLOv8 object detection
- ✅ **OpenCV 4.13.0**: Image/video processing
- ✅ **Pytesseract 0.3.13**: OCR wrapper
- ✅ **Celery 5.6.2**: Async task queue
- ✅ **SQLAlchemy**: Database ORM
- ✅ **bcrypt**: Password hashing
- ✅ **python-jose**: JWT tokens
- And 40+ more dependencies...

---

## 🚀 Quick Commands

### Start All Services
```bash
./start_servers.sh
```

### Stop All Services
```bash
./stop_servers.sh
```

### Check Service Status
```bash
# Redis
redis-cli ping

# Celery
ps aux | grep celery

# FastAPI
curl http://localhost:8000/
```

### View Logs
```bash
# FastAPI logs
tail -f logs/fastapi.log

# Celery logs
tail -f logs/celery.log
```

---

## 📚 Documentation Files

1. **[README.md](README.md)** - Main documentation with setup and API reference
2. **[VIDEO_PROCESSING_GUIDE.md](VIDEO_PROCESSING_GUIDE.md)** - Comprehensive video processing guide
3. **[EMAIL_SETUP.md](EMAIL_SETUP.md)** - Email configuration for OTP delivery
4. **[API_REFERENCE.md](API_REFERENCE.md)** - Quick API reference

---

## 🔗 Access Points

- **API Base**: http://localhost:8000
- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc
- **Root Endpoint**: http://localhost:8000/

---

## 🧪 Testing

### Manual Testing (Swagger UI)
1. Open http://localhost:8000/docs
2. Test authentication endpoints:
   - POST `/auth/signup` - Create user
   - POST `/auth/verify-otp` - Verify OTP
   - POST `/auth/login` - Get JWT token
3. Test video endpoints (requires JWT token):
   - POST `/video/upload` - Upload video
   - GET `/video/status/{video_id}` - Check status
   - GET `/video/results/{video_id}` - Get results

### Automated Testing
```bash
python test_video_api.py
```

This script will:
1. Check server status
2. Test signup/login
3. Upload test video (optional)
4. Monitor processing
5. Retrieve results

---

## 📁 Project Structure

```
V2T Backend/
├── app/
│   ├── api/           # API endpoints
│   │   ├── auth.py    # Authentication
│   │   ├── video.py   # Video processing
│   │   └── routes.py  # General routes
│   ├── core/          # Core configuration
│   │   ├── config.py       # Settings
│   │   ├── database.py     # Database
│   │   ├── security.py     # Auth utilities
│   │   └── celery_app.py   # Celery config
│   ├── models/        # Database models
│   │   ├── user.py    # User & OTP
│   │   └── video.py   # Video processing
│   ├── services/      # Business logic
│   │   ├── email.py            # Email service
│   │   └── video_processing.py # Video processing
│   └── tasks/         # Celery tasks
│       └── video_tasks.py      # Video processing tasks
├── uploads/           # Upload directories
│   ├── videos/        # Uploaded videos
│   └── frames/        # Extracted frames
├── logs/              # Application logs
│   ├── celery.log     # Celery worker logs
│   └── fastapi.log    # FastAPI server logs
├── venv/              # Python virtual environment
├── main.py            # Application entry point
├── requirements.txt   # Python dependencies
├── .env               # Environment configuration
├── start_servers.sh   # Start all services
├── stop_servers.sh    # Stop all services
└── test_video_api.py  # API testing script
```

---

## 🔐 Environment Configuration

Located in `.env` file:

```ini
# Database
DATABASE_URL=sqlite:///./v2t.db

# Security
SECRET_KEY=your-secret-key-here
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=1440

# Email (Gmail Example)
SMTP_HOST=smtp.gmail.com
SMTP_PORT=587
SMTP_USER=your-email@gmail.com
SMTP_PASSWORD=your-app-password

# Video Processing
VIDEO_UPLOAD_DIR=./uploads/videos
VIDEO_FRAMES_DIR=./uploads/frames
MAX_VIDEO_SIZE_MB=500
FRAME_EXTRACTION_INTERVAL=1
YOLO_CONFIDENCE_THRESHOLD=0.5

# Celery/Redis
REDIS_URL=redis://localhost:6379/0
CELERY_BROKER_URL=redis://localhost:6379/0
CELERY_RESULT_BACKEND=redis://localhost:6379/0

# AI Features
GPT_MODEL=gpt-5.1-codex-max
ENABLE_GPT_5_1_CODEX_MAX=true
```

---

## 🎯 Features Implemented

### ✅ Authentication System
- User registration with email/OTP verification
- JWT token-based authentication
- Password hashing with bcrypt
- Role-based access (Student, Teacher, Others)
- Session management

### ✅ Video Processing System
- Video upload with validation
- Frame extraction using FFmpeg
- YOLOv8 object detection
- Tesseract OCR text extraction
- Asynchronous processing with Celery
- Real-time status tracking
- Complete results API

### ✅ Infrastructure
- FastAPI web framework
- SQLite database
- Redis message broker
- Celery task queue
- CORS support
- Automatic API documentation
- Email service (SMTP)
- GPT-5.1-Codex-Max integration

---

## 🔧 Troubleshooting

### Server Won't Start
```bash
# Check port 8000 is available
lsof -i :8000

# Kill existing process
kill -9 $(lsof -t -i:8000)

# Restart services
./stop_servers.sh
./start_servers.sh
```

### Redis Connection Error
```bash
# Check Redis status
redis-cli ping

# Start Redis if not running
brew services start redis
```

### Celery Worker Not Processing
```bash
# Check if worker is running
ps aux | grep celery

# Restart worker
pkill -f celery
cd "/Users/waqassafdar/V2T/V2T Backend"
source venv/bin/activate
celery -A app.tasks.video_tasks worker --loglevel=info
```

### Video Processing Fails
1. Check FFmpeg: `ffmpeg -version`
2. Check Tesseract: `tesseract --version`
3. Check Celery logs: `tail -f logs/celery.log`
4. Verify video format: .mp4, .avi, .mov, .mkv
5. Check file size: Max 500MB by default

---

## 📊 Performance Metrics

### Video Processing Time (60-second video, 1 frame/sec)
- Frame extraction: ~5 seconds
- YOLO processing (60 frames): ~3-6 seconds
- OCR processing (60 frames): ~12-30 seconds
- **Total**: ~20-40 seconds

### Resource Usage
- CPU: Moderate (spikes during processing)
- RAM: ~500MB-1GB (includes PyTorch models)
- Disk: ~2GB (includes dependencies + models)
- Network: Minimal (local processing)

---

## 🔄 Development Workflow

### Making Changes

1. **Code Changes**: Edit files in `app/` directory
2. **Server Auto-Reload**: FastAPI hot-reloads automatically
3. **Celery Restart**: Manually restart worker after task changes
   ```bash
   pkill -f celery
   celery -A app.tasks.video_tasks worker --loglevel=info
   ```

### Database Migrations
Currently using SQLite with SQLAlchemy. Tables are created automatically on startup.

To reset database:
```bash
rm v2t.db
# Tables will be recreated on next startup
```

---

## 🚀 Next Steps

### Recommended Enhancements
1. **Frontend Integration**: Build React/Vue.js frontend
2. **WebSocket Support**: Real-time processing updates
3. **User Dashboard**: View all videos and analytics
4. **Video Preview**: Thumbnail generation
5. **Batch Processing**: Process multiple videos
6. **Export Results**: Download JSON/CSV/PDF reports
7. **Advanced YOLO**: Use larger models for better accuracy
8. **Custom OCR**: Fine-tune for specific text types
9. **Cloud Storage**: S3/GCS integration
10. **Rate Limiting**: Prevent API abuse

### Production Deployment
- Switch to PostgreSQL for production database
- Use Nginx as reverse proxy
- Deploy with Docker/Kubernetes
- Set up monitoring (Prometheus, Grafana)
- Configure SSL/TLS certificates
- Enable logging and error tracking (Sentry)
- Set up CI/CD pipeline

---

## 📞 Support & Resources

### Documentation
- **FastAPI**: https://fastapi.tiangolo.com/
- **Celery**: https://docs.celeryproject.org/
- **YOLOv8**: https://docs.ultralytics.com/
- **Tesseract**: https://github.com/tesseract-ocr/tesseract

### Logs Location
- **FastAPI**: `logs/fastapi.log`
- **Celery**: `logs/celery.log`
- **Redis**: Check with `redis-cli MONITOR`

### Health Checks
- Server: `curl http://localhost:8000/`
- Redis: `redis-cli ping`
- Celery: `celery -A app.tasks.video_tasks inspect active`

---

## 📅 Version History

**v1.0.0** - Initial Release (2026-01-20)
- ✅ Authentication system with OTP
- ✅ Video-to-text extraction
- ✅ YOLO object detection
- ✅ Tesseract OCR
- ✅ Async processing with Celery
- ✅ Complete API documentation
- ✅ Automated startup scripts

---

**System Status**: ✅ **FULLY OPERATIONAL**

Last Updated: 2026-01-20
