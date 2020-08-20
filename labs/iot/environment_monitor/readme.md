# Environment Monitor

This folder contains a lab with multiple parts working towards an environment monitor using a Raspberry Pi and Azure IoT Services. It is designed for complete beginners who are new to IoT and Azure.

> If you have some experience with cloud services and are able to program using .NET, there is a hands-on learning path on Microsoft Learn that covers some similar scenarios to this lab, as well as additional scenarios.
>
> [Develop IoT solutions with Azure IoT Central](https://docs.microsoft.com/learn/paths/develop-iot-solutions-with-azure-iot-central/?WT.mc_id=iotcurriculum-github-jabenn)

## The lab parts

This lab has the following parts

1. Set up IoT Central and send simulated data
1. Send mock temperature data from your PC or Mac
1. Set up a Raspberry Pi to send temperature data
1. Set up IoT Central and the Raspberry Pi to send humidity and sound data
1. Perform simple analytics and create alerts on the data using rules
1. Perform more advanced analytics to detect anomalies in the data
1. Build AI models to make predictions on temperatures

These parts will cover in detail what needs to be done at each step were appropriate, or link to official documentation to cover steps - that way the parts will stay more up to date.

## Azure IoT Central

[Azure IoT Central](https://azure.microsoft.com/services/iot-central/?WT.mc_id=iotcurriculum-github-jabenn) is a software-as-a-service IoT platform which allows you to connect devices to the cloud with minimal code, create dashboards to show IoT data, and export data to other Azure services.

If you have some experience with cloud services and are able to program using .NET, there is a hands-on learning path on Microsoft Learn that covers some similar scenarios to these labs, as well as additional scenarios:

[Develop IoT solutions with Azure IoT Central](https://docs.microsoft.com/learn/paths/develop-iot-solutions-with-azure-iot-central/?WT.mc_id=iotcurriculum-github-jabenn)

Azure IoT Central has a free tier for up to 2 devices. If you want to add more devices, you will need to pay per device per month. You can find pricing details on the [Azure IoT Central pricing page](https://azure.microsoft.com/pricing/details/iot-central/?WT.mc_id=iotcurriculum-github-jabenn).

## Pre-requisites

### Hardware requirements

To work through these labs you will need:

* A Raspberry Pi 4
* A micro SD Card
* An SD card to USB converter that matches the USB ports on your device if you r device doesn't have an SD card slot
* A Raspberry Pi 4 power supply (USB-C)
* [A Grove Pi+ Starter Kit](https://www.seeedstudio.com/GrovePi-Starter-Kit-for-Raspberry-Pi-A-B-B-2-3-CE-certified.html)
* A PC or Mac
* WiFi or wired internet
* A keyboard, mouse and monitor
* A [micro-HDMI to HDMI adapter or cable](https://www.raspberrypi.org/products/micro-hdmi-to-standard-hdmi-a-cable/)

### Software requirements

On your PC or Mac, you will need the following installed:

* [Visual Studio Code](http://code.visualstudio.com?WT.mc_id=iotcurriculum-github-jabenn)
* [Raspberry Pi Imager](https://www.raspberrypi.org/downloads/)

There are optional installs for Windows and Linux that you may need to install later to connect to the Pi, depending on which version of the OS you are using.

### Technology skills

You will need to be reasonably proficient at using a computer, including installing software and running commands from a command line or terminal.

These labs will use Python, but if you are not proficient in Python you can simply copy and paste the provided code and run it to see the end results, rather than trying to understand the code.

## Azure subscription

These labs are designed for courses where Azure resources are provided to students by the institution. To try them out, you can use one of our free subscriptions. Head to the [Azure Subscriptions Guide](./azure-subscriptions.md) for from information on setting up a subscription.

## Labs

These labs all build on one another, so you need to work through them in order.

1. [Set up IoT Central and send simulated data](./steps/set-up-iot-central.md)
1. [Set up a Raspberry Pi to send temperature data](./steps/set-up-pi.md)
1. [Set up IoT Central and the Raspberry Pi to send humidity and sound data](./steps/set-up-humidity-sound.md)
1. [Perform simple analytics and create alerts on the data using rules](./steps/rules.md)
1. [Perform more advanced analytics to detect anomalies in the data](./steps/anomaly-detection.md)
1. [Build AI models to make predictions on temperatures](./steps/build-ai-models.md)
1. [Clean up](./steps/clean-up.md)
