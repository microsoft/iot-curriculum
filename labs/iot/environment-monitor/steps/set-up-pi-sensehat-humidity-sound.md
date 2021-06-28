# Set up the Raspberry Pi to send humidity and sound data

In the [previous step](./set-up-humidity-sound.md) you set up IoT Central to receive humidity and sound data.

In this step you will set up the Raspberry Pi and run code to connect and send humidity and sound data.

## Connect the sensors

The humidity data can be gathered from the existing sensor eembeded in the Sense HAT.

## Program the Pi

The Pi code needs to be changed to read the new values and send them to IoT Central.

### Update the code

In this section you will be adding code to the Python file. If you haven't used Python before, be aware it is very specific about how the lines are indented, so make sure the code is indented the same as the code around it. You can find the full code in the [app.py](../code/pi/sound-humidity/app.py) file in the [code/pi/sound-humidity](../code/pi/sound-humidity) folder to check your code against if you get errors.

1. Connect to the Pi using Visual Studio Code, open the `Environment Monitor` folder, and open the `app.py` file.

    ```

1. Head to the `get_telemetry` function and replace the code of this function with the following:

    ```python
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
    ```

    This code makes the following changes:

    * The humidity value is now used from the call to `grovepi.dht`, and is added to the telemetry dictionary
    * The sound value is read by reading the analog signal from the A0 port, and is added to the telemetry dictionary

1. Save the file

1. Run the code from the VS Code terminal using the following command:

    ```sh
    python3 app.py
    ```

1. The app will start up, connect to Azure IoT Central, then send temperature, humidity and sound values:

    ```output
    pi@jim-iot-pi:~/EnvironmentMonitor $ python3 app.py
    RegistrationStage(RequestAndResponseOperation): Op will transition into polling after interval 2.  Setting timer.
    Connecting
    Connected
    Telemetry: {"Temperature": 27.0, "Humidity": 44.0, "Sound": 304}
    Telemetry: {"Temperature": 26.0, "Humidity": 45.0, "Sound": 326}
    Telemetry: {"Temperature": 26.0, "Humidity": 45.0, "Sound": 400}
    Telemetry: {"Temperature": 26.0, "Humidity": 45.0, "Sound": 361}
    ```

    Try adjusting sound levels near the sensor such as by playing music, and adjusting humidity level by breathing on the sensor, and see the values change both in the output of the Python code, and in IoT Central.

## Next steps

In this step you set up the Raspberry Pi to send humidity and sound data.

In the [next step](./rules.md) you will perform simple analytics and create alerts on the data using IoT Central rules.
