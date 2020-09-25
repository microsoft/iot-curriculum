import time
import serial

# Using the Python Device SDK for IoT Hub:
#   https://github.com/Azure/azure-iot-sdk-python
# The sample connects to a device-specific MQTT endpoint on your IoT Hub.
from azure.iot.device import IoTHubDeviceClient, Message

# The device connection string to authenticate the device with your IoT hub.
CONNECTION_STRING = "<Device_Connection_String>"

# Define the JSON message to send to IoT Hub.
MSG_TXT = '{{"latitude": {latitude},"longitude": {longitude}}}'

SERIAL_PORT = "/dev/serial0"

gps = serial.Serial(SERIAL_PORT, baudrate = 9600, timeout = 1.5)

#This method converts a transmitted string from DDMM.MMMMM to DD.MMMM
def formatDegreesMinutes(coordinates, digits):
    
    parts = coordinates.split(".")

    if (len(parts) != 2):
        return coordinates

    if (digits > 3 or digits < 2):
        return coordinates
    
    left = parts[0]
    right = parts[1]
    degrees = str(left[:digits])
    minutes = str(right[:3])

    return degrees + "." + minutes

# This method reads the data from the serial port, the GPS sensor is attached to,
# and then parses the NMEA messages it transmits.
# gps is the serial port, that's used to communicate with the GPS adapter
def getPositionData(gps):
    data = gps.readline()
    message = data[0:6]
    print(message);
    if (message.decode('utf-8') == "$GPRMC"):        
        # GPRMC = Recommended minimum specific GPS/Transit data
        parts = data.decode('utf-8').split(",")
        if parts[2] == 'V':
            # V = Warning, most likely, there are no satellites in view...
            print ("GPS receiver warning")
        else:
            # Get the position data that was transmitted with the GPRMC message
            # Find the Latitude and Longitude
            longitude = formatDegreesMinutes(parts[5], 3)
            latitude = formatDegreesMinutes(parts[3], 2)
            return (latitude, longitude);
    else:
        # Handle other NMEA messages and unsupported strings
        return (0, 0);
        pass
    


def iothub_client_init():
    # Create an IoT Hub client
    client = IoTHubDeviceClient.create_from_connection_string(CONNECTION_STRING)
    return client

def iothub_client_telemetry_sample_run():

    try:
        client = iothub_client_init()
        print ( "IoT Hub device sending periodic messages, press Ctrl-C to exit" )

        while True:
            latitude, longitude = getPositionData(gps)
            if latitude != 0:   
                # Build the message with simulated telemetry values.
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
    iothub_client_telemetry_sample_run()