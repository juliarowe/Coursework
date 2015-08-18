//VARIABLES
//my location variables
var myLat = 35.99159;
var myLng = -78.90402;
var myLogin = "KeithHauenstein";
var myIcon = "brontosaurus.png"
var me = new google.maps.LatLng(myLat, myLng);

//map variables
var map;
var marker;
var mapOptions = {
			zoom: 13,
			center: me,
		};
var infowindow = new google.maps.InfoWindow();

//other variables
var request = new XMLHttpRequest();
var R = 3959; //radius earth in miles
var students;

function construct() 
{
	map = new google.maps.Map(document.getElementById('map-canvas'), mapOptions);
	getMyLocation();
}

//Get initial location and request data from server
function getMyLocation() 
{
	if (navigator.geolocation) { 
		navigator.geolocation.getCurrentPosition(function(position) {
			myLat = position.coords.latitude;
			myLng = position.coords.longitude;

			//see mmap_server for implementation of server (currently offline)
			request.open("post", "https://floating-fortress-7965.herokuapp.com/sendLocation", true);
			request.setRequestHeader("Content-type", "application/x-www-form-urlencoded");
			request.send("login=" + myLogin + "&lat=" + myLat + "&lng=" + myLng);
			
			//on succesful receipt of student info
			request.onreadystatechange=function() 
			{
				if (request.readyState==4 && request.status==200) {
					students=JSON.parse(request.responseText);
					for (i = 1; i < students.length; i++) { 
						createMarker(students[i]);
					}
				}
			}
			renderMap();
		});
	}
	else {
		alert("Geolocation is not supported by your web browser.");
	}
}

//Render the map
function renderMap() 
{
	me = new google.maps.LatLng(myLat, myLng);
	map.panTo(me);
	marker = new google.maps.Marker({
		position: me,
		title: myLogin,
		icon: myIcon
	});
	marker.setMap(map);

	google.maps.event.addListener(marker, 'click', function() 
	{
		infowindow.setContent(marker.title);
		infowindow.open(map, marker);
	});
}

//Create a marker for the given object
function createMarker(student)
{
	var marker = new google.maps.Marker({
		map: map,
		position: new google.maps.LatLng(student.lat, student.lng),
		title: student.login
	});
	marker.setMap(map);	

	//add listener to show distance on click	
	google.maps.event.addListener(marker, 'click', function() 
	{
		infowindow.close(); //close any open info windows
		infowindow.setContent(student.login + "<br\>" + getDistance(me, marker.position))
		infowindow.open(map, this);
	});
}

//Calculate distance between two locations
function getDistance(loc1, loc2) 
{
	var phi1 = toRadians(loc1.lat());
	var phi2 = toRadians(loc2.lat());
	var dPhi = phi2 - phi1;
	var dLambda = toRadians(loc2.lng()-loc1.lng());

	var a = Math.sin(dPhi / 2) * Math.sin(dPhi / 2) +
			Math.cos(phi1) * Math.cos(phi2) *
			Math.sin(dLambda / 2) * Math.sin(dLambda / 2);
	var c = 2 * Math.atan2(Math.sqrt(a), Math.sqrt(1-a));
	var d = R * c;

	return d.Round(4);
}

//Convert angle to radians
function toRadians(angle) {
	return angle * Math.PI / 180;
}

//Round number to desired number of digits
Number.prototype.Round = function(digits) {
	var re = new RegExp("(\\d+\\.\\d{" + digits + "})(\\d)"),
	m = this.toString().match(re);
	return m ? parseFloat(m[1]) : this.valueOf();
};

//Constructor
google.maps.event.addDomListener(window, 'load', construct);