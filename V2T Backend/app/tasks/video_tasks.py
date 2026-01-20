import os
from sqlalchemy.orm import Session
from app.core.celery_app import celery_app
from app.services.video_processing import video_service
from app.models.video import Video, DetectedObject, ExtractedText, VideoStatus
from app.core.database import SessionLocal
from datetime import datetime
import logging

logger = logging.getLogger(__name__)


@celery_app.task(bind=True, name='process_video')
def process_video_task(self, video_id: str, video_path: str, frame_interval: int = 1):
    """
    Celery task to process video asynchronously.
    
    Args:
        video_id: Unique video identifier
        video_path: Path to the uploaded video
        frame_interval: Extract frame every N seconds
    """
    db = SessionLocal()
    
    try:
        # Update status to processing
        video = db.query(Video).filter(Video.video_id == video_id).first()
        if not video:
            logger.error(f"Video {video_id} not found in database")
            return {'status': 'failed', 'error': 'Video not found'}
        
        video.status = VideoStatus.PROCESSING
        db.commit()
        
        logger.info(f"Starting video processing for {video_id}")
        
        # Update task state
        self.update_state(state='PROCESSING', meta={'progress': 10, 'status': 'Extracting frames'})
        
        # Process video
        result = video_service.process_video_complete(
            video_path=video_path,
            video_id=video_id,
            frame_interval=frame_interval,
            confidence_threshold=0.5
        )
        
        if result['status'] == 'failed':
            video.status = VideoStatus.FAILED
            video.error_message = result.get('error', 'Unknown error')
            db.commit()
            return result
        
        # Update task state
        self.update_state(state='PROCESSING', meta={'progress': 50, 'status': 'Saving results'})
        
        # Save metadata
        metadata = result.get('metadata', {})
        video.duration = metadata.get('duration')
        video.fps = metadata.get('fps')
        
        # Save detected objects
        for obj_data in result['detected_objects']:
            detected_obj = DetectedObject(
                video_id=video_id,
                frame_number=obj_data['frame_number'],
                timestamp=obj_data['timestamp'],
                object_class=obj_data['class'],
                confidence=obj_data['confidence'],
                bbox_x1=obj_data['bbox']['x1'],
                bbox_y1=obj_data['bbox']['y1'],
                bbox_x2=obj_data['bbox']['x2'],
                bbox_y2=obj_data['bbox']['y2']
            )
            db.add(detected_obj)
        
        # Save extracted texts
        for text_data in result['extracted_texts']:
            extracted_text = ExtractedText(
                video_id=video_id,
                frame_number=text_data['frame_number'],
                timestamp=text_data['timestamp'],
                text_content=text_data['text'],
                confidence=text_data.get('confidence')
            )
            db.add(extracted_text)
        
        # Update video status
        video.status = VideoStatus.COMPLETED
        video.completed_at = datetime.utcnow()
        db.commit()
        
        logger.info(f"Video processing completed for {video_id}")
        
        return {
            'status': 'completed',
            'video_id': video_id,
            'total_frames': result['total_frames_processed'],
            'objects_detected': len(result['detected_objects']),
            'texts_extracted': len(result['extracted_texts'])
        }
        
    except Exception as e:
        logger.error(f"Error processing video {video_id}: {str(e)}")
        
        # Update video status to failed
        try:
            video = db.query(Video).filter(Video.video_id == video_id).first()
            if video:
                video.status = VideoStatus.FAILED
                video.error_message = str(e)
                db.commit()
        except:
            pass
        
        return {
            'status': 'failed',
            'error': str(e)
        }
    
    finally:
        db.close()
