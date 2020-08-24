# Plant monitor

This workshop is a hands on lab for building an AgroTech solution using [Azure IoT](https://azure.microsoft.com/overview/iot/?WT.mc_id=iotcurriculum-github-jabenn).

| Author | [Jim Bennett](https://github.com/JimBobBennett) |
|:---|:---|
| Target platform   | Raspberry Pi |
| Hardware required | Raspberry Pi 4<br>Micro SD Card<br>An SD card to USB converter that matches the USB ports on your device if your device doesn't have an SD card slot<br>Raspberry Pi 4 power supply (USB-C)<br>[Grove Pi+ Starter Kit](https://www.seeedstudio.com/GrovePi-Starter-Kit-for-Raspberry-Pi-A-B-B-2-3-CE-certified.html)<br>[Grove capacitive moisture sensor](http://wiki.seeedstudio.com/Grove-Capacitive_Moisture_Sensor-Corrosion-Resistant/)<br>A plant |
| Software required | [Visual Studio Code](http://code.visualstudio.com?WT.mc_id=iotcurriculum-github-jabenn)<br>[Azure Functions Core Tools](https://docs.microsoft.com/azure/azure-functions/functions-run-local?WT.mc_id=iotcurriculum-github-jabenn)<br>[Raspberry Pi Imager](https://www.raspberrypi.org/downloads/)<br>*There are optional installs for Windows and Linux that you may need to install later to connect to the Pi, depending on which version of the OS you are using.* |
| Azure Services | [Azure IoT Central](https://azure.microsoft.com/services/iot-central/?WT.mc_id=iotcurriculum-github-jabenn)<br>[Azure Stream Analytics](https://azure.microsoft.com/services/stream-analytics/?WT.mc_id=iotcurriculum-github-jabenn)<br>[Azure Event Hubs](https://azure.microsoft.com/services/event-hubs/?WT.mc_id=iotcurriculum-github-jabenn)<br>[Azure blob storage](https://azure.microsoft.com/services/storage/blobs/?WT.mc_id=iotcurriculum-github-jabenn)<br>[Azure Functions](https://azure.microsoft.com/services/functions/?WT.mc_id=iotcurriculum-github-jabenn)<br>[Azure Maps](https://azure.microsoft.com/services/azure-maps/?WT.mc_id=iotcurriculum-github-jabenn) |
| Programming Language | Python |
| Prerequisites | You will need to be reasonably proficient at using a computer, including installing software and running commands from a command line or terminal.<br>These labs will use Python, but if you are not proficient in Python you can simply copy and paste the provided code and run it to see the end results, rather than trying to understand the code.<br><br>You will also need an [Azure subscription](https://github.com/microsoft/iot-curriculum/tree/main/labs/iot/environment_monitor#azure-subscription) |
| Date | August 2020 |
| Learning Objectives | Set up IoT Central<br>Send IoT Data from a device to IoT Central<br>Export data from IoT Central<br>Use Stream Analytics to send aggregate data for processing<br>Query Azure Maps for weather<br>Control IoT Central from Azure Functions |
| Time to complete | 4 hours |

The final project that will be created is an internet connected plant with environment sensors, that connects to a set of services that will store the telemetry data and predict the weather using [Azure Maps](https://azure.microsoft.com/services/azure-maps/?WT.mc_id=iotcurriculum-github-jabenn). This weather prediction will be combined with soil moisture data, and used to send a signal back to the device to indicate if the plants need watering, and this will be indicated by an LED, lit if the plant needs watering.

Most of this implementation will use a no-code IoT platform called [Azure IoT Central](https://azure.microsoft.com/services/iot-central/?WT.mc_id=iotcurriculum-github-jabenn), an IoT Software-as-a-service (SaaS) platform. There will be some coding required for the connected device, and this will all be in Python.

## Steps

1. [Set up the environment monitor](./Steps/SetUpTheEnvironmentMonitor.md)

1. [Create the application in Azure IoT Central](./Steps/CreateTheAppInIoTCentral.md)

1. [Write the code to capture telemetry from the Raspberry Pi](./Steps/WriteThePiCode.md)

1. [Export IoT telemetry to Azure Event Hubs](./Steps/ExportDataToEventHubs.md)

1. [Create a storage account to store telemetry data](./Steps/CreateBlobStorage.md)

1. [Use Azure Stream Analytics to stream data into the storage account](./Steps/ExportDataToBlobStorage.md)

1. [Create an Azure Function triggered by Azure Stream Analytics to check soil moisture](./Steps/CreateFunction.md)

1. [Trigger an Azure IoT Central command if the soil moisture is too low](./Steps/ExecuteIoTCommand.md)

1. [Call Azure Maps to check the weather forecast before sending the needs watering command](./Steps/CheckWeatherWithAzureMaps.md)

1. [Summary](./Steps/Summary.md)

1. [Clean up](./Steps/CleanUp.md)

## Clean up

Don't forget to clean up your Azure resources when you are finished, to avoid spending money, or using up your credit from your free subscription. All the instructions to clean up are in the [Clean up you Azure resources guide](./Steps/CleanUp.md).
