import { useState, useCallback } from 'react'

interface UsePaginationReturn {
  page: number
  pageSize: number
  total: number
  setPage: (page: number) => void
  setPageSize: (pageSize: number) => void
  setTotal: (total: number) => void
  handleChange: (page: number, pageSize: number) => void
}

const usePagination = (defaultPageSize = 20): UsePaginationReturn => {
  const [page, setPageState] = useState(1)
  const [pageSize, setPageSizeState] = useState(defaultPageSize)
  const [total, setTotal] = useState(0)

  const setPage = useCallback((newPage: number) => {
    setPageState(newPage)
  }, [])

  const setPageSize = useCallback((newPageSize: number) => {
    setPageSizeState(newPageSize)
    setPageState(1)
  }, [setPage])

  const setTotalState = useCallback((newTotal: number) => {
    setTotal(newTotal)
  }, [])

  const handleChange = useCallback((newPage: number, newPageSize: number) => {
    setPageState(newPage)
    setPageSizeState(newPageSize)
  }, [])

  return {
    page,
    pageSize,
    total,
    setPage,
    setPageSize,
    setTotal: setTotalState,
    handleChange,
  }
}

export default usePagination
