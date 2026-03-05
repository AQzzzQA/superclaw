import React from 'react'
import ReactDOM from 'react-dom/client'
import { BrowserRouter } from 'react-router-dom'
import App from './App'
import './index.css'

console.log('main.tsx loading...')
console.log('Root element:', document.getElementById('root'))

const rootElement = document.getElementById('root')

if (!rootElement) {
  console.error('Root element not found!')
  throw new Error('Root element not found')
}

try {
  const root = ReactDOM.createRoot(rootElement)
  root.render(
    <React.StrictMode>
      <BrowserRouter>
        <App />
      </BrowserRouter>
    </React.StrictMode>,
  )
  console.log('React app mounted successfully')
} catch (error) {
  console.error('Failed to mount React app:', error)
  rootElement.innerHTML = '<div style="padding: 50px; text-align: center;"><h1>应用加载失败</h1><p>' + error + '</p></div>'
}
