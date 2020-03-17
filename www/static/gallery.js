function show_pic(imgs) {
  //Load clicked pic
  var expandImg = document.getElementById("gallery-show-image");
  expandImg.src = imgs.src;
  expandImg.parentElement.style.display = "block";
  //Load img title
  var art_title_dom = document.getElementById("art-title");
  art_title_dom.style.display=''
  art_title_dom.innerHTML = imgs.name;
  //Load img gallery-description
  var gallery_description_dom = document.getElementById("gallery-description");
  gallery_description_dom.style.display=''
  gallery_description_dom.innerText = imgs.alt;
  //Hide unchoosen pics
  var x = document.getElementsByClassName("gallery-column");
  var i;
  for (i = 0; i < x.length; i++) {
    x[i].style.display='none'
  }
}

function hide_pic(colse_btn) {
  //Hide close button
  colse_btn.parentElement.style.display='none'
  //Hide img title
  var art_title_dom = document.getElementById("art-title");
  art_title_dom.style.display='none'
  //Show all pics
  var x = document.getElementsByClassName("gallery-column");
  var i;
  for (i = 0; i < x.length; i++) {
    x[i].style.display=''
  }
}

function append_images() {
    document.getElementsByClassName("gallery-row")[0].innerHTML = ""
    for (let line in art_work_in_gallery) {
        let img_div = document.createElement("DIV");                 // Create a <li> node
        img_div.setAttribute("class", "gallery-column")
        let img = document.createElement("img");
        img.setAttribute("src", art_work_in_gallery[line]["src"]);
        img.setAttribute("alt", art_work_in_gallery[line]["alt"]);
        img.setAttribute("name", art_work_in_gallery[line]["name"]);
        img.setAttribute("style", "width:100%");
        img.setAttribute("onclick", "show_pic(this);")
        img_div.appendChild(img)
        document.getElementsByClassName("gallery-row")[0].appendChild(img_div)
    }
}

function resize(){
  artiest_index_chart.resize()
  word_cloud_chart.resize()
  chart_tree_chart.resize()
  artiest_index_chart.resize()
  stack_chart.resize()
}

