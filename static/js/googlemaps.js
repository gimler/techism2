function displayLocation(street, city){
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