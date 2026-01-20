# V2T Backend - Deployment Checklist

## ✅ Pre-Deployment Setup (COMPLETED)

### System Dependencies
- [x] Python 3.12 installed
- [x] FFmpeg 8.0.1 installed (`brew install ffmpeg`)
- [x] Tesseract 5.5.1 installed (`brew install tesseract`)
- [x] Redis 8.4.0 installed (`brew install redis`)

### Python Environment
- [x] Virtual environment created (`python3 -m venv venv`)
- [x] Dependencies installed (`pip install -r requirements.txt`)
- [x] All packages verified (68 packages total)

### Project Structure
- [x] Application code in `app/` directory
- [x] Upload directories created (`uploads/videos`, `uploads/frames`)
- [x] Logs directory created (`logs/`)
- [x] Startup scripts created (`start_servers.sh`, `stop_servers.sh`)

### Configuration
- [x] `.env` file configured
- [x] Database URL set
- [x] Secret key configured
- [x] SMTP settings configured (Gmail)
- [x] Redis URL configured
- [x] Video processing settings configured

### Services
- [x] Redis running (brew services)
- [x] Celery worker running
- [x] FastAPI server running on port 8000

---

## 📋 Verification Steps

### 1. System Dependencies
```bash
# Check FFmpeg
ffmpeg -version | head -1
# Expected: ffmpeg version 8.0.1

# Check Tesseract
tesseract --version | head -1
# Expected: tesseract 5.5.1

# Check Redis
redis-cli ping
# Expected: PONG
```

### 2. Server Status
```bash
# Check if server is running
curl http://localhost:8000/
# Expected: JSON response with "Welcome to V2T Backend"

# Check API docs
curl -I http://localhost:8000/docs
# Expected: HTTP/1.1 200 OK
```

### 3. Celery Worker
```bash
# Check if worker is running
ps aux | grep "celery.*worker" | grep -v grep
# Expected: Process with celery command

# Check worker status
celery -A app.tasks.video_tasks inspect active
# Expected: Worker status information
```

### 4. Database
```bash
# Check if database exists
ls -lh v2t.db
# Expected: File exists

# Check tables (SQLite)
sqlite3 v2t.db ".tables"
# Expected: users, otps, videos, detected_objects, extracted_texts
```

---

## 🧪 Functional Testing

### Test 1: Root Endpoint
```bash
curl http://localhost:8000/
```
✅ **Expected**: JSON with version and features

### Test 2: Health Check
```bash
curl http://localhost:8000/health
```
✅ **Expected**: 200 OK

### Test 3: Authentication Flow

**Signup:**
```bash
curl -X POST http://localhost:8000/auth/signup \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Test User",
    "username": "testuser",
    "email": "test@example.com",
    "password": "password123",
    "role": "Student"
  }'
```
✅ **Expected**: 201 Created with success message

**Login:**
```bash
curl -X POST http://localhost:8000/auth/login \
  -H "Content-Type: application/json" \
  -d '{
    "username_or_email": "testuser",
    "password": "password123"
  }'
```
✅ **Expected**: 200 OK with JWT token

### Test 4: Video Upload (Requires JWT Token)
```bash
# Get token first
TOKEN=$(curl -X POST http://localhost:8000/auth/login \
  -H "Content-Type: application/json" \
  -d '{"username_or_email": "testuser", "password": "password123"}' \
  | jq -r '.access_token')

# Upload video
curl -X POST http://localhost:8000/video/upload \
  -H "Authorization: Bearer $TOKEN" \
  -F "file=@test_video.mp4"
```
✅ **Expected**: 200 OK with video_id

### Test 5: Automated Test Script
```bash
python test_video_api.py
```
✅ **Expected**: All tests pass

---

## 🔐 Security Checklist

### Environment Configuration
- [x] `.env` file exists and is properly configured
- [x] `.env` is in `.gitignore` (DO NOT commit)
- [x] `SECRET_KEY` is strong and unique
- [x] SMTP credentials are secure (using app password)
- [ ] Change default passwords in production
- [ ] Enable HTTPS in production

### API Security
- [x] JWT authentication implemented
- [x] Password hashing with bcrypt
- [x] File upload validation (size, format)
- [x] CORS configured
- [ ] Rate limiting (consider adding for production)
- [ ] API key management (if needed)

### File Security
- [x] Upload directory permissions set correctly
- [x] File path sanitization implemented
- [x] Temporary files cleaned up after processing
- [ ] Consider file encryption for sensitive videos

---

## 📊 Performance Monitoring

### Resource Usage
```bash
# CPU usage
top -o cpu | head -20

# Memory usage
top -o mem | head -20

# Disk space
df -h

# Check upload directory size
du -sh uploads/
```

### Log Monitoring
```bash
# FastAPI logs
tail -f logs/fastapi.log

# Celery logs
tail -f logs/celery.log

# Redis logs
redis-cli INFO
```

---

## 🚀 Production Deployment (TODO)

### Database
- [ ] Migrate from SQLite to PostgreSQL
- [ ] Set up database backups
- [ ] Configure connection pooling
- [ ] Set up database monitoring

