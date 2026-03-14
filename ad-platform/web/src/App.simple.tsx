import React from 'react'

function App() {
  return (
    <div style={{ padding: '24px', background: '#f0f0f0' }}>
      <h1>广告平台测试页面</h1>
      <p>如果你能看到这行字，React 正在工作！</p>
      <div style={{ background: 'white', padding: '20px', marginBottom: '16px' }}>
        <h2>测试：侧边栏和内容</h2>
        <p>左侧：蓝色菜单（如果看不到，CSS 加载失败）</p>
        <p>右侧：内容区（如果看不到，路由或组件错误）</p>
      </div>
    </div>
  )
}

export default App
