import os
import shutil
from fastapi import APIRouter, UploadFile, File, HTTPException, Depends, status, BackgroundTasks
from fastapi.responses import FileResponse
from sqlalchemy.orm import Session
from typing import List, Dict
from pathlib import Path
from app.core.database import get_db
from app.core.config import settings
from app.core.security import get_current_user
from app.models.video import (
    Video, DetectedObject, ExtractedText, VideoStatus,
    VideoUploadResponse, VideoProcessingResult, VideoStatusResponse,
    BoundingBox, DetectedObjectResponse, ExtractedTextResponse
)
from app.services.video_processing import VideoProcessingService
from app.services.export_service import ExportService
from app.tasks.video_tasks import process_video_task
import logging

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/video", tags=["Video Processing"])

# Allowed video formats
ALLOWED_EXTENSIONS = {'.mp4', '.avi', '.mov', '.mkv', '.flv', '.wmv'}
MAX_FILE_SIZE = 500 * 1024 * 1024  # 500MB


def validate_video_file(filename: str, file_size: int):
    """Validate uploaded video file."""
    file_ext = Path(filename).suffix.lower()
    
    if file_ext not in ALLOWED_EXTENSIONS:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Invalid file format. Allowed formats: {', '.join(ALLOWED_EXTENSIONS)}"
        )
    
    if file_size > MAX_FILE_SIZE:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"File size exceeds maximum allowed size of {MAX_FILE_SIZE // (1024*1024)}MB"
        )


@router.post("/upload", response_model=VideoUploadResponse, status_code=status.HTTP_201_CREATED)
async def upload_video(
    file: UploadFile = File(...),
    background_tasks: BackgroundTasks = None,
    db: Session = Depends(get_db),
    current_user: Dict = Depends(get_current_user)
):
    """
    Upload a video file for processing.
    
    The video will be processed asynchronously:
    - Frames will be extracted
    - YOLO object detection will be applied
    - OCR text extraction will be performed
    
    Returns a video_id to track processing status.
    """
    try:
        # Read file size
        file.file.seek(0, 2)
        file_size = file.file.tell()
        file.file.seek(0)
        
        # Validate file
        validate_video_file(file.filename, file_size)
        
        # Generate unique video ID
        video_service = VideoProcessingService()
        video_id = video_service.generate_video_id()
        
        # Create upload directory
        upload_dir = Path(settings.video_upload_dir)
        upload_dir.mkdir(parents=True, exist_ok=True)
        
        # Save uploaded file
        file_ext = Path(file.filename).suffix
        video_filename = f"{video_id}{file_ext}"
        video_path = upload_dir / video_filename
        
        with open(video_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
        
        # Create video record in database
        video = Video(
            video_id=video_id,
            filename=file.filename,
            file_path=str(video_path),
            file_size=file_size,
            status=VideoStatus.UPLOADED
        )
        db.add(video)
        db.commit()
        db.refresh(video)
        
        # Queue video processing task
        process_video_task.delay(video_id, str(video_path), frame_interval=1)
        
        logger.info(f"Video uploaded successfully: {video_id}")
        
        return VideoUploadResponse(
            video_id=video_id,
            filename=file.filename,
            file_size=file_size,
            status=VideoStatus.UPLOADED,
            message="Video uploaded successfully. Processing started in background."
        )
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Video upload failed: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to upload video: {str(e)}"
        )


