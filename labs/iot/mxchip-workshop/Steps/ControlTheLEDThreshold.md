# Configure the LED colour threshold using Device Twins

In the [previous step](./ExposeTheTemperature.md) you wrote an Azure Function with an HTTP trigger that returned the temperature for a given device. In this step you will configure the threshold for the LED colour using a Device Twin. This will be done using another HTTP trigger that accepts a JSON document sent as a POST containing the required threshold.

## IoT Hub Device Twins

[Azure IoT Hub Device Twins](https://docs.microsoft.com/azure/iot-hub/iot-hub-devguide-device-twins/?WT.mc_id=academic-7372-jabenn) are JSON documents that store data about a device, and are synchronized between an IoT Hub and a particular device. If you update the device twin for a particular device inside the IoT Hub it will be sent to the device over MQTT, and if you update it on the device it will be sent up to the IoT Hub.

These are designed for state and configuration, as opposed to a live stream of telemetry data.

Device twins have three parts:

1. Tags - data that can be written and read from the IoT Hub. These are not visible to the device
2. Device identity properties - read-only properties about the device such as its identity.
3. Properties - key vale pairs. These properties are split into two sections:
   1. Reported properties - these are properties from the device, for example is it connected to WiFi, what settings have been set on the device.
   2. Desired properties - these are properties set from the cloud and are used to configure the device, for example the temperature threshold for the LED colour.

### Create the REST API to update the threshold

From Visual Studio Code, open the `Functions.csproj` file in the `Functions` folder. This is a .NET project file and from here you can add packages to bring in more SDKs, such as the one needed to interact with Device Twins.

* Find the `<ItemGroup>` section containing `<PackageReference>` elements.
* Add the following new element to this group:

  ```xml  
  <PackageReference Include="Microsoft.Azure.Devices" Version="1.17.2" />
  ```

* A popup will appear in the bottom left asking if you want to restore the packages to download this new reference. Click **Restore**. If you don't see this popup, from the command palette select *.NET: Restore All Projects*.

Once the SDK has been installed, it can be used to interact with Device Twins. The interaction will be done via an HTTP trigger that will listen for GET and POST requests to a resource named with the device name, sent with a query string containing the new temperature threshold.

> The code you will write will handle a GET request as well as a POST, and take the data as a query string. This is not the ideal behavior, instead this is done to allow you to easily test this via a web browser.
> 
> In a production app you should only handle POST requests here, keeping GET requests for reading the threshold value. You should also send the data as the body of the request.
>
> You can read more on good REST API design in the [Microsoft Docs](https://docs.microsoft.com/azure/architecture/best-practices/api-design/?WT.mc_id=academic-7372-jabenn)

* From Visual Studio Code, open the `IoTHubTrigger1.cs` file from the `Functions` folder.
* Add new `using` directives below the existing `using` directives:

  ```cs
  using System;
  using System.Threading.Tasks;
  using System.IO;
  using Microsoft.Azure.Devices;
  ```

* Inside the `IoTHubTrigger1` class, add a `static` field for the connection string to the IoT Hub, using an environment variable. This environment variable is read from the application settings, using a setting that is already set when the function app was deployed.

  ```cs
  static readonly string connectionString = Environment.GetEnvironmentVariable("iotHubConnectionString");
  ```

* Use this connection string to create a `RegistryManager` to interact with the IoT Hub device registry.

  ```cs
  static readonly RegistryManager registryManager = RegistryManager.CreateFromConnectionString(connectionString);
  ```

* Add a new HTTP Trigger function to the class, with the `FunctionName` set to `"SetTemperatureThreshold"`. This should handle a POST request to `temperaturethreshold/{devicename}`.

  ```cs
  [FunctionName("SetTemperatureThreshold")]
  public static async Task<IActionResult> SetThreshold(
    [HttpTrigger(AuthorizationLevel.Anonymous, "get", "post", Route = "temperaturethreshold/{devicename}")] HttpRequest req,  // GET support for testing only
    string devicename,
    ILogger log)
  {
  }
  ```

  The `string devicename` parameter is automatically populated using the `{devicename}` part of the URL. For example, if the POST is sent to `https://MyTemperatureSensor.azurewebsites.net/api/temperature/MyDevice`, the `devicename` parameter will be auto-populated as `MyDevice`.

  This trigger returns a `Task<IActionResult>`. This is different to the last function that returned an `IActionResult`. This is because this function needs to be `async` to call async methods on the registry manager. You can read more on async/await and Tasks in the [.NET documentation](https://docs.microsoft.com/dotnet/csharp/programming-guide/concepts/async/?WT.mc_id=academic-7372-jabenn).

* Extract the temperature threshold from the query string

  ```cs
  var temperatureThreshold = double.Parse(req.Query["threshold"]);
  ```

* To update a device twin you don't update the entire document, instead you can issue a patch to add or replace fields. Create an [anonymous object](https://docs.microsoft.com/dotnet/csharp/programming-guide/classes-and-structs/anonymous-types/?WT.mc_id=academic-7372-jabenn) for the patch to add the temperature threshold to the desired properties.

  ```cs
  var patch = new
  {
    properties = new
    {
      desired = new
      {
        temperatureThreshold = temperatureThreshold
      }
    }
  };
  ```

* Get the twin for the device and patch it.

  ```cs
  var twin = await registryManager.GetTwinAsync(devicename);
  await registryManager.UpdateTwinAsync(twin.DeviceId, JsonConvert.SerializeObject(patch), twin.ETag);
  ```

* Return a 200 status code

  ```cs
  return new OkResult();
  ```

### Deploy the REST API

* From the Visual Studio Code command palette, select *Azure IoT Device Workbench: Deploy to Azure...*
* The palette will show you are deploying the Azure Functions app, so press enter to continue
* The deployment will begin. You will be asked if you want to overwrite the existing deployment, so click **Deploy**.
  
  ![The dialog box asking if you want to overwrite the existing Azure Functions app](../Images/OverwriteFunctionApp.png)

  The function app will be deployed, and this should take a few seconds.

* From Visual Studio Code, select the *Azure* tab.

* Expand the *FUNCTIONS* section.

* Expand your subscription.

* Right-click on the function app you created earlier and select *Restart*.
* 
  The function app will be restarted, and this should take a few seconds.

### Add support for Device Twins to the MXChip

When the MXChip first connects to the IoT Hub, the latest Device Twin is downloaded. Every time the Device Twin is updated by the registry manager, the new JSON document is sent over MQTT to the MXChip. The device code needs to detect this initial document and all changes, and handle the new JSON.

* From Visual Studio Code, open the `device.ino` Arduino sketch file.
* Add a new `include` directive for `parson.h` to the top of the file.

  ```c
  #include "parson.h"
  ```

* Add a new method called `DeviceTwinCallback` above the `setup` method. This will be the callback whenever a Device Twin update happens.

  ```c
  static void DeviceTwinCallback(DEVICE_TWIN_UPDATE_STATE updateState, const unsigned char *payLoad, int size) {
  }
  ```

* The payload is raw data, so needs to be converted to a null terminated string so that it can be deserialized into JSON

  ```c
  static void DeviceTwinCallback(DEVICE_TWIN_UPDATE_STATE updateState, const unsigned char *payLoad, int size) {
    char *message = (char *)malloc(size + 1);
    memcpy(message, payLoad, size);
    message[size] = '\0';
  }
  ```

* Convert the string to a JSON document and extract the root object from it

  ```c
  static void DeviceTwinCallback(DEVICE_TWIN_UPDATE_STATE updateState, const unsigned char *payLoad, int size) {
    ...
    JSON_Value *root_value = json_parse_string(message);
    JSON_Object *root_object = json_value_get_object(root_value);
  }
  ```

* Depending on the state of the update, extract the temperature threshold from the JSON

  ```cs
  static void DeviceTwinCallback(DEVICE_TWIN_UPDATE_STATE updateState, const unsigned char *payLoad, int size) {
    ...
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
  }
  ```

* Add some code to clean up the allocated objects

  ```c
  static void DeviceTwinCallback(DEVICE_TWIN_UPDATE_STATE updateState, const unsigned char *payLoad, int size) {
    ...
    json_value_free(root_value);
    free(message);
  }
  ```

* Register the `DeviceTwinCallback` at the end of the `setup` method after the MQTT connection has been initialized.

  ```c
  void setup() {
    ...
    DevKitMQTTClient_Init(true);
    DevKitMQTTClient_SetDeviceTwinCallback(DeviceTwinCallback);
  }
  ```

### Deploy the new device code

* Compile and upload the code to the device. From the command palette select *Azure IoT Device Workbench: Upload Device Code*. Your code will compile and be uploaded to the board.
* Once the code has been compiled and uploaded, the board will reboot and start running your new code.

## Test the API

This API was written to support using a GET request to make the update, simply to make testing easier. This means it can be tested from a browser.

> In a production API you would want this to be POST only, with a GET version to retrieve the threshold

* From a web browser, open `https://<your URL>/api/temperaturethreshold/<devicename>?threshold=<xx>` where `<your URL>` is the URL of your Azure Function app, `<devicename>` is the name you gave your IoT device and `<xx>` is the threshold you want to set. You can find the URL of the Azure Function app from the *Overview* page and it will be in the format `<your function app name>.azurewebsites.net`. If you need to double check the IoT Device name, you can get it from the document in the Cosmos DB collection.
* The threshold value will be pushed to the device, and on the next loop the value will be updated on the display, with the LED changing colour if applicable.
* Test this out with thresholds above and below the current temperature to see the LED change color.

<hr>

The full code for the new Azure Function is below:

```cs
static readonly string connectionString = Environment.GetEnvironmentVariable("iotHubConnectionString");
static readonly RegistryManager registryManager = RegistryManager.CreateFromConnectionString(connectionString);

[FunctionName("SetTemperatureThreshold")]
public static async Task<IActionResult> SetThreshold(
  [HttpTrigger(AuthorizationLevel.Anonymous, "get", "post", Route = "temperaturethreshold/{devicename}")] HttpRequest req, // GET support for testing only
  string devicename,
  ILogger log)
{
  var temperatureThreshold = double.Parse(req.Query["threshold"]);
  
  var patch = new
  {
    properties = new
    {
      desired = new
      {
        temperatureThreshold = temperatureThreshold
      }
    }
  };

  var twin = await registryManager.GetTwinAsync(devicename);
  await registryManager.UpdateTwinAsync(twin.DeviceId, JsonConvert.SerializeObject(patch), twin.ETag);

  return new OkResult();
}
```

The full code for the Device Twin callback and updated `setup` method is below:

```c
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
```

<hr>

In this step you added an Azure Function REST API to control the temperature threshold for the LED color. Now move on to the [next step](./CleanUp.md) where you will clean up the resources you have used.
