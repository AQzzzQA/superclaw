/**
 * 图表卡片组件
 */
import React from 'react'
import { Card } from 'antd'
import ReactECharts from 'echarts-for-react'

interface ChartCardProps {
  title: string
  option: any
  height?: number
  style?: React.CSSProperties
}

const ChartCard: React.FC<ChartCardProps> = ({
  title,
  option,
  height = 300,
  style = {}
}) => {
  return (
    <Card title={title} style={style}>
      <ReactECharts
        option={option}
        style={{ height: `${height}px` }}
        opts={{ renderer: 'svg' }}
      />
    </Card>
  )
}

export default ChartCard