@router.get("/status/{video_id}", response_model=VideoStatusResponse)
async def get_video_status(
    video_id: str, 
    db: Session = Depends(get_db),
    current_user: Dict = Depends(get_current_user)
):
    """
    Get the processing status of a video.
    
    Returns the current status and progress information.
    Requires authentication.
    """
    video = db.query(Video).filter(Video.video_id == video_id).first()
    
    if not video:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Video not found"
        )
    
    # Calculate progress
    progress = None
    if video.status == VideoStatus.UPLOADED:
        progress = 0
    elif video.status == VideoStatus.PROCESSING:
        progress = 50
    elif video.status == VideoStatus.COMPLETED:
        progress = 100
    elif video.status == VideoStatus.FAILED:
        progress = 0
    
    # Status message
    status_messages = {
        VideoStatus.UPLOADED: "Video uploaded, waiting to be processed",
        VideoStatus.PROCESSING: "Processing video frames and extracting data",
        VideoStatus.COMPLETED: "Processing completed successfully",
        VideoStatus.FAILED: "Processing failed"
    }
    
    return VideoStatusResponse(
        video_id=video_id,
        status=video.status,
        progress=progress,
        message=status_messages.get(video.status, "Unknown status"),
        error_message=video.error_message
    )


@router.get("/results/{video_id}", response_model=VideoProcessingResult)
async def get_video_results(
    video_id: str, 
    db: Session = Depends(get_db),
    current_user: Dict = Depends(get_current_user)
):
    """
    Get the complete processing results for a video.
    
    Returns:
    - Video metadata
    - Detected objects with bounding boxes
    - Extracted text from frames
    
    Requires authentication.
    """
    # Get video
    video = db.query(Video).filter(Video.video_id == video_id).first()
    
    if not video:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Video not found"
        )
    
    if video.status != VideoStatus.COMPLETED:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Video processing not completed yet. Current status: {video.status}"
        )
    
    # Get detected objects
    detected_objects = db.query(DetectedObject).filter(
        DetectedObject.video_id == video_id
    ).all()
    
    detected_objects_response = [
        DetectedObjectResponse(
            frame_number=obj.frame_number,
            timestamp=obj.timestamp,
            object_class=obj.object_class,
            confidence=obj.confidence,
            bbox=BoundingBox(
                x1=obj.bbox_x1,
                y1=obj.bbox_y1,
                x2=obj.bbox_x2,
                y2=obj.bbox_y2
            )
        )
        for obj in detected_objects
    ]
    
    # Get extracted texts
    extracted_texts = db.query(ExtractedText).filter(
        ExtractedText.video_id == video_id
    ).all()
    
    extracted_texts_response = [
        ExtractedTextResponse(
            frame_number=text.frame_number,
            timestamp=text.timestamp,
            text=text.text_content,
            confidence=text.confidence
        )
        for text in extracted_texts
    ]
    
    # Calculate total frames
    total_frames = max(
        max((obj.frame_number for obj in detected_objects), default=0),
        max((text.frame_number for text in extracted_texts), default=0)
    ) + 1
    
    return VideoProcessingResult(
        video_id=video_id,
        filename=video.filename,
        status=video.status,
        duration=video.duration,
        fps=video.fps,
        total_frames=total_frames,
        detected_objects=detected_objects_response,
        extracted_texts=extracted_texts_response,
        error_message=video.error_message,
        created_at=video.created_at,
        completed_at=video.completed_at
    )


@router.delete("/delete/{video_id}")
async def delete_video(
    video_id: str, 
    db: Session = Depends(get_db),
    current_user: Dict = Depends(get_current_user)
):
    """
    Delete a video and all associated data.
    
    Removes:
    - Video file
    - Extracted frames
    - Database records
    
    Requires authentication.
    """
    video = db.query(Video).filter(Video.video_id == video_id).first()
    
    if not video:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Video not found"
        )
    
    try:
        # Delete video file
        if os.path.exists(video.file_path):
            os.remove(video.file_path)
        
        # Delete frames
        video_service = VideoProcessingService()
        video_service.cleanup_frames(video_id)
        
        # Delete database records
        db.query(DetectedObject).filter(DetectedObject.video_id == video_id).delete()
        db.query(ExtractedText).filter(ExtractedText.video_id == video_id).delete()
        db.query(Video).filter(Video.video_id == video_id).delete()
        db.commit()
        
        logger.info(f"Video {video_id} deleted successfully")
        
        return {
            "message": "Video and all associated data deleted successfully",
            "video_id": video_id
        }
        
    except Exception as e:
        logger.error(f"Failed to delete video {video_id}: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to delete video: {str(e)}"
        )


