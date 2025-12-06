# AI Models

This directory contains the AI enhancement models.

## Required Models

### Real-ESRGAN (Image Upscaling)
- **File**: `RealESRGAN_x4plus.pth`
- **Size**: ~67MB
- **Download**: https://github.com/xinntao/Real-ESRGAN/releases/download/v0.1.0/RealESRGAN_x4plus.pth
- **Purpose**: 4x image upscaling with AI

### GFPGAN (Face Restoration)
- **File**: `GFPGANv1.4.pth`
- **Size**: ~348MB
- **Download**: https://github.com/TencentARC/GFPGAN/releases/download/v1.3.0/GFPGANv1.4.pth
- **Purpose**: Face enhancement and restoration

## Setup

1. Download the model files from the links above
2. Place them in this `models/` directory
3. Run `python setup_models.py` to verify

## Usage

The system will automatically:
- Try AI models first if available
- Fallback to basic enhancement if models missing
- Use GPU if available, CPU otherwise

## Performance

- **GPU**: Recommended for Real-ESRGAN (much faster)
- **CPU**: Works but slower, especially for video
- **Memory**: 4GB+ RAM recommended for large images/videos