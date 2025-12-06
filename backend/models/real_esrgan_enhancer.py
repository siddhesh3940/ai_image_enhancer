import cv2
import torch
from basicsr.archs.rrdbnet_arch import RRDBNet
from realesrgan import RealESRGANer
import os
from pathlib import Path

class RealESRGANEnhancer:
    def __init__(self):
        self.model = None
        self.device = 'cuda' if torch.cuda.is_available() else 'cpu'
        
    def load_model(self):
        """Load Real-ESRGAN model"""
        if self.model is None:
            model = RRDBNet(num_in_ch=3, num_out_ch=3, num_feat=64, num_block=23, num_grow_ch=32, scale=4)
            
            # Download model if not exists
            model_path = 'models/RealESRGAN_x4plus.pth'
            if not os.path.exists(model_path):
                os.makedirs('models', exist_ok=True)
                # In production, download from official source
                print(f"Model not found at {model_path}. Please download RealESRGAN_x4plus.pth")
                return False
            
            self.model = RealESRGANer(
                scale=4,
                model_path=model_path,
                model=model,
                tile=0,
                tile_pad=10,
                pre_pad=0,
                half=False,
                device=self.device
            )
        return True
    
    def enhance_image(self, input_path: str, output_path: str) -> bool:
        """Enhance image using Real-ESRGAN"""
        try:
            if not self.load_model():
                return False
                
            img = cv2.imread(input_path, cv2.IMREAD_COLOR)
            if img is None:
                return False
            
            # Enhance image
            output, _ = self.model.enhance(img, outscale=4)
            
            # Save result
            cv2.imwrite(output_path, output)
            return True
            
        except Exception as e:
            print(f"Enhancement failed: {e}")
            return False