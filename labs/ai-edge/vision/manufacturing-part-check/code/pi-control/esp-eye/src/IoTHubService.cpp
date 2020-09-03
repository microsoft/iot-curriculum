// Copyright (c) Microsoft Corporation.
// Licensed under the MIT license.

#include "IoTHubService.h"
#include "Config.h"

#include <Arduino.h>
#include <AzureIoTProtocol_MQTT.h>
#include <AzureIoTSocket_WiFi.h>
#include <Esp.h>
#include <iothubtransportmqtt.h>
#include <WiFiClientSecure.h>

const IOTHUB_CLIENT_TRANSPORT_PROVIDER protocol = MQTT_Protocol;
const string ERROR_MESSAGE = "Error";

// A helper method to build a response in the format that IoT Hub expects
static void BuildResult(const char *result, unsigned char **response, size_t *response_size)
{
    // Create a JSON document with the classificaiton result
    char resultBuff[128];
    sprintf(resultBuff, "{\"Result\":\"%s\"}", result);

    // Set the size of the response
    *response_size = strlen(resultBuff);

    // Allocate memory for the response, and copy the values into the allocated memory
    *response = (unsigned char*)malloc(*response_size);
    memcpy(*response, resultBuff, *response_size);
}

// A callback used when the IoT Hub invokes a direct method
// This is a static method as opposed to a method on the class so it can be pass to the 
// IoT hub configuration
static int CommandCallback(const char *method_name, const unsigned char *payload, size_t size, unsigned char **response, size_t *response_size, void *userContextCallback)
{
    // Log the command received
    Serial.printf("Command received %s\r\n", method_name);

    // The userContextCallback is the IoT Hub Service, so cast it so it can be used
    IoTHubService *iotHubService = (IoTHubService*)userContextCallback;

    // We only support the ValidateItem method, any other method calls return an error status
    if (strcmp(method_name, "ValidateItem") == 0)
    {
        // Take an image and classify it
        string classification = iotHubService->TakeImageAndClassify();

        // If the classification gives an error, return the error
        if (classification == ERROR_MESSAGE)
        {
            BuildResult("Error classifying item", response, response_size);
            return IOTHUB_CLIENT_ERROR;
        }

        // Return the classification result
        BuildResult(classification.c_str(), response, response_size);
        return IOTHUB_CLIENT_OK;
    }
    else
    {
        BuildResult("Method is not supported", response, response_size);
        return IOTHUB_CLIENT_ERROR;
    }
}

IoTHubService::IoTHubService() : _camera(),
                                 _imageClassifier()
{
    // Used to initialize IoTHub SDK subsystem
    IoTHub_Init();

    // Create the client from the connection string
    _device_ll_handle = IoTHubDeviceClient_LL_CreateFromConnectionString(deviceConnectionString, protocol);

    Serial.println("Connected to IoT Hub!");

    // If the client connection fails, report an error and restart the device
    if (_device_ll_handle == NULL)
    {
        Serial.println("Error AZ002: Failure creating Iothub device. Hint: Check your connection string.");
        ESP.restart();
    }
        
    // Set any option that are neccessary.
    // For available options please see the iothub_sdk_options.md documentation in the main C SDK
    // turn off diagnostic sampling
    int diag_off = 1;
    IoTHubDeviceClient_LL_SetOption(_device_ll_handle, OPTION_DIAGNOSTIC_SAMPLING_PERCENTAGE, &diag_off);

    bool traceOn = true;
    IoTHubDeviceClient_LL_SetOption(_device_ll_handle, OPTION_LOG_TRACE, &traceOn);

    // Setting the Trusted Certificate.
    IoTHubDeviceClient_LL_SetOption(_device_ll_handle, OPTION_TRUSTED_CERT, certificates);

    //Setting the auto URL Encoder (recommended for MQTT). Please use this option unless
    //you are URL Encoding inputs yourself.
    //ONLY valid for use with MQTT
    bool urlEncodeOn = true;
    IoTHubDeviceClient_LL_SetOption(_device_ll_handle, OPTION_AUTO_URL_ENCODE_DECODE, &urlEncodeOn);

    // Setting method call back, so we can receive Commands.
    IoTHubClient_LL_SetDeviceMethodCallback(_device_ll_handle, CommandCallback, this);
}

// Let the IoT Hub do whatever work is needed to send or receive messages
void IoTHubService::DoWork()
{
    // Let the IoT Hub do whatever work is needed to send or receive messages
    IoTHubDeviceClient_LL_DoWork(_device_ll_handle);
}

// Takes an image using the camera and classifies it, returning the classification result
string IoTHubService::TakeImageAndClassify()
{
    // Take a photo with the camera
    Serial.println("Taking a photo...");
    camera_fb_t *fb = _camera.TakePhoto();

    // Verify the photo was taken
    if (!fb)
    {
        Serial.println("Camera capture failed");
        return "Error";
    }

    // Classify the photo
    string result = _imageClassifier.ClassifyImage(fb);

    // Release the frame buffer to free up the memory
    _camera.ReleaseFrameBuffer(fb);

    // Return the classification result
    return result;
}