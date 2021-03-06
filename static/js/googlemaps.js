function displayLocation(street, city){
  var where = $("#map_location");
  var mapHtml = where.html();
  var location = street +","+city+","+ "Bayern";
  var width = where.width();
  var height = Math.round(width / 3);
  if (mapHtml.substring(0, 4) == "<div"){
    if (street.length > 0 && city.length > 0){
        geocoder = new google.maps.Geocoder();
        geocodeAndSetMarker (map, location, true);
      }
    } else {
        var newMap = '<img id="map_location" src="http://maps.google.com/maps/api/staticmap?center=' + location + '&size='+width+'x'+height+'&zoom=15&sensor=false&markers=color:red|' + location + '" />';
        where.replaceWith(newMap);
    }
}


function initializeMunichCityCenter() {
  //var myOptions = getOptionsMunichCityCenter ();
  //map = new google.maps.Map($("map_canvas"), myOptions);  
  var where = $("#map_canvas");
  var width = where.width();
  var height = Math.round(width / 3);
  var mapId = "map_location";
  if(width < 640) {
    // static map with link for small screens, max. size of static map is 640x640
    var query ="48.13788,11.575953";
    where.append('<img id="'+mapId+'" src="http://maps.google.com/maps/api/staticmap?center='+query+'&size='+width+'x'+height+'&zoom=15&sensor=false" />');
  }
  else {
    // dynamic map for larger screens
    where.append('<div id="'+mapId+'" style="height: '+height+'px; width: 100%" />');
    var myOptions = getOptionsMunichCityCenter ();
    map = new google.maps.Map(document.getElementById(mapId), myOptions);
  }
}

function renderEventDetailMap() {
	var where = $(this).children("section.where");
	
	// the id of that map div
	var mapId = "map_" + where[0].id;
	
	// only load the map once
	if( $("#"+mapId).length > 0) {
		return;
	}
	
	// get the map link
	var mapLink = where.find('a')
	
	// exit if there isn't a map link
	if( mapLink.length == 0) {
		return;
	}
	
	// extract query string and 'q' parameter from link
	var query = $.parseQuery(mapLink[0].search, {'f':function(v){return v;}}).q
	
	var width = where.width();
	var height = Math.round(width / 3);
	if(width < 640) {
		// static map with link for small screens, max. size of static map is 640x640
		where.append('<a id="'+mapId+'" href="http://maps.google.de/maps?q='+query+'&z=17"><img src="http://maps.google.com/maps/api/staticmap?center='+query+'&size='+width+'x'+height+'&zoom=15&sensor=false&markers=color:red|'+query+'" /></a>');
	}
	else {
		// dynamic map for larger screens
		where.append('<div id="'+mapId+'" style="height: '+height+'px; width: 100%" />');
		var myOptions = getOptionsMunichCityCenter ();
		map = new google.maps.Map(document.getElementById(mapId), myOptions);
		var geocoder = new google.maps.Geocoder();
		geocodeAndSetMarker (map, decodeURIComponent(query), false)
	}
}


jQuery.parseQuery = function(qs,options) {
	var q = (typeof qs === 'string'?qs:window.location.search), o = {'f':function(v){return unescape(v).replace(/\+/g,' ');}}, options = (typeof qs === 'object' && typeof options === 'undefined')?qs:options, o = jQuery.extend({}, o, options), params = {};
	jQuery.each(q.match(/^\??(.*)$/)[1].split('&'),function(i,p){
		p = p.split('=');
		p[1] = o.f(p[1]);
		params[p[0]] = params[p[0]]?((params[p[0]] instanceof Array)?(params[p[0]].push(p[1]),params[p[0]]):[params[p[0]],p[1]]):p[1];
	});
	return params;
}


//utility methods

function getOptionsMunichCityCenter (){
    var latlng = new google.maps.LatLng(48.13788,11.575953);
    var myOptions = {
    zoom: 15,
    center: latlng,
    mapTypeId: google.maps.MapTypeId.ROADMAP,
    scrollwheel: false
  };
  return myOptions;
}

function geocodeAndSetMarker (myMap, location, isDraggable){
      geocoder.geocode( { 'address': location}, function(results, status) {
      if (status == google.maps.GeocoderStatus.OK) {
          myMap.setCenter(results[0].geometry.location);
          var marker = new google.maps.Marker({
              map: myMap, 
              position: results[0].geometry.location,
              draggable: isDraggable
          });
        } 
      });
}
