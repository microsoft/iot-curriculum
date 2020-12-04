# Run the image classifier on the Raspberry Pi using IoT Edge

In the previous step, you controlled the Pi with either [the keyboard](./iot-hub-control), or [a button and LEDs using a Grove Pi+ kit](./pi-button-led.md).

In this step you will run the image classifier on the Raspberry Pi using IoT Edge.

## IoT Edge

IoT Edge involves running workloads that you would traditionally run in the cloud on an IoT device so that it is closer to your data. This has a number of upsides:

* It can be faster, and reduces bandwidth needs as you are not uploading data to the internet - for example if you want to run live video analytics on a video stream you don't need to upload that stream continually over the internet, you can analyze it locally.
* The data stays local - this could be important for privacy considerations, such as medical data
* It can be cheaper - by using your own hardware yo don't have to pay cloud fees

The traditional IoT Edge use case is AI on the edge. You train a model using the power of the cloud, then download the model to run on an Edge device. This is what you will be doing in this lab - taking the model trained by Custom Vision and running in on the Raspberry Pi.

## Set up IoT Edge

## Deploy the model to the edge

## Call the edge model from the ESP-EYE

## Next steps

In this step you ran the image classifier on the Raspberry Pi using IoT Edge.

In the [next step](./upload-iot-hub.md), you will upload the result data to Azure IoT Hub.
