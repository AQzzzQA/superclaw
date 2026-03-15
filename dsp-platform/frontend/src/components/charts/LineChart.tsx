import React, { useMemo } from 'react'
import ReactECharts from 'echarts-for-react'
import type { EChartsOption } from 'echarts'

interface DataPoint {
  name: string
  value: number
}

interface LineChartProps {
  title: string
  data: DataPoint[]
  xKey?: string
  yKey?: string
  color?: string
  smooth?: boolean
  showArea?: boolean
  height?: string
}

const LineChart = ({
  title,
  data,
  xKey = 'name',
  yKey = 'value',
  color = '#1890ff',
  smooth = true,
  showArea = false,
  height = '400px',
}: LineChartProps) => {
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
      xAxis: {
        type: 'category',
        data: data.map((d) => d[xKey]),
        boundaryGap: false,
      },
      yAxis: {
        type: 'value',
      },
      series: [
        {
          name: title,
          type: 'line',
          data: data.map((d) => d[yKey]),
          smooth,
          showSymbol: true,
          symbolSize: 8,
          itemStyle: {
            color,
          },
          lineStyle: {
            width: 2,
          },
          areaStyle: showArea
            ? {
                opacity: 0.3,
                color,
              }
            : undefined,
        },
      ],
    }
  }, [title, data, xKey, yKey, color, smooth, showArea])

  return <ReactECharts option={option} style={{ height }} />
}

export default LineChart