function set_logo(){
  let logo_dom = document.getElementById("logo")
  let logo_inner_div = document.createElement("DIV")
  logo_inner_div.innerHTML = "<svg style=\"width:100%;height:100%;\"\n" +
      "   xmlns:dc=\"http://purl.org/dc/elements/1.1/\"\n" +
      "   xmlns:cc=\"http://creativecommons.org/ns#\"\n" +
      "   xmlns:rdf=\"http://www.w3.org/1999/02/22-rdf-syntax-ns#\"\n" +
      "   xmlns:svg=\"http://www.w3.org/2000/svg\"\n" +
      "   xmlns=\"http://www.w3.org/2000/svg\"\n" +
      "   xmlns:xlink=\"http://www.w3.org/1999/xlink\"\n" +
      "   xmlns:sodipodi=\"http://sodipodi.sourceforge.net/DTD/sodipodi-0.dtd\"\n" +
      "   xmlns:inkscape=\"http://www.inkscape.org/namespaces/inkscape\"\n" +
      "   id=\"svg8\"\n" +
      "   version=\"1.1\"\n" +
      "   viewBox=\"0 0 14.2875 5.0270901\"\n" +
      "   height=\"5.0270901mm\"\n" +
      "   width=\"14.2875mm\"\n" +
      "   sodipodi:docname=\"logo.svg\"\n" +
      "   inkscape:version=\"0.92.2 (unknown)\">\n" +
      "  <sodipodi:namedview\n" +
      "     pagecolor=\"#ffffff\"\n" +
      "     bordercolor=\"#666666\"\n" +
      "     borderopacity=\"1\"\n" +
      "     objecttolerance=\"10\"\n" +
      "     gridtolerance=\"10\"\n" +
      "     guidetolerance=\"10\"\n" +
      "     inkscape:pageopacity=\"0\"\n" +
      "     inkscape:pageshadow=\"2\"\n" +
      "     inkscape:window-width=\"2560\"\n" +
      "     inkscape:window-height=\"1391\"\n" +
      "     id=\"namedview21\"\n" +
      "     showgrid=\"true\"\n" +
      "     inkscape:pagecheckerboard=\"true\"\n" +
      "     inkscape:zoom=\"45.254834\"\n" +
      "     inkscape:cx=\"39.523695\"\n" +
      "     inkscape:cy=\"21.875026\"\n" +
      "     inkscape:window-x=\"0\"\n" +
      "     inkscape:window-y=\"240\"\n" +
      "     inkscape:window-maximized=\"1\"\n" +
      "     inkscape:current-layer=\"layer1\">\n" +
      "    <inkscape:grid\n" +
      "       type=\"xygrid\"\n" +
      "       id=\"grid890\" />\n" +
      "  </sodipodi:namedview>\n" +
      "  <defs\n" +
      "     id=\"defs2\">\n" +
      "    <linearGradient\n" +
      "       id=\"linearGradient877\">\n" +
      "      <stop\n" +
      "         id=\"stop873\"\n" +
      "         offset=\"0\"\n" +
      "         style=\"stop-color:#ffffff;stop-opacity:1;\" />\n" +
      "      <stop\n" +
      "         id=\"stop875\"\n" +
      "         offset=\"1\"\n" +
      "         style=\"stop-color:#ffffff;stop-opacity:0;\" />\n" +
      "    </linearGradient>\n" +
      "    <linearGradient\n" +
      "       gradientUnits=\"userSpaceOnUse\"\n" +
      "       y2=\"66.96991\"\n" +
      "       x2=\"113.5116\"\n" +
      "       y1=\"66.96991\"\n" +
      "       x1=\"110.56506\"\n" +
      "       id=\"linearGradient885\"\n" +
      "       xlink:href=\"#linearGradient877\" />\n" +
      "    <linearGradient\n" +
      "       gradientUnits=\"userSpaceOnUse\"\n" +
      "       y2=\"62.549137\"\n" +
      "       x2=\"117.00831\"\n" +
      "       y1=\"62.549137\"\n" +
      "       x1=\"105.24258\"\n" +
      "       id=\"linearGradient887\"\n" +
      "       xlink:href=\"#linearGradient877\" />\n" +
      "  </defs>\n" +
      "  <metadata\n" +
      "     id=\"metadata5\">\n" +
      "    <rdf:RDF>\n" +
      "      <cc:Work\n" +
      "         rdf:about=\"\">\n" +
      "        <dc:format>image/svg+xml</dc:format>\n" +
      "        <dc:type\n" +
      "           rdf:resource=\"http://purl.org/dc/dcmitype/StillImage\" />\n" +
      "        <dc:title></dc:title>\n" +
      "      </cc:Work>\n" +
      "    </rdf:RDF>\n" +
      "  </metadata>\n" +
      "  <g\n" +
      "     transform=\"translate(-76.464583,-54.906256)\"\n" +
      "     id=\"layer1\">\n" +
      "    <g\n" +
      "       aria-label=\"ART\"\n" +
      "       transform=\"scale(0.99738874,1.0026181)\"\n" +
      "       style=\"font-style:normal;font-weight:normal;font-size:5.4221921px;line-height:28.79999924;font-family:sans-serif;letter-spacing:-1.082744px;word-spacing:0px;fill:#ffffff;fill-opacity:1;stroke:none;stroke-width:0.25416526\"\n" +
      "       id=\"text817\">\n" +
      "      <path\n" +
      "         d=\"M 80.817308,57.996925 H 79.22348 l -0.251518,0.720135 h -1.024603 l 1.464097,-3.952799 h 1.215228 l 1.464098,3.952799 h -1.024604 z m -1.339663,-0.733372 h 1.08285 l -0.540101,-1.572648 z\"\n" +
      "         style=\"font-weight:bold;letter-spacing:0px;fill:#ffffff;fill-opacity:1;stroke-width:0.25416526\"\n" +
      "         id=\"path874\" />\n" +
      "      <path\n" +
      "         d=\"m 84.060562,56.516942 q 0.320355,0 0.458027,-0.11914 0.140321,-0.11914 0.140321,-0.391838 0,-0.270051 -0.140321,-0.386543 -0.137672,-0.116492 -0.458027,-0.116492 h -0.428903 v 1.014013 z m -0.428903,0.70425 V 58.71706 H 82.61235 v -3.952799 h 1.556762 q 0.781029,0 1.143744,0.262108 0.365362,0.262108 0.365362,0.828684 0,0.391839 -0.190624,0.643356 -0.187976,0.251518 -0.569224,0.370658 0.209157,0.04766 0.373305,0.217099 0.166796,0.166796 0.33624,0.508331 l 0.553339,1.122563 h -1.085498 l -0.481855,-0.982243 q -0.145615,-0.296526 -0.296526,-0.405076 -0.148263,-0.108549 -0.397133,-0.108549 z\"\n" +
      "         style=\"font-weight:bold;letter-spacing:0px;fill:#ffffff;fill-opacity:1;stroke-width:0.25416526\"\n" +
      "         id=\"path876\" />\n" +
      "      <path\n" +
      "         d=\"m 86.070057,54.764261 h 3.643035 v 0.770438 h -1.31054 v 3.182361 h -1.019308 v -3.182361 h -1.313187 z\"\n" +
      "         style=\"font-weight:bold;letter-spacing:0px;fill:#ffffff;fill-opacity:1;stroke-width:0.25416526\"\n" +
      "         id=\"path878\" />\n" +
      "    </g>\n" +
      "    <g\n" +
      "       aria-label=\"OMNI\"\n" +
      "       transform=\"scale(1.0246478,0.97594511)\"\n" +
      "       style=\"font-style:normal;font-weight:normal;font-size:1.03632343px;line-height:28.79999924;font-family:sans-serif;letter-spacing:-0.20694083px;word-spacing:0px;fill:#ffffff;fill-opacity:1;stroke:none;stroke-width:0.04857766\"\n" +
      "       id=\"text821\">\n" +
      "      <path\n" +
      "         d=\"m 84.378536,60.754895 q -0.08906,0 -0.138143,0.06578 -0.04908,0.06578 -0.04908,0.185202 0,0.118914 0.04908,0.184697 0.04908,0.06578 0.138143,0.06578 0.08957,0 0.138649,-0.06578 0.04908,-0.06578 0.04908,-0.184697 0,-0.11942 -0.04908,-0.185202 -0.04908,-0.06578 -0.138649,-0.06578 z m 0,-0.141179 q 0.182166,0 0.285394,0.104239 0.103227,0.10424 0.103227,0.287924 0,0.183178 -0.103227,0.287418 -0.103228,0.10424 -0.285394,0.10424 -0.18166,0 -0.285394,-0.10424 -0.103227,-0.10424 -0.103227,-0.287418 0,-0.183684 0.103227,-0.287924 0.103734,-0.104239 0.285394,-0.104239 z\"\n" +
      "         style=\"font-weight:bold;letter-spacing:-0.02428884px;fill:#ffffff;fill-opacity:1;stroke-width:0.04857766\"\n" +
      "         id=\"path881\" />\n" +
      "      <path\n" +
      "         d=\"m 84.889614,60.627378 h 0.247948 l 0.172046,0.404308 0.173058,-0.404308 h 0.247442 v 0.755484 h -0.18419 v -0.552571 l -0.17407,0.407344 H 85.24838 l -0.17407,-0.407344 v 0.552571 h -0.184696 z\"\n" +
      "         style=\"font-weight:bold;letter-spacing:-0.02428884px;fill:#ffffff;fill-opacity:1;stroke-width:0.04857766\"\n" +
      "         id=\"path883\" />\n" +
      "      <path\n" +
      "         d=\"m 85.8976,60.627378 h 0.217587 l 0.274768,0.518162 v -0.518162 h 0.184696 v 0.755484 H 86.357064 L 86.082296,60.8647 v 0.518162 H 85.8976 Z\"\n" +
      "         style=\"font-weight:bold;letter-spacing:-0.02428884px;fill:#ffffff;fill-opacity:1;stroke-width:0.04857766\"\n" +
      "         id=\"path885\" />\n" +
      "      <path\n" +
      "         d=\"m 86.741637,60.627378 h 0.194817 v 0.755484 h -0.194817 z\"\n" +
      "         style=\"font-weight:bold;letter-spacing:-0.02428884px;fill:#ffffff;fill-opacity:1;stroke-width:0.04857766\"\n" +
      "         id=\"path887\" />\n" +
      "    </g>\n" +
      "    <path\n" +
      "       inkscape:connector-curvature=\"0\"\n" +
      "       id=\"path829\"\n" +
      "       d=\"m 89.769748,54.906263 -0.01169,0.793753 h 0.200278 v 3.43958 h -0.529166 v 0.79375 h 1.322916 v -5.02709 z\"\n" +
      "       style=\"fill:#ffffff;fill-opacity:1;stroke:none;stroke-width:0.26499999;stroke-linecap:butt;stroke-linejoin:miter;stroke-miterlimit:4;stroke-dasharray:none;stroke-opacity:1\"\n" +
      "       sodipodi:nodetypes=\"ccccccccc\" />\n" +
      "    <path\n" +
      "       inkscape:connector-curvature=\"0\"\n" +
      "       id=\"path831\"\n" +
      "       d=\"m 77.522926,54.906256 v 0.79376 h -0.264583 v 3.43958 l 8.466657,0 v 0.79375 h -9.260417 v -5.02709 z\"\n" +
      "       style=\"fill:#ffffff;fill-opacity:1;stroke:none;stroke-width:0.26458499px;stroke-linecap:butt;stroke-linejoin:miter;stroke-opacity:1\"\n" +
      "       sodipodi:nodetypes=\"ccccccccc\" />\n" +
      "    <path\n" +
      "       inkscape:connector-curvature=\"0\"\n" +
      "       id=\"path833\"\n" +
      "       d=\"m 77.258343,54.906266 1.058323,-3e-6 v 0.79375 l -1.058323,3e-6 z\"\n" +
      "       style=\"fill:#ffffff;fill-opacity:1;stroke:none;stroke-width:0.08539398px;stroke-linecap:butt;stroke-linejoin:miter;stroke-opacity:1\"\n" +
      "       sodipodi:nodetypes=\"ccccc\" />\n" +
      "  </g>\n" +
      "</svg>";
  logo_inner_div.setAttribute("class", "align-self-center");
  logo_inner_div.setAttribute("style", "height:100px");
  logo_dom.appendChild(logo_inner_div);

}

append_images()
set_logo()
