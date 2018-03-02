
var mapimg = L.tileLayer(
    'images/radarlabviewertiles/{z}/{x}/{y}.png', 
    {
        maxZoom: 7,
        minZoom: 0,
        attribution: '<a href="javascript:attribution()">Map Attributions</a>'
    }
);

function attribution() {
    window.alert('Map data: (c) OpenStreetMap contributors (https://openstreetmap.org).\n' +
                 'Map style: (c) Mapbox (https://mapbox.com).\n' +
                 'Model data courtesy S. van den Heever and A. Igel (http://reef.atmos.colostate.edu/~sue).\n' +
                 'For more information, contact the project creator at ethan.nelson@aos.wisc.edu'
                 );
};

overlays["Map"] = mapimg;

var map = L.map('map', {
    layers: [mapimg, rrimg] })
    .setView(centerCoord, initialZoom);
rlegend.addTo(map)
L.control.layers(mainLayers, overlays).addTo(map);

var latline = new L.polyline([]);
var lonline = new L.polyline([]);



  map.on('baselayerchange', function (eventLayer) {
      if (eventLayer.name == 'Rain rate') {
          rlegend.addTo(map);
          tlegend.removeFrom(map);
          rrimg.bringToBack();
          if (map.hasLayer(swindimg)) {
              swindimg.bringToFront();
          }
      }
      else if (eventLayer.name == 'Surface temp') {
          tlegend.addTo(map);
          rlegend.removeFrom(map);
          stempimg.bringToBack();
          if (map.hasLayer(swindimg)) {
              swindimg.bringToFront();
          }
      }
  })

