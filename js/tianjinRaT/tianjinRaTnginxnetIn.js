var myChart = echarts.init(document.getElementById('tianjinRaTnginxnetIn'));
var option = {
 title : {
        text: '天津广电负载均衡网络入流量',
        subtext: ''
    },
    tooltip : {
        trigger: 'axis'
    },
    legend: {
        data:['入流量']
    },
    toolbox: {
        show : true,
        feature : {
            mark : {show: true},
            dataView : {show: true, readOnly: false},
            magicType : {show: true, type: ['line', 'bar']},
            restore : {show: true},
            saveAsImage : {show: true}
        }
    },
    calculable : true,
    xAxis : [
        {
            type : 'category',
            boundaryGap : false,
            data : ['0点','2点','4点','6点','8点','10点','12点','14点','16点','18点','20点','22点']
        }
    ],
    yAxis : [
        {
            type : 'value',
            axisLabel : {
                formatter: '{value} M'
            }
        }
    ],
    series : [
        {
            name:'入流量',
            type:'line',
            data:['0.26', '0.02', '1.70', '0.20', '0.02', '0.02'],
            markPoint : {
                data : [
                    {type : 'max', name: '最大值'},
                    {type : 'min', name: '最小值'}
                ]
            },
            markLine : {
                data : [
                    {type : 'average', name: '平均值'}
                ]
            }
        }
    ]
};
myChart.setOption(option);