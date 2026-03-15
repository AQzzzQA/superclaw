import { Spin } from 'antd'

interface LoadingOverlayProps {
  loading: boolean
  children: React.ReactNode
  tip?: string
}

const LoadingOverlay = ({ loading, children, tip = '加载中...' }: LoadingOverlayProps) => {
  return (
    <div style={{ position: 'relative', minHeight: loading ? 200 : 'auto' }}>
      {children}
      {loading && (
        <div
          style={{
            position: 'absolute',
            top: 0,
            left: 0,
            right: 0,
            bottom: 0,
            background: 'rgba(255, 255, 255, 0.8)',
            display: 'flex',
            alignItems: 'center',
            justifyContent: 'center',
            zIndex: 1000,
          }}
        >
          <Spin size="large" tip={tip} />
        </div>
      )}
    </div>
  )
}

export default LoadingOverlay
