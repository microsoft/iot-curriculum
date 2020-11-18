# Labs

This folder contains hands-on-labs, workshops and other content for using the hardware that comes with the IoT Cart.

These labs are divided up into multiple sections.

## IoT

These labs cover traditional internet of things scenarios, connecting devices to the cloud

* [Environment Monitor](./iot/environment-monitor/) - a beginners tutorial setting up a Raspberry Pi to send data to the cloud, and perform analytics on the data
* [GPS Lab](./iot/gps-lab/README.md) - A sample application for sending GPS data from GPS sensor connected to a Raspberry Pi to Azure IoT Hub and displaying the location in a web application in real time using Azure Maps.

## AI/Edge

These labs cover running AI workloads either in the cloud from the IoT device, or on the edge running the workload actually on the IoT device itself.

* [OCR](./ai-edge/vision/ocr/) - Optical character recognition using a Raspberry Pi, USB camera and Python
* [Manufacturing part checker](./ai-edge/vision/manufacturing-part-check/) - A prototype of an AI image classification based part validator for  manufacturing showing how to detect broken parts on an assembly line using AI, controlled from another device
* [Speech](./ai-edge/speech) - Speech to text, text to speech and speech translation using a Raspberry Pi and USB microphone/speaker

## Digital Agriculture

These labs cover scenarios around digital agriculture.

* [Plant monitor](./digital-agriculture/plant-monitor/) - a plant monitoring lab based around a Raspberry Pi

## Contributing

We love contributions! Please fork this repo and raise a pull request with new labs. Check out the [lab contribution guidelines](./lab_contribution_guidelines.md)for guidelines on how to create a great lab that is consistent with the content we already have here.
