# Code a web app to visualize the GPS location on a map

In the [previous step](./write-pi-code.md) you wrote write code to gather GPS data and send it to your IoT Hub.

In this step you will write a web application to visualize the GPS location on Azure Maps.

## Set up your development environment

### Set up VS Code

1. Launch Visual Studio Code - you can develope the web app on your Raspberry Pi if you are running VS Code there, otherwise run it on your PC or Mac.

1. If you are running VS Code locally, ensure you have the PyLance extension installed as described in the previous step.

1. Create a folder called `GpsLab-WebApp` and open it in VS Code.

1. Inside this folder, create a Python file called `app.py`. By creating this file, the Python extension will be activated.

### Create a virtual environment

1. Create a Python virtual environment in the `GpsLab-WebApp` folder as described in the previous step. Remember to reload the terminal so that it activates the virtual environment.

1. Create a new file in the `GpsLab-WebApp` folder called `requirements.txt` to list the required pip packages.

1. Add the following to this file. You can also find this code in the [requirements.txt](../code/web-app/requirements.txt) file in the [code/web-app](../code/web-app) folder.

    ```sh
    flask
    flask_socketio
    azure.eventhub
    python-dotenv
    ```

    * `flask` is the Pip package for creating web apps using the [Flask framework](https://flask.palletsprojects.com)
    * `flask_socketio` is a Pip package that provides [Socket.io](https://socket.io) connectivity to Flask apps allowing the web app to talk to the Flask server code over a web socket to get live updates
    * `azure.eventhub` is a Pip package that talks the Event Hub compatible endpoint on an IoT Hub
    * `python-dotenv` is a Pip package that provides the ability to load secrets such as connection strings from an file

1. Install these packages by running the following command in the terminal:

    ```sh
    pip install -r requirements.txt
    ```

### Create the environment file

The web app needs a number of secret keys to talk to the Azure services - it needs the Azure Maps key to render a map, and the connection string for the Event Hub compatible end point on the IoT hub to pull messages off the hub. Just like with the GPS app on the Raspberry Pi, these keys can be read from a `.env` file.

1. Create a file in the `GpsLab-WebApp` folder called `.env`

1. Add the following to this file:

    ```sh
    MAPS_KEY=<Your maps key>
    CONNECTION_STRING=<Your Event Hub compatible endpoint connection string>
    ```

    Replace `<Your maps key>` with the Azure Maps key you obtained in an earlier step.

    Replace `<Your Event Hub compatible endpoint connection string>` with the Event Hub compatible endpoint you obtained in an earlier step

### Create the web app

The web app is a Python Flask app. Flask runs Python on the server side to manage all the web site application logic and serve up web pages, images, JavaScript and CSS files. In this app, the Python code connects to Azure IoT Hub to listen to messages, then sends these to JavaScript running in the browser using a technology called [Socket.io](https://socket.io), which allows real-time messaging between a web page and the web server.

Web pages are served up by the Flask app, using templates that contain the HTML for the page, along with tags that are replaced with code from the Flask app when the page is served, allowing dynamic content.

You can find all the code for this web app in the [code/web-app](../code/web-app) folder.

#### Create the HTML page

This web app has a single HTML page to show a map and plot GPS coordinates received from the IoT Hub.

c1. Create a folder in the `GpsLab-WebApp` folder called `templates`. This is where Flask expects to load HTML templates from.

1. Add a new file to this folder called `index.html`

1. Add the following code to this file:

    ```html
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <title>GPS Lab</title>

        <meta charset="utf-8" />
        <meta http-equiv="x-ua-compatible" content="IE=Edge" />

        <!-- Add references to the Azure Maps Map control JavaScript and CSS files. -->
        <link rel="stylesheet" href="https://atlas.microsoft.com/sdk/javascript/mapcontrol/2/atlas.min.css" type="text/css" />
        <script src="https://atlas.microsoft.com/sdk/javascript/mapcontrol/2/atlas.min.js"></script>

        <!-- Add a reference to the Azure Maps Services Module JavaScript file. -->
        <script src="https://atlas.microsoft.com/sdk/javascript/service/2/atlas-service.min.js"></script>

        <!-- Add a reference to the Socket.io JavaScript file -->
        <script type="text/javascript" src="https://cdn.jsdelivr.net/npm/socket.io-client@2/dist/socket.io.js"></script>

        <!-- Add a reference to the GPS Lab maps app JavaScript file -->
        <script src="static/js/application.js" type="text/javascript" charset="utf-8"></script>

        <style>
            html,
            body {
                margin: 0;
            }
            #myMap {
                height: 100vh;
                width: 100vw;
            }
        </style>
    </head>

    <!-- When the body loads, run code to create the map using a kay passed from the Flask app -->
    <body onload="GetMap('{{ data.maps_key }}')">
        <!-- This div is passed to the map control to be converted into a map -->
        <div id="myMap"></div>
    </body>

    </html>
    ```

    This HTML code loads the JavaScript libraries for Azure Maps, Socket.io, and code that will be written later to update the map. The HTML body contains a single `div` with an id of `myMap`, and this will be used to attache the Azure Maps control to in JavaScript using the `GetMap` function that is called when the body loads.

    The value passed to the `GetMap` function is `{{ data.maps_key }}`. This double curly brace syntax is special Flask syntax for text that will be replaced. This is an HTML template - with areas that get replaced by data coming in from the Flask app. The HTML template will be rendered with a value called `data` which will have a property on it called `maps_key`, and the `{{ data.maps_key }}` value will be replaced with the value of `maps_key`.

#### Create the application javascript code

JavaScript is served up by Flask apps from a static files folder.

1. Create a folder in the `GpsLab-WebApp` folder called `static`

1. Inside the `static` folder, create a sub folder called `js`

1. Inside the `js` folder, create a file called `application.js`

1. Add the following code to this file:

    ```js
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
    ```

    This code defines a function, `GetMap`, that is called when the HTML body loads. It is passed the Azure Maps subscription key. Read the code and the comments to get a full understanding of what each line of code does.

    This function creates the Map control, adding an event that is fired when the map is ready. This event shows the map zoom control, then sets up 2 layers - a point layer and a line layer. These layers are backed by a data source, and render the data from the data source. The point layer has a point data source containing GPS points as latitude and longitude, and renders these points as pins on the map. The line layer has a line data source containing a set of lines made up of two sets of coordinates - a start point and an end point. This line layer draws lines between the start and end coordinates.

    Finally, this function sets up a socket.io handler which is called every time data with GPS coordinates is sent from the server. This will add these coordinates to the point data source to render them as a pin, and add a line from the previous set of coordinates to the current set to the line data source.

#### Create the server side code

Finally the server side code needs to be added to run the web application.

1. Open the `app.py` file from the `GpsLab-WebApp` folder

1. Add the following code to this file:

    ```python
    import os
    from flask import Flask, render_template
    from azure.eventhub import EventHubConsumerClient
    from flask_socketio import SocketIO
    from threading import Thread

    # Load the environment variables
    maps_key = os.environ["MAPS_KEY"]
    connection_string = os.environ["CONNECTION_STRING"]
    consumer_group_name = "$Default"

    # Create the website with Flask
    app = Flask(__name__)

    # Create a secret key to keep the client side socket.io sessions secure.
    # We are generating a random 24 digit Hex Key.
    app.config["SECRET_KEY"] = os.urandom(24)

    # Create the socket.io app
    socketio = SocketIO(app, async_mode="threading")
    thread = Thread()

    # When a message is received from IoT hub, broadcast it to all clients that are listening through socket
    def on_event_batch(partition_context, events):
        # Loop through all the events on the event hub - each event is a message from IoT Hub
        for event in events:
            # Send the event over the socket
            socketio.emit("mapdata", {"data": event.body_as_str()}, namespace="/get_data", broadcast=True)

        # Update the event hub checkpoint so we don't get the same messages again if we reconnect
        partition_context.update_checkpoint()

    # A background method that is triggered by socket.io. This method connects to the Event Hub compatible endpoint
    # on the IoT Hub and listens for messages
    def event_hub_task():
        # Create the event hub client to receive messages from IoT hub
        client = EventHubConsumerClient.from_connection_string(
            conn_str=connection_string,
            consumer_group=consumer_group_name
        )

        # Set up the batch receiving of messages
        with client:
            client.receive_batch(on_event_batch=on_event_batch)

    # This method is called when a request comes in for the root page
    @app.route("/")
    def root():
        # Create data for the home page to pass the maps key
        data = { "maps_key" : maps_key }

        # Return the rendered HTML page
        return render_template("index.html", data = data)

    # This is called when the socket on the web page connects to the socket.
    # This starts a background thread that listens on the event hub
    @socketio.on("connect", namespace="/get_data")
    def socketio_connect():
        global thread
        print("Client connected")

        # If the thread is not already running, start it as a socket.io background task to
        # listen on messages from IoT Hub
        if not thread.is_alive():
            thread = socketio.start_background_task(event_hub_task)

    # The main method - if this app is run via the command line, it starts the socket.io app.
    def main():
        socketio.run(app)

    if __name__ == "__main__":
        main()
    ```

    This code implements the server side web app code. Read the code and comments to get a complete understanding of each line.

    Flask web apps have functions marked with routes - a web location that triggers the code in the function. In this case, only one route is defined - `@app.route("/")`. This function is called when the root of the web app is loaded, and returns the HTML page rendered using a data object that passes a `maps_key` parameter. This is the API key for the Azure Maps account and ends up being passed into the map creation via the HTML and JavaScript code.

    The function decorated with `@socketio.on("connect", namespace="/get_data")` is called by socket.io when the app connects, and sets up a background task to connect to the Event Hub compatible end point and listen for messages from the IoT Hub. These messages are then handled in the `on_event_batch` method where they are sent to the front end via the socket.io connection.

## Test the web app

Once the code is written, it needs to be tested.

1. Ensure the Raspberry Pi app is running and sending GPS coordinates.

1. Run the following command in the VS Code terminal to run the web app:

    ```sh
    python -m flask run
    ```

1. The app will launch, running on the local machine on port 5000

    ```output
    (.venv) ➜  GpsLab-WebApp python -m flask run
     * Environment: production
       WARNING: This is a development server. Do not use it in a production deployment.
       Use a production WSGI server instead.
     * Debug mode: off
     * Running on http://127.0.0.1:5000/ (Press CTRL+C to quit)
    ```

1. Open [http://127.0.0.1:5000/](http://127.0.0.1:5000/) in your web browser. You will see the map appear, and pins will appear for the GPS coordinates, with the map focusing on the pins as they appear.

1. To test the GPS further, connect the Pi to a portable power source, run the Python app, then travel with the Pi to see the GPS coordinates change. If you are travelling outside of WiFi range, you may need to tether the Pi to a mobile phone.

## Deploy the web app to the cloud

Rather than run this web app locally all the time, you can deploy it to [Azure App Service](https://azure.microsoft.com/services/app-service/?WT.mc_id=academic-7372-jabenn). Azure App Service allows you to quickly deploy and scale web apps in the cloud.

You can find a tutorial with all the steps to deploy this web app with Visual Studio Code in the [Deploy Python apps to Azure App Service on Linux from Visual Studio Code tutorial on Microsoft docs](https://docs.microsoft.com/azure/developer/python/tutorial-deploy-app-service-on-linux-01?WT.mc_id=academic-7372-jabenn). Follow the steps in this tutorial to deploy your web app to the cloud.

## Next steps

In this step you wrote a web application to visualize the GPS location on Azure Maps.

In the [next step](./clean-up.md) you will clean up your resources.
