import cv2
import numpy as np
import os
from pathlib import Path

class VideoEnhancer:
    def __init__(self):
        self.image_enhancer = None
        
    def _get_image_enhancer(self):
        if self.image_enhancer is None:
            try:
                from .real_esrgan_enhancer import RealESRGANEnhancer
                self.image_enhancer = RealESRGANEnhancer()
            except:
                self.image_enhancer = False
        return self.image_enhancer
        
    def enhance_video(self, input_path: str, output_path: str, progress_callback=None) -> bool:
        """Enhance video by processing frames with Real-ESRGAN"""
        try:
            cap = cv2.VideoCapture(input_path)
            if not cap.isOpened():
                return False
            
            # Get video properties
            fps = int(cap.get(cv2.CAP_PROP_FPS))
            total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
            width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
            height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
            
            # Enhanced dimensions (4x upscale)
            new_width = width * 4
            new_height = height * 4
            
            # Setup video writer
            fourcc = cv2.VideoWriter_fourcc(*'mp4v')
            out = cv2.VideoWriter(output_path, fourcc, fps, (new_width, new_height))
            
            # Load enhancement model
            enhancer = self._get_image_enhancer()
            if not enhancer or not enhancer.load_model():
                return False
            
            frame_count = 0
            while True:
                ret, frame = cap.read()
                if not ret:
                    break
                
                # Enhance frame using Real-ESRGAN
                enhanced_frame, _ = enhancer.model.enhance(frame, outscale=4)
                out.write(enhanced_frame)
                
                frame_count += 1
                if progress_callback and total_frames > 0:
                    progress = int((frame_count / total_frames) * 100)
                    progress_callback(progress)
            
            cap.release()
            out.release()
            return True
            
        except Exception as e:
            print(f"Video enhancement failed: {e}")
            return False
    
    def enhance_video_basic(self, input_path: str, output_path: str, progress_callback=None) -> bool:
        """Basic video enhancement without AI upscaling (faster)"""
        try:
            cap = cv2.VideoCapture(input_path)
            if not cap.isOpened():
                return False
            
            fps = int(cap.get(cv2.CAP_PROP_FPS))
            width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
            height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
            total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
            
            fourcc = cv2.VideoWriter_fourcc(*'mp4v')
            out = cv2.VideoWriter(output_path, fourcc, fps, (width, height))
            
            frame_count = 0
            while True:
                ret, frame = cap.read()
                if not ret:
                    break
                
                # Apply basic enhancements
                enhanced = cv2.convertScaleAbs(frame, alpha=1.2, beta=15)
                
                # Sharpening kernel
                kernel = np.array([[-1,-1,-1], [-1,9,-1], [-1,-1,-1]])
                enhanced = cv2.filter2D(enhanced, -1, kernel)
                
                out.write(enhanced)
                
                frame_count += 1
                if progress_callback and total_frames > 0:
                    progress = int((frame_count / total_frames) * 100)
                    progress_callback(progress)
            
            cap.release()
            out.release()
            return True
            
        except Exception as e:
            print(f"Basic video enhancement failed: {e}")
            return False