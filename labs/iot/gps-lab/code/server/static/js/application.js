var map, datasource;

var mapSubscriptionKey = '<Azure_Maps_Subscription_Key>';

// This is the method called from onload event in body
function GetMap()
{
    //Initialize a map instance.
    map = new atlas.Map('myMap', {
        center: [-122.64, 47.58], // Default position for the map.
        zoom: 4,
        view: "Auto",
        style: "satellite",
        authOptions: {
            authType: 'subscriptionKey',
            subscriptionKey: mapSubscriptionKey
        }
    });

    //Wait until the map resources are ready.
    map.events.add('ready', function ()
    {
        //Add the zoom control to the map.
        map.controls.add(new atlas.control.ZoomControl(), {
            position: 'top-right'
        });
        
    console.log("Socket Started -- ");

    // Connect to the socket server.
    var socket = io.connect('http://' + document.domain + ':' + location.port + '/get_data');

    // This callback method will be called when the server (app.py) returns the GPS data that it got from IoT hub
    socket.on('mapdata', function (msg)
    {
        console.log("Received GPS data");

        var data = JSON.parse(msg.data);

        // Set an empty data source and add it to the map
        var dataSource = new atlas.source.DataSource();
        map.sources.add(dataSource);
        console.log([data.longitude, data.latitude]);

        // Create a symbol with the GPS location that came from the IoT hub
        var point = new atlas.Shape(new atlas.data.Point([++data.longitude, ++data.latitude]));

        //Add the symbol to the data source.
        dataSource.add([point]);

        // Add the symbol as a layer in the Map. This will display the GPS point with a pin in the Map
        map.layers.add(new atlas.layer.SymbolLayer(dataSource, null));
    });
    });
}