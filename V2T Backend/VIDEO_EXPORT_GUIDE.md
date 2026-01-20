# Video Export Guide - PDF & Text Export

## Overview

The V2T Backend now supports exporting video processing results to **PDF** and **Text** formats. This allows you to download and share the extracted information from your processed videos.

---

## 📄 Export Formats

### 1. PDF Export
- **Professional formatting** with tables and styling
- **Detailed information** including:
  - Video metadata (ID, filename, status, export date)
  - Detected objects table (object type, confidence, frame, bounding box)
  - Extracted text table (frame number, confidence, text content)
  - Summary statistics with object counts
- **Visual presentation** with color-coded sections
- **Ready for sharing** - professional reports

### 2. Text Export
- **Plain text format** (.txt file)
- **Well-structured** with clear sections
- **Easy to read** with proper formatting
- **All data included**:
  - Video information
  - Detected objects with details
  - Extracted text entries
  - Summary statistics
- **Simple and portable** - works everywhere

---

## 🚀 How to Use

### Prerequisites
1. Video must be **uploaded** and **processing completed**
2. Video status must be `COMPLETED`
3. You need the `video_id` from the upload response

---

## API Endpoints

### 1. Export to Text File

**Endpoint:** `GET /video/export/{video_id}/text`

**Description:** Download video results as a formatted text file

**Example:**
```bash
# Get your JWT token first
TOKEN="your-jwt-token-here"

# Download text file
curl -X GET "http://localhost:8000/video/export/{video_id}/text" \
  -H "Authorization: Bearer $TOKEN" \
  -o "video_results.txt"
```

**Response:** Downloads a `.txt` file

**File Contents:**
```
================================================================================
VIDEO PROCESSING RESULTS
================================================================================

Video ID: abc123
Filename: sample_video.mp4
Status: completed
Export Date: 2026-01-20 18:30:45

--------------------------------------------------------------------------------
DETECTED OBJECTS (15 total)
--------------------------------------------------------------------------------

1. Object: person
   Confidence: 95.30%
   Frame: 10
   Bounding Box: x=120, y=200, width=100, height=300

2. Object: car
   Confidence: 87.50%
   Frame: 25
   Bounding Box: x=450, y=150, width=200, height=150

...

--------------------------------------------------------------------------------
EXTRACTED TEXT (8 entries)
--------------------------------------------------------------------------------

1. Frame 5:
   Confidence: 92.00%
   Text: Welcome to the presentation

2. Frame 120:
   Confidence: 88.00%
   Text: Contact: support@example.com

...

================================================================================
SUMMARY
================================================================================

Object Detection Summary:
  - person: 8
  - car: 4
  - laptop: 3

Total Objects: 15
Total Text Entries: 8

================================================================================
End of Report
================================================================================
```

---

### 2. Export to PDF

**Endpoint:** `GET /video/export/{video_id}/pdf`

**Description:** Download video results as a professionally formatted PDF

**Example:**
```bash
# Get your JWT token first
TOKEN="your-jwt-token-here"

# Download PDF file
curl -X GET "http://localhost:8000/video/export/{video_id}/pdf" \
  -H "Authorization: Bearer $TOKEN" \
  -o "video_results.pdf"
```

**Response:** Downloads a `.pdf` file

**PDF Features:**
- ✅ Professional title and header
- ✅ Video information table
- ✅ Detected objects in formatted table
- ✅ Extracted text in formatted table
- ✅ Summary statistics
- ✅ Color-coded sections (blue headers, grey backgrounds)
- ✅ Proper pagination
- ✅ Print-ready format

---

## 📋 Using Swagger UI

1. **Open Swagger UI**: http://localhost:8000/docs

2. **Navigate to Video Processing section**

3. **Find Export Endpoints**:
   - `GET /video/export/{video_id}/text`
   - `GET /video/export/{video_id}/pdf`

4. **Click "Try it out"**

5. **Enter video_id**

6. **Click "Execute"**

7. **Download the file** from the response

---

## 🔐 Authentication

Both export endpoints require JWT authentication:

```bash
# 1. Login to get token
curl -X POST "http://localhost:8000/auth/login" \
  -H "Content-Type: application/json" \
  -d '{
    "username_or_email": "yourname",
    "password": "yourpassword"
  }' | jq -r '.access_token'

# 2. Use token in export request
curl -X GET "http://localhost:8000/video/export/{video_id}/pdf" \
  -H "Authorization: Bearer YOUR_TOKEN_HERE" \
  -o "results.pdf"
```

