$(document).ready(function(){
$(".detail").hide(); 
/*$("#admin").hide();*/
/* clicks for touch interface */                 
$('.event').live('click', function() {
    //console.log("click!");
    $(this).children(".detail").slideToggle(300);
}); 


/*infinite scrolling*/
$('#content').infinitescroll({
  navSelector  : "a#nextpage:last",                  // selector for the paged navigation (it will be hidden)
  nextSelector : "a#nextpage:last",                 // selector for the NEXT link (to page 2)
  itemSelector : ".event",                         // selector for all items you'll retrieve
},function(arrayOfNewElems){
                    console.log("call");
                      $(".detail").hide();
                    var showevents = $(".event").size();
                    var eventsqty = num_pages *2;
                    if (showevents>eventsqty) $("#loadmore").hide(); 
                     console.log(showevents); 
                });
// kill scroll binding
$(window).unbind('.infscr');
// hook up the manual click guy.
$('#loadmore').click(function(){
  $(document).trigger('retrieve.infscr');   
  return;
});
// remove the paginator when we're done.
$(document).ajaxError(function(e,xhr,opt){
  if (xhr.status == 404) $('#nextpage a').remove();
});

});   