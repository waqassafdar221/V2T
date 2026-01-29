# V2T System Architecture

## Complete System Overview

```
┌─────────────────────────────────────────────────────────────────────────┐
│                              USER BROWSER                                │
│                        http://localhost:3000                             │
└────────────────────────────────┬────────────────────────────────────────┘
                                 │
                                 │ HTTP/HTTPS
                                 ▼
┌─────────────────────────────────────────────────────────────────────────┐
│                         FRONTEND (Next.js)                               │
│ ┌─────────────┬──────────────┬──────────────┬────────────────────────┐  │
│ │   Landing   │     Auth     │  Dashboard   │   Video Status Page    │  │
│ │    Page     │    Pages     │              │                        │  │
│ └─────────────┴──────────────┴──────────────┴────────────────────────┘  │
│                                                                          │
│ ┌──────────────────────────────────────────────────────────────────┐   │
│ │                    API Client (lib/api.ts)                        │   │
│ │  - Axios instance with JWT interceptor                           │   │
│ │  - Type-safe API methods                                         │   │
│ │  - Error handling                                                │   │
│ └──────────────────────────────────────────────────────────────────┘   │
└──────────────────────────────────┬──────────────────────────────────────┘
                                   │
                                   │ REST API (JWT Auth)
                                   ▼
┌─────────────────────────────────────────────────────────────────────────┐
│                      BACKEND API (FastAPI)                               │
│                      http://localhost:8000                               │
│                                                                          │
│ ┌──────────────────────────────────────────────────────────────────┐   │
│ │                      API Routes                                   │   │
│ │  ┌────────────┬──────────────┬────────────────────────────────┐  │   │
│ │  │    Auth    │    Video     │        Export                  │  │   │
│ │  │  Endpoints │  Endpoints   │      Endpoints                 │  │   │
│ │  └────────────┴──────────────┴────────────────────────────────┘  │   │
│ └──────────────────────────────────────────────────────────────────┘   │
│                                                                          │
│ ┌──────────────────────────────────────────────────────────────────┐   │
│ │                    Core Services                                  │   │
│ │  ┌─────────────┬──────────────┬────────────┬──────────────────┐  │   │
│ │  │  Security   │   Database   │   Email    │  Video Processing│  │   │
│ │  │   (JWT)     │  (SQLAlchemy)│  Service   │     Service      │  │   │
│ │  └─────────────┴──────────────┴────────────┴──────────────────┘  │   │
│ └──────────────────────────────────────────────────────────────────┘   │
└───────────────┬────────────────┬─────────────────┬──────────────────────┘
                │                │                 │
                │                │                 │
                ▼                ▼                 ▼
      ┌─────────────────┐ ┌──────────────┐ ┌────────────────┐
      │   PostgreSQL    │ │    Redis     │ │  File Storage  │
      │    Database     │ │   Message    │ │   (uploads/)   │
      │                 │ │    Broker    │ │                │
      │  - users        │ │              │ │  - videos/     │
      │  - videos       │ └──────┬───────┘ │  - frames/     │
      │  - detected_obj │        │         │  - exports/    │
      │  - extracted_txt│        │         └────────────────┘
      │  - otp_codes    │        │
      └─────────────────┘        │
                                 │
                                 ▼
                       ┌──────────────────┐
                       │  Celery Worker   │
                       │                  │
                       │  - Video Tasks   │
                       │  - Frame Extract │
                       │  - YOLO Detect   │
                       │  - OCR Extract   │
                       └──────────────────┘
```

## Data Flow Diagrams

### 1. User Registration Flow
```
User Browser
     │
     │ 1. Fill signup form
     ▼
Frontend (Signup Page)
     │
     │ 2. POST /auth/signup
     ▼
Backend API (Auth Endpoints)
     │
     │ 3. Hash password, Create user
     ▼
PostgreSQL
     │
     │ 4. Generate OTP
     ▼
Email Service (SMTP)
     │
     │ 5. Send OTP email
     ▼
User Email Inbox
     │
     │ 6. Enter OTP
     ▼
Frontend (Verify OTP Page)
     │
     │ 7. POST /auth/verify-otp
     ▼
Backend API
     │
     │ 8. Verify OTP, Activate user
     ▼
PostgreSQL
     │
     │ 9. Success response
     ▼
Frontend (Login Page)
```

