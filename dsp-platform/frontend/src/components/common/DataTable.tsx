import { Table, TableProps, Button, Space, Popconfirm } from 'antd'
import type { ColumnsType, TablePaginationConfig } from 'antd/es/table'
import { ReloadOutlined } from '@ant-design/icons'
import type { ReactNode } from 'react'

interface DataTableProps<T> extends Omit<TableProps<T>, 'columns'> {
  columns: ColumnsType<T>
  loading?: boolean
  onRefresh?: () => void
  showRefreshButton?: boolean
  rowActions?: (record: T) => ReactNode
  batchActions?: {
    label: string
    danger?: boolean
    onClick: (selectedRows: T[]) => void
    confirmText?: string
  }[]
}

const DataTable = <T extends Record<string, any>>({
  columns,
  loading,
  onRefresh,
  showRefreshButton = true,
  rowActions,
  batchActions,
  rowSelection,
  ...restProps
}: DataTableProps<T>) => {
  const extendedColumns: ColumnsType<T> = [
    ...columns,
    ...(rowActions
      ? [
          {
            title: '操作',
            key: 'actions',
            width: 200,
            render: (_: any, record: T) => (
              <Space size="small">
                {rowActions(record)}
              </Space>
            ),
          } as ColumnsType<T>[0],
        ]
      : []),
  ]

  const handleBatchAction = (action: { onClick: (selectedRows: T[]) => void; confirmText?: string }) => {
    const selectedRows = rowSelection?.selectedRowKeys
      ?.map((key) => {
        const row = restProps.dataSource?.find((r) => r.id === key)
        return row
      })
      .filter(Boolean) as T[]

    if (!selectedRows || selectedRows.length === 0) {
      return
    }

    if (action.confirmText) {
      // 需要确认的操作
      action.onClick(selectedRows)
    } else {
      // 不需要确认的操作
      action.onClick(selectedRows)
    }
  }

  return (
    <div>
      {batchActions && batchActions.length > 0 && (
        <div style={{ marginBottom: 16, display: 'flex', gap: 8, alignItems: 'center' }}>
          <span>已选择 {rowSelection?.selectedRowKeys?.length || 0} 项</span>
          <Space>
            {batchActions.map((action, index) => (
              <Popconfirm
                key={index}
                title={action.confirmText}
                onConfirm={() => handleBatchAction(action)}
                okText="确认"
                cancelText="取消"
              >
                <Button danger={action.danger} disabled={!rowSelection?.selectedRowKeys?.length}>
                  {action.label}
                </Button>
              </Popconfirm>
            ))}
          </Space>
        </div>
      )}
      <Table<T>
        columns={extendedColumns}
        loading={loading}
        rowKey="id"
        {...restProps}
        rowSelection={rowSelection}
      />
      {showRefreshButton && onRefresh && (
        <Button
          icon={<ReloadOutlined />}
          onClick={onRefresh}
          style={{ marginTop: 16 }}
        >
          刷新数据
        </Button>
      )}
    </div>
  )
}

export default DataTable
