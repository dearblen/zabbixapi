var myChart = echarts.init(document.getElementById('tianjincuccweb02mem'));
var option = {
 title : {
        text: '天津联通业务二从库内存',
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
            data:['64.38', '64.55', '64.75', '64.84', '64.17', '64.17'],
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