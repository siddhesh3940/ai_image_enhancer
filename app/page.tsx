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
    setIsProcessing(false)
  }

  const enhanceWithBackend = async () => {
    if (!selectedFile) return
    
    console.log('Starting enhancement process...')
    // Clear previous enhanced image
    setEnhancedUrl('')
    setIsProcessing(true)
    setStatus('Uploading file...')
    setProgress(0)

    try {
      // Upload file
      const formData = new FormData()
      formData.append('file', selectedFile)
      
      console.log('Uploading file...')
      const uploadResponse = await fetch('/api/upload', {
        method: 'POST',
        body: formData
      })
      
      if (!uploadResponse.ok) throw new Error('Upload failed')
      const { file_id } = await uploadResponse.json()
      console.log('File uploaded, ID:', file_id)
      
      // Start enhancement
      console.log('Starting enhancement...')
      const enhanceResponse = await fetch(`/api/enhance/${file_id}`, {
        method: 'POST'
      })
      console.log('Enhancement started:', enhanceResponse.ok)
      
      // Wait for enhancement to actually start processing
      await new Promise(resolve => setTimeout(resolve, 1000))
      
      // Poll for progress
      let pollCount = 0
      const maxPolls = 60 // Max 60 seconds
      
      const pollProgress = async () => {
        try {
          pollCount++
          console.log(`Polling attempt ${pollCount}/${maxPolls}`)
          
          if (pollCount > maxPolls) {
            console.log('Timeout reached')
            setStatus('Enhancement timeout')
            setIsProcessing(false)
            return
          }

          const statusResponse = await fetch(`/api/status/${file_id}`)
          if (!statusResponse.ok) {
            throw new Error('Status check failed')
          }
          
          const statusData = await statusResponse.json()
          console.log('Status data:', statusData)
          
          setProgress(statusData.progress)
          setStatus(statusData.status)
          
          if (statusData.progress >= 100) {
            // Download enhanced file with cache-busting timestamp
            const enhancedImageUrl = `/api/download/${file_id}?t=${Date.now()}`
            console.log('Enhancement complete! Setting URL:', enhancedImageUrl)
            setEnhancedUrl(enhancedImageUrl)
            setIsProcessing(false)
          } else if (statusData.progress === 0 && statusData.status.includes('failed')) {
            console.log('Enhancement failed')
            setIsProcessing(false)
          } else {
            console.log('Continuing to poll...')
            setTimeout(pollProgress, 1000)
          }
        } catch (error) {
          console.error('Polling error:', error)
          setStatus('Status check failed')
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

  const handleReset = () => {
    setSelectedFile(null)
    setEnhancedUrl('')
    setProgress(0)
    setStatus('Ready to enhance')
    setIsProcessing(false)
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

          <div style={{ display: 'flex', gap: '10px', justifyContent: 'center' }}>
            <button 
              className="enhance-btn"
              onClick={handleEnhance}
              disabled={isProcessing}
            >
              {isProcessing ? 'Enhancing...' : 'Enhance with AI'}
            </button>
            
            {(enhancedUrl || !isProcessing) && (
              <button 
                className="enhance-btn"
                onClick={handleReset}
                style={{ backgroundColor: '#6b7280' }}
              >
                Start Fresh
              </button>
            )}
          </div>
        </>
      )}
    </div>
  )
}