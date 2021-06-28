# Set up the Raspberry Pi with SenseHAT to send humidity and sound data

In the [previous step](./set-up-humidity-sound.md) you set up IoT Central to receive humidity and sound data.

In this step you will set up the Raspberry Pi and run code to connect and send humidity and sound data. Because the Sense HAT has no sound detector, we will emulate the sound data in the code.

## Connect the sensors

The humidity data can be gathered from the existing sensor eembeded in the Sense HAT.

## Program the Pi

The Pi code needs to be changed to read the new values and send them to IoT Central.

### Update the code

In this section you will be adding code to the Python file. If you haven't used Python before, be aware it is very specific about how the lines are indented, so make sure the code is indented the same as the code around it. You can find the full code in the [app.py](../code/pi/sound-humidity/app.py) file in the [code/pi/sound-humidity](../code/pi/sound-humidity) folder to check your code against if you get errors.

1. Connect to the Pi using Visual Studio Code, open the `Environment Monitor` folder, and open the `app.py` file.

   Head to the `get_telemetry` function and replace the code of this function with the following:

    ```python
    # Use this to see if a high value for the sound should be sent
    # If this is True, a value of 1023 is sent, otherwise a random value
    # from 300-600 is sent
    report_high_sound = False
    
    # Gets telemetry from SenseHat
    # Telemetry needs to be sent as JSON data
    async def get_telemetry() -> str:
        global report_high_sound
        # Get temperature, rounded to 0 decimals
        temperature = round(sense.get_temperature())

        # Get humidity, rounded to 0 decimals
        humidity = round(sense.get_humidity())
        # If a high sound value is wanted, send 1023
        # otherwise pick a random sound level
        if report_high_sound:
            sound = 1023

            # Reset the report high sound flag, so next time
            # a normal sound level is reported
            report_high_sound = False
    else:
            sound = random.randint(300, 600)

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

    * The humidity value is now read, and is added to the telemetry dictionary
    * A random value from 300-600 is returned in the telemetry for the ambient sound levels unless the report_high_sound variable is set to True, in which case it sends a value of 1023, and sets report_high_sound back to false. This allows a single spike to be sent, and in later parts this spike will be detected.

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

    Try adjusting humidity level by breathing on the sensor, and see the values change both in the output of the Python code, and in IoT Central. You change adjust report_high_sound = False into report_high_sound = True to emulate high sound levels.

## Next steps

In this step you set up the Raspberry Pi to send humidity and sound data.

In the [next step](./rules.md) you will perform simple analytics and create alerts on the data using IoT Central rules.
