# Environment Monitor

This folder contains a lab with multiple parts working towards an environment monitor using a Raspberry Pi and Azure IoT Services. It is designed for complete beginners who are new to IoT and Azure.

| Author | [Jim Bennett](https://github.com/JimBobBennett) |
|:---|:---|
| Target platform   | Raspberry Pi                                    |
| Hardware required | Raspberry Pi 4<br>Micro SD Card<br>An SD card to USB converter that matches the USB ports on your device if your device doesn't have an SD card slot<br>Raspberry Pi 4 power supply (USB-C)<br>[Grove Pi+ Starter Kit](https://www.seeedstudio.com/GrovePi-Starter-Kit-for-Raspberry-Pi-A-B-B-2-3-CE-certified.html)<br>keyboard, mouse and monitor<br>[micro-HDMI to HDMI adapter or cable](https://www.raspberrypi.org/products/micro-hdmi-to-standard-hdmi-a-cable/) |
| Software required | [Visual Studio Code](http://code.visualstudio.com?WT.mc_id=iotcurriculum-github-jabenn)<br>[Raspberry Pi Imager](https://www.raspberrypi.org/downloads/)<br>*There are optional installs for Windows and Linux that you may need to install later to connect to the Pi, depending on which version of the OS you are using.* |
| Azure Services | [Azure IoT Central](https://azure.microsoft.com/services/iot-central/?WT.mc_id=iotcurriculum-github-jabenn)<br>[Azure Stream Analytics](https://azure.microsoft.com/services/stream-analytics/?WT.mc_id=iotcurriculum-github-jabenn)<br>[Azure Event Hubs](https://azure.microsoft.com/services/event-hubs/?WT.mc_id=iotcurriculum-github-jabenn)<br>[Azure Cosmos DB](https://azure.microsoft.com/services/cosmos-db/?WT.mc_id=iotcurriculum-github-jabenn) |
| Programming Language | Python |
| Prerequisites | You will need to be reasonably proficient at using a computer, including installing software and running commands from a command line or terminal.<br>These labs will use Python, but if you are not proficient in Python you can simply copy and paste the provided code and run it to see the end results, rather than trying to understand the code.<br><br>You will also need an [Azure subscription](https://github.com/microsoft/iot-curriculum/tree/main/labs/iot/environment_monitor#azure-subscription) |
| Date | August 2020 |
| Learning Objectives | Set up IoT Central<br>Send IoT Data from a device to IoT Central<br>Export data from IoT Central<br>Perform anomaly detection with Stream Analytics<br>Visualize results with Jupyter notebooks in Cosmos DB |
| Time to complete | 4 hours |

> If you have some experience with cloud services and are able to program using .NET, there is a hands-on learning path on Microsoft Learn that covers some similar scenarios to this lab, as well as additional scenarios.
>
> [Develop IoT solutions with Azure IoT Central](https://docs.microsoft.com/learn/paths/develop-iot-solutions-with-azure-iot-central/?WT.mc_id=iotcurriculum-github-jabenn)

## The lab parts

This lab has the following parts

1. Set up IoT Central and send simulated data
1. Send mock temperature data from your PC or Mac
1. Set up a Raspberry Pi to send temperature data
1. Set up IoT Central and the Raspberry Pi to send humidity and sound data
1. Perform simple analytics and create an alert on the data using rules
1. Perform more advanced analytics to detect and visualize anomalies in the data
1. Build AI models to make predictions on temperatures

These parts will cover in detail what needs to be done at each step were appropriate, or link to official documentation to cover steps - that way the parts will stay more up to date.

## Azure IoT Central

[Azure IoT Central](https://azure.microsoft.com/services/iot-central/?WT.mc_id=iotcurriculum-github-jabenn) is a software-as-a-service IoT platform which allows you to connect devices to the cloud with minimal code, create dashboards to show IoT data, and export data to other Azure services.

> If you have some experience with cloud services and are able to program using .NET, there is a hands-on learning path on Microsoft Learn that covers some similar scenarios to these labs, as well as additional scenarios:
>
> [Develop IoT solutions with Azure IoT Central](https://docs.microsoft.com/learn/paths/develop-iot-solutions-with-azure-iot-central/?WT.mc_id=iotcurriculum-github-jabenn)

Azure IoT Central has a free tier for up to 2 devices. If you want to add more devices, you will need to pay per device per month. You can find pricing details on the [Azure IoT Central pricing page](https://azure.microsoft.com/pricing/details/iot-central/?WT.mc_id=iotcurriculum-github-jabenn).

All the documentation for IoT Central is available in the [Microsoft IoT Central docs](https://docs.microsoft.com/azure/iot-central/?WT.mc_id=iotcurriculum-github-jabenn). Refer to these docs for the latest up-to date information on using IoT Central.

## Azure subscription

These labs are designed for courses where Azure resources are provided to students by the institution. To try them out, you can use one of our free subscriptions. Head to the [Azure Subscriptions Guide](./azure-subscriptions.md) for from information on setting up a subscription.

## Labs

These labs all build on one another, so you need to work through them in order. Work through as many labs as you want to, but if you don't complete all the labs, make sure you always do the [last one](./steps/clean-up.md) as that cleans up your Azure resources.

1. [Set up IoT Central and send simulated data](./steps/set-up-iot-central.md)
1. [Set up a Raspberry Pi to send temperature data](./steps/set-up-pi.md)
1. [Set up IoT Central and the Raspberry Pi to send humidity and sound data](./steps/set-up-humidity-sound.md)
1. [Perform simple analytics and create an alert on the data using rules](./steps/rules.md)
1. [Perform more advanced analytics to detect and visualize anomalies in the data](./steps/anomaly-detection.md)
1. [Build AI models to make predictions on temperatures](./steps/build-ai-models.md)
1. [Clean up your Azure resources](./steps/clean-up.md)

## Clean up

Don't forget to clean up your Azure resources when you are finished, to avoid spending money, or using up your credit from your free subscription. All the instructions to clean up are in the [Clean up you Azure resources guide](./steps/clean-up.md).
