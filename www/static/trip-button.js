// Add active class to the current button (highlight it)
let header = document.getElementById("trip-button");
let btns = header.getElementsByClassName("trip_btn");
let eastern_btn = document.getElementById("eastern-trip");
let global_btn = document.getElementById("global-trip");
let western_btn = document.getElementById("western-trip");

for (let i = 0; i < btns.length; i++) {
  btns[i].addEventListener("click", function(e) {
      let current = document.getElementsByClassName("trip_btn_active");
      current[0].className = current[0].className.replace(" trip_btn_active", "");
      this.className += " trip_btn_active";
  });
}
//------------------Description ------------------
let trip_description_dom = document.getElementById("trip-description");
trip_description_dom.innerText = "World art studies is an expression used to define studies in the discipline of art history, which focus on the history of visual arts worldwide, its methodology, concepts and approach. The expression is also used within the academic curricula as title for specific art history courses and schools."
global_btn.addEventListener("click", function () {
    if(trip_type !== trip_type_g) {
        let t_option = stack_chart.getOption();
        let t_series = t_option.series;
        t_series.pop();
        t_option.series = t_series;
        stack_chart.setOption(t_option, true);
        trip_type = trip_type_g;
        stack_chart.dispatchAction({
            type: 'dataZoom',
            startValue: 0,
            endValue:   100
        });
        let trip_description_dom = document.getElementById("trip-description");
        trip_description_dom.innerText = "World art studies is an expression used to define studies in the discipline of art history, which focus on the history of visual arts worldwide, its methodology, concepts and approach. The expression is also used within the academic curricula as title for specific art history courses and schools."
    }
});
western_btn.addEventListener("click", function () {
    if(trip_type !== trip_type_w) {
        let t_option = stack_chart.getOption();
        let t_series = t_option.series;
        if(trip_type !== trip_type_g){
            t_series.pop();
        }
        t_series.push(western_trip_markline);
        t_option.series = t_series;
        stack_chart.setOption(t_option);
        trip_type = trip_type_w;
        stack_chart.dispatchAction({
            type: 'dataZoom',
            startValue: 0,
            endValue:   100
        });
        let trip_description_dom = document.getElementById("trip-description");
        trip_description_dom.innerText ="The art of Europe, or Western art, encompasses the history of visual art in Europe. European prehistoric art started as mobile Upper Paleolithic rock and cave painting and petroglyph art and was characteristic of the period between the Paleolithic and the Iron Age. Written histories of European art often begin with the art of the Ancient Middle East and the Ancient Aegean civilizations, dating from the 3rd millennium BC. Parallel with these significant cultures, art of one form or another existed all over Europe, wherever there were people, leaving signs such as carvings, decorated artifacts and huge standing stones. However a consistent pattern of artistic development within Europe becomes clear only with the art of Ancient Greece, adopted and transformed by Rome and carried; with the Roman Empire, across much of Europe, North Africa and the Middle East."
    }
});