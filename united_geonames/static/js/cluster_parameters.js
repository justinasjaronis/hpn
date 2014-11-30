var anyclusterSettings = {
    mapType : "google", // "google" or "osm"
    gridSize: 256, //integer
    zoom: 3, //initial zoom
    center: [49,11], //initial center in lng lat
    MapTypeId: "TERRAIN", //google only - choose from  ROADMAP,SATELLITE,HYBRID or TERRAIN
    clusterMethod : "kmeans", //"grid" or "kmeans" or "centroid"
    iconType: "exact", //"exact" (with exact cluster counts) or "simple" (with rounded counts)
    singlePinImages: {
        'imperial':'/static/anycluster/pin_imperial.png', //optional, use in conjunction with django settings: 'ANYCLUSTER_PINCOLUMN'
        'stone':'/static/anycluster/pin_stone.png',
        'wild':'/static/anycluster/pin_wild.png',
        'japanese':'/static/anycluster/pin_japan.png',
        'flower':'/static/anycluster/pin_flower.png'
    },
    onFinalClick : function(entries){
        openPopup(entries);
    }
}


var anyclusterSettings_osm = {
    mapType : "osm", // "google" or "osm"
    gridSize: 256, //integer
    zoom: 3, //initial zoom
    center: [49,11], //initial center in lng lat
    clusterMethod : "kmeans", //"grid" or "kmeans" or "centroid"
    iconType: "simple", //"exact" (with exact cluster counts) or "simple" (with rounded counts)
    singlePinImages: {
        'dbvalue':'/static/path/to/image.png' //optional, use in conjunction with django settings: 'ANYCLUSTER_PINCOLUMN'
    }

}


window.onload = function(){
    // do not use both maps simultaneously as this will confuse the cache
    clustermap = new Anycluster("gmap", anyclusterSettings);
    //var osmap = new Anycluster("osmap", anyclusterSettings_osm);
}


//simple popup script
function openPopup(html){
    var content = document.getElementById('clusterContentPopup');
    content.innerHTML = html;
    document.getElementById('clustererPopup').style.display = "";
}
function closePopup(){
    document.getElementById('clustererPopup').style.display = "none";
}

//example script for getting viewport markers
function loadViewportMarkers(){
    clustermap.getViewportContent(function(html){
        document.getElementById('markerList').innerHTML = html;
    });
}
