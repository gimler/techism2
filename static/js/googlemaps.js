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
  var latlng = new google.maps.LatLng(48.13788,11.575953);
  var myOptions = {
    zoom: 15,
    center: latlng,
    mapTypeId: google.maps.MapTypeId.ROADMAP
  };
  map = new google.maps.Map(document.getElementById("map_canvas"), myOptions);  
}