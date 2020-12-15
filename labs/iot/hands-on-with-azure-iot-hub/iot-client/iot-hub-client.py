import json
import random
import re
import sys
import time

from azure.iot.device import IoTHubDeviceClient, Message

AUX_CONNECTION_STRING = sys.argv[1]

AUX_BASE_HEART_RATE = 65
AUX_BASE_BODY_TEMPERATURE = 37.0
AUX_MAXIMUM_BODY_TEMPERATURE = 40.0

#SENSOR DATA WILL HOST SENSOR METRICS
sensor_data = {}

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

        print ( "IoT Hub Simulated body sensor" )
        print ( "Press Ctrl-C to exit" )

	#IT WILL RUN FOREVER UNLESS YOU STOP IT
        while True:
        #COLLECTING SENSOR VALUES
		#NEW METRIC COLLECTION SHOULD ADD CODE HERE
            temperature_measure = get_sensor_temperature()
            heart_rate_measure  = get_sensor_heart_rate()
		
		#STORING SENSOR VALUES IN DATA STRUCTURE
		#NEW METRIC COLLECTION SHOULD ADD CODE HERE
            sensor_data['temperature'] = temperature_measure
            sensor_data['heart_rate']  = heart_rate_measure

		#TRANFORMING IT TO JSON			
            json_sensor_data = json.dumps(sensor_data)
		#CREATING AN AZURE IOT MESSAGE OBJECT		
            azure_iot_message = Message(json_sensor_data)

        #ADDING A CUSTOM PROPERTY OF OUR CHOICE TO THE MESSAGE CALLED temperature_alert
            if temperature_measure > AUX_MAXIMUM_BODY_TEMPERATURE:
              azure_iot_message.custom_properties["temperature_alert"] = "true"
            else:
              azure_iot_message.custom_properties["temperature_alert"] = "false"

        #SETTING PROPER MESSAGE ENCODING
            azure_iot_message.content_encoding='utf-8'
            azure_iot_message.content_type='application/json'

        #SENDING THE MESSAGE
            print( "Sending azure_iot_message: {}".format(azure_iot_message) )
            client.send_message(azure_iot_message)
            print ( "Message successfully sent" )
        #SLEEPING FOR A SECOND BEFORE RESTARTING
            time.sleep(1)

    except KeyboardInterrupt:
        print ( "IoTHubClient sample stopped" )

if __name__ == '__main__':
    iothub_client_telemetry_sample_run()
