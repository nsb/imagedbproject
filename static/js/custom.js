jQuery.preloadImages = function()
{
  for(var i = 0; i<arguments.length; i++)
  {
    jQuery("<img>").attr("src", arguments[i]);
  }
}

function toggleImage(buttonElm, imgover, imgout) {
  buttonElm.mouseover(function(e) {
    $(this).attr("src", imgover); 
  }).mouseout(function(e) {
    $(this).attr("src", imgout);
  });
} 

$(document).ready(function(){

  $.preloadImages("/static/img/button_09.gif",
                  "/static/img/button_05.gif",
                  "/static/img/button2_03.gif",
                  "/static/img/button2_09.gif",
                  "/static/img/Small2.jpg",
                  "/static/img/Medium2.jpg",
                  "/static/img/Large2.jpg",
                  "/static/img/original_size2.jpg");

  toggleImage($('#searchbutton'), "/static/img/button_09.gif", "/static/img/button_07.gif"); 
  toggleImage($('#resetlink'), "/static/img/button_05.gif", "/static/img/button_03.gif"); 
  toggleImage($('#previousbutton'), "/static/img/button2_03.gif", "/static/img/button2_05.gif"); 
  toggleImage($('#nextbutton'), "/static/img/button2_09.gif", "/static/img/button2_07.gif"); 
  toggleImage($('#download-small'), "/static/img/Small2.jpg", "/static/img/Small.jpg"); 
  toggleImage($('#download-medium'), "/static/img/Medium2.jpg", "/static/img/Medium.jpg"); 
  toggleImage($('#download-large'), "/static/img/Large2.jpg", "/static/img/Large.jpg"); 
  toggleImage($('#download-original'), "/static/img/original_size2.jpg", "/static/img/original_size.jpg"); 

});