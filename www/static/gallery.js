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