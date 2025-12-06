interface MediaPreviewProps {
  file: File | null
  title: string
  enhancedUrl?: string
}

export default function MediaPreview({ file, title, enhancedUrl }: MediaPreviewProps) {
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
      {isVideo ? (
        <video 
          className="preview-media" 
          controls 
          src={mediaUrl}
        />
      ) : (
        <img 
          className="preview-media" 
          src={mediaUrl} 
          alt={title}
        />
      )}
    </div>
  )
}