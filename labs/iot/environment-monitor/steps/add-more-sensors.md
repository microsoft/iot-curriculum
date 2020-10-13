# Add more sensors

In the [previous step](./anomaly-detection.md) you performed more advanced analytics to detect and visualize anomalies in the data.

In this step you will see how to add more sensors to the project to capture more data.

## Grove Pi+ Sensors and controllers

This lab is based around the Grove Pi+ Starter Kit, and this kit comes with a range of sensors and controllers that can be added to the environment monitor.

### Connect and interact with the sensors and controllers

The different sensors and controllers connect to the Grove Pi+ using either analog, digital, or I2C (I Squared C) ports. The type of port needed depends on the sensor or controller.

Once connected, the sensors and controllers can be interacted with using the Grove Pi+ Python library.

#### Light Sensor

The Grove - Light sensor integrates a photo-resistor(light dependent resistor) to detect the intensity of light. The resistance of photo-resistor decreases when the intensity of light increases. A dual OpAmp chip LM358 on board produces voltage corresponding to intensity of light(i.e. based on resistance value). The output signal is analog value, the brighter the light is, the larger the value.

To use the light sensor, connect it to an analog port. The code below shows how to read from the sensor.

```python
# Import the Grove Pi library
import grovepi

# The port the light sensor is connected to.
# Change this if a different analog port is used
light_sensor_port = 0

# Set the port to input so values can be read
grovepi.pinMode(light_sensor_port, "INPUT")

# Read the light value from the analog port
sensor_value = grovepi.analogRead(light_sensor_port)
```

This code assumes the sensor is attached to the A0 analog port. If a different port is used, set `light_sensor_port` to the correct value.

#### Rotary Angle Sensor

The rotary angle sensor produces analog output between 0 and 5v. The angular range is 300 degrees with a linear change in value. The resistance value is 10k ohms. This may also be known as a potentiometer.

To use the rotary angle sensor, connect it to an analog port. The code below shows how to read from the sensor, including calculating the voltage coming from the sensor, and the angle of rotation.

```python
# Import the Grove Pi library
import grovepi

# The port the rotary angle sensor is connected to.
# Change this if a different analog port is used
rotary_angle_sensor_port = 0

# Set the port to input so values can be read
grovepi.pinMode(rotary_angle_sensor_port, "INPUT")

# Read the rotary angle value from the analog port
sensor_value = grovepi.analogRead(rotary_angle_sensor_port)

# Voltage of the grove interface is normally 5v
grove_vcc = 5

# Calculate voltage
voltage = round((float)(sensor_value) * grove_vcc / 1023, 2)

# Calculate rotation in degrees (0 to 300)
degrees = round((voltage * full_angle) / grove_vcc, 2)
```

This code assumes the sensor is attached to the A0 analog port. If a different port is used, set `rotary_angle_sensor_port` to the correct value.

#### Ultrasonic Ranger

This Grove - Ultrasonic ranger is a non-contact distance measurement module which works at 40KHz. When we provide a pulse trigger signal with more than 10uS through signal pin, the Grove_Ultrasonic_Ranger will issue 8 cycles of 40kHz cycle level and detect the echo. The pulse width of the echo signal is proportional to the measured distance. Here is the formula: Distance = echo signal high time * Sound speed (340M/S)/2.

To use the ultrasonic ranger, connect it to a digital port. The code below shows how to read from the sensor.

```python
# Import the Grove Pi library
import grovepi

# The port the ultrasonic ranger sensor is connected to.
# Change this if a different digital port is used
ultrasonic_ranger_port = 4

# Get the distance to an object in front of the ultrasonic ranger in cm
distance_cm = grovepi.ultrasonicRead(ultrasonic_ranger_port)
```

This code assumes the sensor is attached to the D4 digital port. If a different port is used, set `ultrasonic_ranger_port` to the correct value.

#### Button

Grove - Button is a momentary push button. It contains one independent "momentary on/off" button. “Momentary” means that the button rebounds on its own after it is released. The button outputs a HIGH signal when pressed, and LOW when released.

To use the button, connect it to a digital port. The code below shows how to read from the sensor. When the value read is `1`, the button is pressed, `0` means it is not pressed.

```python
# Import the Grove Pi library
import grovepi

# Import the time library
import time

# The port the button sensor is connected to.
# Change this if a different digital port is used
button_port = 4

# Set the port to input so values can be read
grovepi.pinMode(button_port, "INPUT")

# Loop forever checking the button
while (TRUE):
    # Read the state of the button
    buttonState = grovepi.digitalRead(button_port)

    # Check the button state - 1 is pressed
    if buttonState == 1:
        # The button is pressed so do something
        ...

    # Sleep for half a second before reading the button again
    time.sleep(.5)
```

