var geocoder;
var map;
google.maps.event.addDomListener(window, 'load', initializeMunichCityCenter);

$(function() {
    $.datepicker.setDefaults( $.datepicker.regional[ "de" ] );
    $("#id_date_time_begin_0").datepicker( $.datepicker.regional[ "de" ]);
    $("#id_date_time_end_0").datepicker( $.datepicker.regional[ "de" ]);
});