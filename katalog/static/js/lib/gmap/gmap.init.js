(function($){

var map, infoWindow;
$(document).ready(function(){
	infoWindow = new google.maps.InfoWindow({});
    map = new GMaps({
        el: '#basic-map',
        lat: 45.959794,
        lng: 16.243112,
        zoomControl : true,
        zoomControlOpt: {
            style : 'SMALL',
            position: 'TOP_LEFT'
        },
        panControl : false,
        streetViewControl : false,
        mapTypeControl: false,
        overviewMapControl: false
    });
	map.loadFromFusionTables({
		query: {
			select: '\'Geocodable address\'',
			from: '1IdvBw2_swORGMvEHilNRDXNkHZ0crhvPK-1flS7u'
		},
		suppressInfoWindows: false
	});
});

})(jQuery);
