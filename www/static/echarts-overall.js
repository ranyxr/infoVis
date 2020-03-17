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

let trip_type_e = "east";
let trip_type_g = "global";
let trip_type_w = "west";

let trip_type = trip_type_g;

let eastern_trip_data = [
    {
        name: 'First presidential debate',
        xAxis: '273'
    },
    {
        name: 'Russia Directed Hacks to Influence Elections',
        xAxis: '844'
    },
    {
        name: 'Hillary Clinton case under review by FBI',
        xAxis: '964'
    },
    {
        name: 'US Presidential Election 2016',
        xAxis: '1085'
    }
];
let western_trip_data = [
    {
        name: 'Medieval art',
        xAxis: '261',
        description: "The medieval art of the Western world covers a vast scope of time and place, over 1000 years of art in Europe, and at times the Middle East and North Africa. It includes major art movements and periods, national and regional art, genres, revivals, the artists' crafts, and the artists themselves."
    },
    {
        name: 'Renaissance',
        xAxis: '1306',
        description: "The Renaissance (UK: /rɪˈneɪsəns/ rin-AY-sənss, US: /ˈrɛnəsɑːns/ (About this soundlisten) REN-ə-sahnss) was a period in European history marking the transition from the Middle Ages to Modernity and covering the 15th and 16th centuries. In addition to the standard periodization, proponents of a long Renaissance put its beginning in the 14th century and its end in the 17th century. The traditional view focuses more on the early modern aspects of the Renaissance and argues that it was a break from the past, but many historians today focus more on its medieval aspects and argue that it was an extension of the Middle Ages."
    },
    {
        name: 'Romanticism',
        xAxis: '1788',
        description: "Romanticism (also known as the Romantic era) was an artistic, literary, musical and intellectual movement that originated in Europe towards the end of the 18th century, and in most areas was at its peak in the approximate period from 1800 to 1850. Romanticism was characterized by its emphasis on emotion and individualism as well as glorification of all the past and nature, preferring the medieval rather than the classical. It was partly a reaction to the Industrial Revolution, the aristocratic social and political norms of the Age of Enlightenment, and the scientific rationalization of nature—all components of modernity."
    },
    {
        name: 'Modern art',
        xAxis: '1869',
        description: "Modern art includes artistic work produced during the period extending roughly from the 1860s to the 1970s, and denotes the styles and philosophy of the art produced during that era. The term is usually associated with art in which the traditions of the past have been thrown aside in a spirit of experimentation.[2] Modern artists experimented with new ways of seeing and with fresh ideas about the nature of materials and functions of art. A tendency away from the narrative, which was characteristic for the traditional arts, toward abstraction is characteristic of much modern art. More recent artistic production is often called contemporary art or postmodern art."
    },
    {
        name: 'Contemporary art',
        xAxis: '1949',
        description: "Contemporary art is the art of today, produced in the second half of the 20th century or in the 21st century. Contemporary artists work in a globally influenced, culturally diverse, and technologically advancing world. Their art is a dynamic combination of materials, methods, concepts, and subjects that continue the challenging of boundaries that was already well underway in the 20th century. Diverse and eclectic, contemporary art as a whole is distinguished by the very lack of a uniform, organising principle, ideology, or \"-ism\". Contemporary art is part of a cultural dialogue that concerns larger contextual frameworks such as personal and cultural identity, family, community, and nationality."
    }
];
let eastern_trip_markline = {
    type: 'bar',
    name: 'Important dates',
    stack: 'one',
    barCategoryGap: 0,
    barGap: 0,
    emphasis: [],
    data: [],
    markLine: {
        data : eastern_trip_data
    }
};
let western_trip_markline = {
    type: 'bar',
    name: 'western',
    stack: 'one',
    barCategoryGap: 0,
    barGap: 0,
    emphasis: [],
    data: [],
    markLine: {
        data: western_trip_data
    }
};