---

## 📊 Complete Workflow Example

### Step 1: Upload Video
```bash
TOKEN="your-jwt-token"

curl -X POST "http://localhost:8000/video/upload" \
  -H "Authorization: Bearer $TOKEN" \
  -F "file=@my_video.mp4"
```

**Response:**
```json
{
  "video_id": "abc123",
  "status": "uploaded",
  "message": "Video uploaded successfully"
}
```

### Step 2: Check Status
```bash
curl -X GET "http://localhost:8000/video/status/abc123" \
  -H "Authorization: Bearer $TOKEN"
```

**Wait until status is `completed`**

### Step 3: Export Results

**Option A: Text File**
```bash
curl -X GET "http://localhost:8000/video/export/abc123/text" \
  -H "Authorization: Bearer $TOKEN" \
  -o "video_abc123.txt"
```

**Option B: PDF File**
```bash
curl -X GET "http://localhost:8000/video/export/abc123/pdf" \
  -H "Authorization: Bearer $TOKEN" \
  -o "video_abc123.pdf"
```

---

## 🎯 Python Example

```python
import requests

BASE_URL = "http://localhost:8000"

# Login
response = requests.post(
    f"{BASE_URL}/auth/login",
    json={"username_or_email": "user", "password": "pass"}
)
token = response.json()["access_token"]

headers = {"Authorization": f"Bearer {token}"}

# Export to PDF
video_id = "abc123"
response = requests.get(
    f"{BASE_URL}/video/export/{video_id}/pdf",
    headers=headers
)

# Save PDF
with open(f"video_{video_id}.pdf", "wb") as f:
    f.write(response.content)

print("PDF downloaded successfully!")

# Export to Text
response = requests.get(
    f"{BASE_URL}/video/export/{video_id}/text",
    headers=headers
)

# Save Text
with open(f"video_{video_id}.txt", "wb") as f:
    f.write(response.content)

print("Text file downloaded successfully!")
```

---

## 📂 File Locations

**Exported files are stored in:**
```
uploads/
  └── exports/
      ├── video_abc123_results_20260120_183045.pdf
      ├── video_abc123_results_20260120_183045.txt
      ├── video_def456_results_20260120_190112.pdf
      └── ...
```

**Filename format:**
- PDF: `video_{video_id}_results_{timestamp}.pdf`
- Text: `video_{video_id}_results_{timestamp}.txt`

---

## ⚠️ Error Handling

### Video Not Found (404)
```json
{
  "detail": "Video not found"
}
```

### Processing Not Complete (400)
```json
{
  "detail": "Video processing not completed yet. Current status: processing"
}
```

### Server Error (500)
```json
{
  "detail": "Failed to export PDF file: [error details]"
}
```

---

## 🔍 What's Included in Exports

### Video Information
- Video ID
- Original filename
- Processing status
- Export timestamp

### Detected Objects
- Object class/label (person, car, laptop, etc.)
- Confidence score (%)
- Frame number
- Bounding box coordinates (x, y, width, height)

### Extracted Text
- Frame number where text was found
- OCR confidence score (%)
- Extracted text content

### Summary Statistics
- Total objects detected
- Object count by category
- Total text entries
- Frame coverage

---

## 💡 Tips

1. **Wait for Completion**: Only export when video status is `completed`

2. **File Naming**: Files are auto-named with timestamp - no conflicts

3. **Multiple Exports**: You can export the same video multiple times

4. **Storage**: Export files persist until manually deleted

5. **Large Videos**: For videos with many detections, PDF may be multiple pages

6. **Text Format**: Text files are UTF-8 encoded for international character support

---

## 🚀 Quick Reference

```bash
# Export to PDF
GET /video/export/{video_id}/pdf
Headers: Authorization: Bearer {token}

# Export to Text
GET /video/export/{video_id}/text
Headers: Authorization: Bearer {token}
```

---

## 📞 Troubleshooting

**Problem:** Download fails with 404
- **Solution**: Verify video_id is correct and video exists

**Problem:** Download fails with 400
- **Solution**: Wait for processing to complete, check status first

**Problem:** PDF looks blank
- **Solution**: Check if video had any detections/text extracted

**Problem:** Authentication error
- **Solution**: Login again to get a fresh JWT token

---

## 🎨 Customization

The export format can be customized by editing:
- `app/services/export_service.py` - Export logic
- PDF styling: Colors, fonts, table layouts
- Text format: Section separators, data arrangement

---

**Happy Exporting!** 📄✨

