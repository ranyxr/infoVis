let stack_chart_height = "300px";
// Get dom in html
let stack_chart_dom = document.getElementById("echarts-stack");
stack_chart_dom.style.height = stack_chart_height;
// Initial chart
let stack_chart = echarts.init(stack_chart_dom);
//----------------------Data----------------------
//--------------------Location--------------------
let wid_stack_gene_chart = "88%";
let lef_stack_gene_chart = "9%";
let top_stack_gene_chart = "10";
let hei_stack_gene_chart = 150;

let wid_stack_gene_legend = "88%";
let lef_stack_gene_legend = "9%";
let top_stack_gene_legend = 180;
let hei_stack_gene_legend = 10;

let wid_stack_datazoom = "88%";
let lef_stack_datazoom = "9%";
let top_stack_datazoom = 210;
let hei_stack_datazoom = 15;
//----------------------Grid----------------------
let grid_stack_gene_chart = {
    width: wid_stack_gene_chart,
    left: lef_stack_gene_chart,
    top: top_stack_gene_chart,
    height: hei_stack_gene_chart,
};
//----------------------Axis----------------------
let stack_xAxis = {
     data: stack_x_axis_data,
     type: 'category',
     gridIndex:0,
     axisLine: {
         onZero: true,
         lineStyle: {
             color: '#eee'
         }
     },
     show: true,
     splitLine: {show: false},
     axisLabel: {
      rotate: -20
     }
 };
let stack_yAxis = {
    type: "value",
    splitArea: {show: false},
    splitLine: {show: false},
    splitNumber: 8,
    axisTick: {},
    axisLine: {
        onZero: true,
        lineStyle: {
            color: '#eee'
        },
    },
    axisLabel: {
        show: true,
        formatter: function (value) {
            if (value >= 0 && value <= 100) return value
        }
    },
    show: true,
    gridIndex: 0,
    position: 'left',
    name: "% of Artwork of the Period",
    nameLocation: "middle",
    nameTextStyle: {
        padding: [3, 4, 25, 4]
    },
    max: 130,
    min: -15,
};
//---------------------Series---------------------
let stack_series_list = [];
let stack_legend_list = [];
for (let key in stack_item_data){
    stack_legend_list.push(key);
    stack_series_list.push(
        {
            name: key,
            type: 'bar',
            stack: 'one',
            barCategoryGap: 0,
            barGap: 0,
            emphasis: chart_config_emphasis_style,
            data: stack_item_data[key]
        }
    )
};
//---------------------Legend---------------------
let stack_legend = {
     data: stack_legend_list,
     type: 'scroll',
     icon: 'roundRect',
     width:      wid_stack_gene_legend,
     left:       lef_stack_gene_legend,
     top:        top_stack_gene_legend,
     itemHeight: hei_stack_gene_legend,
     itemWidth: 10,
     itemGap : 20,
     symbolKeepAspect : true,
     textStyle:{
         color: "#fff",
        //  width:
     },
 };
//-------------------Data Zoom -------------------

let stack_data_zoom_inside = {
    show: true,
    type: 'inside',
    start: data_zoom_start,
    end: data_zoom_end,
    xAxisIndex: 0,
};
let stack_data_zoom = {
    show: true,
    start: data_zoom_start,
    end: data_zoom_end,
    top:    top_stack_datazoom,
    height: hei_stack_datazoom,
    width:  wid_stack_datazoom,
    left:   lef_stack_datazoom,
    xAxisIndex: 0,
};
let stack_data_zoom_list = [stack_data_zoom_inside,stack_data_zoom];
//------------------Generate Graph------------------
let chart_stack_option = {
    backgroundColor: chart_config_background_color,
    grid :grid_stack_gene_chart,
    series: stack_series_list,
    xAxis: stack_xAxis,
    yAxis: stack_yAxis,
    toolbox: chart_config_tool_box,
    tooltip: {show: true},
    legend: stack_legend,
    dataZoom: stack_data_zoom_list,
};
stack_chart.on("datazoom", function(para){
    setTimeout(function(){
        let temp_option = stack_chart.getOption();
        let temp_s = parseInt(temp_option["dataZoom"]["0"]["start"]);
        let temp_e = parseInt(temp_option["dataZoom"]["0"]["end"]);
        temp_s = parseInt(temp_s * 20.1);
        temp_e   = parseInt(temp_e * 20.1);

        if(data_zoom_start === temp_s && data_zoom_end === temp_e){
            return 0;
        }
        data_zoom_start = temp_s;
        data_zoom_end   = temp_e;

        let XHR = new XMLHttpRequest();
        let request_data = {"start_year": temp_s, "end_year": temp_e};

        XHR.open('POST', "http://127.0.0.1:5000/api/filter");
        XHR.setRequestHeader('content-type', 'application/json');

        XHR.send(JSON.stringify(request_data));
        XHR.onreadystatechange = function(){
              if(XHR.readyState === 4 && XHR.status === 200){
                  let t_data = JSON.parse(XHR.responseText);

                  let t_option = word_cloud_chart.getOption();
                  t_option.series[0].data = JSON.parse(t_data.word_cloud);
                  word_cloud_chart.setOption(t_option);
                  // console.log(JSON.parse(t_data.word_cloud));

                  t_option = artiest_index_chart.getOption();
                  artiest_index_chart_data = JSON.parse(t_data.at_index)
                  let t_series_list = to_artiest_index_series_list(artiest_index_chart_data, []);
                  console.log(t_series_list)
                  t_option.series = t_series_list;
                  artiest_index_chart.setOption(t_option);

              }
        };
    }, 3000);
   });
if (chart_stack_option && typeof chart_stack_option === "object") {
     stack_chart.setOption(chart_stack_option, true);
}