### 2. Video Processing Flow
```
User Browser
     │
     │ 1. Select video file
     ▼
Frontend (Dashboard)
     │
     │ 2. POST /video/upload (with file)
     ▼
Backend API (Video Endpoints)
     │
     ├─ 3a. Save file to disk
     │      └─> File Storage (uploads/videos/)
     │
     ├─ 3b. Create video record
     │      └─> PostgreSQL
     │
     └─ 3c. Queue processing task
            └─> Redis (Message Broker)
                    │
                    │ 4. Task picked up
                    ▼
            Celery Worker
                    │
                    ├─ 5a. Extract frames
                    │      └─> File Storage (uploads/frames/)
                    │
                    ├─ 5b. Run YOLO detection
                    │      └─> PostgreSQL (detected_objects)
                    │
                    ├─ 5c. Run OCR extraction
                    │      └─> PostgreSQL (extracted_texts)
                    │
                    └─ 5d. Update status
                           └─> PostgreSQL (video.status = COMPLETED)

Frontend (Status Page)
     │
     │ 6. Poll GET /video/status/{id} (every 3s)
     ▼
Backend API
     │
     │ 7. Return current status & progress
     ▼
Frontend
     │
     │ 8. When COMPLETED, GET /video/results/{id}
     ▼
Backend API
     │
     │ 9. Return full results
     ▼
Frontend (Display results)
```

### 3. Authentication Flow
```
User Login
     │
     │ username/password
     ▼
Frontend (Login Page)
     │
     │ POST /auth/login
     ▼
Backend API
     │
     ├─ Verify credentials
     │  └─> PostgreSQL
     │
     ├─ Generate JWT token
     │  └─> JWT Library
     │
     └─ Return token + user data
            │
            ▼
     Frontend stores in localStorage
            │
            ▼
     Subsequent requests include:
     Authorization: Bearer <token>
```

## Component Architecture

### Frontend Components
```
app/
├── page.tsx (Landing)
│   ├── Header (with auth buttons)
│   ├── Hero (with CTA)
│   ├── Team
│   ├── Contact
│   └── Footer
│
├── auth/
│   ├── login/page.tsx
│   ├── signup/page.tsx
│   └── verify-otp/page.tsx
│
└── dashboard/
    ├── page.tsx (Upload interface)
    └── video/[videoId]/page.tsx (Status & Results)

lib/
└── api.ts (Centralized API client)

contexts/
└── AuthContext.tsx (Global auth state)
```

### Backend Structure
```
app/
├── api/
│   ├── auth.py (Authentication endpoints)
│   ├── video.py (Video processing endpoints)
│   └── routes.py (Other routes)
│
├── core/
│   ├── config.py (Environment config)
│   ├── database.py (DB connection)
│   ├── security.py (JWT, password hashing)
│   └── celery_app.py (Task queue)
│
├── models/
│   ├── user.py (User, OTP models)
│   └── video.py (Video, DetectedObject, ExtractedText)
│
├── services/
│   ├── email.py (Email sending)
│   ├── video_processing.py (YOLO, OCR)
│   └── export_service.py (Export formats)
│
└── tasks/
    └── video_tasks.py (Celery tasks)
```

## Database Schema

```
┌─────────────────────┐
│       users         │
├─────────────────────┤
│ id (PK)             │
│ name                │
│ username (UNIQUE)   │
│ email (UNIQUE)      │
│ hashed_password     │
│ role                │
│ is_verified         │
│ created_at          │
└─────────────────────┘
          │
          │ 1:N
          ▼
┌─────────────────────┐
│    otp_codes        │
├─────────────────────┤
│ id (PK)             │
│ email               │
│ code                │
│ expires_at          │
│ is_used             │
│ created_at          │
└─────────────────────┘

┌─────────────────────┐
│      videos         │
├─────────────────────┤
│ id (PK)             │
│ video_id (UNIQUE)   │
│ filename            │
│ file_path           │
│ file_size           │
│ status              │
│ duration            │
│ fps                 │
│ error_message       │
│ created_at          │
│ completed_at        │
└──────────┬──────────┘
           │
           ├─────────────────┐
           │                 │
           │ 1:N             │ 1:N
           ▼                 ▼
┌─────────────────────┐ ┌─────────────────────┐
│ detected_objects    │ │ extracted_texts     │
├─────────────────────┤ ├─────────────────────┤
│ id (PK)             │ │ id (PK)             │
│ video_id (FK)       │ │ video_id (FK)       │
│ frame_number        │ │ frame_number        │
│ timestamp           │ │ timestamp           │
│ object_class        │ │ text_content        │
│ confidence          │ │ confidence          │
│ bbox_x1, y1, x2, y2 │ │ created_at          │
│ created_at          │ └─────────────────────┘
└─────────────────────┘
```

