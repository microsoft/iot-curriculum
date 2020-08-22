import asyncio
import json
import grovepi
from azure.iot.device.aio import IoTHubDeviceClient, ProvisioningDeviceClient
from azure.iot.device import MethodResponse

# The connection details from IoT Central for the device
id_scope = ID_SCOPE
key = KEY
device_id = "pi-temperature-sensor"

# Set the temperature sensor port to the digital port D4
# and mark it as INPUT meaning data needs to be
# read from it
temperature_sensor_port = 4
grovepi.pinMode(temperature_sensor_port, "INPUT")

# Set the sound sensor port to the analog port A0
# and mark it as INPUT meaning data needs to be
# read from it
sound_sensor_port = 0
grovepi.pinMode(sound_sensor_port, "INPUT")

# Set the LED port to the digital port D3
# and mark it as OUTPUT meaning data needs to be
# written to it
led_port = 3
grovepi.pinMode(led_port, "OUTPUT")

# Gets telemetry from the Grove sensors
# Telemetry needs to be sent as JSON data
async def get_telemetry() -> str:
    # The dht call returns the temperature and the humidity,
    # we only want the temperature, so ignore the humidity
    [temperature, humidity] = grovepi.dht(temperature_sensor_port, 0)

    # The temperature can come as 0, meaning you are reading
    # too fast, if so sleep for a second to ensure the next reading
    # is ready
    while (temperature == 0 or humidity == 0):
        [temperature, humidity] = grovepi.dht(temperature_sensor_port, 0)
        await asyncio.sleep(1)

    # Read the background noise level from an analog port
    sound = grovepi.analogRead(sound_sensor_port)

    # Build a dictionary of data
    # The items in the dictionary need names that match the
    # telemetry values expected by IoT Central
    dict = {
        "Temperature" : temperature,  # The temperature value
        "Humidity" : humidity,        # The humidity value
        "Sound" : sound               # The background noise value
    }

    # Convert the dictionary to JSON
    return json.dumps(dict)

# The main function that runs the program in an async loop
async def main():
    # Connect to IoT Central and request the connection details for the device
    provisioning_device_client = ProvisioningDeviceClient.create_from_symmetric_key(
        provisioning_host="global.azure-devices-provisioning.net",
        registration_id=device_id,
        id_scope=id_scope,
        symmetric_key=key)
    registration_result = await provisioning_device_client.register()

    # Build the connection string - this is used to connect to IoT Central
    conn_str="HostName=" + registration_result.registration_state.assigned_hub + \
                ";DeviceId=" + device_id + \
                ";SharedAccessKey=" + key

    # The client object is used to interact with Azure IoT Central.
    device_client = IoTHubDeviceClient.create_from_connection_string(conn_str)

    # Connect the client.
    print("Connecting")
    await device_client.connect()
    print("Connected")

    # async code to light the LED, wait 10 seconds then
    # turn the LED off
    async def light_led():
            # Send a value of 1 to the digital port
            # This will turn the LED on
            grovepi.digitalWrite(led_port, 1)

            # Wait 10 seconds
            await asyncio.sleep(10)

            # Send a value of 0 to the digital port
            # This will turn the LED off
            grovepi.digitalWrite(led_port, 0)

    # Asynchronously wait for commands from IoT Central
    # If the TooLoud command is called, handle it
    async def command_listener(device_client):
        # Loop forever waiting for commands
        while True:
            # Wait for commands from IoT Central
            method_request = await device_client.receive_method_request("TooLoud")

            # Log that the command was received
            print("Too Loud Command handled")

            # Asynchronously light the LED
            # This will be run in the background, so the result can
            # be returned to IoT Central straight away, not 10 seconds later
            asyncio.gather(light_led())

            # IoT Central expects a response from a command, saying if the call
            # was successful or not, so send a success response
            payload = {"result": True}

            # Build the response
            method_response = MethodResponse.create_from_method_request(
                method_request, 200, payload
            )

            # Send the response to IoT Central
            await device_client.send_method_response(method_response)

    # async loop that sends the telemetry
    async def main_loop():
        while True:
            # Get the telemetry to send
            telemetry = await get_telemetry()
            print("Telemetry:", telemetry)

            # Send the telemetry to IoT Central
            await device_client.send_message(telemetry)

            # Wait for a minute so telemetry is not sent to often
            await asyncio.sleep(60)

    # Start the command listener
    listeners = asyncio.gather(command_listener(device_client))

    # Run the async main loop forever
    await main_loop()

    # Cancel listening
    listeners.cancel()

    # Finally, disconnect
    await device_client.disconnect()

# Start the program running
asyncio.run(main())
