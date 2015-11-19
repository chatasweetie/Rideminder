
// default setting for my routes
var bound = "I";
var line = "1";
var locations = [];

    function init(){
        var mapDiv = document.getElementById("transitmap");
        var mapOptions= {
            center: new google.maps.LatLng(37.7846810, -122.4073680),
            zoom: 15,
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
            $("#stops").empty()
            $(xml).find("direction[tag*="+bound+"]>stop").each(function(){                
                var tag = $(this).attr("tag");
                var stopName =$(xml).find("route>stop[tag*="+tag+"]").attr("title");
                var stopLAT = $(xml).find("route>stop[tag*="+tag+"]").attr("lat");
                var stopLON = $(xml).find("route>stop[tag*="+tag+"]").attr("lon");
                var geolocation = stopLAT+","+stopLON;
                $("#stops").append("<option id=\""+stopName+"\" value=\""+geolocation+"\">"+stopName+"</option>");
                locations.push({name: stopName, lat: stopLAT, lng: stopLON});
                console.log(locations.lat);
            });
            console.log(locations);
            for (var i=0;i<locations.length;i++){

                console.log(locations[i].lat);
                var lat = parseFloat(locations[i].lat);
                var lng = parseFloat(locations[i].lng);
                console.log(lat);
                var myLatLng = {lat, lng};
                console.log(myLatLng);
                var marker = new google.maps.Marker({
                    position: myLatLng,
                    map: map, 
                    title:locations[i].name});
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
    console.log(bound)
   $(function(){
    $.ajax({
        type:"GET",
        url: "http://webservices.nextbus.com/service/publicXMLFeed?command=routeConfig&a=sf-muni&r="+line+"",
        dataType:"xml",
        success: function(xml) {
            console.log("success", xml);
            var optionsHtml = "";
            $("#stops").empty()
            $(xml).find("direction[tag*="+bound+"]>stop").each(function(){               
                var tag = $(this).attr("tag");
                var stopName =$(xml).find("route>stop[tag*="+tag+"]").attr("title");
                var stopLAT = $(xml).find("route>stop[tag*="+tag+"]").attr("lat");
                var stopLON = $(xml).find("route>stop[tag*="+tag+"]").attr("lon");
                var geolocation = stopLAT+","+stopLON;
                $("#stops").append("<option id=\""+stopName+"\" value=\""+geolocation+"\">"+stopName+"</option>");
            });
        }
    });
});
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