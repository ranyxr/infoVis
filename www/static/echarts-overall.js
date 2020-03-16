let chart_config_background_color = 'rgb(46, 47, 51)';
let chart_config_tool_box = {show: false};
let chart_config_emphasis_style = {
    itemStyle: {
        barBorderWidth: 1,
        shadowBlur: 10,
        shadowOffsetX: 0,
        shadowOffsetY: 0,
        shadowColor: 'rgba(0,0,0,0.5)'
    }
};
let app = {};

let data_zoom_start = 0;
let data_zoom_end   = 100;

function to_artiest_index_series_list(in_data, in_list) {
    for (let in_key in in_data) {
        // console.log(in_data[in_key])
        in_list.push(
            {
                type: 'bar',
                xAxisIndex: 0,
                yAxisIndex: 0,
                gridIndex: 0,
                label: {
                    show: true,
                    position: 'insideLeft',
                    formatter: "Index: " + "{c} " + in_data[in_key]["name"]
                },
                data: [in_data[in_key].value]
            }
        )
    }
    return in_list
}