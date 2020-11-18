// This is the method called from onload event in body
// This creates the Azure Maps control and connects to a socket to process
// a real-time stream of IoT Hub events
function GetMap(maps_key) {
    // Initialize a map instance using the subscription key passed in
    var map = new atlas.Map('myMap', {
        zoom: 5,
        authOptions: {
            authType: 'subscriptionKey',
            subscriptionKey: maps_key
        }
    });

    // Wait until the map resources are ready.
    map.events.add('ready', function () {
        //Add the zoom control to the map.
        map.controls.add(new atlas.control.ZoomControl(), {
            position: 'top-right'
        });

        // Define 2 data sources - one for points for each GPS coordinate,
        // and one for lines connecting the GPS coordinates in time order
        var point_dataSource = new atlas.source.DataSource();
        var line_dataSource = new atlas.source.DataSource();

        // Add the data sources to the map control
        map.sources.add(point_dataSource);
        map.sources.add(line_dataSource);

        // Add a line layer to the map to show blue lines between GPS coordinates in order.
        // This will show a path travelled over time.
        map.layers.add(new atlas.layer.LineLayer(line_dataSource, null, {
            strokeColor: 'blue',
            strokeWidth: 5
        }));

        // Add a symbol layer to show a pin at each GPS coordinate
        map.layers.add(new atlas.layer.SymbolLayer(point_dataSource, null));

        // Connect to the socket server.
        var socket = io.connect('http://' + document.domain + ':' + location.port + '/get_data');

        // Set up the previous values of the latitude and longitude
        // This allows values to be ignored if the GPS hasn't moved, and 
        // give the last point when constructing a line when a new point arrives
        last_lat = -999
        last_lon = -999

        // This callback method will be called when the server (app.py) returns the GPS data that it got from IoT hub
        socket.on('mapdata', function (msg) {
            // Log the location received
            console.log('GPS location received: ' + msg.data);

            // Decode the data
            var data = JSON.parse(msg.data);

            // Check the location has changed - if not there's no need to add another point to the map
            if (last_lat != data.latitude && last_lon != data.longitude) {
                // Create a symbol with the GPS location that came from the IoT hub
                var point = new atlas.Shape(new atlas.data.Point([data.longitude, data.latitude]));

                // Add the symbol to the data source.
                point_dataSource.add([point]);

                // Point the map to the GPS location
                map.setCamera({ center: [data.longitude, data.latitude] })

                // If we have a previous value, draw a line from it to the new value
                if (last_lat > -999) {
                    // Create the line
                    var line = new atlas.data.LineString([[last_lon, last_lat], [data.longitude, data.latitude]])

                    // Add the line to the data source
                    line_dataSource.add([line])
                }

                // Store the coordinates ready to connect a line when we get the next coordinates
                last_lat = data.latitude
                last_lon = data.longitude
            }
        });
    });
}