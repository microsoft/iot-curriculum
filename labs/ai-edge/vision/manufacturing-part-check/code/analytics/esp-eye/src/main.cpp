// Copyright (c) Microsoft Corporation.
// Licensed under the MIT license.

#include "Config.h"
#include "IoTHubService.h"

#include <Arduino.h>
#include <WiFi.h>

// The Connection to IoT Hub
IoTHubService *iotHubService;

// The time needs to be set, so set up details for an NTP connection
const char* ntpServer = "pool.ntp.org";
const long  gmtOffset_sec = 0;
const int   daylightOffset_sec = 0;

// Arduino setup function. This is run once by the OS when the
// device first starts up.
// This function intializes the WiFi connection, and starts the web server
void setup()
{
  // Start the serial port at the PlatformIO default speed for debugging
  // You can view the output of this code by connecting to the serial monitor
  Serial.begin(9600);
  Serial.println();

  // Connect to Wi-Fi using the SSID and password from the Config.h file
  WiFi.begin(ssid, password);

  // It can take a few seconds to connect, so loop whilst waiting for the WiFi
  // to connect, waiting a second each time before checking the connection
  while (WiFi.status() != WL_CONNECTED)
  {
    delay(1000);
    Serial.println("Connecting to WiFi...");
  }

  //init and get the time
  configTime(gmtOffset_sec, daylightOffset_sec, ntpServer);

  // Initialise the IoT Hub service to respond to messages
  iotHubService = new IoTHubService();
}

// The loop method is called repeatedly and is used as an event loop
// for the app. This app needs to give the IoT Hub connection time to
// processes messages, so allocate the time, then delay for a millisecond
void loop()
{
  iotHubService->DoWork();
  delay(1);
}
