import json
import random
import re
import sys
import threading
import time

from azure.iot.device import IoTHubDeviceClient, Message

AUX_CONNECTION_STRING = sys.argv[1]

AUX_BASE_HEART_RATE = 65
AUX_BASE_BODY_TEMPERATURE = 37.0
AUX_MAXIMUM_BODY_TEMPERATURE = 40.0

#SENSOR DATA WILL HOST SENSOR METRICS
sensor_data = {}

#MESSAGE FOR RECEIVING DATA FROM IoT HUB. THIS METHOD WILL BE CALLED BY THE RECEPTION THREAD
def message_listener(client):
    while True:
        message = client.receive_message()
        print("Message received")
        print( "    Data: {}".format(message.data.decode("utf-8") ) )
        print( "    Properties: {}".format(message.custom_properties))

#METHOD FOR ONE METRIC
def get_sensor_temperature():
	temperature = AUX_BASE_BODY_TEMPERATURE + (random.random() * random.random() * 5)
	
	return temperature

#METHOD FOR ONE METRIC
def get_sensor_heart_rate():
	heart_rate = AUX_BASE_HEART_RATE + (random.random() * random.random() * 15)
	
	return heart_rate
	
def aux_validate_connection_string():
    if not AUX_CONNECTION_STRING.startswith( 'HostName=' ):
        print ("ERROR  - YOUR IoT HUB CONNECTION STRING IS NOT VALID")
        print ("FORMAT - HostName=your_iot_hub_name.azure-devices.net;DeviceId=your_device_name;SharedAccessKey=your_shared_access_key")
        sys.exit()

def aux_iothub_client_init():
    client = IoTHubDeviceClient.create_from_connection_string(AUX_CONNECTION_STRING)
    return client

def iothub_client_telemetry_sample_run():
    try:
        aux_validate_connection_string()
        client = aux_iothub_client_init()

        print ( "IoT Hub Message receiver" )
        print ( "Press Ctrl-C to exit" )
        
	#ENABLE THE RECEPTION THREAD, DEFINING THE TARGET METHOD
        message_listener_thread = threading.Thread(target=message_listener, args=(client,))
        message_listener_thread.daemon = True
        message_listener_thread.start()

	#IT WILL RUN FOREVER UNLESS YOU STOP IT
        while True:
            time.sleep(1000)
			
    except KeyboardInterrupt:
        print ( "IoTHubClient sample stopped" )

if __name__ == '__main__':
    iothub_client_telemetry_sample_run()
