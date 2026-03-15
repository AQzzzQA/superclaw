import { useState, useCallback } from 'react'

interface UseTableSelectionReturn {
  selectedRowKeys: React.Key[]
  selectedRows: any[]
  setSelectedRowKeys: (keys: React.Key[]) => void
  setSelectedRows: (rows: any[]) => void
  clearSelection: () => void
  isSelected: (key: React.Key) => boolean
}

const useTableSelection = (): UseTableSelectionReturn => {
  const [selectedRowKeys, setSelectedRowKeysState] = useState<React.Key[]>([])
  const [selectedRows, setSelectedRowsState] = useState<any[]>([])

  const setSelectedRowKeys = useCallback((keys: React.Key[]) => {
    setSelectedRowKeysState(keys)
  }, [])

  const setSelectedRows = useCallback((rows: any[]) => {
    setSelectedRowsState(rows)
  }, [])

  const clearSelection = useCallback(() => {
    setSelectedRowKeysState([])
    setSelectedRowsState([])
  }, [])

  const isSelected = useCallback((key: React.Key) => {
    return selectedRowKeys.includes(key)
  }, [selectedRowKeys])

  return {
    selectedRowKeys,
    selectedRows,
    setSelectedRowKeys,
    setSelectedRows,
    clearSelection,
    isSelected,
  }
}

export default useTableSelection
