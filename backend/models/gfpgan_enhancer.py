import cv2
import torch
from gfpgan import GFPGANer
import os

class GFPGANEnhancer:
    def __init__(self):
        self.model = None
        self.device = 'cuda' if torch.cuda.is_available() else 'cpu'
        
    def load_model(self):
        """Load GFPGAN model for face restoration"""
        if self.model is None:
            model_path = 'models/GFPGANv1.4.pth'
            if not os.path.exists(model_path):
                os.makedirs('models', exist_ok=True)
                print(f"Model not found at {model_path}. Please download GFPGANv1.4.pth")
                return False
            
            self.model = GFPGANer(
                model_path=model_path,
                upscale=2,
                arch='clean',
                channel_multiplier=2,
                bg_upsampler=None,
                device=self.device
            )
        return True
    
    def enhance_face(self, input_path: str, output_path: str) -> bool:
        """Enhance faces in image using GFPGAN"""
        try:
            if not self.load_model():
                return False
                
            img = cv2.imread(input_path, cv2.IMREAD_COLOR)
            if img is None:
                return False
            
            # Enhance faces
            _, _, output = self.model.enhance(img, has_aligned=False, only_center_face=False, paste_back=True)
            
            # Save result
            cv2.imwrite(output_path, output)
            return True
            
        except Exception as e:
            print(f"Face enhancement failed: {e}")
            return False