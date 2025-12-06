'use client'

import { useState } from 'react'

interface MediaPreviewProps {
  file: File | null
  title: string
  enhancedUrl?: string
}

export default function MediaPreview({ file, title, enhancedUrl }: MediaPreviewProps) {
  const [imageError, setImageError] = useState(false)

  if (!file && !enhancedUrl) {
    return (
      <div className="preview-card">
        <h3>{title}</h3>
        <div className="preview-media" style={{ 
          display: 'flex', 
          alignItems: 'center', 
          justifyContent: 'center',
          minHeight: '200px',
          color: '#9ca3af'
        }}>
          No media selected
        </div>
      </div>
    )
  }

  const isVideo = file?.type.startsWith('video/') || enhancedUrl?.includes('.mp4')
  const mediaUrl = enhancedUrl || (file ? URL.createObjectURL(file) : '')

  return (
    <div className="preview-card">
      <h3>{title}</h3>
      {imageError && enhancedUrl ? (
        <div className="preview-media" style={{ 
          display: 'flex', 
          alignItems: 'center', 
          justifyContent: 'center',
          minHeight: '200px',
          color: '#ef4444'
        }}>
          Failed to load enhanced media
        </div>
      ) : isVideo ? (
        <video 
          className="preview-media" 
          controls 
          src={mediaUrl}
          onError={() => setImageError(true)}
        />
      ) : (
        <img 
          className="preview-media" 
          src={mediaUrl} 
          alt={title}
          onError={() => setImageError(true)}
          onLoad={() => console.log('Image loaded:', mediaUrl)}
        />
      )}
    </div>
  )
}