
// default setting for my routes
var bound = "I";
var line = "1";
var locations = [];
var markers= [];

function clearMapMarkers() {
  for (var i = 0; i < markers.length; i++) {
    markers[i].setMap(null);
  }
}




function init(){
    var mapDiv = document.getElementById("transitmap");
    var mapOptions= {
        center: new google.maps.LatLng(37.7846810, -122.4073680),
        zoom: 13,
        mapTypeId: google.maps.MapTypeId.ROADMAP
    };
    var map = new google.maps.Map(mapDiv, mapOptions);


// Takes in the line/route and returns the stop title/name, lat & lon
$("#line").bind("change lines", function() { 
   line = ($(this).val()); 
   $(function(){
    $.ajax({
        type:"GET",
        url: "http://webservices.nextbus.com/service/publicXMLFeed?command=routeConfig&a=sf-muni&r="+line+"",
        dataType:"xml",
        success: function(xml) {
            console.log("success", xml);
            var optionsHtml = "";
            $("#stops").empty();
            clearMapMarkers();
            $(xml).find("direction[tag*="+bound+"]>stop").each(function(){                
                var tag = $(this).attr("tag");
                var stopName =$(xml).find("route>stop[tag*="+tag+"]").attr("title");
                var stopLAT = $(xml).find("route>stop[tag*="+tag+"]").attr("lat");
                var stopLON = $(xml).find("route>stop[tag*="+tag+"]").attr("lon");
                var geolocation = stopLAT+","+stopLON;
                $("#stops").append("<option id=\""+stopName+"\" value=\""+geolocation+"\">"+stopName+"</option>");
                locations.push({name: stopName, lat: stopLAT, lng: stopLON});
            });

            for (var i=0;i<locations.length;i++){
                var lat = parseFloat(locations[i].lat);
                var lng = parseFloat(locations[i].lng);
                var myLatLng = {lat, lng};
                var marker = new google.maps.Marker({
                    position: myLatLng,
                    map: map, 
                    title:locations[i].name,
                    clickable: true}
                );
                    markers.push(marker);
            }
            locations = [];
        }
    });
});
});

// Takes in the bound/direction and returns the stop title/name, lat & lon
$("#bound").bind("change paste keyup", function() {
    bound = ($(this).val()); 
    if (bound == "Outbound"){
        bound = "O";
    }else {
        bound = "I";
    }
   $(function(){
    $.ajax({
        type:"GET",
        url: "http://webservices.nextbus.com/service/publicXMLFeed?command=routeConfig&a=sf-muni&r="+line+"",
        dataType:"xml",
        success: function(xml) {
            console.log("success", xml);
            var optionsHtml = "";
            $("#stops").empty()
            clearMapMarkers();
            $(xml).find("direction[tag*="+bound+"]>stop").each(function(){               
                var tag = $(this).attr("tag");
                var stopName =$(xml).find("route>stop[tag*="+tag+"]").attr("title");
                var stopLAT = $(xml).find("route>stop[tag*="+tag+"]").attr("lat");
                var stopLON = $(xml).find("route>stop[tag*="+tag+"]").attr("lon");
                var geolocation = stopLAT+","+stopLON;
                $("#stops").append("<option id=\""+stopName+"\" value=\""+geolocation+"\">"+stopName+"</option>");
                locations.push({name: stopName, lat: stopLAT, lng: stopLON});
            });
            for (var i=0;i<locations.length;i++){
                var lat = parseFloat(locations[i].lat);
                var lng = parseFloat(locations[i].lng);
                var myLatLng = {lat, lng};
                var marker = new google.maps.Marker({
                    position: myLatLng,
                    map: map, 
                    title:locations[i].name});
                    markers.push(marker);
            }
            locations = [];
        }
    });
});
});




}

function addInfoWindow(marker, message) {

    var infoWindow = new google.maps.InfoWindow({
        content: message
    });

    google.maps.event.addListener(marker, 'click', function () {
        infoWindow.open(map, marker);
    });
}

    window.onload = init;




// ask for geolocation of user when they come to my site
// navigator.geolocation.getCurrentPosition(GetLocation);
// function GetLocation(location) {
//     alert(location.coords.latitude);
//     alert(location.coords.longitude);
//     alert(location.coords.accuracy);
// }