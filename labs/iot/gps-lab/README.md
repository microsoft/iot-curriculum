# GPS Lab

This folder contains a lab which displays the GPS coordinate in an Azure Maps in real time. It collects the GPS coordinates from a GPS sensor attached to a Raspberry Pi and transmits the data
to IoT hub. The web application containing the Azure Maps reads the data from IoT Hub and displays on the map.

| Author | [Tanmoy Rajguru](https://github.com/Tanmoy-TCS) |
|:---|:---|
| Team | [Microsoft AI & IoT Insiders Lab](https://microsoftiotinsiderlabs.com/en) |
| Target platform   | <ul><li>Raspberry Pi</li><li>Python with Flask</li></ul> |
| Hardware required | <ul><li>[GPS Module Receiver](https://www.amazon.com/Navigation-Positioning-Microcontroller-Compatible-Sensitivity/dp/B084MK8BS2)</li><li>Raspberry Pi 4</li><li>Micro SD Card</li><li>An SD card to USB converter that matches the USB ports on your device if your device doesn't have an SD card slot</li><li>Raspberry Pi 4 power supply (USB-C)</li><li>keyboard, mouse and monitor</li><li>[micro-HDMI to HDMI adapter or cable](https://www.raspberrypi.org/products/micro-hdmi-to-standard-hdmi-a-cable/)</li></ul> |
| Software required | <ul><li>[Visual Studio Code](http://code.visualstudio.com?WT.mc_id=iotcurriculum-github-jabenn)</li></ul><ul><li>[Raspberry Pi Imager](https://www.raspberrypi.org/downloads/)</li></ul>*There are optional installs for Windows and Linux that you may need to install later to connect to the Pi, depending on which version of the OS you are using.* |
| Azure Services | <ul><li>[Azure IoT Hub](https://azure.microsoft.com/services/iot-hub/?WT.mc_id=iotcurriculum-github-jabenn)</li><li>[Azure Maps](https://azure.microsoft.com/services/azure-maps/?WT.mc_id=iotcurriculum-github-jabenn)</li></ul> |
| Programming Language | <ul><li>Python</li></ul> |
| Prerequisites | You will need to be reasonably proficient at using a computer, including installing software and running commands from a command line or terminal.<br>These labs will use Python, but if you are not proficient in Python you can simply copy and paste the provided code and run it to see the end results, rather than trying to understand the code.<br>If you want to learn Python, check out these free resources:<br><ul><li>[Python for beginners video series on Channel9](https://channel9.msdn.com/Series/Intro-to-Python-Development?WT.mc_id=iotcurriculum-github-jabenn)</li><li>[Take your first steps with Python learning path on Microsoft Learn](https://docs.microsoft.com/learn/paths/python-first-steps/?WT.mc_id=iotcurriculum-github-jabenn)</li></ul><br>You will also need an [Azure subscription](https://github.com/microsoft/iot-curriculum/tree/main/labs/iot/environment_monitor#azure-subscription)<br>If you are new to Azure, check out these free resources:<ul><li>[Azure Fundamentals learning path on Microsoft Learn](https://docs.microsoft.com/learn/paths/azure-fundamentals/?WT.mc_id=iotcurriculum-github-jabenn)</li></ul> |
| Date | September 2020 |
| Learning Objectives | <ul><li>Set up IoT Hub</li><li>Set up Azure Maps</li><li>Read GPS data from the GPS Module Receiver</li><li>Send GPS Data from a device to IoT Hub</li><li>Read the GPS data from IoT Hub</li><li>Show the GPS location in Azure Maps with a Python Flask web application</li></ul> |
| Time to complete | 4 hours |

## The lab parts

This lab has the following parts

1. Set up Azure Maps 
1. Set up IoT Hub
2. Set up a Raspberry Pi with GPS receiver
4. Set up the web server to show the GPS data coming from IoT Hub

These parts will cover in detail what needs to be done at each step were appropriate, or link to official documentation to cover steps - that way the parts will stay more up to date.

## Azure subscription

These labs are designed for courses where Azure resources are provided to students by the institution. To try them out, you can use one of our free subscriptions. Head to the [Azure Subscriptions Guide](../../../azure-subscription.md) for more information on setting up a subscription.

## Labs

These labs all build on one another, so you need to work through them in order. Work through as many labs as you want to, but if you don't complete all the labs, make sure you always do the [last one](./steps/clean-up.md) as that cleans up your Azure resources.

1. [Set up Azure Maps](./steps/set-up-azure-maps.md)

1. [Set up IoT Hub](./steps/set-up-iot-hub.md)

1. [Set up Raspberry Pi](../environment-monitor/steps/set-up-pi.md)

1. [Add the GPS Sensor to the Raspberry Pi](./steps/add-gps-to-pi.md)

1. [Run the web app](./steps/set-up-web-app.md)

1. [Clean up](./steps/clean-up.md)

## Clean up

Don't forget to clean up your Azure resources when you are finished, to avoid spending money, or using up your credit from your free subscription. All the instructions to clean up are in the [Clean up you Azure resources guide](./steps/clean-up.md).
