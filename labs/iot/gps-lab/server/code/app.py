import os
from flask_socketio import SocketIO, emit
from flask import Flask, render_template
from threading import Thread, Event
from azure.eventhub import TransportType
from azure.eventhub import EventHubConsumerClient
from dotenv import load_dotenv
load_dotenv()

CONNECTION_STR = os.getenv("CONNECTION_STR")
CONSUMER_GROUP_NAME = os.getenv("CONSUMER_GROUP_NAME")

def on_event_batch(partition_context, events):
    for event in events:
        socketio.emit('mapdata', {'data': event.body_as_str()}, namespace='/get_data', broadcast=True)
    partition_context.update_checkpoint()
     
def on_error(partition_context, error):
    # Put your code here. partition_context can be None in the on_error callback.
    if partition_context:
        print("An exception: {} occurred during receiving from Partition: {}.".format(
            partition_context.partition_id,
            error
        ))
    else:
        print("An exception: {} occurred during the load balance process.".format(error))


#New Code
app = Flask(__name__)
app.config['SECRET_KEY'] = os.urandom(24)
socketio = SocketIO(app, async_mode='threading')
thread = Thread()
thread_stop_event = Event()

def index():    
    client = EventHubConsumerClient.from_connection_string(
        conn_str=CONNECTION_STR,
        consumer_group=CONSUMER_GROUP_NAME
    )
    try:
        with client:
           client.receive_batch(on_event_batch=on_event_batch, on_error=on_error)
    except KeyboardInterrupt:
        print("Receiving has stopped.")


@app.route('/')
def root():
    return render_template('index.html')

@socketio.on('connect', namespace='/get_data')
def test_connect():
    # need visibility of the global thread object
    global thread
    print('Client connected')

    if not thread.is_alive():
        thread = socketio.start_background_task(index)

@socketio.on('disconnect', namespace='/get_data')
def test_disconnect():
    print('Client disconnected')

def main():
    socketio.run(app);

if __name__ == '__main__':
    main()