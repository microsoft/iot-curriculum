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

print("Configuring ports...")

# Configure the ports for the LEDs and button
red_led_port = 3
green_led_port = 4
button_port = 2
grovepi.pinMode(red_led_port, "OUTPUT")
grovepi.pinMode(green_led_port, "OUTPUT")
grovepi.pinMode(button_port, "INPUT")

time.sleep(1)

# LEDs are turned on by writing a digital value of 1, off by writing 0
def set_led(led, on):
    if on:
        time.sleep(0.1)
        grovepi.digitalWrite(led, 1)
    else:
        time.sleep(0.1)
        grovepi.digitalWrite(led, 0)

print("Ports configured, flashing LEDs")
# Flash on then off the LEDs
set_led(red_led_port, True)
set_led(green_led_port, True)
time.sleep(1)
set_led(red_led_port, False)
set_led(green_led_port, False)
print("LEDs turned off")

# Connect to the IoT Hub
print("Connecting to IoT Hub...")
registry_manager = IoTHubRegistryManager(iothub_connection_str)
print("Connected to IoT Hub!")

# Invoke a direct method on the device to validate the item by
# taking a picture and classifying it as a pass or fail
def invoke_device_method() -> str:
    print("Validating item...")

    # Create a method call with a long response time to allow the image classifier to run
    deviceMethod = CloudToDeviceMethod(method_name="ValidateItem", response_timeout_in_seconds=30, connect_timeout_in_seconds=30)

    # Invoke the method on the device
    method_result = registry_manager.invoke_device_method(device_id, deviceMethod)

    # Return the result from the method call
    return method_result.payload['Result']

# Turn the LEDs on or off depending on the result
# pass - turn the green LED on and red off
# Anything else - turn the green LED off and red on
def set_leds(result:str):
    print("Setting leds for a result of", result)

    set_led(red_led_port, result != "pass")
    set_led(green_led_port, result == "pass")

# Get the current time - this is used to avoid a long button press
# being seen as multiple presses. Ignore any button press less than 
# # 2 seconds after the previous one
last_button_time = 0

# Loop forever waiting for button presses
print("Waiting for button press...")
while True:
    # Check if the button is pressed by reading the digital value from the
    # port. 1 is pressed, 0 is not
    if grovepi.digitalRead(button_port) == 1:
        if  (time.time() - last_button_time) < 2:
            print("Button pressed too soon, ignoring")
        else:
            print("Button pressed")

            # Turn the LEDs off whilst we process
            set_led(red_led_port, False)
            set_led(green_led_port, False)
            
            # Invoke the method on the device
            method_result = invoke_device_method()

            # Light the relevant LEDs
            set_leds(method_result)

            # Get the button press time to avoid multiple calls from a long press
            last_button_time = time.time()
            print("Waiting for button press...")

    # Sleep for 10 ms before checking the button
    time.sleep(.01)
