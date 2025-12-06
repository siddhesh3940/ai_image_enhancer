'use client'

import { useState } from 'react'
import FileUpload from './components/FileUpload'
import MediaPreview from './components/MediaPreview'
import ProgressBar from './components/ProgressBar'

export default function Home() {
  const [selectedFile, setSelectedFile] = useState<File | null>(null)
  const [enhancedUrl, setEnhancedUrl] = useState<string>('')
  const [progress, setProgress] = useState(0)
  const [status, setStatus] = useState('Ready to enhance')
  const [isProcessing, setIsProcessing] = useState(false)

  const handleFileSelect = (file: File) => {
    setSelectedFile(file)
    setEnhancedUrl('')
    setProgress(0)
    setStatus('File selected - Ready to enhance')
  }

  const enhanceWithBackend = async () => {
    if (!selectedFile) return
    
    setIsProcessing(true)
    setStatus('Uploading file...')
    setProgress(0)

    try {
      // Upload file
      const formData = new FormData()
      formData.append('file', selectedFile)
      
      const uploadResponse = await fetch('http://localhost:8000/upload', {
        method: 'POST',
        body: formData
      })
      
      if (!uploadResponse.ok) throw new Error('Upload failed')
      const { file_id } = await uploadResponse.json()
      
      // Start enhancement
      await fetch(`http://localhost:8000/enhance/${file_id}`, {
        method: 'POST'
      })
      
      // Poll for progress
      const pollProgress = async () => {
        const statusResponse = await fetch(`http://localhost:8000/status/${file_id}`)
        const statusData = await statusResponse.json()
        
        setProgress(statusData.progress)
        setStatus(statusData.status)
        
        if (statusData.progress < 100) {
          setTimeout(pollProgress, 1000)
        } else {
          // Download enhanced file
          setEnhancedUrl(`http://localhost:8000/download/${file_id}`)
          setIsProcessing(false)
        }
      }
      
      pollProgress()
      
    } catch (error) {
      setStatus('Enhancement failed')
      setIsProcessing(false)
      console.error('Enhancement error:', error)
    }
  }

  const handleEnhance = () => {
    if (selectedFile) {
      enhanceWithBackend()
    }
  }

  return (
    <div className="container">
      <div className="header">
        <h1>AI Video Enhancer</h1>
        <p>Upload your images or videos to enhance them with AI</p>
      </div>

      <FileUpload 
        onFileSelect={handleFileSelect}
        acceptedTypes="image/*,video/*"
      />

      {selectedFile && (
        <>
          <div className="preview-section">
            <MediaPreview 
              file={selectedFile} 
              title="Original"
            />
            <MediaPreview 
              file={null}
              title="Enhanced"
              enhancedUrl={enhancedUrl}
            />
          </div>

          {isProcessing && (
            <ProgressBar 
              progress={progress}
              status={status}
              isProcessing={isProcessing}
            />
          )}

          <button 
            className="enhance-btn"
            onClick={handleEnhance}
            disabled={isProcessing}
          >
            {isProcessing ? 'Enhancing...' : 'Enhance with AI'}
          </button>
        </>
      )}
    </div>
  )
}