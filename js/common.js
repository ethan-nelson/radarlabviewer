var frequencystring={};
frequencystring['sbutton'] = 'S band (3 GHz)';
frequencystring['kubutton'] = 'Ku band (13 GHz)';
frequencystring['kabutton'] = 'Ka band (35 GHz)';
frequencystring['wbutton'] = 'W band (94 GHz)';

var frequencydef={};
frequencydef['sbutton'] = 1;
frequencydef['kubutton'] = 2;
frequencydef['kabutton'] = 3;
frequencydef['wbutton'] = 4;

var mdrLabel=[ "Improved mission MDR shown", "Current mission MDR shown"];
var mdrdef={};
mdrdef[1] = 'h';
mdrdef[0] = 'l';

var attLabel=[ "Attenuated", "No attenuation" ];
var attdef={};
attdef[1] = '0';
attdef[0] = '1';

var levelListing = {};
levelListing[0] = " 1.5 km";
levelListing[1] = " 2 km";
levelListing[2] = " 3 km";
levelListing[3] = " 4 km";
levelListing[4] = " 5 km";
levelListing[5] = " 6 km";
levelListing[6] = " 7 km";
levelListing[7] = " 8 km";
levelListing[8] = " 9 km";
levelListing[9] = " 10 km";
levelListing[10] = " 12 km";

var isvertloaded = false;
var ishoriloaded = false;

var latImage = -1;
var lonImage = -1;
var vertImage = -1;
var imageFrequency = 0;

var mdrval = 0;
var mdrLevel = 0;

var attval = 0;
var attLevel = 0;

function setCases() {
    var casediv = document.createElement('div');
    casediv.innerHTML = ""
    if (typeof caseOne === 'function') {
        casediv.innerHTML += "<button onclick='caseOne();'>Load Case #1</button>";
    }
    if (typeof caseTwo === 'function') {
        casediv.innerHTML += " <button onclick='caseTwo();'>Load Case #2</button>";
    }
    if (typeof caseThree === 'function') {
        casediv.innerHTML += " <button onclick='caseThree();'>Load Case #3</button>";
    }
    document.getElementById('cases').replaceChild(casediv, document.getElementById('cases').childNodes[0]);
};

function resetMdr() {
    mdrLevel = 0;

    document.getElementById('mdr').style.display = "";
    document.getElementById('mdr').value = mdrLabel[0];
};

function resetAtt() {
    attLevel = 0;

    document.getElementById('att').style.display = "";
    document.getElementById('att').value = attLabel[0];
};

function displayLoading() {
    var loadingdiv = document.createElement('div');
    loadingdiv.innerHTML = "<center><b>Loading...</b></center>";
    document.getElementById('images').replaceChild(loadingdiv,document.getElementById('images').childNodes[0]);
};


function setFreqButtons() {
    var frequencydiv = document.createElement('div');
    frequencydiv.innerHTML = "";
    for (var key in frequencystring) {
        frequencydiv.innerHTML += "<input type='button' id='" + key + 
                                  "' onclick='togglefrequency(this.id)' value='" + 
                                  frequencystring[key] + "'>";
    };
    document.getElementById('frequencies').replaceChild(frequencydiv, document.getElementById('frequencies').childNodes[0]);
};


function setVertBlank() {
    var blankUrl = 'images/transparent.png';

    var imagediv = document.createElement('div');
    imagediv.innerHTML = "";
    for (i = 1; i < 4; i++) {
        imagediv.innerHTML += "<img id='latcs" + i + "' height='" + vertHgt +
                              "' width='" + vertWid + "' src='" + blankUrl + "'>" +
                              "<img id='horilegend" + i + "' height='" + legHgt +
                              "' width='" + legWid + "' src='" + blankUrl + "'>" +
                              "<img id='loncs" + i + "' height='" + vertHgt +
                              "' width='" + vertWid + "' src='" + blankUrl + "'>";
    };
    document.getElementById('images').replaceChild(imagediv, document.getElementById('images').childNodes[0]);

    vertImage = -1;
};


function setHorBlank() {
    var blankUrl = 'images/transparent.png';

    var imagediv = document.createElement('div');
    imagediv.innerHTML = "";
    for (i = 1; i < 4; i++) {
        imagediv.innerHTML += "<img id='vertcs" + i + "' height='" + horHgt +
                              "' width='" + horWid + "' src='" + blankUrl + "'>" +
                              "<img id='vertlegend" + i + "' height='" + legHgt +
                              "' width='" + legWid + "' src='" + blankUrl + "'>";
    };
    document.getElementById('images').replaceChild(imagediv, document.getElementById('images').childNodes[0]);

    latImage = -1;
    lonImage = -1;
};


function setVertSlider() {
    var values = [["latrange", "Latitude:", "updatelatcs();", "latLabel"],
                  ["lonrange", "Longitude:", "updateloncs();", "lonLabel"]];

    var sliderdiv = document.createElement('div');
    sliderdiv.innerHTML = "";
    for (i=0; i < 2; i++) {
        sliderdiv.innerHTML += "<label for='" + values[i][0] + "'>" + values[i][1] +
                               "</label><input id='" + values[i][0] + "' type='range' " +
                               "min='0' max='5' value='0' onmousemove='" + values[i][2] +
                               "' onchange='" + values[i][2] + "'><input type='text' id='" +
                               values[i][3] + "' size='6' value='' readonly='true'>"
    };
    document.getElementById('sliders').replaceChild(sliderdiv, document.getElementById('sliders').childNodes[0]);
}


function setHorSlider() {
    var sliderdiv = document.createElement('div');
    sliderdiv.innerHTML = "<label for='vertrange'>Height:</label>" +
                          "<input id='vertrange' type='range' min='0' max='10'" +
                          "value='0' onmousemove='updatevertcs();' onchange='updatevertcs();'>" +
                          "<input type='text' id='vertLabel' size='6' value='' readonly='true'>";
    document.getElementById('sliders').replaceChild(sliderdiv,document.getElementById('sliders').childNodes[0]);
}
