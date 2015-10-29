<script src="https://cdn.firebase.com/js/client/2.3.1/firebase.js"></script>

// var myFirebaseRef = new Firebase("https://publicdata-transit.firebaseio.com/");
	
// firebaseRef.on('child_changed', function(childSnapshot, prevChildKey) {
//   // code to handle child data changes.
// });


var transitLine = 'X';
var transitRef = new Firebase('https://publicdata-transit.firebaseio.com/sf_muni');
var lineIndex = transitRef.child('index').child(transitLine);
lineIndex.on('child_added', function(snapshot) {
    var id = snapshot.key();
    transitRef.child('data').child(id).on('value', busUpdated);
});
lineIndex.on('child_removed', function(snapshot) {
    var id = snapshot.key();
    transitRef.child('data').child(id).off('value', busUpdated);
});
function busUpdated(snapshot) {
    // Bus line 'X' changed location.
    var info = snapshot.val();
    // Retrieve latitude/longitude with info.lat/info.lon.
