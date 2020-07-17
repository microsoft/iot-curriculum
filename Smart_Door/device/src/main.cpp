
#include <WiFi.h>
#include "Esp32MQTTClient.h"
#include <ArduinoJson.h>
#include <Stepper.h>

#define STEPS 100
#define INTERVAL 10000
#define MESSAGE_MAX_LEN 512

const char* ssid     = "Micronet";
const char* password = "lalalala";
static const char* connectionString = "HostName=University-IoT-Cart.azure-devices.net;DeviceId=DoorMonitor001;SharedAccessKey=4nl/aeAOildT9flb1tu2ePiC8LqVZQIfdBwm/88pBds=";
const char *messageData = "{\"messageId\":%d, \"DoorStatus\":\"%s\", \"device_type\":\"door_monitor\"}";
Stepper stepper(STEPS, 8, 9, 10, 11);

static bool hasIoTHub = false;
static bool hasWifi = false;
int messageCount = 1;
static bool messageSending = true;
static uint64_t send_interval_ms;


const int numReadings = 10;

int readings[numReadings];      // the readings from the analog input
int readIndex = 0;              // the index of the current reading
int total = 0;                  // the running total
int average = 0;                // the average

bool doorOpen = false;
bool doorOpenStatus = false;
bool isInit = true; //is initial startup if so it needs to send

static void SendConfirmationCallback(IOTHUB_CLIENT_CONFIRMATION_RESULT result)
{

  if (result == IOTHUB_CLIENT_CONFIRMATION_OK)
  {
    Serial.println("Send Confirmation Callback finished.");
  }
}

static void MessageCallback(const char* payLoad, int size)
{
  Serial.println("Message callback:");
  Serial.println(payLoad);
  StaticJsonDocument<200> doc;
    DeserializationError error = deserializeJson(doc, payLoad);

  // Test if parsing succeeds.
  if (error) {
    Serial.print(F("deserializeJson() failed: "));
    Serial.println(error.c_str());
    return;
  }
 const char* lockunlock = doc["lockunlock"];
char lockstatus[] = "lock";
  int val = analogRead(0);


 
  if(strcmp(lockunlock, lockstatus))
  {
    Serial.println("unlocking");
    val = 100 - val;   
    val = 100;
  }else
  {
    Serial.println("locking");
    val = 0 - val;
    val = 0;
  }
 stepper.step(val);
 
}
/*
static void DeviceTwinCallback(DEVICE_TWIN_UPDATE_STATE updateState, const unsigned char *payLoad, int size)
{
  char *temp = (char *)malloc(size + 1);
  if (temp == NULL)
  {
    return;
  }
  memcpy(temp, payLoad, size);
  temp[size] = '\0';
  // Display Twin message.
  Serial.println(temp);
  free(temp);
}
*/
static int  DeviceMethodCallback(const char *methodName, const unsigned char *payload, int size, unsigned char **response, int *response_size)
{
  LogInfo("Try to invoke method %s", methodName);
  const char *responseMessage = "\"Successfully invoke device method\"";
  int result = 200;

  if (strcmp(methodName, "start") == 0)
  {
    LogInfo("Start sending temperature and humidity data");
    messageSending = true;
  }
  else if (strcmp(methodName, "stop") == 0)
  {
    LogInfo("Stop sending temperature and humidity data");
    messageSending = false;
  }
  else
  {
    LogInfo("No method %s found", methodName);
    responseMessage = "\"No method found\"";
    result = 404;
  }

  *response_size = strlen(responseMessage) + 1;
  *response = (unsigned char *)strdup(responseMessage);

  return result;
}



void setup() {
  Serial.begin(9600);
  Serial.println("ESP32 Device");
  Serial.println("Initializing...");
  Serial.println(" > WiFi");
  Serial.println("Starting connecting WiFi.");
  stepper.setSpeed(30);
  delay(10);
  WiFi.mode(WIFI_AP);
  WiFi.begin(ssid, password);
  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
    hasWifi = false;
  }
  hasWifi = true;
  
  Serial.println("WiFi connected");
  Serial.println("IP address: ");
  Serial.println(WiFi.localIP());
  Serial.println(" > IoT Hub");
  if (!Esp32MQTTClient_Init((const uint8_t*)connectionString, true))
  {
    hasIoTHub = false;
    Serial.println("Initializing IoT hub failed.");
    return;
  }
  hasIoTHub = true;
  Esp32MQTTClient_SetSendConfirmationCallback(SendConfirmationCallback);
  Esp32MQTTClient_SetMessageCallback(MessageCallback);
  //Esp32MQTTClient_SetDeviceTwinCallback(DeviceTwinCallback);
  //Esp32MQTTClient_SetDeviceMethodCallback(DeviceMethodCallback);
  Serial.println("Start sending events.");
  randomSeed(analogRead(0));
  send_interval_ms = millis();

  for (int thisReading = 0; thisReading < numReadings; thisReading++) {
    readings[thisReading] = 0;
  }



}



void loop() {
if (hasWifi && hasIoTHub)
  {
    if (messageSending && 
        (int)(millis() - send_interval_ms) >= INTERVAL)
    {

  
        total = total - readings[readIndex];
  // read from the sensor:
  readings[readIndex] = hallRead();
  // add the reading to the total:
  total = total + readings[readIndex];
  // advance to the next position in the array:
  readIndex = readIndex + 1;

  // if we're at the end of the array...
  if (readIndex >= numReadings) {
    // ...wrap around to the beginning:
    readIndex = 0;
  }

  // calculate the average:
  average = total / numReadings;
  
  doorOpen = average > 10;

  char* doorText = "closed";

  if(doorOpen != doorOpenStatus || isInit)
  {
  isInit = false;
//char lockstatus[] = "lock";
//  if(strcmp(lockunlock, lockstatus))

  if(doorOpen)
  {
    doorText = "open";
    }
     // Send teperature data
      char messagePayload[MESSAGE_MAX_LEN];
      snprintf(messagePayload, MESSAGE_MAX_LEN, messageData, messageCount++, doorText);
      Serial.println(messagePayload);
      EVENT_INSTANCE* message = Esp32MQTTClient_Event_Generate(messagePayload, MESSAGE);
      Esp32MQTTClient_SendEventInstance(message);
      send_interval_ms = millis();
   
  doorOpenStatus = doorOpen;
  }

  

      }
    else
    {
      Esp32MQTTClient_Check();
    }
  }
  delay(10);
}