@router.get("/list")
async def list_videos(
    skip: int = 0,
    limit: int = 100,
    status_filter: str = None,
    db: Session = Depends(get_db),
    current_user: Dict = Depends(get_current_user)
):
    """
    List all uploaded videos with optional filtering by status.
    Requires authentication.
    """
    query = db.query(Video)
    
    if status_filter:
        query = query.filter(Video.status == status_filter)
    
    videos = query.offset(skip).limit(limit).all()
    
    return {
        "total": len(videos),
        "videos": [
            {
                "video_id": v.video_id,
                "filename": v.filename,
                "status": v.status,
                "created_at": v.created_at,
                "completed_at": v.completed_at
            }
            for v in videos
        ]
    }


@router.get("/export/{video_id}/text")
async def export_video_text(
    video_id: str, 
    db: Session = Depends(get_db),
    current_user: Dict = Depends(get_current_user)
):
    """
    Export video processing results to a text file.
    
    Downloads a formatted .txt file containing:
    - Video information
    - Detected objects with details
    - Extracted text from frames
    - Summary statistics
    
    Requires authentication.
    """
    # Get video
    video = db.query(Video).filter(Video.video_id == video_id).first()
    
    if not video:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Video not found"
        )
    
    if video.status != VideoStatus.COMPLETED:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Video processing not completed yet. Current status: {video.status}"
        )
    
    try:
        # Get detected objects and texts
        detected_objects = db.query(DetectedObject).filter(
            DetectedObject.video_id == video_id
        ).order_by(DetectedObject.frame_number).all()
        
        extracted_texts = db.query(ExtractedText).filter(
            ExtractedText.video_id == video_id
        ).order_by(ExtractedText.frame_number).all()
        
        # Generate text file
        export_service = ExportService()
        file_path = export_service.export_to_text(
            video_id=video_id,
            video_filename=video.filename,
            detected_objects=detected_objects,
            extracted_texts=extracted_texts,
            status=video.status
        )
        
        # Return file download
        return FileResponse(
            path=file_path,
            filename=os.path.basename(file_path),
            media_type='text/plain',
            headers={
                "Content-Disposition": f"attachment; filename={os.path.basename(file_path)}"
            }
        )
        
    except Exception as e:
        logger.error(f"Failed to export text for video {video_id}: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to export text file: {str(e)}"
        )


@router.get("/export/{video_id}/pdf")
async def export_video_pdf(
    video_id: str, 
    db: Session = Depends(get_db),
    current_user: Dict = Depends(get_current_user)
):
    """
    Export video processing results to a PDF file.
    
    Downloads a professionally formatted PDF containing:
    - Video information
    - Detected objects table with bounding boxes
    - Extracted text table
    - Summary statistics with visualizations
    
    Requires authentication.
    """
    # Get video
    video = db.query(Video).filter(Video.video_id == video_id).first()
    
    if not video:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Video not found"
        )
    
    if video.status != VideoStatus.COMPLETED:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Video processing not completed yet. Current status: {video.status}"
        )
    
    try:
        # Get detected objects and texts
        detected_objects = db.query(DetectedObject).filter(
            DetectedObject.video_id == video_id
        ).order_by(DetectedObject.frame_number).all()
        
        extracted_texts = db.query(ExtractedText).filter(
            ExtractedText.video_id == video_id
        ).order_by(ExtractedText.frame_number).all()
        
        # Generate PDF file
        export_service = ExportService()
        file_path = export_service.export_to_pdf(
            video_id=video_id,
            video_filename=video.filename,
            detected_objects=detected_objects,
            extracted_texts=extracted_texts,
            status=video.status
        )
        
        # Return file download
        return FileResponse(
            path=file_path,
            filename=os.path.basename(file_path),
            media_type='application/pdf',
            headers={
                "Content-Disposition": f"attachment; filename={os.path.basename(file_path)}"
            }
        )
        
    except Exception as e:
        logger.error(f"Failed to export PDF for video {video_id}: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to export PDF file: {str(e)}"
        )


