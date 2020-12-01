// Copyright (c) Microsoft Corporation.
// Licensed under the MIT license.

#ifndef _IOTHUBSERVICE_H_
#define _IOTHUBSERVICE_H_

#include "Camera.h"
#include "ImageClassifier.h"

#include <AzureIoTHub.h>
#include <string>

using namespace std;

/**
 * @brief A class that handles interaction with the Azure IoT Hub.
 */
class IoTHubService
{
public:
    /**
     * @brief Create the class, making a connection to Azure IoT Hub and waiting for commands
     */
    IoTHubService();

    /**
     * @brief Allocate some time to the IoT Hub connection to process messages coming in and out
     */
    void DoWork();

    /**
     * @brief Take a picture with the camera and send it to the classifier
     *
     * @return The classification result
     */
    string TakeImageAndClassify();

private:
    IOTHUB_DEVICE_CLIENT_LL_HANDLE _device_ll_handle;
    Camera _camera;
    ImageClassifier _imageClassifier;
};

#endif