#include "Config.h"
#include "WebServer.h"

#include <WiFi.h>

// Create the webserver
WebServer *webServer;

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

  // Initialise the web server ready to respond to web requests
  webServer = new WebServer();
}

// The loop method is called repeatedly and is used as an event loop
// for the app. In this app, there is nothing to do as the web server
// handles everything, so just delay for 10 seconds every loop
// to allow the web server to process requests
void loop()
{
  delay(10000);
}
