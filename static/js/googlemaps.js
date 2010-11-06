function displayLocation(street, city){
  if (street.length > 0 && city.length > 0){
      var location = street +","+city+","+ "Bayern";
      
      if (geocoder) {
        geocoder.geocode( { 'address': location}, function(results, status) {
          if (status == google.maps.GeocoderStatus.OK) {
            map.setCenter(results[0].geometry.location);
            var marker = new google.maps.Marker({
                map: map, 
                position: results[0].geometry.location,
                draggable: true
            });
          } else {
            document.getElementById("map_error").innerHTML="Geocode war nicht erfolgreich: " + status;
          }
        });
      }
  }
}


function initializeMunichCityCenter() {
  geocoder = new google.maps.Geocoder();
  var myOptions = getOptionsMunichCityCenter ();
  map = new google.maps.Map(document.getElementById("map_canvas"), myOptions);  
}


function renderEventDetailMap() {
	var where = $(this).children("section.where");
	var map_id = "map_" + where[0].id;
	
	// only load the map once
	if( $("#"+map_id).length > 0) {
		return;
	}
	
	// extract query string and 'q' parameter from link
	var a = where.find('a')
	var query = $.parseQuery(a[0].search, {'f':function(v){return v;}}).q
	
	if(where.width() < 640) {
		// static map with link for small screens, max. size of static map is 640x640
		var width = where.width();
		var height = Math.round(width / 3);
		where.append('<a id="'+map_id+'" href="http://maps.google.de/maps?q='+query+'&z=17"><img src="http://maps.google.com/maps/api/staticmap?center='+query+'&size='+width+'x'+height+'&zoom=15&sensor=false&markers=color:red|'+query+'" /></a>');
	}
	else {
		// dynamic map for larger screens
		where.append('<div id="'+map_id+'" style="height: 200px; width: 100%" />');
		
		var myOptions = getOptionsMunichCityCenter ();
		map = new google.maps.Map(document.getElementById(map_id), myOptions);
		
		var geocoder = new google.maps.Geocoder();
		geocoder.geocode( { 'address': decodeURIComponent(query)}, function(results, status) {
			if (status == google.maps.GeocoderStatus.OK) {
				map.setCenter(results[0].geometry.location);
				var marker = new google.maps.Marker({
					map: map, 
					position: results[0].geometry.location,
					draggable: false
				});
			}
		});
	}
}


jQuery.parseQuery = function(qs, options) {
	var q = (typeof qs === 'string'?qs:window.location.search), o = {'f':function(v){return unescape(v).replace(/\+/g,' ');}}, options = (typeof qs === 'object' && typeof options === 'undefined')?qs:options, o = jQuery.extend({}, o, options), params = {};
	jQuery.each(q.match(/^\??(.*)$/)[1].split('&'),function(i,p){
		p = p.split('=');
		p[1] = o.f(p[1]);
		params[p[0]] = params[p[0]]?((params[p[0]] instanceof Array)?(params[p[0]].push(p[1]),params[p[0]]):[params[p[0]],p[1]]):p[1];
	});
	return params;
}


// Helper functions

function getOptionsMunichCityCenter (){
  var latlng = new google.maps.LatLng(48.13788,11.575953);
  var myOptions = {
    zoom: 15,
    center: latlng,
    mapTypeId: google.maps.MapTypeId.ROADMAP
  };
  return myOptions;
}
