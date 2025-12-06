# AI Image & Video Enhancer

A full-stack application for AI-powered image and video enhancement using Real-ESRGAN and GFPGAN models.

## Screenshots

### Upload Interface
![Upload Interface](screenshots/Screenshot%202025-12-06%20144009.png)

### Processing
![Processing](screenshots/Screenshot%202025-12-06%20144241.png)

### Results
![Results](screenshots/Screenshot%202025-12-06%20154740.png)

### Enhanced Output
![Enhanced Output](screenshots/Screenshot%202025-12-06%20163254.png)

## Features

- **File Upload**: Drag & drop or browse to select images/videos
- **AI Enhancement**: Real-ESRGAN for upscaling, GFPGAN for face restoration
- **Preview**: Side-by-side comparison of original and enhanced media
- **Progress Tracking**: Real-time progress bar during enhancement
- **Responsive Design**: Clean UI that works on desktop and mobile
- **Start Fresh**: Reset button to begin new enhancement

## Quick Start

### Backend Setup

```bash
cd backend
python -m venv .venv
.venv\Scripts\activate  # Windows
pip install -r requirements_basic.txt
pip install torch torchvision
pip install basicsr facexlib gfpgan realesrgan
python setup_models.py  # Download AI models
python main.py
```

### Frontend Setup

```bash
npm install
npm run dev
```

Open [http://localhost:3001](http://localhost:3001) in your browser.

## Tech Stack

### Frontend
- Next.js 14
- React 18
- TypeScript

### Backend
- FastAPI
- PyTorch
- Real-ESRGAN (4x upscaling)
- GFPGAN (face restoration)
- OpenCV

## File Structure

```
app/
├── api/                 # Next.js API routes
│   ├── upload/
│   ├── enhance/
│   ├── status/
│   └── download/
├── components/
│   ├── FileUpload.tsx   # Drag & drop file upload
│   ├── MediaPreview.tsx # Image/video preview
│   └── ProgressBar.tsx  # Enhancement progress
└── page.tsx             # Main page

backend/
├── models/              # AI model implementations
├── uploads/             # Uploaded files
├── outputs/             # Enhanced files
├── main.py              # FastAPI server
└── ai_enhancer.py       # Enhancement logic
```

## Supported Formats

- **Images**: JPG, PNG, GIF, WebP
- **Videos**: MP4, WebM, MOV

## How It Works

1. Upload an image or video through the web interface
2. Backend processes the file using AI models:
   - Real-ESRGAN for 4x upscaling
   - GFPGAN for face restoration (optional)
3. Real-time progress updates via polling
4. Download or view enhanced result
5. Use "Start Fresh" to enhance another file

## License

MIT