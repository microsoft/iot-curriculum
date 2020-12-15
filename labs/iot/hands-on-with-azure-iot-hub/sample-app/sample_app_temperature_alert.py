import datetime
import os
import sys
from azure.eventhub import EventHubConsumerClient
from azure.iot.hub import IoTHubRegistryManager

IOT_HUB_BUILT_IN_ENDPOINT_CONNECTION_STRING = sys.argv[1]

AUX_EVENT_HUB_NAMESPACE_CONNECTION_STRING = ";".join(IOT_HUB_BUILT_IN_ENDPOINT_CONNECTION_STRING.split(";")[0:3])
AUX_EVENTHUB_NAME = IOT_HUB_BUILT_IN_ENDPOINT_CONNECTION_STRING.split(";")[3].split("=")[1]
AUX_EVENTHUB_SAS  = IOT_HUB_BUILT_IN_ENDPOINT_CONNECTION_STRING.split(";")[2][16:]
AUX_IOT_HUB_CONNECTION_STRING="HostName={}.azure-devices.net;SharedAccessKeyName=iothubowner;SharedAccessKey={}".format(AUX_EVENTHUB_NAME, AUX_EVENTHUB_SAS)

#AUX METHOD - NO NEED TO TOUCH
def aux_validate_connection_string():
    if not IOT_HUB_BUILT_IN_ENDPOINT_CONNECTION_STRING.startswith( 'Endpoint=sb://' ):
        print ("ERROR  - YOUR IoT HUB CONNECTION STRING IS NOT VALID")
        print ("FORMAT - Endpoint=sb://iothub-ns-blablabla.servicebus.windows.net/;SharedAccessKeyName=service;SharedAccessKey=your_shared_access_key;EntityPath=your_iot_hub_name")
        sys.exit()

#AUX METHOD - NO NEED TO TOUCH
def aux_iot_hub_send_message_to_device(device_name, message_body, message_properties):
    #CONNECT TO THE IOT HUB DEVICE REGISTRY MANAGER
    aux_iot_hub_registry_manager = IoTHubRegistryManager(AUX_IOT_HUB_CONNECTION_STRING)
    message_properties.update(contentType = "application/json")
    aux_iot_hub_registry_manager.send_c2d_message(device_name, message_body, message_properties)

#YOUR PROGRAM LOGIC GOES HERE
#EVERY TIME THERE IS A MESSAGE FROM THE DEVICE THIS METHOD WILL BE CALLED
def on_iot_hub_message_event(partition_context, event):

    #READ MESSAGE CONTENT
    event_body=event.body_as_json()

    #READ MESSAGE PROPERTIES
    #IF YOUR DEVICE DOES NOT SEND TEMPERATURE JUST CHANGE THE FOLLOWING LINES
    event_temperature=event_body['temperature']
    event_device_name=event_body['device_name']
    print("Temperature {} from device {} is lower than {}".format(event_temperature, event_device_name, MAXIMUM_TEMPERATURE))

    if event_temperature > MAXIMUM_TEMPERATURE:

        print("Temperature {} from device {} is higher than {}".format(event_temperature, event_device_name, MAXIMUM_TEMPERATURE))
        print("Sending alert to device {}".format(event_device_name))

        #MESSAGES TO DEVICES HAVE A BODY
        command_to_device_message_body = "ONE ACTION CODE YOU SHOULD IMPLEMENT"
        #MESSAGES TO DEVICES HAVE A DICTIONARY OF PROPERTIES
        command_to_device_message_properties={}
        command_to_device_message_properties['onePropertyNameIShouldGiveAProperName'] = 'youShouldChangeThis'

        aux_iot_hub_send_message_to_device(device_name=event_device_name, message_body=command_to_device_message_body, message_properties=command_to_device_message_properties)


if __name__ == '__main__':

    #FIRST CHECK IF THE CONNECTION STRING IS OK
    aux_validate_connection_string()

    #CONNECT TO THE IOT HUB BUILT IT ENDPOINT
    aux_iot_hub_built_in_event_hub_consumer_client = EventHubConsumerClient.from_connection_string(conn_str=AUX_EVENT_HUB_NAMESPACE_CONNECTION_STRING, consumer_group='app', eventhub_name=AUX_EVENTHUB_NAME)

    MAXIMUM_TEMPERATURE=38

    try:
        with aux_iot_hub_built_in_event_hub_consumer_client:
            print("Starting sample temperature monitor application")
            print("Maximum temperature set to {} degrees".format( MAXIMUM_TEMPERATURE))
            #EVERY TIME WE RECEIVE AN EVENT WE CALL THE METHOD ON EVENT
            aux_iot_hub_built_in_event_hub_consumer_client.receive(on_event=on_iot_hub_message_event, starting_position="@latest")
    except KeyboardInterrupt:
        print('Stopped receiving.')