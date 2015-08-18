// Initialization
var express = require('express');
var bodyParser = require('body-parser');
var validator = require('validator'); 
var app = express();

app.use(bodyParser.json());
app.use(bodyParser.urlencoded({ extended: true }));

// Mongo initialization and connect to database
var mongoUri = process.env.MONGOLAB_URI || process.env.MONGOHQ_URL || 'mongodb://localhost/mmapdatabase';
var MongoClient = require('mongodb').MongoClient, format = require('util').format;
var db = MongoClient.connect(mongoUri, function(error, databaseConnection) {
    db = databaseConnection;
});

app.use(function(req, res, next) {
    res.header('Access-Control-Allow-Origin', '*');
    res.header('Access-Control-Allow-Header', 'Origin, X-Requested-Width, Content-Type, Accept');
    next();
});


//Post data to the locations collection in the database
app.post('/sendLocation', function(request, response) {
    //read info from client
    var theLogin = request.body.login; 
    var theLat = request.body.lat;
    var theLng = request.body.lng;

    //validate information
    if (theLogin == undefined || theLat == undefined || theLng == undefined) {
        response.send('{"error":"Whoops, something is wrong with your data!"}');
    }
    else {
        //insert data into collection
        db.collection('locations', function(error, coll) {
            var toInsert = {
                login:theLogin,
                lat:parseFloat(theLat), //convert string to float
                lng:parseFloat(theLng), //ditto
                created_at:new Date()
            };
            //prevent repeats
            coll.update({"login":theLogin}, toInsert, {upsert:true}, function(error, result) {
                if (!error) {
                    coll.find().toArray(function(error, results) {
                        if (!error) 
                            response.send(results);
                    });
                }
            });
        });
    }
});

//get and display locations from the database
app.get('/', function(request, response) {
    var output = "";
    output += "<!DOCTYPE HTML><html><head><title>mmap server</title></head><body><h1>Check ins:</h1><ul>";
    response.set('Content-Type', 'text/html');
    locationDB = db.collection('locations');
    
    //get and sort locations from DB
    locationDB.find().sort({created_at:-1}).toArray(function(error, data) {
        data.forEach(function(elem) {
            output += '<p>' + elem.login + ' checked in at ' + elem.lat + ', ' + elem.lng
                      + ' on ' + elem.created_at + '</p>';
        })
        response.send(output);
    });
});


//get specific login's location
app.get('/location.json', function(request, response) {
    var entry = request.query.login;
    if (entry == null || entry == undefined) {
        response.send('{}');
    } else {
        db.collection('locations', function(error, coll) {
            //find instance in database
            coll.findOne({login:entry}, function(error, result) {
                if (result) {
                    response.send(result);
                } else {
                    response.send('{}');
                }
            });
        });
    }
});

app.listen(process.env.PORT || 3000);

