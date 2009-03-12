
  $(function() {

    $("select")

      .mouseover(function(){
          $(this)
              .data("origWidth", $(this).css("width"))
              .css("width", "auto");
      })

      .mouseout(function(){
          $(this).css("width", $(this).data("origWidth"));
      });

  });

