#ifndef _CONFIG_H_
#define _CONFIG_H_

// The SSID and password of the WiFI network to use.
// Replace these with your network credentials
// Note that this won't work with enterprise security
const char * const ssid = "<Your SSID>";
const char * const password = "<Your password>";

// The prediction URL and key come from Custom Vision.
// Set these to the value from your published iteration
const char * const predictionUrl = "<Your prediction URL>";
const char * const predictionKey = "<Your prediction key>";

// The device connection string comes from Azure IoT Hub
// Set these to the value for your device, not the Hub
const char * const deviceConnectionString = "<Device connection string>";

#endif