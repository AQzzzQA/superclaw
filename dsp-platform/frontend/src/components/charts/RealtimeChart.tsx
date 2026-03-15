import React, { useState, useEffect, useMemo } from 'react'
import ReactECharts from 'echarts-for-react'
import type { EChartsOption } from 'echarts'

interface DataPoint {
  timestamp: string
  value: number
}

interface RealtimeChartProps {
  title: string
  data: DataPoint[]
  maxDataPoints?: number
  color?: string
  height?: string
}

const RealtimeChart = ({
  title,
  data,
  maxDataPoints = 60,
  color = '#1890ff',
  height = '300px',
}: RealtimeChartProps) => {
  const option: EChartsOption = useMemo(() => {
    const displayData = data.slice(-maxDataPoints)

    return {
      title: {
        text: title,
        left: 'center',
        textStyle: {
          fontSize: 14,
          fontWeight: 500,
        },
      },
      tooltip: {
        trigger: 'axis',
        formatter: (params: any) => {
          const point = params[0]
          const time = new Date(point.name).toLocaleTimeString('zh-CN')
          return `${time}<br/>${title}: ${point.value}`
        },
      },
      grid: {
        left: '3%',
        right: '4%',
        bottom: '3%',
        top: '15%',
        containLabel: true,
      },
      xAxis: {
        type: 'category',
        data: displayData.map((d) => d.timestamp),
        boundaryGap: false,
        axisLabel: {
          formatter: (value: string) => new Date(value).toLocaleTimeString('zh-CN', { hour: '2-digit', minute: '2-digit' }),
        },
      },
      yAxis: {
        type: 'value',
        splitLine: {
          lineStyle: {
            type: 'dashed',
          },
        },
      },
      series: [
        {
          name: title,
          type: 'line',
          data: displayData.map((d) => d.value),
          smooth: true,
          showSymbol: false,
          itemStyle: {
            color,
          },
          areaStyle: {
            opacity: 0.3,
            color,
          },
          animationDuration: 300,
        },
      ],
    }
  }, [title, data, maxDataPoints, color])

  return <ReactECharts option={option} style={{ height }} />
}

export default RealtimeChart