## Technology Stack

### Frontend
- **Framework**: Next.js 14 (React 18)
- **Language**: TypeScript
- **HTTP**: Axios
- **Styling**: CSS Modules
- **State**: React Context + Hooks

### Backend
- **Framework**: FastAPI
- **Language**: Python 3.9+
- **Database**: PostgreSQL + SQLAlchemy
- **Cache/Queue**: Redis
- **Task Queue**: Celery
- **Auth**: JWT (python-jose)
- **Password**: bcrypt (passlib)

### AI/ML
- **Object Detection**: YOLOv8 (Ultralytics)
- **OCR**: Tesseract (pytesseract)
- **Image Processing**: OpenCV, Pillow

### DevOps
- **Process Manager**: Uvicorn (ASGI)
- **Task Worker**: Celery
- **Email**: SMTP (Gmail)

## API Endpoints Summary

### Authentication
```
POST   /auth/signup       - Register user
POST   /auth/verify-otp   - Verify email
POST   /auth/login        - Login user
POST   /auth/resend-otp   - Resend OTP
```

### Video Processing
```
POST   /video/upload           - Upload video
GET    /video/status/{id}      - Get status
GET    /video/results/{id}     - Get results
GET    /video/list             - List videos
DELETE /video/delete/{id}      - Delete video
```

### Export
```
GET    /video/export/{id}/txt  - Export TXT
GET    /video/export/{id}/json - Export JSON
GET    /video/export/{id}/csv  - Export CSV
GET    /video/export/{id}/pdf  - Export PDF
```

## Deployment Architecture

```
                    ┌──────────────┐
                    │   Users      │
                    └──────┬───────┘
                           │
                           │ HTTPS
                           ▼
                    ┌──────────────┐
                    │  Load Bal.   │
                    │  (nginx)     │
                    └──────┬───────┘
                           │
              ┌────────────┴────────────┐
              │                         │
              ▼                         ▼
      ┌───────────────┐        ┌───────────────┐
      │   Frontend    │        │   Backend     │
      │   (Next.js)   │        │   (FastAPI)   │
      │   Vercel      │        │   AWS/GCP     │
      └───────────────┘        └───────┬───────┘
                                       │
                       ┌───────────────┼───────────────┐
                       │               │               │
                       ▼               ▼               ▼
              ┌────────────┐  ┌────────────┐  ┌────────────┐
              │ PostgreSQL │  │   Redis    │  │   Celery   │
              │    (RDS)   │  │  (Elastic) │  │  Workers   │
              └────────────┘  └────────────┘  └────────────┘
```

## Security Layers

```
┌─────────────────────────────────────────────┐
│           Frontend Security                  │
│  - Input validation                         │
│  - XSS protection                           │
│  - CSRF tokens                              │
│  - Secure token storage                     │
└─────────────────────────────────────────────┘
                    │
                    ▼
┌─────────────────────────────────────────────┐
│          Transport Security                  │
│  - HTTPS/TLS                                │
│  - CORS configuration                       │
└─────────────────────────────────────────────┘
                    │
                    ▼
┌─────────────────────────────────────────────┐
│           Backend Security                   │
│  - JWT authentication                       │
│  - Password hashing (bcrypt)                │
│  - SQL injection protection (ORM)           │
│  - Rate limiting                            │
│  - File validation                          │
└─────────────────────────────────────────────┘
                    │
                    ▼
┌─────────────────────────────────────────────┐
│          Database Security                   │
│  - Connection encryption                    │
│  - User permissions                         │
│  - Regular backups                          │
└─────────────────────────────────────────────┘
```

This architecture provides a scalable, secure, and maintainable system for video-to-text processing with AI capabilities.
