# GPS Lab

This folder contains a lab which displays the GPS coordinate on a map in real time using a Raspberry Pi and Azure IoT services.

The end project collects GPS coordinates from a GPS sensor attached to a Raspberry Pi and transmits the data to [Azure IoT Hub](https://azure.microsoft.com/services/iot-hub/?WT.mc_id=academic-7372-jabenn). This location data is then visualized on a web application that uses [Azure Maps](https://azure.microsoft.com/services/azure-maps/?WT.mc_id=academic-7372-jabenn).

| Author | [Tanmoy Rajguru](https://github.com/Tanmoy-TCS), [Jim Bennett](https://GitHub.com/JimBobBennett) |
|:---|:---|
| Target platform   | <ul><li>Raspberry Pi</li></ul> |
| Hardware required | <ul><li>[NEO-6M GPS Receiver Module with external antenna](https://www.amazon.com/Navigation-Positioning-Microcontroller-Compatible-Sensitivity/dp/B084MK8BS2)</li><li>4 female to female jumper cables</li><li>Raspberry Pi 4</li><li>Micro SD Card</li><li>An SD card to USB converter that matches the USB ports on your device if your device doesn't have an SD card slot</li><li>Raspberry Pi 4 power supply (USB-C)</li><li>keyboard, mouse and monitor</li><li>[micro-HDMI to HDMI adapter or cable](https://www.raspberrypi.org/products/micro-hdmi-to-standard-hdmi-a-cable/)</li></ul> |
| Software required | <ul><li>[Visual Studio Code](http://code.visualstudio.com?WT.mc_id=academic-7372-jabenn)</li></ul><ul><li>[Raspberry Pi Imager](https://www.raspberrypi.org/downloads/)</li></ul>*There are optional installs for Windows and Linux that you may need to install later to connect to the Pi, depending on which version of the OS you are using.* |
| Azure Services | <ul><li>[Azure IoT Hub](https://azure.microsoft.com/services/iot-hub/?WT.mc_id=academic-7372-jabenn)</li><li>[Azure Maps](https://azure.microsoft.com/services/azure-maps/?WT.mc_id=academic-7372-jabenn)</li><li>[Azure App Service](https://azure.microsoft.com/services/app-service/?WT.mc_id=academic-7372-jabenn))</li></ul> |
| Programming Language | <ul><li>Python</li><li>JavaScript</li></ul> |
| Prerequisites | You will need to be reasonably proficient at using a computer, including installing software and running commands from a command line or terminal.<br>These labs will use Python and JavaScript, but if you are not proficient in these languages you can simply copy and paste the provided code and run it to see the end results, rather than trying to understand the code.<br><br>If you want to learn Python, check out these free resources:<br><ul><li>[Python for beginners video series on Channel9](https://channel9.msdn.com/Series/Intro-to-Python-Development?WT.mc_id=academic-7372-jabenn)</li><li>[Take your first steps with Python learning path on Microsoft Learn](https://docs.microsoft.com/learn/paths/python-first-steps/?WT.mc_id=academic-7372-jabenn)</li></ul><br>If you want to learn JavaScript, check out these free resources:<ul><li>[Beginner's Series to: JavaScript - a beginner's guide to JavaScript on Node.js](https://channel9.msdn.com/Series/Beginners-Series-to-JavaScript?WT.mc_id=academic-7372-jabenn)</li></ul><br>You will also need an [Azure subscription](https://github.com/microsoft/iot-curriculum/tree/main/labs/iot/environment_monitor#azure-subscription)<br>If you are new to Azure, check out these free resources:<ul><li>[Azure Fundamentals learning path on Microsoft Learn](https://docs.microsoft.com/learn/paths/azure-fundamentals/?WT.mc_id=academic-7372-jabenn)</li></ul> |
| Date | November 2020 |
| Learning Objectives | <ul><li>Set up IoT Hub</li><li>Set up Azure Maps</li><li>Read GPS data from the GPS Module Receiver</li><li>Send GPS Data from a device to IoT Hub</li><li>Read the GPS data from IoT Hub</li><li>Show the GPS location in Azure Maps with a Python Flask web application</li></ul> |
| Time to complete | 2 hours |

## The lab parts

This lab has the following parts

1. Set up the Azure services
1. Set up a Raspberry Pi with a GPS receiver to send GPS data to IoT Hub
1. Set up a web application to show the GPS data coming from IoT Hub

These parts will cover in detail what needs to be done at each step were appropriate, or link to official documentation to cover steps - that way the parts will stay more up to date.

## Azure subscription

These labs are designed for courses where Azure resources are provided to students by the institution. To try them out, you can use one of our free subscriptions. Head to the [Azure Subscriptions Guide](../../../azure-subscription.md) for more information on setting up a subscription.

## Labs

If you don't complete all the labs, make sure you always do the [last one](./steps/clean-up.md) as that cleans up your Azure resources.

1. [Set up the Azure services](./steps/set-up-azure-services.md)

1. [Set up the Raspberry Pi](./steps/set-up-pi.md)

1. [Code the Raspberry Pi to send GPS data to IoT Hub](./steps/write-pi-code.md)

1. [Code a web app to visualize the GPS location on a map](./steps/web-app.md)

1. [Clean up](./steps/clean-up.md)

## Clean up

Don't forget to clean up your Azure resources when you are finished, to avoid spending money, or using up your credit from your free subscription. All the instructions to clean up are in the [Clean up you Azure resources guide](./steps/clean-up.md).
