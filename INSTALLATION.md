# Installation Instructions

## Quick Install Commands

### Frontend Dependencies
```bash
cd "V2T Front End"
npm install
```

This will install:
- next@14.0.4
- react@18.2.0
- react-dom@18.2.0
- axios@1.6.2
- typescript@5
- @types/node@20
- @types/react@18
- @types/react-dom@18
- eslint@8
- eslint-config-next@14.0.4

### Backend Dependencies
```bash
cd "V2T Backend"
pip install -r requirements.txt
```

## System Requirements

### Required Software
1. **Node.js** (v18 or higher)
   - Download: https://nodejs.org/

2. **Python** (v3.9 or higher)
   - Download: https://www.python.org/downloads/

3. **PostgreSQL** (v12 or higher)
   - macOS: `brew install postgresql`
   - Ubuntu: `sudo apt install postgresql postgresql-contrib`
   - Windows: https://www.postgresql.org/download/windows/

4. **Redis** (v6 or higher)
   - macOS: `brew install redis`
   - Ubuntu: `sudo apt install redis-server`
   - Windows: https://redis.io/download

### Optional (for Development)
- **Git** for version control
- **VS Code** or your preferred IDE
- **Postman** for API testing

## Detailed Installation Steps

### 1. Clone/Navigate to Project
```bash
cd /path/to/V2T
```

### 2. Install Frontend
```bash
cd "V2T Front End"

# Install dependencies
npm install

# Verify installation
npm list
```

### 3. Install Backend
```bash
cd ../V2T\ Backend

# Create virtual environment (recommended)
python -m venv venv

# Activate virtual environment
# On macOS/Linux:
source venv/bin/activate
# On Windows:
venv\Scripts\activate

# Upgrade pip
pip install --upgrade pip

# Install dependencies
pip install -r requirements.txt

# Verify installation
pip list
```

### 4. Setup PostgreSQL Database
```bash
# Start PostgreSQL service
# macOS:
brew services start postgresql
# Ubuntu:
sudo service postgresql start

# Create database
psql -U postgres -c "CREATE DATABASE v2t_db;"

# Verify
psql -U postgres -l
```

### 5. Setup Redis
```bash
# Start Redis service
# macOS:
brew services start redis
# Ubuntu:
sudo service redis-server start

# Verify
redis-cli ping
# Should respond with "PONG"
```

### 6. Configure Environment Variables

**Frontend** - Create `V2T Front End/.env.local`:
```env
NEXT_PUBLIC_API_URL=http://localhost:8000
NEXT_PUBLIC_APP_NAME=V2T - Video to Text
```

**Backend** - Create `V2T Backend/.env`:
```env
# Database
DATABASE_URL=postgresql://postgres:password@localhost/v2t_db

# Security
SECRET_KEY=your-super-secret-key-min-32-chars-long
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30

# Celery
CELERY_BROKER_URL=redis://localhost:6379/0
CELERY_RESULT_BACKEND=redis://localhost:6379/0

# Email (use your Gmail account)
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
CORS_ORIGINS=http://localhost:3000
```

### 7. Initialize Database Tables
```bash
cd "V2T Backend"

# Tables will be created automatically on first run
# Or run manually:
python -c "from app.core.database import create_tables; create_tables()"
```

## Running the Application

### Start Backend (3 terminals needed)

**Terminal 1 - FastAPI Server**:
```bash
cd "V2T Backend"
source venv/bin/activate  # if using venv
uvicorn main:app --reload --port 8000
```

**Terminal 2 - Celery Worker**:
```bash
cd "V2T Backend"
source venv/bin/activate  # if using venv
celery -A app.core.celery_app worker --loglevel=info
```

**OR use the convenience script**:
```bash
cd "V2T Backend"
./start_servers.sh
```

### Start Frontend

**Terminal 3 - Next.js**:
```bash
cd "V2T Front End"
npm run dev
```

## Verify Installation

### Check Services
```bash
# PostgreSQL
psql -U postgres -c "SELECT version();"

# Redis
redis-cli ping

# Backend API
curl http://localhost:8000/docs

# Frontend
curl http://localhost:3000
```

### Access Points
- Frontend: http://localhost:3000
- Backend API: http://localhost:8000
- API Docs: http://localhost:8000/docs

## Troubleshooting

### Frontend Issues

**npm install fails**:
```bash
# Clear cache
npm cache clean --force

# Delete node_modules and package-lock.json
rm -rf node_modules package-lock.json

# Reinstall
npm install
```

**Port 3000 already in use**:
```bash
# Use different port
PORT=3001 npm run dev
```

### Backend Issues

**pip install fails**:
```bash
# Upgrade pip
pip install --upgrade pip

# Install with no cache
pip install --no-cache-dir -r requirements.txt
```

**PostgreSQL connection error**:
```bash
# Check if PostgreSQL is running
# macOS:
brew services list

# Ubuntu:
sudo service postgresql status

# Check connection
psql -U postgres -d v2t_db
```

**Redis connection error**:
```bash
# Check if Redis is running
redis-cli ping

# Start Redis
# macOS:
brew services start redis

# Ubuntu:
sudo service redis-server start
```

**Celery worker fails**:
```bash
# Check Redis connection
redis-cli ping

# Restart Celery with verbose logging
celery -A app.core.celery_app worker --loglevel=debug
```

### Email Issues

**Gmail SMTP not working**:
1. Enable 2-factor authentication on Gmail
2. Generate App Password: https://myaccount.google.com/apppasswords
3. Use app password in SMTP_PASSWORD (not your Gmail password)

### Database Issues

**Tables not created**:
```bash
# Manually create tables
python -c "from app.core.database import create_tables; create_tables()"
```

**Reset database**:
```bash
# Drop and recreate
psql -U postgres -c "DROP DATABASE v2t_db;"
psql -U postgres -c "CREATE DATABASE v2t_db;"
```

## Dependency Versions

### Frontend
```json
{
  "next": "14.0.4",
  "react": "^18.2.0",
  "react-dom": "^18.2.0",
  "axios": "^1.6.2",
  "typescript": "^5"
}
```

### Backend (Key Packages)
```
fastapi>=0.104.0
uvicorn[standard]>=0.24.0
sqlalchemy>=2.0.0
psycopg2-binary>=2.9.9
celery>=5.3.4
redis>=5.0.1
python-jose[cryptography]
passlib[bcrypt]
python-multipart
opencv-python
ultralytics
pytesseract
Pillow
```

## Post-Installation

### Create First User
1. Navigate to http://localhost:3000
2. Click "Sign Up"
3. Fill in details
4. Check email for OTP
5. Verify and login

### Test Video Upload
1. Login to dashboard
2. Upload a test video (MP4 recommended)
3. Monitor processing status
4. View results
5. Export data

## Production Setup

### Frontend Production Build
```bash
cd "V2T Front End"
npm run build
npm start
```

### Backend Production Server
```bash
cd "V2T Backend"
gunicorn main:app -w 4 -k uvicorn.workers.UvicornWorker --bind 0.0.0.0:8000
```

### Environment Variables
- Set strong SECRET_KEY
- Use production database
- Configure production CORS origins
- Enable HTTPS
- Set production email credentials

## Support
For installation issues, check:
1. Node.js and Python versions
2. PostgreSQL and Redis services running
3. Environment variables set correctly
4. Firewall/antivirus not blocking ports
5. Sufficient disk space for uploads
