# Environment Monitor

This folder contains a lab with multiple parts working towards an environment monitor using a Raspberry Pi and Azure IoT Services. It is designed for complete beginners who are new to IoT and Azure.

> If you don't have access to a Raspberry Pi, instructions are included to run the Pi code on a PC or Mac, using simulated data instead of real data. Follow the instructions below, and in the sections that mention the Pi, you will find alternative instructions to create a virtual IoT device running on your PC or Mac.

| Author | [Jim Bennett](https://github.com/JimBobBennett) |
|:---|:---|
| Target platform   | <ul><li>Raspberry Pi</li></ul><i>Optionally you can run this on a PC or Mac using a virtual IoT device</i> |
| Hardware required | If you are running this on a Raspberry Pi:<ul><li>Raspberry Pi 4</li><li>Micro SD Card</li><li>An SD card to USB converter that matches the USB ports on your device if your device doesn't have an SD card slot</li><li>Raspberry Pi 4 power supply (USB-C)</li><li>[Grove Pi+ Starter Kit](https://www.seeedstudio.com/GrovePi-Starter-Kit-for-Raspberry-Pi-A-B-B-2-3-CE-certified.html)</li><li>keyboard, mouse and monitor</li><li>[micro-HDMI to HDMI adapter or cable](https://www.raspberrypi.org/products/micro-hdmi-to-standard-hdmi-a-cable/)</li></ul> |
| Software required | <ul><li>[Visual Studio Code](http://code.visualstudio.com?WT.mc_id=academic-7372-jabenn)</li></ul><br>If you are running this on a Raspberry Pi:<ul><li>[Raspberry Pi Imager](https://www.raspberrypi.org/downloads/)</li></ul>*There are optional installs for Windows and Linux that you may need to install later to connect to the Pi, depending on which version of the OS you are using.* |
| Azure Services | <ul><li>[Azure IoT Central](https://azure.microsoft.com/services/iot-central/?WT.mc_id=academic-7372-jabenn)</li><li>[Azure Stream Analytics](https://azure.microsoft.com/services/stream-analytics/?WT.mc_id=academic-7372-jabenn)</li><li>[Azure Event Hubs](https://azure.microsoft.com/services/event-hubs/?WT.mc_id=academic-7372-jabenn)</li><li>[Azure Cosmos DB](https://azure.microsoft.com/services/cosmos-db/?WT.mc_id=academic-7372-jabenn)</li></ul> |
| Programming Language | <ul><li>Python</li></ul> |
| Prerequisites | You will need to be reasonably proficient at using a computer, including installing software and running commands from a command line or terminal.<br>These labs will use Python, but if you are not proficient in Python you can simply copy and paste the provided code and run it to see the end results, rather than trying to understand the code.<br>If you want to learn Python, check out these free resources:<br><ul><li>[Python for beginners video series on Channel9](https://channel9.msdn.com/Series/Intro-to-Python-Development?WT.mc_id=academic-7372-jabenn)</li><li>[Take your first steps with Python learning path on Microsoft Learn](https://docs.microsoft.com/learn/paths/python-first-steps/?WT.mc_id=academic-7372-jabenn)</li></ul><br>You will also need an [Azure subscription](https://github.com/microsoft/iot-curriculum/tree/main/labs/iot/environment_monitor#azure-subscription)<br>If you are new to Azure, check out these free resources:<ul><li>[Azure Fundamentals learning path on Microsoft Learn](https://docs.microsoft.com/learn/paths/azure-fundamentals/?WT.mc_id=academic-7372-jabenn)</li></ul> |
| Date | August 2020 |
| Learning Objectives | <ul><li>Set up IoT Central</li><li>Send IoT Data from a device to IoT Central</li><li>Export data from IoT Central</li><li>Perform anomaly detection with Stream Analytics</li><li>Visualize results with Jupyter notebooks in Cosmos DB</li></ul> |
| Time to complete | 4 hours |
| Video walkthrough | YouTube playlists with video walkthroughs are available for this lab, either using a Raspberry Pi and Grove Pi+, or using a virtual device.<ul><li>[Video walkthrough playlist using a Raspberry Pi](https://www.youtube.com/playlist?list=PLGi0uFHAUvEGIXv0dm93Dca84FT3EXGY0)</li><li>[Video walkthrough playlist using a virtual IoT device](https://www.youtube.com/playlist?list=PLGi0uFHAUvEFQGKn_56f1L8LMPvhHbvOE)</li></ul>|

> If you have some experience with cloud services and are able to program using .NET, there is a hands-on learning path on Microsoft Learn that covers some similar scenarios to this lab, as well as additional scenarios.
>
> [Develop IoT solutions with Azure IoT Central](https://docs.microsoft.com/learn/paths/develop-iot-solutions-with-azure-iot-central/?WT.mc_id=academic-7372-jabenn)

## The lab parts

This lab has the following parts

1. Set up IoT Central and send simulated data
1. Set up a Raspberry Pi or virtual IoT device to send temperature data
1. Set up IoT Central and the Raspberry Pi/virtual IoT device to send humidity and sound data
1. Perform simple analytics and create an alert on the data using rules
1. Perform more advanced analytics to detect and visualize anomalies in the data

These parts will cover in detail what needs to be done at each step were appropriate, or link to official documentation to cover steps - that way the parts will stay more up to date.

## Azure IoT Central

[Azure IoT Central](https://azure.microsoft.com/services/iot-central/?WT.mc_id=academic-7372-jabenn) is a software-as-a-service IoT platform which allows you to connect devices to the cloud with minimal code, create dashboards to show IoT data, and export data to other Azure services.

> If you have some experience with cloud services and are able to program using .NET, there is a hands-on learning path on Microsoft Learn that covers some similar scenarios to these labs, as well as additional scenarios:
>
> [Develop IoT solutions with Azure IoT Central](https://docs.microsoft.com/learn/paths/develop-iot-solutions-with-azure-iot-central/?WT.mc_id=academic-7372-jabenn)

Azure IoT Central has a free tier for up to 2 devices. If you want to add more devices, you will need to pay per device per month. You can find pricing details on the [Azure IoT Central pricing page](https://azure.microsoft.com/pricing/details/iot-central/?WT.mc_id=academic-7372-jabenn).

All the documentation for IoT Central is available in the [Microsoft IoT Central docs](https://docs.microsoft.com/azure/iot-central/?WT.mc_id=academic-7372-jabenn). Refer to these docs for the latest up-to date information on using IoT Central.

## Azure IoT SDK

The Raspberry Pi or simulated device will connect to Azure IoT Central using the [Azure IoT Python SDK](https://github.com/Azure/azure-iot-sdk-python). This is an open-source Python library that can talk to Azure IoT Central, register devices, and send and receive messages. As this is open-source, you can read the source code to get a deeper understanding of how it works, report bugs or add fixes via pull requests.

This library connects using [MQTT](https://mqtt.org) either directly,or over websockets. MQTT is a popular standard for communicating with IoT devices, it's a lightweight protocol for publish/subscribe message transport. You can read more on MQTT and the implementation in the [Communicate with your IoT hub using the MQTT protocol documentation](https://docs.microsoft.com/azure/iot-hub/iot-hub-mqtt-support?WT.mc_id=academic-7372-jabenn). This documentation covers the protocol and how messages are published or subscribed to.

## Azure subscription

These labs are designed for courses where Azure resources are provided to students by the institution. To try them out, you can use one of our free subscriptions. Head to the [Azure Subscriptions Guide](../../../azure-subscription.md) for more information on setting up a subscription.

## Labs

These labs all build on one another, so you need to work through them in order. Work through as many labs as you want to, but if you don't complete all the labs, make sure you always do the [last one](./steps/clean-up.md) as that cleans up your Azure resources.

Some labs have two options - select the Raspberry Pi option if you have a Pi and the sensors, otherwise use the virtual device option.

1. [Set up IoT Central and send simulated data](./steps/set-up-iot-central.md)

1. [Add a physical device to IoT Central](./steps/add-pi-to-iot-central.md)

1. Set up an IoT device to send temperature data:
    * [Set up a Raspberry Pi to send temperature data](./steps/set-up-pi.md)
    * [Set up a virtual IoT device to send temperature data](./steps/set-up-virtual-pi.md)

1. [Set up IoT Central to receive humidity and sound data](./steps/set-up-humidity-sound.md)

1. Set up an IoT device to send humidity and sound data
    * [Set up the Raspberry Pi to send humidity and sound data](./steps/set-up-pi-humidity-sound.md)
    * [Set up the virtual IoT device to send humidity and sound data](./steps/set-up-virtual-humidity-sound.md)

1. [Perform simple analytics and create an email alert on the data using rules](./steps/rules.md)

1. Set up an IoT device to listen for an IoT Central command
    * [Set up the Raspberry Pi to light an LED triggered by an IoT Central command](./steps/rules-pi-led.md)
    * [Set up the virtual IoT device Pi to report to the console triggered by an IoT Central command](./steps/rules-virtual-led.md)

1. [Create the IoT Central command and trigger it from a rule](./steps/rules-command.md)

1. [Perform more advanced analytics to detect and visualize anomalies in the data](./steps/anomaly-detection.md)

1. [Add more sensors](./steps/add-more-sensors.md)

1. [Clean up](./steps/clean-up.md)

## Clean up

Don't forget to clean up your Azure resources when you are finished, to avoid spending money, or using up your credit from your free subscription. All the instructions to clean up are in the [Clean up you Azure resources guide](./steps/clean-up.md).
