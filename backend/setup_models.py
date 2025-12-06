#!/usr/bin/env python3
"""
Setup script to download AI models for enhancement
"""
import os
import requests
from pathlib import Path
from tqdm import tqdm

def download_file(url: str, filepath: str):
    """Download file with progress bar"""
    print(f"\nDownloading {filepath}...")
    response = requests.get(url, stream=True)
    response.raise_for_status()
    
    total_size = int(response.headers.get('content-length', 0))
    
    with open(filepath, 'wb') as f, tqdm(
        total=total_size,
        unit='B',
        unit_scale=True,
        unit_divisor=1024,
    ) as pbar:
        for chunk in response.iter_content(chunk_size=8192):
            f.write(chunk)
            pbar.update(len(chunk))
    
    print(f"✓ Downloaded {filepath}")

def setup_models():
    """Download required AI models"""
    models_dir = Path("models")
    models_dir.mkdir(exist_ok=True)
    
    print("=" * 60)
    print("AI Model Setup for Image Enhancer")
    print("=" * 60)
    
    # Real-ESRGAN model
    esrgan_path = models_dir / "RealESRGAN_x4plus.pth"
    if not esrgan_path.exists():
        try:
            url = "https://github.com/xinntao/Real-ESRGAN/releases/download/v0.1.0/RealESRGAN_x4plus.pth"
            download_file(url, str(esrgan_path))
        except Exception as e:
            print(f"✗ Failed to download Real-ESRGAN: {e}")
            print(f"  Please download manually from: {url}")
            print(f"  Save to: {esrgan_path}")
    else:
        print(f"✓ Real-ESRGAN model already exists")
    
    # GFPGAN model
    gfpgan_path = models_dir / "GFPGANv1.4.pth"
    if not gfpgan_path.exists():
        try:
            url = "https://github.com/TencentARC/GFPGAN/releases/download/v1.3.0/GFPGANv1.4.pth"
            download_file(url, str(gfpgan_path))
        except Exception as e:
            print(f"✗ Failed to download GFPGAN: {e}")
            print(f"  Please download manually from: {url}")
            print(f"  Save to: {gfpgan_path}")
    else:
        print(f"✓ GFPGAN model already exists")
    
    print("\n" + "=" * 60)
    print("Model setup complete!")
    print("=" * 60)

if __name__ == "__main__":
    setup_models()