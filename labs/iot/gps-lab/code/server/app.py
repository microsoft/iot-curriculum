import os
from flask import Flask, render_template
from flask_socketio import SocketIO, emit
from threading import Thread, Event
from azure.eventhub import TransportType
from azure.eventhub import EventHubConsumerClient
from dotenv import load_dotenv
load_dotenv()

# Get the connection sting and consumer group name of the IoT hub from .env file
CONNECTION_STR = os.getenv("CONNECTION_STR")
CONSUMER_GROUP_NAME = os.getenv("CONSUMER_GROUP_NAME")

# When message received from IoT hub, broadcast it to all clients that are listening through socket
def on_event_batch(partition_context, events):
    for event in events:
        socketio.emit('mapdata', {'data': event.body_as_str()}, namespace='/get_data', broadcast=True)
    partition_context.update_checkpoint()

# Error handling and display error message while trying to receive message from IoT hub
def on_error(partition_context, error):
    if partition_context:
        print("An exception: {} occurred during receiving from Partition: {}.".format(
            partition_context.partition_id,
            error
        ))
    else:
        print("An exception: {} occurred during the load balance process.".format(error))


# Create the website with Flask
app = Flask(__name__)
# Below 'SECRET_KEY' helps to keep the client side sessions secure.
# We are generating a random 24 digit Hex Key.
app.config['SECRET_KEY'] = os.urandom(24)
socketio = SocketIO(app, async_mode='threading')
thread = Thread()
thread_stop_event = Event()

def index():    
    # Create the event hub client to receive messages from IoT hub
    client = EventHubConsumerClient.from_connection_string(
        conn_str=CONNECTION_STR,
        consumer_group=CONSUMER_GROUP_NAME
    )
    try:
        with client:
           client.receive_batch(on_event_batch=on_event_batch, on_error=on_error)
    except KeyboardInterrupt:
        print("Receiving has stopped.")


# Default page when http://localhost:5000 is opened.
@app.route('/')
def root():
    return render_template('index.html')

# Start the socket and connect any client calling get_data. This is called from application.js
@socketio.on('connect', namespace='/get_data')
def test_connect():
    # need visibility of the global thread object
    global thread
    print('Client connected')

    if not thread.is_alive():
        thread = socketio.start_background_task(index)

# Disconnect the client
@socketio.on('disconnect', namespace='/get_data')
def test_disconnect():
    print('Client disconnected')

def main():
    socketio.run(app);

if __name__ == '__main__':
    main()