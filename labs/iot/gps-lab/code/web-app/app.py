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
