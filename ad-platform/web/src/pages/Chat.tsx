import React, { useState, useEffect, useRef } from 'react'
import { Card, List, Input, Button, Space, Avatar, Typography, Divider } from 'antd'
import { SendOutlined, UserOutlined, MoreOutlined } from '@ant-design/icons'

const { Text } = Typography
const { InputRef } = Input

interface Message {
  id: string
  sender: 'user' | 'assistant'
  content: string
  timestamp: string
}

interface Conversation {
  id: string
  title?: string
  createdAt: string
  lastMessage?: Message
  messageCount: number
}

const Chat: React.FC = () => {
  const [message, setMessage] = useState<string>('')
  const [messages, setMessages] = useState<Message[]>([])
  const [inputValue, setInputValue] = useState('')
  const [loading, setLoading] = useState(false)
  const messagesEndRef = useRef<HTMLDivElement>(null)
  const [conversations, setConversations] = useState<Conversation[]>([])
  const [activeConversationId, setActiveConversationId] = useState<string | null>(null)
  
  const [sendMessage, setSendMessage] = useState(false)

  // 模拟对话历史数据（实际应该从数据库或 API 获取）
  const mockConversations: Conversation[] = [
    {
      id: 'C3A7C8A9D8B4C3C20DA94037CC13EBBB',
      title: '广告平台对接讨论',
      createdAt: '2026-03-05 00:00',
      lastMessage: {
        sender: 'user',
        content: '你好，在吗？',
        timestamp: '1772676968000'
      },
      messageCount: 12,
    },
  ]

  const currentUser = {
    id: 'C3A7C8A9D8B4C3C20DA94037CC13EBBB',
    name: '测试用户',
    avatar: 'https://api.dicebear.com/avatar/100',
  }

  // 获取对话列表
  const fetchConversations = async () => {
    setLoading(true)
    try {
      // TODO: 实际上应该从 API 获取对话历史
      await new Promise(resolve => setTimeout(resolve, 500))
      // 模拟数据
      setConversations(mockConversations)
    } finally {
      setLoading(false)
    }
  }

  // 选择对话
  const selectConversation = (id: string) => {
    setActiveConversationId(id)
    // TODO: 加载该对话的完整历史
  }

  // 发送消息
  const handleSend = async () => {
    if (!inputValue.trim()) return
    
    const newMessage: Message = {
      id: Date.now().toString(),
      sender: 'assistant',
      content: inputValue,
      timestamp: new Date().toISOString(),
    }

    const updatedMessages = [...messages, newMessage]
    setMessages(updatedMessages)
    setInputValue('')
    
    // 滚动到底部
    setTimeout(() => {
      messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' })
    }, 100)
    
    // 模拟回复（实际应该调用 API）
    setTimeout(() => {
      const replyMessage: Message = {
        id: Date.now().toString(),
        sender: 'user',
        content: `我明白了！把你对接到网页对话窗口，通过唯一链接区分用户`,
        timestamp: new Date().toISOString(),
      }
      
      const updatedMessages = [...messages, replyMessage]
      setMessages(updatedMessages)
      setLoading(false)
    }, 1500)
  }

  // 清空对话
  const clearConversation = () => {
    setActiveConversationId(null)
    setMessages([])
    setInputValue('')
  }

  return (
    <div style={{ height: 'calc(100vh - 64px)', display: 'flex' }}>
      {/* 左侧对话列表 */}
      <Card
        title="对话列表"
        style={{
          width: 300,
          height: '100%',
          overflow: 'auto',
          borderRadius: 8,
        }}
      >
        <List
          dataSource={conversations}
          renderItem={(item) => (
            <List.Item
              onClick={() => selectConversation(item.id)}
              style={{
                cursor: 'pointer',
                padding: '12px 0',
              }}
            >
              <Space>
                <Avatar src={currentUser.avatar} />
                <div>
                  <Text strong>{item.title || item.id.slice(0, 8)}</Text>
                <Text type="secondary" style={{ fontSize: 12 }}>
                  {item.messageCount} 条消息
                </Text>
              </div>
              </Space>
            </List.Item>
          )}
        />
      </Card>

      {/* 右侧对话内容 */}
      <Card
        title={conversations.find(c => c.id === activeConversationId)?.title || '新对话'}
        extra={
          currentUser.id === activeConversationId ? (
            <Button type="text" onClick={clearConversation}>清空</Button>
          ) : null
        }
        style={{
          flex: 1,
          borderRadius: 8,
          height: '100%',
          overflow: 'hidden',
        }}
      >
        <div
          <div
            <Typography.Title level={4} style={{ marginBottom: 16 }}>
              {conversations.find(c => c.id === activeConversationId)?.title || '新对话'}
            </Typography.Title>
            
            <div
              style={{
                height: 'calc(100% - 120px)',
                overflowY: 'auto',
                overflowY: 'auto',
                padding: '16px 0',
                backgroundColor: '#F5F7FA',
              }}
              ref={messagesEndRef}
            >
              {messages.map((msg, index) => (
                <div
                  key={msg.id}
                  style={{
                    marginBottom: 12,
                    padding: '12px',
                    backgroundColor: msg.sender === 'assistant' ? '#E6F7FF' : 'white',
                    borderRadius: 8,
                    maxWidth: '70%',
                  }}
                >
                  <div style={{ display: 'flex', alignItems: 'flex-start', gap: 8 }}>
                    <Avatar 
                      src={msg.sender === 'user' ? currentUser.avatar : 'https://api.dicebear.com/avatar/user.png'} 
                      style={{ fontSize: 24, marginRight: 8 }}
                    />
                    <div style={{ flex: 1, minWidth: 0 }}>
                      <div style={{ fontWeight: msg.sender === 'user' ? 'bold' : 'normal' }}>
                        <Text>{msg.sender === 'user' ? '用户' : '我'}</Text>
                      </div>
                      <Text type="secondary" style={{ fontSize: 12, marginLeft: 8 }}>
                        {new Date(msg.timestamp).toLocaleTimeString('zh-CN', {
                          hour12: false,
                          minute: true,
                          second: false
                        })}
                      </Text>
                    </div>
                  </div>
                  </div>
                  
                  {/* 消息内容 */}
                  <div
                    style={{
                      padding: '8px 12px',
                      backgroundColor: '#F0F5F7FA',
                      borderRadius: 8,
                      wordBreak: 'break-all',
                    }}
                  >
                    <Text>{msg.content}</Text>
                  </div>
                  
                  {/* 消息时间 */}
                  <Text type="secondary" style={{ fontSize: 12 }}>
                    {new Date(msg.timestamp).toLocaleTimeString('zh-CN', {
                      month: 'short',
                      day: 'numeric',
                      hour: 'numeric',
                      minute: 'numeric',
                    })}
                  </Text>
                </div>
              ))}
              
              <Divider />
              
              {/* 输入框 */}
              <Input.TextArea
                ref={inputRef}
                placeholder="输入消息..."
                value={inputValue}
                onChange={(e) => setInputValue(e.target.value)}
                onPressEnter={handleSend}
                autoSize={{ minRows: 3, maxRows: 6 }}
                style={{ marginTop: 12 }}
              />
              
              {/* 发送按钮 */}
              <Button
                type="primary"
                icon={<SendOutlined />}
                onClick={handleSend}
                loading={loading}
              >
                发送
              </Button>
              
            </div>
          </div>
        </Card>
      </div>
    </div>
  )
}

export default Chat
