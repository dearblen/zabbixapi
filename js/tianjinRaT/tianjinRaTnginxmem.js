var myChart = echarts.init(document.getElementById('tianjinRaTnginxmem'));
var option = {
 title : {
        text: '天津广电负载均衡内存',
        subtext: ''
    },
    tooltip : {
        trigger: 'axis'
    },
    legend: {
        data:['内存使用率']
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
                formatter: '{value} %'
            }
        }
    ],
    series : [
        {
            name:'内存使用率',
            type:'line',
            data:['88.76', '88.76', '88.76', '88.77', '88.76', '88.76'],
            markPoint : {
                data : [
                    {type : 'max', name: '最大值'},
                    {type : 'min', name: '最小值'}
                ]
            },
            markLine : {
                data : [
                    {type : 'average', name : '平均值'}
                ]
            }
        }
    ]
};
myChart.setOption(option);