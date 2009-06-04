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

  // $('body').supersleight();

  $("#rightbox").tabs({ selected: 3 });
  // try to hide tab items, except default

  $.preloadImages("/static/img/Search2.png",
                  "/static/img/reset2.png",
                  "/static/img/prev2.png",
                  "/static/img/next2.png",
                 "/static/img/Images2.png",
                  "/static/img/logos2.png",
                  "/static/img/Small2.png",
                  "/static/img/Medium2.png",
                  "/static/img/Large2.png",
                  "/static/img/original_size2.png",
                  "/static/img/cmyk2.png",
                  "/static/img/pantone2.png");

  toggleImage($('#searchbutton'), "/static/img/Search2.png", "/static/img/Search.png"); 
  toggleImage($('#resetlink'), "/static/img/reset2.png", "/static/img/reset.png");
  toggleImage($('#previousbutton'), "/static/img/prev2.png", "/static/img/prev.png"); 
  toggleImage($('#nextbutton'), "/static/img/next2.png", "/static/img/next.png"); 
  toggleImage($('#download-small'), "/static/img/Small2.png", "/static/img/Small.png"); 
  toggleImage($('#download-medium'), "/static/img/Medium2.png", "/static/img/Medium.png"); 
  toggleImage($('#download-large'), "/static/img/Large2.png", "/static/img/Large.png"); 
  toggleImage($('#download-original'), "/static/img/original_size2.png", "/static/img/original_size.png"); 
  toggleImage($('#download-cmyk'), "/static/img/cmyk2.png", "/static/img/cmyk.png"); 
  toggleImage($('#download-pantone'), "/static/img/pantone2.png", "/static/img/pantone.png");
  toggleImage($('.logos #images-section'), "/static/img/Images2.png", "/static/img/Images.png"); 
  toggleImage($('.images #logos-section'), "/static/img/logos2.png", "/static/img/logos.png"); 

});
