var caseDir = 'images/';

var vertHgt = '200';
var vertWid = '400';

var horHgt = '400';
var horWid = '600';

var legHgt = '200';
var legWid = '37';

var rrUrl = caseDir + 'rr.png',
  rrBounds = [[26.7010,-105.9209], [46.4409,-66.8973]];
var swindUrl = caseDir + 'swind.png',
  swindBounds = [[26.7010,-105.9209], [46.4409,-66.8973]];
var stempUrl = caseDir + 'stemp.png',
  stempBounds = [[26.7010,-105.9209], [46.4409,-66.8973]];

var rrimg = L.imageOverlay(rrUrl, rrBounds, {"opacity": 0.9});
var swindimg = L.imageOverlay(swindUrl, swindBounds);
var stempimg = L.imageOverlay(stempUrl, stempBounds, {"opacity": 0.9});

var centerCoord = [36.5709, -86.4091];
var initialZoom = 4;

var mainLayers = {
      "Rain rate": rrimg,
      "Surface temp": stempimg
};
var overlays = {
  "Surface winds": swindimg
};

  var rlegend = L.control({position: 'bottomleft'});
  var tlegend = L.control({position: 'bottomleft'});

  rlegend.onAdd = function (map){
        var div = L.DomUtil.create('div','info legend');
        div.innerHTML += "<img src='"+caseDir+"rlegend.png' alt='Rain rate legend' height='150'>";
        return div;
        };

  tlegend.onAdd = function (map){
        var div = L.DomUtil.create('div','info legend');
        div.innerHTML += "<img src='"+caseDir+"tlegend.png' alt='Temperature legend' height='150'>";
        return div;
        };


function highlightLayers() {
        if (map.hasLayer(swindimg)) {
                swindimg.bringToFront();
        }
        if (map.hasLayer(rrimg)) {
                rrimg.bringToBack();
        } else if (map.hasLayer(stempimg)) {
                stempimg.bringToBack();
        }
};


function caseOne(){
        loadhoricrosses();
        document.getElementById('vertrange').value = 9;
        togglefrequency('wbutton');
        updatevertcs();
}


function caseTwo(){
        loadvertcrosses();
        document.getElementById('lonrange').value = 1;
        document.getElementById('latrange').value = 3;
        togglefrequency('wbutton');
        updateloncs();
        updatelatcs();
}

