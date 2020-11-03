import asyncio
import json
import os
from dotenv import load_dotenv
from azure.iot.device.aio import IoTHubDeviceClient
from azure.iot.device import Message
from gps import *

# Load the device connection string from an environment variable read from the .env file
load_dotenv()
connection_string = os.getenv("CONNECTION_STRING")

# The main function that runs the program in an async loop
async def main():
    # The client object is used to interact with your Azure IoT hub.
    device_client = IoTHubDeviceClient.create_from_connection_string(connection_string)

    # Connect the client.
    print("Connecting")
    await device_client.connect()
    print("Connected")

    # Connect to the GPSD daemon
    gpsd = gps(mode=WATCH_ENABLE|WATCH_NEWSTYLE) 

    # The main loop - loops forever reading GPS values and sending them to IoT Hub
    async def main_loop():
        while True:
            # Get the next value reported by the GPS device
            report = gpsd.next()

            # GPS values can have multiple types, such as:
            # TPV - Time, position, velocity giving the time signal, current position and current calculated velocity
            # SKY - the sky view of GPS satellite positions
            # GST - error ranges
            # Monitor for the TPV values to get the position. Sometimes this value can come without the properties if
            # the values aren't available yet, so ignore if the lat and lon are not set
            if report["class"] == "TPV" and hasattr(report, 'lat') and hasattr(report, 'lon'):
                # Build the message with GPS location values.
                message_body = {
                    "latitude": report.lat,
                    "longitude": report.lon
                }

                # Convert to an IoT Hub message
                message = Message(json.dumps(message_body))
                  
                # Send the message.
                print("Sending message:", message)
                await device_client.send_message(message)
                print("Message successfully sent")

                # Wait for a minute so telemetry is not sent to often
                # Only sleep after receiving TPV values so we don't waste
                # time sleeping after other values that are ignored
                await asyncio.sleep(60)

    # Run the async main loop forever
    await main_loop()

    # Finally, disconnect
    await device_client.disconnect()

# Run the async main loop
if __name__ == "__main__":
    asyncio.run(main())
