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

  $.preloadImages("/static/img/Search2.jpg",
                  "/static/img/clear2.jpg",
                  "/static/img/prev2.jpg",
                  "/static/img/next2.jpg",
/*                  "/static/img/Images2.gif",
                  "/static/img/logos2.jpg",*/
                  "/static/img/Small2.jpg",
                  "/static/img/Medium2.jpg",
                  "/static/img/Large2.jpg",
                  "/static/img/original_size2.jpg");

  toggleImage($('#searchbutton'), "/static/img/Search2.jpg", "/static/img/Search.jpg"); 
  toggleImage($('#resetlink'), "/static/img/clear2.jpg", "/static/img/clear.jpg");
  toggleImage($('#previousbutton'), "/static/img/prev2.jpg", "/static/img/prev.jpg"); 
  toggleImage($('#nextbutton'), "/static/img/next2.jpg", "/static/img/next.jpg"); 
  toggleImage($('#download-small'), "/static/img/Small2.jpg", "/static/img/Small.jpg"); 
  toggleImage($('#download-medium'), "/static/img/Medium2.jpg", "/static/img/Medium.jpg"); 
  toggleImage($('#download-large'), "/static/img/Large2.jpg", "/static/img/Large.jpg"); 
  toggleImage($('#download-original'), "/static/img/original_size2.jpg", "/static/img/original_size.jpg"); 
//   toggleImage($('#images-section'), "/static/img/Images2.gif", "/static/img/Images.gif"); 
//   toggleImage($('#logos-section'), "/static/img/logos2.jpg", "/static/img/logos.jpg"); 


});