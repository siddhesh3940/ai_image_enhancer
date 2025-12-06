'use client'

import { useState, useRef } from 'react'

interface FileUploadProps {
  onFileSelect: (file: File) => void
  acceptedTypes: string
}

export default function FileUpload({ onFileSelect, acceptedTypes }: FileUploadProps) {
  const [isDragOver, setIsDragOver] = useState(false)
  const fileInputRef = useRef<HTMLInputElement>(null)

  const handleDragOver = (e: React.DragEvent) => {
    e.preventDefault()
    setIsDragOver(true)
  }

  const handleDragLeave = (e: React.DragEvent) => {
    e.preventDefault()
    setIsDragOver(false)
  }

  const handleDrop = (e: React.DragEvent) => {
    e.preventDefault()
    setIsDragOver(false)
    
    const files = e.dataTransfer.files
    if (files.length > 0) {
      onFileSelect(files[0])
    }
  }

  const handleFileSelect = (e: React.ChangeEvent<HTMLInputElement>) => {
    const files = e.target.files
    if (files && files.length > 0) {
      onFileSelect(files[0])
    }
  }

  const handleClick = () => {
    fileInputRef.current?.click()
  }

  return (
    <div
      className={`upload-area ${isDragOver ? 'drag-over' : ''}`}
      onDragOver={handleDragOver}
      onDragLeave={handleDragLeave}
      onDrop={handleDrop}
      onClick={handleClick}
    >
      <div className="upload-icon">📁</div>
      <div className="upload-text">
        Drag & drop your image or video here
      </div>
      <button className="browse-btn" type="button">
        Browse Files
      </button>
      <input
        ref={fileInputRef}
        type="file"
        className="file-input"
        accept={acceptedTypes}
        onChange={handleFileSelect}
      />
    </div>
  )
}