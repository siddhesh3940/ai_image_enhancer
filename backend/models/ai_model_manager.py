from .real_esrgan_enhancer import RealESRGANEnhancer
from .gfpgan_enhancer import GFPGANEnhancer
from .video_enhancer import VideoEnhancer
import os
from pathlib import Path

class AIModelManager:
    def __init__(self):
        self.esrgan = RealESRGANEnhancer()
        self.gfpgan = GFPGANEnhancer()
        self.video_enhancer = VideoEnhancer()
        
    def enhance_image(self, input_path: str, output_path: str, enhancement_type: str = "upscale") -> bool:
        """Enhance image based on type"""
        try:
            if enhancement_type == "face":
                return self.gfpgan.enhance_face(input_path, output_path)
            else:  # default to upscaling
                return self.esrgan.enhance_image(input_path, output_path)
        except Exception as e:
            print(f"Image enhancement failed: {e}")
            return False
    
    def enhance_video(self, input_path: str, output_path: str, use_ai: bool = True, progress_callback=None) -> bool:
        """Enhance video with optional AI processing"""
        try:
            if use_ai:
                return self.video_enhancer.enhance_video(input_path, output_path, progress_callback)
            else:
                return self.video_enhancer.enhance_video_basic(input_path, output_path, progress_callback)
        except Exception as e:
            print(f"Video enhancement failed: {e}")
            return False
    
    def get_available_models(self) -> dict:
        """Check which models are available"""
        models = {
            "real_esrgan": os.path.exists("models/RealESRGAN_x4plus.pth"),
            "gfpgan": os.path.exists("models/GFPGANv1.4.pth")
        }
        return models