This code assumes the sensor is attached to the D4 digital port. If a different port is used, set `button_port` to the correct value.

#### Buzzer

The Grove - Buzzer module has a piezo buzzer as the main component. The piezo can be connected to digital outputs, and will emit a tone when the output is HIGH.

To use the buzzer, connect it to a digital port. The code below shows how to make the buzzer buzz. Write a high value of 1 to the port to start buzzing, write a low value of 0 to stop the buzzer.

```python
# Import the Grove Pi library
import grovepi

# Import the time library
import time

# The port the buzzer is connected to.
# Change this if a different digital port is used
buzzer_port = 4

# Set the port to output so values can be written
grovepi.pinMode(buzzer_port, "OUTPUT")

# Start the buzzer buzzing
grovepi.digitalWrite(buzzer_port, 1)

# Sleep for 1 second
time.sleep(1)

# Stop the buzzer buzzing
grovepi.digitalWrite(buzzer_port, 0)
```

This code assumes the buzzer is attached to the D4 digital port. If a different port is used, set `buzzer_port` to the correct value.

#### LCD RGB Backlight

Done with tedious mono color backlight? This Grove enables you to set the color to whatever you like via the simple and concise Grove interface. It takes I2C as communication method with your microcontroller. So number of pins required for data exchange and backlight control shrinks from ~10 to 2, relieving IOs for other challenging tasks. Besides, Grove - LCD RGB Backlight supports user-defined characters. Want to get a love heart or some other foreign characters? Just take advantage of this feature and design it!

To use the LCD, connect it to one of the I2C ports. The code below shows how to set the text and the background color.

```python
# Import the RGB LCD library
import grove_rgb_lcd

# Set the text on the display
grove_rgb_lcd.setText("Hello world")

# Set the backlight to red using the RGB value 255, 0, 0
grove_rgb_lcd.setRGB(255, 0, 0)
```

#### Relay

The Grove-Relay module is a digital normally-open switch. Through it, you can control circuit of high voltage with low voltage, say 5V on the controller. There is an indicator LED on the board, which will light up when the controlled terminals get closed.

To use the buzzer, connect it to a digital port. The code below turns the relay on, then off.

```python
# Import the Grove Pi library
import grovepi

# Import the time library
import time

# The port the relay is connected to.
# Change this if a different digital port is used
relay_port = 4

# Set the port to output so the relay can be written to
grovepi.pinMode(relay_port, "OUTPUT")

# Turn the relay on
grovepi.digitalWrite(relay_port, 1)

# Sleep for 1 second
time.sleep(1)

# Stop the relay off
grovepi.digitalWrite(relay_port, 0)
```

This code assumes the relay is attached to the D4 digital port. If a different port is used, set `relay_port` to the correct value.

### Add the sensors to IoT Central

Adding the sensors to IoT Central involves repeating the steps in the [Set up the new telemetry values in IoT Central section of the Set up IoT Central and the Raspberry Pi to send humidity and sound data step](https://github.com/microsoft/iot-curriculum/blob/main/labs/iot/environment-monitor/steps/set-up-humidity-sound.md#set-up-the-new-telemetry-values-in-iot-central). Work through these instructions for whatever new sensor value you want to monitor. You can then add additional logic via [Rules](https://github.com/microsoft/iot-curriculum/blob/main/labs/iot/environment-monitor/steps/rules.md), [Stream Analytics](https://github.com/microsoft/iot-curriculum/blob/main/labs/iot/environment-monitor/steps/anomaly-detection.md) or other services to process this information

## Other sensors

There are literally thousands of sensors and kits that can be connected to a Raspberry Pi - either directly with kits designed to sit on top of the Pi (called hats), or via individual GPIO pins. Each one comes with it's own ways to connect and either Python libraries, or you can use the [Raspberry Pi GPIO library](https://pypi.org/project/RPi.GPIO/).

Some examples include:

* [Pimoroni Grow Kit](https://shop.pimoroni.com/products/grow?variant=32208365486163) - A compact Raspberry Pi powered monitoring system designed to help you take the best possible care of your plants. It will tell you how well they're hydrated, attract your attention when they need water and, if you want to go a step further, even give them water!

* [Enviro + Air Quality monitor](https://shop.pimoroni.com/products/enviro?variant=31155658457171) - Monitor your world with Enviro and Enviro + Air Quality for Raspberry Pi! There's a whole bunch of fancy environmental sensors on these boards, and a gorgeous little full-colour LCD to display your data. They're the perfect way to get started with citizen science and environmental monitoring!

## Next steps

In this step you saw how to add more sensors to the project to capture more data.

In the [next step](./clean-up.md) you will clean up your resources.
