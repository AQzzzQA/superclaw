import React, { useMemo } from 'react'
import ReactECharts from 'echarts-for-react'
import type { EChartsOption } from 'echarts'

interface DataPoint {
  name: string
  value: number
}

interface BarChartProps {
  title: string
  data: DataPoint[]
  xKey?: string
  yKey?: string
  color?: string
  horizontal?: boolean
  height?: string
}

const BarChart = ({
  title,
  data,
  xKey = 'name',
  yKey = 'value',
  color = '#1890ff',
  horizontal = false,
  height = '400px',
}: BarChartProps) => {
  const option: EChartsOption = useMemo(() => {
    return {
      title: {
        text: title,
        left: 'center',
        textStyle: {
          fontSize: 16,
          fontWeight: 600,
        },
      },
      tooltip: {
        trigger: 'axis',
        axisPointer: {
          type: 'shadow',
        },
      },
      grid: {
        left: '3%',
        right: '4%',
        bottom: '3%',
        containLabel: true,
      },
      xAxis: horizontal
        ? {
            type: 'value',
          }
        : {
            type: 'category',
            data: data.map((d) => d[xKey]),
          },
      yAxis: horizontal
        ? {
            type: 'category',
            data: data.map((d) => d[xKey]),
          }
        : {
            type: 'value',
          },
      series: [
        {
          name: title,
          type: 'bar',
          data: data.map((d) => d[yKey]),
          itemStyle: {
            color,
          },
          barWidth: '60%',
        },
      ],
    }
  }, [title, data, xKey, yKey, color, horizontal])

  return <ReactECharts option={option} style={{ height }} />
}

export default BarChart
