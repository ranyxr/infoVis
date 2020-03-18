let chart_tree_height = "350px";
// Get dom in html
let chart_tree_dom = document.getElementById("echarts-tree");
chart_tree_dom.style.height = chart_tree_height;
// Initial chart
let chart_tree_chart = echarts.init(chart_tree_dom);
//----------------------Data----------------------
let tree_data                          = [{
    "name": "",
    "children": [
        {
            "name": "photograph",
            "children": [
                {"name": "architecture"},
                {"name": "album"},
                {"name": "photo"}
            ]
        },
        {
            "name": "textile",
            "children": [
                {"name": "leather"},
                {"name": "costume"},
                {"name": "badge"}
            ]
        },
        {
            "name": "painting",
            "children": [
                {"name": "illumination"},
                {"name": "lacquer"},
                {"name": "enamel"},
                {"name": "painting"},
            ]
        },
        {
            "name": "weapons and armor",
            "children": [
                {
                    "name": "weapons", "children":
                        [
                            {"name": "weapon"},
                            {"name": "bows"},
                            {"name": "dagger"},
                            {"name": "sword"},
                            {"name": "firearms"},
                            {"name": "knife"},
                            {"name": "shield"}
                        ]
                },
                {
                    "name": "armor", "children":
                        [
                            {"name": "helmet"},
                            {"name": "archery equipment"},
                            {"name": "armor"},
                            {"name": "equestrian"}
                        ]
                }
            ]
        },
        {
            "name": "modern art",
            "children": [
                {"name": "mixed media", "children": [{"name": "architecture"}]},
                {"name": "Performance art", "children": [{"name": "performance"}]},
                {"name": "installation", "children": [{"name": "installation"}]},
                {"name": "design", "children": [{"name": "stucco"}, {"name": "design"}]},
                {
                    "name": "new media", "children": [
                        {"name": "audio"},
                        {"name": "video"},
                        {"name": "tapestry"},
                        {"name": "film"},
                        {"name": "textiles"}
                    ]
                }]
        },
        {
            "name": "sculpture",
            "children": [
                {"name": "miniature"},
                {"name": "netsuke"},
                {"name": "ivory"},
                {"name": "tablet"},
                {"name": "sculpture"},
                {"name": "crche"},
                {"name": "bone"}]
        },
        {
            "name": "print",
            "children": [
                {"name": "manuscript"},
                {"name": "calligraphy"},
                {"name": "photo"},
                {"name": "illustrated book"},
                {"name": "papyrus"},
                {"name": "print"},
                {"name": "book"}]
        },
        {
            "name": "drawing",
            "children": [
                {"name": "periodical"},
                {"name": "graphics"},
                {"name": "poster"},
                {"name": "calligraphy"}]
        },
        {
            "name": "craft",
            "children": [
                {
                    "name": "miscellaneous", "children":
                        [{"name": "cricket cages"},
                            {"name": "gaming pieces"},
                            {"name": "tomb pottery"},
                            {"name": "chordophone"},
                            {"name": "plaquette"},
                            {"name": "smoking equipment"},
                            {"name": "horology"},
                            {"name": "chess set"},
                            {"name": "basketry"},
                            {"name": "frames"},
                            {"name": "cloisonn"},
                            {"name": "aerophone"},
                            {"name": "fans"},
                            {"name": "mirrors"},
                            {"name": "seal"},
                            {"name": "mosaic"}
                        ]
                },
                {
                    "name": "ornament", "children":
                        [{"name": "ceramics"},
                            {"name": "vase"},
                            {"name": "cloisonn"},
                            {"name": "screens"},
                            {"name": "gems"},
                            {"name": "furniture"},
                            {"name": "shell"},
                            {"name": "jewelry"},
                            {"name": "beads"},
                            {"name": "amber"}
                        ]
                },
                {
                    "name": "metal", "children":
                        [{"name": "medal"},
                            {"name": "coin"},
                            {"name": "lapidary"},
                            {"name": "Inro"}
                        ]
                },
                {
                    "name": "material", "children":
                        [{"name": "wood"},
                            {"name": "jade"},
                            {"name": "rubbing"}
                        ]
                }
            ]
        }
    ]
}]
//--------------------Location--------------------
let wid_tree_series = "100%";
let lef_tree_series = "center";
let top_tree_series = "8%";
let bot_tree_series = "8%";
let hei_tree_series = "60%";
//---------------------Series---------------------
let tree_series = {
    type: 'tree',
    name: 'Art types',
    orient: 'vertical',
    initialTreeDepth: 1,
    data: tree_data,
    color: "#eee",
    top: top_tree_series,
    bottom: bot_tree_series,
    left: lef_tree_series,
    width: wid_tree_series,
    height: hei_tree_series,
    symbolSize: 7,

    label: {
        position: 'top',
        verticalAlign: 'middle',
        align: 'middle'
    },

    leaves: {
        label: {
            position: 'bottom',
            rotate: -60,
            verticalAlign: 'middle',
            align: 'left',
        }
    },
    expandAndCollapse: true,
    animationDuration: 550,
    animationDurationUpdate: 750

};
let tree_series_list = [tree_series];
//------------------Generate Graph------------------
let chart_tree_option = {
    backgroundColor: chart_config_background_color,
    series: tree_series_list,
    toolbox: chart_config_tool_box,
    tooltip: {show: true},
};
if (chart_tree_option && typeof chart_tree_option === "object") {
     chart_tree_chart.setOption(chart_tree_option, true);
}

