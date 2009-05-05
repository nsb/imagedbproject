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

  $.preloadImages("/static/img/button_09.gif", "/static/img/button_05.gif");

  toggleImage($('#searchbutton'), "/static/img/button_09.gif", "/static/img/button_07.gif"); 
  toggleImage($('#resetlink'), "/static/img/button_05.gif", "/static/img/button_03.gif"); 

});