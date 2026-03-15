import React, { useMemo } from 'react'
import ReactECharts from 'echarts-for-react'
import type { EChartsOption } from 'echarts'

interface DataPoint {
  name: string
  value: number
}

interface PieChartProps {
  title: string
  data: DataPoint[]
  colors?: string[]
  roseType?: boolean
  height?: string
}

const PieChart = ({
  title,
  data,
  colors,
  roseType = false,
  height = '400px',
}: PieChartProps) => {
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
        trigger: 'item',
        formatter: '{a} <br/>{b}: {c} ({d}%)',
      },
      legend: {
        orient: 'vertical',
        left: 'left',
      },
      series: [
        {
          name: title,
          type: 'pie',
          radius: roseType ? ['20%', '70%'] : '70%',
          roseType: roseType ? 'radius' : false,
          data: data,
          emphasis: {
            itemStyle: {
              shadowBlur: 10,
              shadowOffsetX: 0,
              shadowColor: 'rgba(0, 0, 0, 0.5)',
            },
          },
          itemStyle: colors
            ? {
                color: (params: any) => colors[params.dataIndex % colors.length],
              }
            : undefined,
          label: {
            show: true,
            formatter: '{b}: {d}%',
          },
        },
      ],
    }
  }, [title, data, colors, roseType])

  return <ReactECharts option={option} style={{ height }} />
}

export default PieChart
