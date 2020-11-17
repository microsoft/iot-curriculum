#include "AZ3166WiFi.h"
#include "DevKitMQTTClient.h"
#include "Sensor.h"
#include "parson.h"

DevI2C *ext_i2c;
HTS221Sensor *ht_sensor;
RGB_LED rgbLed;

static float temperatureThreshold = 25.0;

void initSensor() {
  ext_i2c = new DevI2C(D14, D15);
  ht_sensor = new HTS221Sensor(*ext_i2c);
  ht_sensor->init(NULL);
}

float getSensorData() {
  float temperature;

  ht_sensor->enable();
  ht_sensor->getTemperature(&temperature);
  ht_sensor->disable();
  ht_sensor->reset();

  char buff[16];
  sprintf(buff, "Temp:%sC\r\n", f2s(temperature, 1));
  Screen.print(1, buff);

  sprintf(buff, "Threshold:%sC\r\n", f2s(temperatureThreshold, 1));
  Screen.print(2, buff);

  return temperature;
}

static void DeviceTwinCallback(DEVICE_TWIN_UPDATE_STATE updateState, const unsigned char *payLoad, int size) {
  char *message = (char *)malloc(size + 1);
  memcpy(message, payLoad, size);
  message[size] = '\0';

  JSON_Value *root_value = json_parse_string(message);
  JSON_Object *root_object = json_value_get_object(root_value);

  if (updateState == DEVICE_TWIN_UPDATE_COMPLETE) {
    JSON_Object *desired_object = json_object_get_object(root_object, "desired");
    if (desired_object != NULL) {
      if (json_object_has_value(desired_object, "temperatureThreshold")) {
        temperatureThreshold = json_object_get_number(desired_object, "temperatureThreshold");
      }
    }
  }
  else {
    if (json_object_has_value(root_object, "temperatureThreshold")) {
      temperatureThreshold = json_object_get_number(root_object, "temperatureThreshold");
    }
  }
  
  json_value_free(root_value);
  free(message);
}

void setup() {
  initSensor();
  WiFi.begin();
  DevKitMQTTClient_Init(true);
  DevKitMQTTClient_SetDeviceTwinCallback(DeviceTwinCallback);
}

void sendData(const char *data) {
  time_t t = time(NULL);
  char buf[sizeof "2011-10-08T07:07:09Z"];
  strftime(buf, sizeof buf, "%FT%TZ", gmtime(&t));

  EVENT_INSTANCE* message = DevKitMQTTClient_Event_Generate(data, MESSAGE);

  DevKitMQTTClient_Event_AddProp(message, "$$CreationTimeUtc", buf);
  DevKitMQTTClient_Event_AddProp(message, "$$MessageSchema", "temperature;v1");
  DevKitMQTTClient_Event_AddProp(message, "$$ContentType", "JSON");

  DevKitMQTTClient_SendEventInstance(message);
}

void loop() {
  float temperature = getSensorData();

  if (temperature > temperatureThreshold) {
    rgbLed.setColor(255, 0, 0);
  }
  else {  
    rgbLed.setColor(0, 0, 255);
  }

  char sensorData[200];
  sprintf_s(sensorData,
            sizeof(sensorData),
            "{\"temperature\":%s,\"threshold\":%s}",
            f2s(temperature, 1),
            f2s(temperatureThreshold, 1));

  sendData(sensorData);

  delay(5000);
}
