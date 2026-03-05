/**
 * 饼图配置
 */
export const createPieChartOption = (data: any[], nameField: string, valueField: string, title?: string) => {
  return {
    title: {
      text: title,
      left: 'center'
    },
    tooltip: {
      trigger: 'item',
      formatter: '{a} <br/>{b}: {c} ({d}%)'
    },
    legend: {
      orient: 'vertical',
      left: 'left'
    },
    series: [
      {
        name: title || '数据',
        type: 'pie',
        radius: '50%',
        data: data.map(item => ({
          name: item[nameField],
          value: item[valueField]
        })),
        emphasis: {
          itemStyle: {
            shadowBlur: 10,
            shadowOffsetX: 0,
            shadowColor: 'rgba(0, 0, 0, 0.5)'
          }
        }
      }
    ]
  }
}
