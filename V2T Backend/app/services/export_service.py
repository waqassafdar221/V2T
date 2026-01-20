"""
Service for exporting video processing results to various formats
"""

import os
from datetime import datetime
from pathlib import Path
from typing import List
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak, Image
from reportlab.lib import colors
from app.core.config import settings


class ExportService:
    """Service for exporting video results to different formats."""
    
    @staticmethod
    def export_to_text(video_id: int, video_filename: str, detected_objects: List, extracted_texts: List, status: str) -> str:
        """
        Export video processing results to a text file.
        
        Args:
            video_id: ID of the video
            video_filename: Original filename
            detected_objects: List of detected objects
            extracted_texts: List of extracted texts
            status: Processing status
            
        Returns:
            Path to the generated text file
        """
        # Create exports directory
        export_dir = Path(settings.video_upload_dir).parent / "exports"
        export_dir.mkdir(exist_ok=True)
        
        # Generate filename
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        output_filename = f"video_{video_id}_results_{timestamp}.txt"
        output_path = export_dir / output_filename
        
        # Write text file
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write("=" * 80 + "\n")
            f.write("VIDEO PROCESSING RESULTS\n")
            f.write("=" * 80 + "\n\n")
            
            f.write(f"Video ID: {video_id}\n")
            f.write(f"Filename: {video_filename}\n")
            f.write(f"Status: {status}\n")
            f.write(f"Export Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
            f.write(f"\n")
            
            # Detected Objects Section
            f.write("-" * 80 + "\n")
            f.write(f"DETECTED OBJECTS ({len(detected_objects)} total)\n")
            f.write("-" * 80 + "\n\n")
            
            if detected_objects:
                for idx, obj in enumerate(detected_objects, 1):
                    f.write(f"{idx}. Object: {obj.object_class}\n")
                    f.write(f"   Confidence: {obj.confidence:.2%}\n")
                    f.write(f"   Frame: {obj.frame_number}\n")
                    f.write(f"   Bounding Box: x1={obj.bbox_x1}, y1={obj.bbox_y1}, "
                           f"x2={obj.bbox_x2}, y2={obj.bbox_y2}\n")
                    f.write(f"\n")
            else:
                f.write("No objects detected.\n\n")
            
            # Extracted Texts Section
            f.write("-" * 80 + "\n")
            f.write(f"EXTRACTED TEXT\n")
            f.write("-" * 80 + "\n\n")
            
            if extracted_texts:
                # Deduplicate text and create paragraph
                unique_texts = []
                seen_texts = set()
                
                for text in extracted_texts:
                    # Normalize text for comparison (strip whitespace, lowercase)
                    normalized = text.text_content.strip().lower()
                    if normalized and normalized not in seen_texts:
                        seen_texts.add(normalized)
                        unique_texts.append(text.text_content.strip())
                
                if unique_texts:
                    # Join all unique texts into a paragraph
                    paragraph = " ".join(unique_texts)
                    f.write(f"{paragraph}\n\n")
                    f.write(f"(Combined from {len(extracted_texts)} text entries, "
                           f"{len(unique_texts)} unique texts)\n\n")
                else:
                    f.write("No readable text extracted.\n\n")
            else:
                f.write("No text extracted.\n\n")
            
            # Summary Section
            f.write("=" * 80 + "\n")
            f.write("SUMMARY\n")
            f.write("=" * 80 + "\n\n")
            
            # Count objects by label
            object_counts = {}
            for obj in detected_objects:
                object_counts[obj.object_class] = object_counts.get(obj.object_class, 0) + 1
            
            f.write("Object Detection Summary:\n")
            for label, count in sorted(object_counts.items(), key=lambda x: x[1], reverse=True):
                f.write(f"  - {label}: {count}\n")
            
            f.write(f"\nTotal Objects: {len(detected_objects)}\n")
            f.write(f"Total Text Entries: {len(extracted_texts)}\n")
            
            f.write("\n" + "=" * 80 + "\n")
            f.write("End of Report\n")
            f.write("=" * 80 + "\n")
        
        return str(output_path)
    
    @staticmethod
    def export_to_pdf(video_id: int, video_filename: str, detected_objects: List, extracted_texts: List, status: str) -> str:
        """
        Export video processing results to a PDF file.
        
        Args:
            video_id: ID of the video
            video_filename: Original filename
            detected_objects: List of detected objects
            extracted_texts: List of extracted texts
            status: Processing status
            
        Returns:
            Path to the generated PDF file
        """
        # Create exports directory
        export_dir = Path(settings.video_upload_dir).parent / "exports"
        export_dir.mkdir(exist_ok=True)
        
        # Generate filename
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        output_filename = f"video_{video_id}_results_{timestamp}.pdf"
        output_path = export_dir / output_filename
        
        # Create PDF document
        doc = SimpleDocTemplate(str(output_path), pagesize=letter)
        story = []
        styles = getSampleStyleSheet()
        
        # Custom styles
        title_style = ParagraphStyle(
            'CustomTitle',
            parent=styles['Heading1'],
            fontSize=24,
            textColor=colors.HexColor('#1f77b4'),
            spaceAfter=30,
            alignment=1  # Center
        )
        
        heading_style = ParagraphStyle(
            'CustomHeading',
            parent=styles['Heading2'],
            fontSize=16,
            textColor=colors.HexColor('#2ca02c'),
            spaceAfter=12,
            spaceBefore=12
        )
        
        # Add logo if exists
        logo_path = Path(__file__).parent.parent.parent / "Assets" / "logo.png"
        if logo_path.exists():
            try:
                logo = Image(str(logo_path), width=2*inch, height=1*inch)
                logo.hAlign = 'CENTER'
                story.append(logo)
                story.append(Spacer(1, 0.3 * inch))
            except Exception as e:
                # If logo fails to load, continue without it
                pass
        
        # Title
        story.append(Paragraph("Video Processing Results", title_style))
        story.append(Spacer(1, 0.2 * inch))
        
        # Video Information
        video_info = [
            ["Video ID:", str(video_id)],
            ["Filename:", video_filename],
            ["Status:", status],
            ["Export Date:", datetime.now().strftime('%Y-%m-%d %H:%M:%S')]
        ]
        
        info_table = Table(video_info, colWidths=[2*inch, 4*inch])
        info_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (0, -1), colors.lightgrey),
            ('TEXTCOLOR', (0, 0), (-1, -1), colors.black),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, -1), 10),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
            ('GRID', (0, 0), (-1, -1), 1, colors.black)
        ]))
        story.append(info_table)
        story.append(Spacer(1, 0.3 * inch))
        
        # Detected Objects Section
        story.append(Paragraph(f"Detected Objects ({len(detected_objects)} total)", heading_style))
        
        if detected_objects:
            # Create table data
            obj_data = [["#", "Object", "Confidence", "Frame", "Bounding Box"]]
            for idx, obj in enumerate(detected_objects, 1):
                bbox = f"({obj.bbox_x1:.0f}, {obj.bbox_y1:.0f})<br/>to ({obj.bbox_x2:.0f}, {obj.bbox_y2:.0f})"
                obj_data.append([
                    str(idx),
                    obj.object_class,
                    f"{obj.confidence:.1%}",
                    str(obj.frame_number),
                    bbox
                ])
            
            obj_table = Table(obj_data, colWidths=[0.5*inch, 1.5*inch, 1*inch, 0.8*inch, 1.5*inch])
            obj_table.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                ('FONTSIZE', (0, 0), (-1, 0), 10),
                ('BOTTOMPADDING', (0, 0), (-1, 0), 10),
                ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
                ('GRID', (0, 0), (-1, -1), 1, colors.black),
                ('FONTSIZE', (0, 1), (-1, -1), 8),
                ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.lightgrey])
            ]))
            story.append(obj_table)
        else:
            story.append(Paragraph("No objects detected.", styles['Normal']))
        
        story.append(Spacer(1, 0.3 * inch))
        
        # Extracted Texts Section
        story.append(Paragraph(f"Extracted Text ({len(extracted_texts)} entries)", heading_style))
        
        if extracted_texts:
            # Create table data
            text_data = [["#", "Frame", "Confidence", "Extracted Text"]]
            for idx, text in enumerate(extracted_texts, 1):
                # Truncate long text for table
                display_text = text.text_content[:100] + "..." if len(text.text_content) > 100 else text.text_content
                text_data.append([
                    str(idx),
                    str(text.frame_number),
                    f"{text.confidence:.1%}",
                    display_text
                ])
            
            text_table = Table(text_data, colWidths=[0.5*inch, 0.8*inch, 1*inch, 4*inch])
            text_table.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                ('ALIGN', (0, 0), (2, -1), 'CENTER'),
                ('ALIGN', (3, 0), (3, -1), 'LEFT'),
                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                ('FONTSIZE', (0, 0), (-1, 0), 10),
                ('BOTTOMPADDING', (0, 0), (-1, 0), 10),
                ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
                ('GRID', (0, 0), (-1, -1), 1, colors.black),
                ('FONTSIZE', (0, 1), (-1, -1), 8),
                ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.lightgrey]),
                ('VALIGN', (0, 0), (-1, -1), 'MIDDLE')
            ]))
            story.append(text_table)
        else:
            story.append(Paragraph("No text extracted.", styles['Normal']))
        
        story.append(Spacer(1, 0.3 * inch))
        
        # Summary Section
        story.append(Paragraph("Summary", heading_style))
        
        # Count objects by label
        object_counts = {}
        for obj in detected_objects:
            object_counts[obj.object_class] = object_counts.get(obj.object_class, 0) + 1
        
        summary_text = "<b>Object Detection Summary:</b><br/>"
        if object_counts:
            for label, count in sorted(object_counts.items(), key=lambda x: x[1], reverse=True):
                summary_text += f"&nbsp;&nbsp;• {label}: {count}<br/>"
        else:
            summary_text += "&nbsp;&nbsp;No objects detected<br/>"
        
        summary_text += f"<br/><b>Total Objects:</b> {len(detected_objects)}<br/>"
        summary_text += f"<b>Total Text Entries:</b> {len(extracted_texts)}"
        
        story.append(Paragraph(summary_text, styles['Normal']))
        
        # Build PDF
        doc.build(story)
        
        return str(output_path)
