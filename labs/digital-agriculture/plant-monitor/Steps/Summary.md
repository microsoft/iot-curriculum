# Summary

In the [previous step](./CheckWeatherWithAzureMaps.md) you called Azure Maps to check the weather forecast before sending the needs watering command. This step gives a summary of the completed solution.

## What you have built

In this workshop, you built an IoT device to capture environment data from sensors, set up an IoT Central app as a dashboard for all the data, sent telemetry to storage, and queried based on average telemetry and weather data to see if the plant needed watering.

### The IoT Device

The IoT Device is a Raspberry Pi running Raspbian Lite. It is connected to a soil sensor, and a temperature, humidity and pressure sensor. It is also connected to a LED to indicate if the plant needs water.

The Raspberry Pi runs a Python app that connects to Azure IoT Central to send telemetry data, and receive a command to turn the LED on and off.

### The Azure IoT Central app

The Azure IoT Central app is the central point for ingesting telemetry data from the Raspberry Pi, and sending commands. The telemetry is shown on a dashboard, showing the current and historical values. The Azure IoT Central app is configued to send telemetry to an Azure Event Hub.

### Stream analytics to blob storage

There is an Azure Stream Analytics job set up to stream data from the Azure Event Hub into an Azure Storage Account, storing the data in blob storage.

### Stream analytics to a function app

There is an Azure Stream Analytics job set up to create an average of the data over a 5 minute window, and send this to an Azure Function

### Azure Function app

The Azure Function app is called with average telemetry values over a 5 minute window. It's job is to determine if the plant needs watering or not. It checks the weather using Azure Maps. If rain is forecast, then the plant doesn't need to be watered. If there is no rain forecast, it checks the soil moisture level, and if it is too low then the plant needs to be watered. Once this decision is made, a command on the Azure IoT Central app is executed to turn an LED on or off on the Raspberry Pi.

## Suggestions to improve this app

There are many ways to improve this app. Suggestions include:

* Handling multiple devices. To do this the device id would need to be sent in the telemetry so the Azure Function knows which device to execute the command for.

* Handle devices in multiple locations. To do this, the Azure Function will need to know the location of each device to check the local weather. This can be done using a Cloud Property in Azure IoT Central with the latitude and longitude of each device, retrieved using the device id.

* Add a second device to water the plant. Using an IoT powered watering system, actually set up automated watering controlled by a different device.

* Use AI and the temperature and humidity data to predict the weather instead of using Azure Maps. You can read a way to do this in the [IoT docs](https://docs.microsoft.com/azure/iot-hub/iot-hub-weather-forecast-machine-learning?WT.mc_id=academic-7372-jabenn)

Have a go at adding some of these yourself.

<hr>

This step gave a summary of the completed solution. In the [next step](./CleanUp.md) you will clean up your resources.
