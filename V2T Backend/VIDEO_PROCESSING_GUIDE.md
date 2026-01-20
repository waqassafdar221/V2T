# Video Processing System Guide

## Overview

The V2T Backend includes a comprehensive video-to-text extraction system that:
- Accepts video uploads via REST API
- Extracts frames at configurable intervals using FFmpeg
- Performs object detection on frames using YOLOv8
- Extracts text from frames using Tesseract OCR
- Processes videos asynchronously using Celery + Redis
- Provides status checking and results retrieval APIs

## System Requirements

### Already Installed ✅
- **FFmpeg 8.0.1**: For video frame extraction
- **Tesseract 5.5.1**: For OCR text extraction
- **Redis 8.4.0**: For Celery message broker
- **Python Packages**:
  - torch 2.9.1
  - torchvision 0.24.1
  - ultralytics 8.4.6 (YOLOv8)
  - opencv-python 4.13.0
  - pytesseract 0.3.13
  - celery 5.6.2
  - redis 7.1.0
  - Pillow 12.1.0
  - ffmpeg-python 0.2.0

## Architecture

```
Video Upload → Save to Disk → Trigger Celery Task → Background Processing
                                                    ├─ Extract Frames (FFmpeg)
                                                    ├─ Detect Objects (YOLO)
                                                    ├─ Extract Text (OCR)
                                                    └─ Save Results to DB
```

## API Endpoints

### 1. Upload Video
**POST** `/video/upload`

Upload a video file for processing.

**Request:**
- **Content-Type**: multipart/form-data
- **Body**: 
  - `file`: Video file (.mp4, .avi, .mov, .mkv)

**Response:**
```json
{
  "video_id": 1,
  "message": "Video uploaded successfully. Processing started.",
  "status": "pending"
}
```

**cURL Example:**
```bash
curl -X POST "http://localhost:8000/video/upload" \
  -H "Authorization: Bearer YOUR_JWT_TOKEN" \
  -F "file=@/path/to/video.mp4"
```

### 2. Check Processing Status
**GET** `/video/status/{video_id}`

Get current processing status of a video.

**Response:**
```json
{
  "video_id": 1,
  "status": "processing",
  "progress": 45,
  "created_at": "2025-01-19T10:30:00"
}
```

**Possible Statuses:**
- `pending`: Video uploaded, waiting to be processed
- `processing`: Currently extracting frames and running analysis
- `completed`: All processing finished successfully
- `failed`: Error occurred during processing

**cURL Example:**
```bash
curl -X GET "http://localhost:8000/video/status/1" \
  -H "Authorization: Bearer YOUR_JWT_TOKEN"
```

### 3. Get Processing Results
**GET** `/video/results/{video_id}`

Retrieve complete processing results.

**Response:**
```json
{
  "video_id": 1,
  "status": "completed",
  "file_path": "uploads/videos/video_1_20250119_103000.mp4",
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
  "created_at": "2025-01-19T10:30:00",
  "updated_at": "2025-01-19T10:32:15"
}
```

**cURL Example:**
```bash
curl -X GET "http://localhost:8000/video/results/1" \
  -H "Authorization: Bearer YOUR_JWT_TOKEN"
```

## Running the System

### 1. Start Redis (Already Running)
Redis is running as a background service via Homebrew.

Check status:
```bash
redis-cli ping  # Should return PONG
```

### 2. Start Celery Worker

**Option A: Terminal (Recommended for Development)**
```bash
cd "/Users/waqassafdar/V2T/V2T Backend"
source venv/bin/activate
celery -A app.tasks.video_tasks worker --loglevel=info
```

**Option B: Background Process**
```bash
cd "/Users/waqassafdar/V2T/V2T Backend"
source venv/bin/activate
celery -A app.tasks.video_tasks worker --loglevel=info --detach
```

### 3. Start FastAPI Server
```bash
cd "/Users/waqassafdar/V2T/V2T Backend"
source venv/bin/activate
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

## Configuration

Edit `.env` or `app/core/config.py` to customize:

```ini
# Video Processing Settings
VIDEO_UPLOAD_DIR=./uploads/videos
VIDEO_FRAMES_DIR=./uploads/frames
MAX_VIDEO_SIZE_MB=500
FRAME_EXTRACTION_INTERVAL=1  # Extract 1 frame per second
YOLO_CONFIDENCE_THRESHOLD=0.5  # Minimum confidence for object detection

