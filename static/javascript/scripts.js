"use strict";

// a nice loading image for when user submits form
function showLoading(evt) {
  evt.preventDefault();
  $("#loadinggif").show();
  $(this).unbind('submit').submit();
}
$("#request").submit(showLoading);

var bound = "I";
var line = "1";
var locations = [];
var markers= [];

$(document).ready(function() {
    console.log( "ready!" );
    $("#agency").change(function(){
        $.get('/agency.json', { "agency": $(this).val()},
            function (routes) {
                $('#stop-options').append('<option value= None>SELECT STOP</option>');
                $('#route-options').empty();
                $('#route-options').append('<option value= None>SELECT ROUTE</option>');
                var route;

                for (var key in routes){
                    route = routes[key];

                    $('#route-options').append('<option value=' + route.route_id + '>' + route.name + '</option>');
                }
                console.log($("#route-options").val());
                $('#stop-options').append('<option value= None>SELECT STOP</option>');
            });
    });
});

$(document).ready(function() {
    $("#route-options").change(function(){
        console.log($(this).val());
        $.get('/route.json', { "route_id": $(this).val()},
            function (stops) {
                console.log(stops);
                $('#stop-options').empty();
                $('#stop-options').append('<option value= None>SELECT STOP</option>');
                    var stop;

                    for (var key in stops){
                        stop = stops[key];

                    $('#stop-options').append('<option value=' + stop.stop_code + ' data-lat= ' + stop.lat +' data-lon= ' + stop.lon + '>' + stop.name + '</option>');
                }
            });
    });
});

// function clearMapMarkers() {
//   for (var i = 0; i < markers.length; i++) {
//     markers[i].setMap(null);
//   }
// }


// var user_geolocation = (37.7846810, -122.4073680);


// function init(){
//     var mapDiv = document.getElementById("transitmap");
//     var mapOptions= {
//         center: new google.maps.LatLng(37.7846810, -122.4073680),
//         zoom: 14,
//         mapTypeId: google.maps.MapTypeId.ROADMAP
//     };
//     var map = new google.maps.Map(mapDiv, mapOptions);

//     var infoWindow = new google.maps.InfoWindow({map: map});



// // Takes in the bound/direction and returns the stop title/name, lat & lon
// $("#bound").bind("change paste keyup", function() {
//     bound = ($(this).val());
//    $(function(){
//     $.ajax({
//         type:"GET",
//         url: "http://webservices.nextbus.com/service/publicXMLFeed?command=routeConfig&a=sf-muni&r="+line+"",
//         dataType:"xml",
//         success: function(xml) {
//             console.log("success", xml);
//             var optionsHtml = "";
//             $("#stops").empty();
//             clearMapMarkers();
//             $(xml).find("direction[tag*="+bound+"]>stop").each(function(){
//                 var tag = $(this).attr("tag");
//                 var stopName =$(xml).find("route>stop[tag*="+tag+"]").attr("title");
//                 var stopLAT = $(xml).find("route>stop[tag*="+tag+"]").attr("lat");
//                 var stopLON = $(xml).find("route>stop[tag*="+tag+"]").attr("lon");
//                 var geolocation = stopLAT+","+stopLON;
//                 $("#stops").append("<option id=\""+stopName+"\" value=\""+geolocation+"\">"+stopName+"</option>");
//                 locations.push({name: stopName, lat: stopLAT, lng: stopLON});
//             });
//             for (var i=0;i<locations.length;i++){
//                 var lat = parseFloat(locations[i].lat);
//                 var lng = parseFloat(locations[i].lng);
//                 var myLatLng = {lat, lng};
//                 var marker = new google.maps.Marker({
//                     position: myLatLng,
//                     map: map,
//                     title:locations[i].name});
//                     markers.push(marker);
//             }
//             locations = [];
//         }
//     });
// });
// });



// if (navigator.geolocation) {
//     navigator.geolocation.getCurrentPosition(function(position) {
//       var pos = {
//         lat: position.coords.latitude,
//         lng: position.coords.longitude,
//       };
//       $("#lat").append("<option id=\"lat\" value=\""+pos.lat+"\">"+pos.lat+"</option>");
//       $("#lng").append("<option id=\"lng\" value=\""+pos.lng+"\">"+pos.lng+"</option>");
//       infoWindow.setPosition(pos);
//       infoWindow.setContent('You are here');
//       map.setCenter(pos);
//     }, function() {
//       handleLocationError(true, infoWindow, map.getCenter());
//     });
//   } else {
//     // Browser doesn't support Geolocation
//     handleLocationError(false, infoWindow, map.getCenter());
//   }
// }

// function handleLocationError(browserHasGeolocation, infoWindow, pos) {
//   infoWindow.setPosition(pos);
//   infoWindow.setContent(browserHasGeolocation ?
//                         'Error: The Geolocation service failed.' :
//                         'Error: Your browser doesn\'t support geolocation.');
// }



// function addInfoWindow(marker, message) {

//     var infoWindow = new google.maps.InfoWindow({
//         content: message
//     });

//     google.maps.event.addListener(marker, 'click', function () {
//         infoWindow.close();
//         infoWindow.open(map, marker);
//     });
// }

//     window.onload = init;
