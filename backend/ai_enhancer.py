from PIL import Image, ImageEnhance, ImageFilter
import cv2
import numpy as np

# Try to import AI models, fallback if not available
try:
    from models import AIModelManager
    ai_models = AIModelManager()
    AI_AVAILABLE = True
except Exception as e:
    print(f"AI models not available: {e}")
    ai_models = None
    AI_AVAILABLE = False

def enhance_image(input_path: str, output_path: str, enhancement_type: str = "upscale"):
    """Enhance image using AI models or fallback to basic enhancement"""
    # Try AI enhancement first
    if AI_AVAILABLE and ai_models and ai_models.enhance_image(input_path, output_path, enhancement_type):
        return True
    
    # Fallback to basic enhancement
    try:
        with Image.open(input_path) as img:
            if img.mode != 'RGB':
                img = img.convert('RGB')
            
            enhancer = ImageEnhance.Sharpness(img)
            img = enhancer.enhance(1.2)
            
            enhancer = ImageEnhance.Contrast(img)
            img = enhancer.enhance(1.1)
            
            enhancer = ImageEnhance.Color(img)
            img = enhancer.enhance(1.05)
            
            img = img.filter(ImageFilter.UnsharpMask(radius=1, percent=150, threshold=3))
            img.save(output_path, quality=95)
            return True
    except Exception as e:
        print(f"Basic image enhancement failed: {e}")
        return False

def enhance_video(input_path: str, output_path: str, progress_callback=None):
    """Enhance video using AI models or fallback to basic enhancement"""
    # Try AI enhancement first (set use_ai=False for faster processing)
    if AI_AVAILABLE and ai_models and ai_models.enhance_video(input_path, output_path, use_ai=False, progress_callback=progress_callback):
        return True
    
    # Fallback to basic enhancement
    try:
        cap = cv2.VideoCapture(input_path)
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
            
            enhanced = cv2.convertScaleAbs(frame, alpha=1.1, beta=10)
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