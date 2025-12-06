interface ProgressBarProps {
  progress: number
  status: string
  isProcessing: boolean
}

export default function ProgressBar({ progress, status, isProcessing }: ProgressBarProps) {
  return (
    <div className="progress-section">
      <div className="status-text">{status}</div>
      <div className="progress-bar">
        <div 
          className="progress-fill" 
          style={{ width: `${progress}%` }}
        />
      </div>
      <div style={{ textAlign: 'center', fontSize: '0.9rem', color: '#6b7280' }}>
        {progress}% Complete
      </div>
    </div>
  )
}