@router.get("/export/{video_id}/json")
async def export_video_json(
    video_id: str, 
    db: Session = Depends(get_db),
    current_user: Dict = Depends(get_current_user)
):
    """
    Export video processing results to a JSON file.
    
    Returns structured JSON with:
    - Video metadata
    - Array of detected objects
    - Array of extracted texts
    - Processing statistics
    
    Requires authentication.
    """
    # Get video
    video = db.query(Video).filter(Video.video_id == video_id).first()
    
    if not video:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Video not found"
        )
    
    if video.status != VideoStatus.COMPLETED:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Video processing not completed yet. Current status: {video.status}"
        )
    
    try:
        # Get detected objects and texts
        detected_objects = db.query(DetectedObject).filter(
            DetectedObject.video_id == video_id
        ).order_by(DetectedObject.frame_number).all()
        
        extracted_texts = db.query(ExtractedText).filter(
            ExtractedText.video_id == video_id
        ).order_by(ExtractedText.frame_number).all()
        
        # Generate JSON file
        export_service = ExportService()
        file_path = export_service.export_to_json(
            video_id=video_id,
            video_filename=video.filename,
            detected_objects=detected_objects,
            extracted_texts=extracted_texts,
            status=video.status,
            duration=video.duration,
            fps=video.fps
        )
        
        # Return file download
        return FileResponse(
            path=file_path,
            filename=os.path.basename(file_path),
            media_type='application/json',
            headers={
                "Content-Disposition": f"attachment; filename={os.path.basename(file_path)}"
            }
        )
        
    except Exception as e:
        logger.error(f"Failed to export JSON for video {video_id}: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to export JSON file: {str(e)}"
        )


@router.get("/export/{video_id}/csv")
async def export_video_csv(
    video_id: str, 
    db: Session = Depends(get_db),
    current_user: Dict = Depends(get_current_user)
):
    """
    Export video processing results to a CSV file.
    
    Returns CSV with separate sections for:
    - Detected objects (frame, timestamp, class, confidence, bbox)
    - Extracted texts (frame, timestamp, text, confidence)
    
    Requires authentication.
    """
    # Get video
    video = db.query(Video).filter(Video.video_id == video_id).first()
    
    if not video:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Video not found"
        )
    
    if video.status != VideoStatus.COMPLETED:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Video processing not completed yet. Current status: {video.status}"
        )
    
    try:
        # Get detected objects and texts
        detected_objects = db.query(DetectedObject).filter(
            DetectedObject.video_id == video_id
        ).order_by(DetectedObject.frame_number).all()
        
        extracted_texts = db.query(ExtractedText).filter(
            ExtractedText.video_id == video_id
        ).order_by(ExtractedText.frame_number).all()
        
        # Generate CSV file
        export_service = ExportService()
        file_path = export_service.export_to_csv(
            video_id=video_id,
            video_filename=video.filename,
            detected_objects=detected_objects,
            extracted_texts=extracted_texts
        )
        
        # Return file download
        return FileResponse(
            path=file_path,
            filename=os.path.basename(file_path),
            media_type='text/csv',
            headers={
                "Content-Disposition": f"attachment; filename={os.path.basename(file_path)}"
            }
        )
        
    except Exception as e:
        logger.error(f"Failed to export CSV for video {video_id}: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to export CSV file: {str(e)}"
        )


@router.get("/export/{video_id}/txt")
async def export_video_txt(
    video_id: str, 
    db: Session = Depends(get_db),
    current_user: Dict = Depends(get_current_user)
):
    """
    Alias for export_video_text endpoint.
    Export video processing results to a TXT file.
    """
    return await export_video_text(video_id, db, current_user)
