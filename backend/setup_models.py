#!/usr/bin/env python3
"""
Setup script to download AI models for enhancement
"""
import os
import requests
from pathlib import Path

def download_file(url: str, filepath: str):
    """Download file with progress"""
    print(f"Downloading {filepath}...")
    response = requests.get(url, stream=True)
    response.raise_for_status()
    
    with open(filepath, 'wb') as f:
        for chunk in response.iter_content(chunk_size=8192):
            f.write(chunk)
    print(f"Downloaded {filepath}")

def setup_models():
    """Download required AI models"""
    models_dir = Path("models")
    models_dir.mkdir(exist_ok=True)
    
    # Real-ESRGAN model
    esrgan_path = models_dir / "RealESRGAN_x4plus.pth"
    if not esrgan_path.exists():
        print("Real-ESRGAN model not found. Please download manually from:")
        print("https://github.com/xinntao/Real-ESRGAN/releases/download/v0.1.0/RealESRGAN_x4plus.pth")
        print(f"Save to: {esrgan_path}")
    
    # GFPGAN model
    gfpgan_path = models_dir / "GFPGANv1.4.pth"
    if not gfpgan_path.exists():
        print("GFPGAN model not found. Please download manually from:")
        print("https://github.com/TencentARC/GFPGAN/releases/download/v1.3.0/GFPGANv1.4.pth")
        print(f"Save to: {gfpgan_path}")
    
    print("\nModel setup complete!")
    print("Note: Models are large files (100MB+). Download manually for better control.")

if __name__ == "__main__":
    setup_models()