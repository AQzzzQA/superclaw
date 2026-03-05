export const createBarChartOption = (data: any[], xField: string, yField: string, title?: string) => {
  return {
    title: {
      text: title,
      left: 'center'
    },
    tooltip: {
      trigger: 'axis',
      axisPointer: {
        type: 'shadow'
      }
    },
    xAxis: {
      type: 'category',
      data: data.map(item => item[xField])
    },
    yAxis: {
      type: 'value'
    },
    series: [
      {
        name: yField,
        type: 'bar',
        data: data.map(item => item[yField]),
        itemStyle: {
          color: '#1890ff'
        }
      }
    ]
  }
}
