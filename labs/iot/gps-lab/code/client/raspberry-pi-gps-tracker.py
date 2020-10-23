import time
import serial
import pynmea2
# Using the Python Device SDK for IoT Hub:
#   https://github.com/Azure/azure-iot-sdk-python
# The sample connects to a device-specific MQTT endpoint on your IoT Hub.
from azure.iot.device import IoTHubDeviceClient, Message

# The device connection string to authenticate the device with your IoT hub.
CONNECTION_STRING = "<Device_Connection_String>"

# Define the JSON message to send to IoT Hub.
MSG_TXT = '{{"latitude": {latitude},"longitude": {longitude}}}'

# The GPS receiver is connected to serial port. 
# As we do not have any other device connected to the serial port
# /dev/serial0 will be where the GPS receiver will send data to
SERIAL_PORT = "/dev/serial0"

# Most GPS receiver sends data in 9600 baudrate including the the [GPS sensor](https://www.amazon.com/Navigation-Positioning-Microcontroller-Compatible-Sensitivity/dp/B084MK8BS2) included with the lab
gps = serial.Serial(SERIAL_PORT, baudrate = 9600, timeout = 1.5)

# This method reads the data from the serial port, the GPS sensor is attached to,
# and then parses the NMEA messages it transmits.
# gps is the serial port, that's used to communicate with the GPS adapter
# For more information about the GPS message standards please go to https://www.gpsinformation.org/dale/nmea.htm
def get_position_data(gps):
    data = gps.readline()

    # pynmea2 library (https://github.com/Knio/pynmea2 helps parse the GPS data coming from the GPS receiver through serial port
    # Example of GPS data $GPRMC,184050.84,A,3907.3839,N,12102.4772,W,00.0,000.0,080301,15,E*54
    try:
        msg= pynmea2.parse(data.decode('utf-8'))
        return (msg.latitude, msg.longitude)
    except serial.SerialException as e:
        print('Device error: {}'.format(e))
        return (0,0)
    except pynmea2.ParseError as e:
        print('Parse error: {}'.format(e))
        return (0,0)

def iothub_client_init():
    # Create an IoT Hub client
    client = IoTHubDeviceClient.create_from_connection_string(CONNECTION_STRING)
    return client

def iothub_gps_client_run():

    try:
        client = iothub_client_init()
        print ( "IoT Hub device sending periodic messages, press Ctrl-C to exit" )

        while True:
            # get_position_data will return the GPS coordinates
            latitude, longitude = get_position_data(gps)
            if latitude != 0:   
                # Build the message with GPS location values.
                msg_txt_formatted = MSG_TXT.format(latitude=latitude, longitude=longitude)
                message = Message(msg_txt_formatted)
                  
                # Send the message.
                print( "Sending message: {}".format(message) )
                client.send_message(message)
                print ( "Message successfully sent" )
            else:
                pass
            time.sleep(1)

    except KeyboardInterrupt:
        print ( "IoTHubClient sample stopped" )

if __name__ == '__main__':
    print ( "IoT Hub GPS LAB" )
    print ( "Press Ctrl-C to exit" )
    iothub_gps_client_run()