# Redis/Celery
REDIS_URL=redis://localhost:6379/0
CELERY_BROKER_URL=redis://localhost:6379/0
CELERY_RESULT_BACKEND=redis://localhost:6379/0
```

## Directory Structure

```
/Users/waqassafdar/V2T/V2T Backend/
├── uploads/
│   ├── videos/          # Uploaded video files
│   └── frames/          # Extracted frames (auto-cleaned after processing)
├── app/
│   ├── api/
│   │   └── video.py     # Video processing endpoints
│   ├── models/
│   │   └── video.py     # Video, DetectedObject, ExtractedText models
│   ├── services/
│   │   └── video_processing.py  # FFmpeg, YOLO, OCR logic
│   ├── tasks/
│   │   └── video_tasks.py       # Celery async tasks
│   └── core/
│       └── celery_app.py        # Celery configuration
```

## Workflow Example

1. **Upload Video:**
   ```bash
   # Login first to get JWT token
   curl -X POST "http://localhost:8000/auth/login" \
     -H "Content-Type: application/json" \
     -d '{"username": "testuser", "password": "password123"}'
   
   # Upload video (use token from login response)
   curl -X POST "http://localhost:8000/video/upload" \
     -H "Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGc..." \
     -F "file=@sample_video.mp4"
   ```

2. **Monitor Progress:**
   ```bash
   # Check status periodically
   curl -X GET "http://localhost:8000/video/status/1" \
     -H "Authorization: Bearer YOUR_TOKEN"
   ```

3. **Get Results:**
   ```bash
   # Once status is "completed"
   curl -X GET "http://localhost:8000/video/results/1" \
     -H "Authorization: Bearer YOUR_TOKEN"
   ```

## Troubleshooting

### Celery Worker Not Processing Tasks
```bash
# Check if worker is running
ps aux | grep celery

# Check Celery logs
celery -A app.tasks.video_tasks worker --loglevel=debug

# Restart worker
pkill -f celery
celery -A app.tasks.video_tasks worker --loglevel=info
```

### Redis Connection Error
```bash
# Check if Redis is running
redis-cli ping

# Start Redis if not running
brew services start redis
```

### FFmpeg Not Found
```bash
# Verify FFmpeg is installed
which ffmpeg
ffmpeg -version

# Install if needed
brew install ffmpeg
```

### Tesseract Not Found
```bash
# Verify Tesseract is installed
which tesseract
tesseract --version

# Install if needed
brew install tesseract
```

### YOLO Model Download
The first time YOLO runs, it will automatically download the model weights (~6MB for YOLOv8n). This is normal and happens once.

### Video Upload Errors
- **File too large**: Increase `MAX_VIDEO_SIZE_MB` in config
- **Invalid format**: Ensure video is .mp4, .avi, .mov, or .mkv
- **Permission denied**: Check upload directory permissions
  ```bash
  chmod -R 755 uploads/
  ```

## Performance Notes

- **Frame Extraction**: 1 frame/second is default (configurable)
- **YOLO Processing**: ~50-100ms per frame on M1/M2 Mac
- **OCR Processing**: ~200-500ms per frame
- **Total Time**: For a 60-second video:
  - Frame extraction: ~5 seconds
  - YOLO on 60 frames: ~3-6 seconds
  - OCR on 60 frames: ~12-30 seconds
  - **Total**: ~20-40 seconds

## Security Considerations

1. **File Validation**: Only .mp4, .avi, .mov, .mkv allowed
2. **Size Limits**: Default 500MB max upload
3. **Authentication**: JWT token required for all endpoints
4. **Path Sanitization**: Prevents directory traversal attacks
5. **Temporary Cleanup**: Frames deleted after processing

## Advanced Usage

### Custom YOLO Model
Edit `app/services/video_processing.py`:
```python
# Use a larger, more accurate model
model = YOLO("yolov8m.pt")  # Medium model
# or
model = YOLO("yolov8x.pt")  # Extra large model
```

### Adjust Frame Extraction Rate
Edit `.env`:
```ini
FRAME_EXTRACTION_INTERVAL=0.5  # Extract 2 frames per second
# or
FRAME_EXTRACTION_INTERVAL=2    # Extract 1 frame every 2 seconds
```

### Multiple Workers
```bash
# Start multiple workers for parallel processing
celery -A app.tasks.video_tasks worker -Q video_processing --concurrency=4
```

## API Testing with Swagger

Access interactive API docs:
- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

## Database Schema

**Videos Table:**
- `id`: Primary key
- `filename`: Original filename
- `file_path`: Stored file path
- `status`: pending/processing/completed/failed
- `created_at`, `updated_at`: Timestamps

**DetectedObjects Table:**
- `id`: Primary key
- `video_id`: Foreign key to videos
- `label`: Object class (person, car, etc.)
- `confidence`: Detection confidence (0-1)
- `bbox_x, bbox_y, bbox_width, bbox_height`: Bounding box
- `frame_number`: Frame index

**ExtractedTexts Table:**
- `id`: Primary key
- `video_id`: Foreign key to videos
- `text`: Extracted text content
- `confidence`: OCR confidence (0-1)
- `frame_number`: Frame index

## Next Steps

1. ✅ All dependencies installed
2. ✅ Redis running
3. 🔄 Start Celery worker
4. 🔄 Start FastAPI server
5. 🔄 Test video upload via Swagger UI

## Support

For issues or questions:
- Check server logs: Console where uvicorn is running
- Check Celery logs: Console where worker is running
- Check Redis: `redis-cli monitor`
