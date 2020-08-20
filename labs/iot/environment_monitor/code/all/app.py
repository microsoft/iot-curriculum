import asyncio
import json
import grovepi
from azure.iot.device.aio import IoTHubDeviceClient, ProvisioningDeviceClient

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

    # async loop that sends the telemetry
    async def main_loop():
        while True:
            # Get the telemetry to send
            telemetry = await get_telemetry()
            print("Telemetry:", telemetry)

            # Send the telemetry to IoT Central
            await device_client.send_message(telemetry)

            # Wait for a minute so telemetry is not sent to often
            await asyncio.sleep(10)

    # Run the async main loop forever
    await main_loop()

    # Finally, disconnect
    await device_client.disconnect()

# Start the program running
asyncio.run(main())
