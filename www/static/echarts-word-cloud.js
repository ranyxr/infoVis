let word_cloud_chart_height = "300px";
// Get dom in html
let word_cloud_chart_dom = document.getElementById("echarts-word-cloud");
word_cloud_chart_dom.style.height = word_cloud_chart_height;
// Initial chart
let word_cloud_chart = echarts.init(word_cloud_chart_dom);
//--------------------Location--------------------
let wid_word_cloud_chart = "98%";
let lef_word_cloud_chart = "center";
let top_word_cloud_chart = "center";
let hei_word_cloud_chart = 300;
//---------------------Series---------------------
let word_cloud_series = {
    type: 'wordCloud',
    name: 'wc',
    gridSize: 14,
    sizeRange: [12, 30],
    rotationRange: [-2, 2],
    // shape: 'pentagon',
    width: wid_word_cloud_chart,
    height: hei_word_cloud_chart,
    left: lef_word_cloud_chart,
    top: top_word_cloud_chart,
    drawOutOfBound: false,
    textStyle: {
        normal: {
            color: function () {
                return 'rgb(' + [
                    Math.round(Math.random() * 200 + 50),
                    Math.round(Math.random() * 200 + 50),
                    Math.round(Math.random() * 200 + 50)
                ].join(',') + ')';
            }
        },
        emphasis: {
            shadowBlur: 3,
            shadowColor: '#333'
        }
    },
    data: word_cloud_chart_data
};
//------------------Generate Graph------------------
let word_cloud_chart_option = {
    backgroundColor: chart_config_background_color,
    series: word_cloud_series,
    // toolbox: chart_config_tool_box,
    // tooltip: {show: true},
};
if (word_cloud_chart_option && typeof word_cloud_chart_option === "object") {
     word_cloud_chart.setOption(word_cloud_chart_option, true);
}

