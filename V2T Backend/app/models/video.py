from sqlalchemy import Column, Integer, String, Float, Text, DateTime, Boolean, JSON
from datetime import datetime
from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any
from enum import Enum
from app.models.user import Base


class VideoStatus(str, Enum):
    """Video processing status enumeration."""
    UPLOADED = "uploaded"
    PROCESSING = "processing"
    COMPLETED = "completed"
    FAILED = "failed"


class Video(Base):
    """Video database model."""
    __tablename__ = "videos"
    
    id = Column(Integer, primary_key=True, index=True)
    video_id = Column(String, unique=True, index=True, nullable=False)
    filename = Column(String, nullable=False)
    file_path = Column(String, nullable=False)
    file_size = Column(Integer)  # in bytes
    duration = Column(Float)  # in seconds
    fps = Column(Float)  # frames per second
    status = Column(String, default=VideoStatus.UPLOADED)
    user_id = Column(Integer, nullable=True)  # Optional: link to user
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    completed_at = Column(DateTime, nullable=True)
    error_message = Column(Text, nullable=True)


class DetectedObject(Base):
    """Detected object database model."""
    __tablename__ = "detected_objects"
    
    id = Column(Integer, primary_key=True, index=True)
    video_id = Column(String, index=True, nullable=False)
    frame_number = Column(Integer, nullable=False)
    timestamp = Column(Float)  # in seconds
    object_class = Column(String, nullable=False)
    confidence = Column(Float, nullable=False)
    bbox_x1 = Column(Float)  # Bounding box coordinates
    bbox_y1 = Column(Float)
    bbox_x2 = Column(Float)
    bbox_y2 = Column(Float)
    created_at = Column(DateTime, default=datetime.utcnow)


class ExtractedText(Base):
    """Extracted text database model."""
    __tablename__ = "extracted_texts"
    
    id = Column(Integer, primary_key=True, index=True)
    video_id = Column(String, index=True, nullable=False)
    frame_number = Column(Integer, nullable=False)
    timestamp = Column(Float)  # in seconds
    text_content = Column(Text, nullable=False)
    confidence = Column(Float, nullable=True)
    bbox_data = Column(JSON, nullable=True)  # OCR bounding box data
    created_at = Column(DateTime, default=datetime.utcnow)


# Pydantic models for API
class VideoUploadResponse(BaseModel):
    """Video upload response model."""
    video_id: str
    filename: str
    file_size: int
    status: VideoStatus
    message: str


class BoundingBox(BaseModel):
    """Bounding box model."""
    x1: float
    y1: float
    x2: float
    y2: float


class DetectedObjectResponse(BaseModel):
    """Detected object response model."""
    frame_number: int
    timestamp: float
    object_class: str
    confidence: float
    bbox: BoundingBox


class ExtractedTextResponse(BaseModel):
    """Extracted text response model."""
    frame_number: int
    timestamp: float
    text: str
    confidence: Optional[float] = None


class VideoProcessingResult(BaseModel):
    """Video processing result model."""
    video_id: str
    filename: str
    status: VideoStatus
    duration: Optional[float] = None
    fps: Optional[float] = None
    total_frames: int
    detected_objects: List[DetectedObjectResponse]
    extracted_texts: List[ExtractedTextResponse]
    error_message: Optional[str] = None
    created_at: datetime
    completed_at: Optional[datetime] = None


class VideoStatusResponse(BaseModel):
    """Video status response model."""
    video_id: str
    status: VideoStatus
    progress: Optional[float] = None  # 0-100
    message: str
    error_message: Optional[str] = None
