from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware
import os
import uuid
import asyncio
from pathlib import Path
from ai_enhancer import enhance_image, enhance_video

app = FastAPI(title="AI Video Enhancer API")

# CORS for frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Storage directories
UPLOAD_DIR = Path("uploads")
OUTPUT_DIR = Path("outputs")
UPLOAD_DIR.mkdir(exist_ok=True)
OUTPUT_DIR.mkdir(exist_ok=True)

# Store processing status
processing_status = {}

@app.post("/upload")
async def upload_file(file: UploadFile = File(...)):
    if not file.content_type.startswith(('image/', 'video/')):
        raise HTTPException(400, "Only images and videos allowed")
    
    file_id = str(uuid.uuid4())
    file_ext = Path(file.filename).suffix
    file_path = UPLOAD_DIR / f"{file_id}{file_ext}"
    
    with open(file_path, "wb") as f:
        content = await file.read()
        f.write(content)
    
    return {"file_id": file_id, "filename": file.filename}

@app.post("/enhance/{file_id}")
async def enhance_file(file_id: str):
    # Find uploaded file
    upload_files = list(UPLOAD_DIR.glob(f"{file_id}.*"))
    if not upload_files:
        raise HTTPException(404, "File not found")
    
    input_path = upload_files[0]
    output_path = OUTPUT_DIR / f"enhanced_{input_path.name}"
    
    # Initialize processing status
    processing_status[file_id] = {"progress": 0, "status": "Starting enhancement..."}
    
    # Start enhancement in background
    asyncio.create_task(process_enhancement(file_id, input_path, output_path))
    
    return {"message": "Enhancement started", "file_id": file_id}

async def process_enhancement(file_id: str, input_path: Path, output_path: Path):
    try:
        processing_status[file_id] = {"progress": 10, "status": "Analyzing media..."}
        await asyncio.sleep(0.5)
        
        processing_status[file_id] = {"progress": 20, "status": "Loading AI models..."}
        await asyncio.sleep(0.5)
        
        def update_progress(progress):
            # Map video frame progress to overall progress (20-90%)
            overall_progress = 20 + int(progress * 0.7)
            processing_status[file_id] = {"progress": overall_progress, "status": "Applying AI enhancement..."}
        
        # Determine file type and enhance
        success = False
        if input_path.suffix.lower() in ['.jpg', '.jpeg', '.png', '.gif', '.webp']:
            success = enhance_image(str(input_path), str(output_path))
        else:
            success = enhance_video(str(input_path), str(output_path), update_progress)
        
        if success:
            processing_status[file_id] = {"progress": 100, "status": "Enhancement complete!"}
        else:
            processing_status[file_id] = {"progress": 0, "status": "Enhancement failed"}
        
    except Exception as e:
        processing_status[file_id] = {"progress": 0, "status": f"Error: {str(e)}"}

@app.get("/status/{file_id}")
async def get_status(file_id: str):
    if file_id not in processing_status:
        raise HTTPException(404, "Processing not found")
    return processing_status[file_id]

@app.get("/download/{file_id}")
async def download_file(file_id: str):
    # Find enhanced file
    output_files = list(OUTPUT_DIR.glob(f"enhanced_{file_id}.*"))
    if not output_files:
        raise HTTPException(404, "Enhanced file not found")
    
    file_path = output_files[0]
    return FileResponse(
        path=file_path,
        filename=f"enhanced_{file_path.name}",
        media_type='application/octet-stream'
    )

@app.get("/models/status")
async def get_models_status():
    """Check which AI models are available"""
    try:
        from ai_enhancer import ai_models, AI_AVAILABLE
        if AI_AVAILABLE and ai_models:
            return ai_models.get_available_models()
        else:
            return {"real_esrgan": False, "gfpgan": False, "status": "AI models not loaded"}
    except Exception as e:
        return {"real_esrgan": False, "gfpgan": False, "error": str(e)}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)