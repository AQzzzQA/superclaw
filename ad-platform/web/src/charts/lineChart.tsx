export const createLineChartOption = (data: any[], xField: string, yField: string, title?: string) => {
  return {
    title: {
      text: title,
      left: 'center'
    },
    tooltip: {
      trigger: 'axis'
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
        type: 'line',
        data: data.map(item => item[yField]),
        smooth: true,
        areaStyle: {
          opacity: 0.3
        }
      }
    ]
  }
}
