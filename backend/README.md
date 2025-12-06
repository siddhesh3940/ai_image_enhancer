# AI Video Enhancer Backend

FastAPI backend for AI-powered image and video enhancement.

## Setup

### Basic Setup (Works without AI models)
```bash
cd backend
pip install -r requirements_basic.txt
python test_basic.py  # Test if everything works
python run.py
```

### Full AI Setup (Optional)
```bash
# After basic setup
pip install -r requirements_ai.txt
python setup_models.py  # Download model instructions
```

Server runs on http://localhost:8000

## API Endpoints

- `POST /upload` - Upload image/video file
- `POST /enhance/{file_id}` - Start enhancement process
- `GET /status/{file_id}` - Check enhancement progress
- `GET /download/{file_id}` - Download enhanced file

## Enhancement Features

- **Images**: Sharpness, contrast, color enhancement
- **Videos**: Brightness, contrast, sharpening filters

## Integration

- **Basic Mode**: Works immediately with PIL/OpenCV enhancement
- **AI Mode**: Download models and install AI requirements for advanced enhancement
- **Graceful Fallback**: Automatically uses basic enhancement if AI models fail