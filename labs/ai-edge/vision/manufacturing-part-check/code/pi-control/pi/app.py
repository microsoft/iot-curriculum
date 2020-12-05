# Copyright (c) Microsoft Corporation.
# Licensed under the MIT license.

import os
from dotenv import load_dotenv
from azure.iot.hub import IoTHubRegistryManager
from azure.iot.hub.models import CloudToDeviceMethod

# Load the connection string and device id from the .env file
load_dotenv()
iothub_connection_str = os.getenv("IOTHUB_CONNECTION_STRING")
device_id = os.getenv("IOTHUB_DEVICE_ID")

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

# Loop forever waiting for a key press
while True:
    # Wait for enter to be pressed
    input("Press Enter to validate the item on the assembly line...")

    # Invoke the device method and display the result
    method_result = invoke_device_method()
    print("Validate item result", method_result)
