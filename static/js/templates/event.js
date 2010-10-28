var geocoder;
var map;
google.maps.event.addDomListener(window, 'load', function() {
	initializeMunichCityCenter();
	update_location();
});

$(function() {
	$.datepicker.setDefaults( $.datepicker.regional[ "de" ] );
	$("#id_date_time_begin_0").datepicker( $.datepicker.regional[ "de" ]);
	$("#id_date_time_end_0").datepicker( $.datepicker.regional[ "de" ]);
	$("#id_location").change(update_location);
});

var update_location = function() {
	var id = $("#id_location").val();
	if(id == "") {
		$("#id_location_name").val('')
		$("#id_location_name").attr('disabled', false)
		$("#id_location_street").val('')
		$("#id_location_street").attr('disabled', false)
		$("#id_location_city").val('')
		$("#id_location_city").attr('disabled', false)
	}
	else {
		$("#id_location_name").val(locations[id].name)
		$("#id_location_name").attr('disabled', true)
		$("#id_location_street").val(locations[id].street)
		$("#id_location_street").attr('disabled', true)
		$("#id_location_city").val(locations[id].city)
		$("#id_location_city").attr('disabled', true)
		$("#id_location_show_in_map").click()
	}
};

