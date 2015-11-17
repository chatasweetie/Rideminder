
// finds all the stop ids for N route that is going Inbound
// http://webservices.nextbus.com/service/publicXMLFeed?command=routeConfig&a=sf-muni&r=1

var bound = "I";
var line = "1";

// Takes in the line/route and returns the stop title/name, lat & lon
$("#line").bind("change paste keyup", function() {
   line = ($(this).val()); 
   $(function(){
    $.ajax({
        type:"GET",
        url: "http://webservices.nextbus.com/service/publicXMLFeed?command=routeConfig&a=sf-muni&r="+line+"",
        dataType:"xml",
        success: function(xml) {
            console.log("success", xml);
            var optionsHtml = "";
            $(xml).find("direction[tag*="+bound+"]>stop").each(function(){                
                var tag = $(this).attr("tag");
                var stopName =$(xml).find("route>stop[tag*="+tag+"]").attr("title");
                var stopLAT = $(xml).find("route>stop[tag*="+tag+"]").attr("lat");
                var stopLON = $(xml).find("route>stop[tag*="+tag+"]").attr("lon");
                console.log(stopName);
                console.log(stopLAT);
                console.log(stopLON);
            $("#stops").text(stopname);
                
            });
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
            $(xml).find("direction[tag*="+bound+"]>stop").each(function(){               
                var tag = $(this).attr("tag");
                var stopname =$(xml).find("route>stop[tag*="+tag+"]").attr("title");
                var stopName =$(xml).find("route>stop[tag*="+tag+"]").attr("title");
                var stopLAT = $(xml).find("route>stop[tag*="+tag+"]").attr("lat");
                var stopLON = $(xml).find("route>stop[tag*="+tag+"]").attr("lon");
                console.log(stopName);
                console.log(stopLAT);
                console.log(stopLON);
            });
        }
    });
});
});




// click event in JavaScript using JQuery
// $('stop').on('click', alertMe);



// ask for geolocation of user when they come to my site
// navigator.geolocation.getCurrentPosition(GetLocation);
// function GetLocation(location) {
//     alert(location.coords.latitude);
//     alert(location.coords.longitude);
//     alert(location.coords.accuracy);
// }