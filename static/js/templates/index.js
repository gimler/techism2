$(document).ready(function(){

  $(".detail").hide(); 

  /*$("#admin").hide();*/

  // clicks for touch interface
  $('article.event > header')
    .live('click', function() {
      $(this)
        .parent()
        .children(".detail")
        .slideToggle(300, renderEventDetailMap);
    });

  // infinite scrolling
  $('#content').infinitescroll({
    navSelector  : ".next",  // selector for the paged navigation (it will be hidden)
    nextSelector : ".next",  // selector for the NEXT link (to page 2)
    itemSelector : ".event", // selector for all items you'll retrieve
    errorCallback: function(){ $('#infscr-loading').remove() }
    },function(arrayOfNewElems){
      // hide all event details
      $(".detail").hide();

      // add ajax click handler to more link
      var pagina = arrayOfNewElems[arrayOfNewElems.length - 1];
      $('.prev', pagina).remove();

      // add click handler or remove pagina when there is no next page
      var next = $('.next', pagina);
      if (next.length > 0){
        next.bind('click', moreHandler);
      }else{
        $(pagina).remove();
      }
  });

  function moreHandler(e){
    e.preventDefault();

    // remove old pagina
    $(this).parent().parent().parent().remove();

    $(document).trigger('retrieve.infscr');
  }

  // kill scroll binding
  $(window).unbind('.infscr');

  // hook up the manual click guy.
  $('.next').bind('click', moreHandler);

  // remove the paginator when we're done.
//  $(document).ajaxError(function(e,xhr,opt){
//    if (xhr.status == 404) $('.next').remove();
//  });
});
