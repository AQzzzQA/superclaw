/**
 * 加载状态组件
 */
import { Spin } from 'antd'

interface LoadingProps {
  size?: 'small' | 'default' | 'large'
  tip?: string
  spinning?: boolean
  children?: React.ReactNode
}

const Loading: React.FC<LoadingProps> = ({ size = 'default', tip, spinning = true, children }) => {
  if (children) {
    return (
      <Spin size={size} tip={tip} spinning={spinning}>
        {children}
      </Spin>
    )
  }

  return (
    <div style={{
      display: 'flex',
      justifyContent: 'center',
      alignItems: 'center',
      minHeight: '200px'
    }}>
      <Spin size={size} tip={tip} />
    </div>
  )
}

export default Loading
