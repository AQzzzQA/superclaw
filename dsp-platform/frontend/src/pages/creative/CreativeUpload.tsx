import { Form, Button, message, Card, Upload, Progress, Divider, List, Tag } from 'antd'
import { ArrowLeftOutlined, CloudUploadOutlined, DeleteOutlined } from '@ant-design/icons'
import { useNavigate } from 'react-router-dom'
import { useState } from 'react'
import type { UploadFile, UploadProps } from 'antd'
import CreativeForm from '../../components/forms/CreativeForm'
import { useGetAdGroupsQuery } from '../../store/services/adGroupApi'

const CreativeUpload = () => {
  const navigate = useNavigate()
  const [form] = Form.useForm()
  const [uploadedFiles, setUploadedFiles] = useState<UploadFile[]>([])
  const [uploading, setUploading] = useState(false)
  const [uploadProgress, setUploadProgress] = useState(0)

  const { data: adGroupsData } = useGetAdGroupsQuery({ page: 1, pageSize: 100 })

  const beforeUpload = (file: File) => {
    const isValidType = ['image/jpeg', 'image/png', 'image/gif', 'video/mp4'].includes(file.type)
    if (!isValidType) {
      message.error('只能上传 JPG/PNG/GIF 图片或 MP4 视频')
      return false
    }
    const isLt50M = file.size / 1024 / 1024 < 50
    if (!isLt50M) {
      message.error('文件大小不能超过 50MB')
      return false
    }
    return true
  }

  const handleUploadChange: UploadProps['onChange'] = ({ fileList }) => {
    setUploadedFiles(fileList)
  }

  const handleRemove = (file: UploadFile) => {
    setUploadedFiles(uploadedFiles.filter((f) => f.uid !== file.uid))
  }

  const onFinish = async (values: any) => {
    if (uploadedFiles.length === 0) {
      message.error('请至少上传一个素材文件')
      return
    }

    setUploading(true)
    setUploadProgress(0)

    // 模拟上传进度
    const progressInterval = setInterval(() => {
      setUploadProgress((prev) => {
        if (prev >= 90) {
          clearInterval(progressInterval)
          return 90
        }
        return prev + 10
      })
    }, 200)

    try {
      // TODO: 调用实际的API上传创意
      await new Promise((resolve) => setTimeout(resolve, 2000))

      setUploadProgress(100)
      setTimeout(() => {
        clearInterval(progressInterval)
        setUploading(false)
        message.success('上传成功')
        navigate('/creatives')
      }, 500)
    } catch (error) {
      clearInterval(progressInterval)
      setUploading(false)
      message.error('上传失败')
    }
  }

  return (
    <div>
      <Card
        title={
          <div>
            <Button
              icon={<ArrowLeftOutlined />}
              onClick={() => navigate('/creatives')}
              style={{ marginRight: 16 }}
            >
              返回
            </Button>
            上传广告创意
          </div>
        }
      >
        <Form
          form={form}
          layout="vertical"
          onFinish={onFinish}
        >
          <Card title="上传素材" style={{ marginBottom: 16 }}>
            <Upload.Dragger
              listType="picture"
              fileList={uploadedFiles}
              beforeUpload={beforeUpload}
              onChange={handleUploadChange}
              onRemove={handleRemove}
              multiple
              accept="image/*,video/*"
            >
              <p className="ant-upload-drag-icon">
                <CloudUploadOutlined />
              </p>
              <p className="ant-upload-text">点击或拖拽文件到此处上传</p>
              <p className="ant-upload-hint">
                支持 JPG、PNG、GIF 图片和 MP4 视频，单个文件不超过 50MB
              </p>
            </Upload.Dragger>

            {uploading && (
              <div style={{ marginTop: 16 }}>
                <Progress percent={uploadProgress} status="active" />
              </div>
            )}

            {uploadedFiles.length > 0 && (
              <div style={{ marginTop: 16 }}>
                <Divider />
                <h4>已选择的文件：</h4>
                <List
                  dataSource={uploadedFiles}
                  renderItem={(file) => (
                    <List.Item
                      actions={[
                        <Button
                          type="link"
                          danger
                          icon={<DeleteOutlined />}
                          onClick={() => handleRemove(file)}
                        >
                          删除
                        </Button>
                      ]}
                    >
                      <List.Item.Meta
                        avatar={
                          file.type?.startsWith('image') ? (
                            <img src={URL.createObjectURL(file.originFileObj as File)} alt="" style={{ width: 48, height: 48, objectFit: 'cover' }} />
                          ) : (
                            <div style={{ width: 48, height: 48, background: '#f0f0f0', display: 'flex', alignItems: 'center', justifyContent: 'center' }}>
                              🎬
                            </div>
                          )
                        }
                        title={file.name}
                        description={
                          <Space>
                            <Tag color="blue">{file.type?.startsWith('image') ? '图片' : '视频'}</Tag>
                            <span>{(file.size / 1024 / 1024).toFixed(2)} MB</span>
                          </Space>
                        }
                      />
                    </List.Item>
                  )}
                />
              </div>
            )}
          </Card>

          <CreativeForm
            form={form}
            adGroups={adGroupsData?.items || []}
          />

          <div style={{ marginTop: 24, textAlign: 'right' }}>
            <Button onClick={() => navigate('/creatives')} style={{ marginRight: 8 }}>
              取消
            </Button>
            <Button type="primary" htmlType="submit" loading={uploading}>
              上传
            </Button>
          </div>
        </Form>
      </Card>
    </div>
  )
}

export default CreativeUpload
