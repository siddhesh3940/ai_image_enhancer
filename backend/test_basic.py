#!/usr/bin/env python3
"""Test basic functionality without AI models"""

import sys
import os
sys.path.append(os.path.dirname(__file__))

def test_imports():
    """Test if basic imports work"""
    try:
        from ai_enhancer import enhance_image, enhance_video, AI_AVAILABLE
        print(f"✓ Basic imports work. AI Available: {AI_AVAILABLE}")
        return True
    except Exception as e:
        print(f"✗ Import error: {e}")
        return False

def test_fastapi():
    """Test if FastAPI starts"""
    try:
        from main import app
        print("✓ FastAPI app created successfully")
        return True
    except Exception as e:
        print(f"✗ FastAPI error: {e}")
        return False

if __name__ == "__main__":
    print("Testing basic functionality...")
    
    success = True
    success &= test_imports()
    success &= test_fastapi()
    
    if success:
        print("\n✓ All basic tests passed! You can run the server.")
        print("Run: python run.py")
    else:
        print("\n✗ Some tests failed. Check dependencies.")
        print("Install: pip install -r requirements_basic.txt")