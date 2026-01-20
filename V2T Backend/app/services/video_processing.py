import os
import cv2
import uuid
import ffmpeg
import pytesseract
import numpy as np
from pathlib import Path
from typing import List, Tuple, Dict, Optional
from datetime import datetime
from ultralytics import YOLO
from PIL import Image
from app.core.config import settings
import logging

logger = logging.getLogger(__name__)


class VideoProcessingService:
    """Service for processing videos: frame extraction, object detection, and OCR."""
    
    def __init__(self):
        self.yolo_model = None
        self._load_yolo_model()
    
    def _load_yolo_model(self):
        """Load YOLO model for object detection."""
        try:
            # Load YOLOv8 pretrained model
            self.yolo_model = YOLO('yolov8n.pt')  # Using nano model for speed
            logger.info("YOLO model loaded successfully")
        except Exception as e:
            logger.error(f"Failed to load YOLO model: {str(e)}")
            self.yolo_model = None
    
    @staticmethod
    def generate_video_id() -> str:
        """Generate unique video ID."""
        return str(uuid.uuid4())
    
    @staticmethod
    def get_video_metadata(video_path: str) -> Dict:
        """Extract video metadata using ffmpeg."""
        try:
            probe = ffmpeg.probe(video_path)
            video_info = next(s for s in probe['streams'] if s['codec_type'] == 'video')
            
            duration = float(probe['format']['duration'])
            fps = eval(video_info['r_frame_rate'])  # Convert fraction to float
            width = int(video_info['width'])
            height = int(video_info['height'])
            
            return {
                'duration': duration,
                'fps': fps,
                'width': width,
                'height': height,
                'total_frames': int(duration * fps)
            }
        except Exception as e:
            logger.error(f"Failed to extract video metadata: {str(e)}")
            return {}
    
    def extract_frames(
        self, 
        video_path: str, 
        output_dir: str, 
        interval: int = 1
    ) -> List[Tuple[int, str, float]]:
        """
        Extract frames from video at specified interval.
        
        Args:
            video_path: Path to the video file
            output_dir: Directory to save extracted frames
            interval: Extract frame every N seconds
            
        Returns:
            List of tuples (frame_number, frame_path, timestamp)
        """
        try:
            Path(output_dir).mkdir(parents=True, exist_ok=True)
            
            cap = cv2.VideoCapture(video_path)
            fps = cap.get(cv2.CAP_PROP_FPS)
            frame_interval = int(fps * interval)
            
            frames_data = []
            frame_count = 0
            saved_count = 0
            
            while True:
                ret, frame = cap.read()
                if not ret:
                    break
                
                if frame_count % frame_interval == 0:
                    timestamp = frame_count / fps
                    frame_filename = f"frame_{saved_count:06d}.jpg"
                    frame_path = os.path.join(output_dir, frame_filename)
                    
                    cv2.imwrite(frame_path, frame)
                    frames_data.append((saved_count, frame_path, timestamp))
                    saved_count += 1
                
                frame_count += 1
            
            cap.release()
            logger.info(f"Extracted {saved_count} frames from video")
            return frames_data
            
        except Exception as e:
            logger.error(f"Frame extraction failed: {str(e)}")
            return []
    
    def detect_objects(
        self, 
        frame_path: str, 
        confidence_threshold: float = 0.5
    ) -> List[Dict]:
        """
        Detect objects in a frame using YOLO.
        
        Args:
            frame_path: Path to the frame image
            confidence_threshold: Minimum confidence for detections
            
        Returns:
            List of detected objects with bounding boxes and labels
        """
        if self.yolo_model is None:
            logger.warning("YOLO model not loaded")
            return []
        
        try:
            # Run inference
            results = self.yolo_model(frame_path, conf=confidence_threshold)
            
            detected_objects = []
            for result in results:
                boxes = result.boxes
                for box in boxes:
                    # Get bounding box coordinates
                    x1, y1, x2, y2 = box.xyxy[0].tolist()
                    
                    # Get class and confidence
                    cls = int(box.cls[0])
                    conf = float(box.conf[0])
                    class_name = result.names[cls]
                    
                    detected_objects.append({
                        'class': class_name,
                        'confidence': conf,
                        'bbox': {
                            'x1': x1,
                            'y1': y1,
                            'x2': x2,
                            'y2': y2
                        }
                    })
            
            logger.info(f"Detected {len(detected_objects)} objects in frame")
            return detected_objects
            
        except Exception as e:
            logger.error(f"Object detection failed: {str(e)}")
            return []
    
    def extract_text_ocr(
        self, 
        frame_path: str,
        language: str = 'eng'
    ) -> Dict:
        """
        Extract text from frame using Tesseract OCR.
        
        Args:
            frame_path: Path to the frame image
            language: OCR language (default: English)
            
        Returns:
            Dictionary with extracted text and confidence
        """
        try:
            # Read image
            image = Image.open(frame_path)
            
            # Perform OCR with detailed data
            ocr_data = pytesseract.image_to_data(
                image, 
                lang=language, 
                output_type=pytesseract.Output.DICT
            )
            
            # Extract text with confidence
            texts = []
            confidences = []
            bboxes = []
            
            n_boxes = len(ocr_data['text'])
            for i in range(n_boxes):
                text = ocr_data['text'][i].strip()
                conf = int(ocr_data['conf'][i])
                
                if text and conf > 0:  # Only keep valid text with confidence
                    texts.append(text)
                    confidences.append(conf)
                    bboxes.append({
                        'x': ocr_data['left'][i],
                        'y': ocr_data['top'][i],
                        'width': ocr_data['width'][i],
                        'height': ocr_data['height'][i]
                    })
            
            combined_text = ' '.join(texts)
            avg_confidence = sum(confidences) / len(confidences) if confidences else 0
            
            result = {
                'text': combined_text,
                'confidence': avg_confidence,
                'word_count': len(texts),
                'bboxes': bboxes
            }
            
            if combined_text:
                logger.info(f"Extracted {len(texts)} words from frame")
            
            return result
            
        except Exception as e:
            logger.error(f"OCR extraction failed: {str(e)}")
            return {
                'text': '',
                'confidence': 0,
                'word_count': 0,
                'bboxes': []
            }
    
    def process_video_complete(
        self,
        video_path: str,
        video_id: str,
        frame_interval: int = 1,
        confidence_threshold: float = 0.5
    ) -> Dict:
        """
        Complete video processing pipeline.
        
        Args:
            video_path: Path to video file
            video_id: Unique video identifier
            frame_interval: Extract frame every N seconds
            confidence_threshold: YOLO confidence threshold
            
        Returns:
            Dictionary with all processing results
        """
        try:
            # Create output directory for frames
            frames_dir = os.path.join(settings.video_frames_dir, video_id)
            Path(frames_dir).mkdir(parents=True, exist_ok=True)
            
            # Get video metadata
            metadata = self.get_video_metadata(video_path)
            
            # Extract frames
            frames = self.extract_frames(video_path, frames_dir, frame_interval)
            
            # Process each frame
            all_detections = []
            all_texts = []
            
            for frame_num, frame_path, timestamp in frames:
                # Object detection
                objects = self.detect_objects(frame_path, confidence_threshold)
                for obj in objects:
                    obj['frame_number'] = frame_num
                    obj['timestamp'] = timestamp
                    all_detections.append(obj)
                
                # OCR text extraction
                ocr_result = self.extract_text_ocr(frame_path)
                if ocr_result['text']:
                    all_texts.append({
                        'frame_number': frame_num,
                        'timestamp': timestamp,
                        'text': ocr_result['text'],
                        'confidence': ocr_result['confidence'],
                        'word_count': ocr_result['word_count']
                    })
            
            return {
                'status': 'completed',
                'metadata': metadata,
                'total_frames_processed': len(frames),
                'detected_objects': all_detections,
                'extracted_texts': all_texts,
                'error': None
            }
            
        except Exception as e:
            logger.error(f"Video processing failed: {str(e)}")
            return {
                'status': 'failed',
                'error': str(e),
                'detected_objects': [],
                'extracted_texts': []
            }
    
    @staticmethod
    def cleanup_frames(video_id: str):
        """Clean up extracted frames for a video."""
        try:
            frames_dir = os.path.join(settings.video_frames_dir, video_id)
            if os.path.exists(frames_dir):
                import shutil
                shutil.rmtree(frames_dir)
                logger.info(f"Cleaned up frames for video {video_id}")
        except Exception as e:
            logger.error(f"Failed to cleanup frames: {str(e)}")


# Singleton instance
video_service = VideoProcessingService()
