# Copyright (c) Microsoft Corporation.
# Licensed under the MIT license.

import os
import grovepi
import time
from dotenv import load_dotenv
from azure.iot.hub import IoTHubRegistryManager
from azure.iot.hub.models import CloudToDeviceMethod

# Load the connection string and device id from the .env file
load_dotenv()
iothub_connection_str = os.getenv("IOTHUB_CONNECTION_STRING")
device_id = os.getenv("IOTHUB_DEVICE_ID")

# Configure the ports for the LEDs and button
red_led_port = 3
green_led_port = 4
button_port = 2
grovepi.pinMode(red_led_port, "OUTPUT")
grovepi.pinMode(green_led_port, "OUTPUT")
grovepi.pinMode(button_port, "INPUT")

# Turn off the LEDs
grovepi.digitalWrite(red_led_port, 0)
grovepi.digitalWrite(green_led_port, 0)

# Connect to the IoT Hub
registry_manager = IoTHubRegistryManager(iothub_connection_str)

# Invoke a direct method on the device to validate the item by
# taking a picture and classifying it as a pass or fail
def invoke_device_method() -> str:
    print("Validating item...")

    # Create a method call
    deviceMethod = CloudToDeviceMethod(method_name="ValidateItem")

    # Invoke the method on the device
    method_result = registry_manager.invoke_device_method(device_id, deviceMethod)

    # Return the result from the method call
    return method_result.payload['Result']

# Turn the LEDs on or off depending on the result
# pass - turn the green LED on and red off
# Anything else - turn the green LED off and red on
# LEDs are turned on by writing a digital value of 1, off by writing 0
def set_leds(result:str):
    print("Setting leds for a result of", result)

    if result == "pass":
        grovepi.digitalWrite(green_led_port, 1)
        grovepi.digitalWrite(red_led_port, 0)
    else:
        grovepi.digitalWrite(green_led_port, 0)
        grovepi.digitalWrite(red_led_port, 1)

# Loop forever waiting for button presses
while True:
    # Check if the button is pressed by reading the digital value from the
    # port. 1 is pressed, 0 is not
    if grovepi.digitalRead(button_port) == 1:
        print("Button pressed")
        
        # Invoke the method on the device
        method_result = invoke_device_method()

        # Light the relevant LEDs
        set_leds(method_result)

    # Sleep for 100 ms before checking the button
    time.sleep(.1)
