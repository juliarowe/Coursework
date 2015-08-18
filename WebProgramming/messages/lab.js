//gets the data
function parse() 
{
	var request = new XMLHttpRequest();

	request.open("GET", "data.json", true);
	request.setRequestHeader("Content-type", "https://secret-about-box.herokuapp.com/sendLocation");
	request.onreadystatechange = parseData(request);
}

//parses the data and adds it to the DOM
function parseData(request) 
{
	if (request.readyState==4 && request.status==200) {
		var msgs = JSON.parse(request.responseText);
		var insertInto = document.getElementById("messages");
		var content = '';

		for (var i in msgs) {
			content += '<p>' + msgs[i].content + ' - ' + msgs[i].username + '</p>';
		}
		
		insertInto.innerHTML += content;
	}
}