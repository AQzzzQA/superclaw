/**
 * 批量上传转化组件
 */
import React, { useState } from 'react'
import { Modal, Upload, Button, Table, message, Progress, Space } from 'antd'
import { UploadOutlined, InboxOutlined } from '@ant-design/icons'
import type { UploadProps } from 'antd'

const { Dragger } = Upload

interface BatchUploadConversionProps {
  open: boolean
  onClose: () => void
  onUpload: (file: File) => Promise<any>
}

const BatchUploadConversion: React.FC<BatchUploadConversionProps> = ({
  open,
  onClose,
  onUpload
}) => {
  const [fileList, setFileList] = useState<any[]>([])
  const [uploading, setUploading] = useState(false)
  const [uploadProgress, setUploadProgress] = useState(0)
  const [result, setResult] = useState<any>(null)

  const handleUpload = async () => {
    if (fileList.length === 0) {
      message.warning('请选择文件')
      return
    }

    setUploading(true)
    setUploadProgress(0)

    try {
      // 模拟上传进度
      const progressInterval = setInterval(() => {
        setUploadProgress(prev => {
          if (prev >= 90) {
            clearInterval(progressInterval)
            return 90
          }
          return prev + 10
        })
      }, 100)

      const res = await onUpload(fileList[0].originFileObj)

      clearInterval(progressInterval)
      setUploadProgress(100)

      setResult(res)
      message.success('上传成功')
    } catch (error) {
      message.error('上传失败')
    } finally {
      setUploading(false)
    }
  }

  const uploadProps: UploadProps = {
    fileList,
    onChange: ({ fileList: newFileList }) => {
      setFileList(newFileList)
    },
    beforeUpload: (file) => {
      const isExcel = file.name.endsWith('.xlsx') || file.name.endsWith('.csv')
      if (!isExcel) {
        message.error('仅支持 xlsx 或 csv 格式')
        return false
      }
      const isLt10M = file.size / 1024 / 1024 < 10
      if (!isLt10M) {
        message.error('文件大小不能超过 10MB')
        return false
      }
      return false
    },
    onRemove: () => {
      setResult(null)
      setUploadProgress(0)
    }
  }

  const errorColumns = [
    { title: '错误信息', dataIndex: 'error', key: 'error' }
  ]

  return (
    <Modal
      title="批量上传转化"
      open={open}
      onCancel={onClose}
      footer={[
        <Button key="cancel" onClick={onClose} disabled={uploading}>
          关闭
        </Button>,
        <Button
          key="upload"
          type="primary"
          loading={uploading}
          onClick={handleUpload}
          disabled={fileList.length === 0}
        >
          上传
        </Button>
      ]}
      width={600}
    >
      <Space direction="vertical" style={{ width: '100%' }}>
        <Dragger {...uploadProps}>
          <p className="ant-upload-drag-icon">
            <InboxOutlined />
          </p>
          <p className="ant-upload-text">点击或拖拽文件到此处上传</p>
          <p className="ant-upload-hint">支持 xlsx 或 csv 格式，最大 10MB</p>
        </Dragger>

        {uploading && (
          <Progress percent={uploadProgress} status="active" />
        )}

        {result && (
          <div>
            <p>上传结果：</p>
            <p>总计: {result.total} 条</p>
            <p>成功: {result.success} 条</p>
            <p>失败: {result.failed} 条</p>

            {result.errors && result.errors.length > 0 && (
              <Table
                dataSource={result.errors.map((error: string, index: number) => ({
                  key: index,
                  error
                }))}
                columns={errorColumns}
                pagination={false}
                size="small"
                style={{ marginTop: 16 }}
              />
            )}
          </div>
        )}
      </Space>
    </Modal>
  )
}

export default BatchUploadConversion