### Web Server
- [ ] Set up Nginx as reverse proxy
- [ ] Configure SSL/TLS certificates (Let's Encrypt)
- [ ] Enable HTTP/2
- [ ] Set up gzip compression
- [ ] Configure static file serving

### Application
- [ ] Use Gunicorn or similar production WSGI server
- [ ] Set `DEBUG=False` in production
- [ ] Configure proper logging (rotating logs)
- [ ] Set up error tracking (Sentry)
- [ ] Configure environment-specific settings

### Celery
- [ ] Use supervisor/systemd for process management
- [ ] Configure multiple workers for scalability
- [ ] Set up task monitoring (Flower)
- [ ] Configure result backend
- [ ] Set up dead letter queue

### Redis
- [ ] Configure Redis persistence
- [ ] Set up Redis replication for high availability
- [ ] Configure memory limits
- [ ] Enable Redis AUTH
- [ ] Set up Redis monitoring

### Monitoring & Logging
- [ ] Set up application monitoring (Prometheus)
- [ ] Configure alerting (AlertManager)
- [ ] Set up dashboards (Grafana)
- [ ] Centralized logging (ELK stack)
- [ ] Set up uptime monitoring

### Infrastructure
- [ ] Containerize with Docker
- [ ] Set up Docker Compose for multi-container deployment
- [ ] Configure CI/CD pipeline
- [ ] Set up staging environment
- [ ] Configure auto-scaling (if using cloud)
- [ ] Set up CDN for static assets

### Backup & Recovery
- [ ] Database backup strategy
- [ ] Uploaded files backup (S3 or similar)
- [ ] Configuration backup
- [ ] Disaster recovery plan
- [ ] Test restoration procedures

### Security Hardening
- [ ] Security audit
- [ ] Penetration testing
- [ ] Configure firewall rules
- [ ] Set up intrusion detection
- [ ] Regular security updates
- [ ] GDPR compliance (if applicable)

---

## 📈 Scaling Considerations

### Current Capacity
- Single server setup
- Local file storage
- SQLite database
- 1 Celery worker (8 concurrent processes)
- Suitable for: Development, small deployments

### Scaling Strategy

**Phase 1: Vertical Scaling**
- Increase server resources (CPU, RAM)
- Add more Celery workers
- Optimize YOLO model size

**Phase 2: Horizontal Scaling**
- Multiple web servers (load balancer)
- Distributed Celery workers
- Shared Redis cluster
- Centralized file storage (S3, NFS)

**Phase 3: Cloud Native**
- Kubernetes deployment
- Auto-scaling based on load
- Managed database (RDS, Cloud SQL)
- Object storage (S3, GCS)
- CDN for media delivery

---

## 🔄 Maintenance Tasks

### Daily
- [ ] Check server logs for errors
- [ ] Monitor disk space usage
- [ ] Verify all services are running

### Weekly
- [ ] Review application performance
- [ ] Check database size and optimize if needed
- [ ] Clean up old uploaded files
- [ ] Review security logs

### Monthly
- [ ] Update dependencies (security patches)
- [ ] Review and rotate logs
- [ ] Database maintenance (vacuum, analyze)
- [ ] Performance optimization review
- [ ] Backup verification

---

## 📞 Emergency Contacts & Procedures

### Service Restart
```bash
# Quick restart
./stop_servers.sh && ./start_servers.sh

# Full restart (including Redis)
brew services restart redis
./stop_servers.sh
./start_servers.sh
```

### Database Recovery
```bash
# Backup current database
cp v2t.db v2t.db.backup.$(date +%Y%m%d_%H%M%S)

# Restore from backup
cp v2t.db.backup.TIMESTAMP v2t.db
```

### Clear Stuck Tasks
```bash
# Purge all Celery tasks
celery -A app.tasks.video_tasks purge

# Restart Celery worker
pkill -f celery
celery -A app.tasks.video_tasks worker --loglevel=info
```

---

## ✅ Final Verification

Run this complete verification script:

```bash
#!/bin/bash
echo "=== V2T Backend Deployment Verification ==="
echo ""

echo "1. System Dependencies:"
ffmpeg -version > /dev/null 2>&1 && echo "  ✅ FFmpeg" || echo "  ❌ FFmpeg"
tesseract --version > /dev/null 2>&1 && echo "  ✅ Tesseract" || echo "  ❌ Tesseract"
redis-cli ping > /dev/null 2>&1 && echo "  ✅ Redis" || echo "  ❌ Redis"

echo ""
echo "2. Services:"
curl -s http://localhost:8000/ > /dev/null 2>&1 && echo "  ✅ FastAPI" || echo "  ❌ FastAPI"
ps aux | grep "celery.*worker" | grep -v grep > /dev/null 2>&1 && echo "  ✅ Celery" || echo "  ❌ Celery"

echo ""
echo "3. Directories:"
[ -d "uploads/videos" ] && echo "  ✅ uploads/videos" || echo "  ❌ uploads/videos"
[ -d "uploads/frames" ] && echo "  ✅ uploads/frames" || echo "  ❌ uploads/frames"
[ -d "logs" ] && echo "  ✅ logs" || echo "  ❌ logs"

echo ""
echo "4. Configuration:"
[ -f ".env" ] && echo "  ✅ .env" || echo "  ❌ .env"
[ -f "v2t.db" ] && echo "  ✅ Database" || echo "  ❌ Database"

echo ""
echo "=== Verification Complete ==="
```

---

**Deployment Status**: ✅ **READY FOR USE**

**Environment**: Development  
**Date**: 2026-01-20  
**Version**: 1.0.0
