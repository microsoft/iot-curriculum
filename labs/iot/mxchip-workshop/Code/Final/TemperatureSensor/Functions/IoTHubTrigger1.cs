using IoTHubTrigger = Microsoft.Azure.WebJobs.EventHubTriggerAttribute;

using Microsoft.Azure.WebJobs;
using Microsoft.Azure.WebJobs.Host;
using Microsoft.Azure.EventHubs;
using System.Text;
using System.Net.Http;
using Microsoft.Extensions.Logging;
using Newtonsoft.Json;
using Microsoft.Azure.WebJobs.Extensions.Http;
using Microsoft.AspNetCore.Mvc;
using Microsoft.AspNetCore.Http;
using System;
using System.Threading.Tasks;
using System.IO;
using Microsoft.Azure.Devices;

namespace IoTWorkbench
{
    public class TemperatureItem
    {
        [JsonProperty("id")]
        public string Id {get; set;}
        public double Temperature {get; set;}
        public double Threshold {get; set;}
}

    public static class IoTHubTrigger1
    {

        [FunctionName("IoTHubTrigger1")]
        public static void Run([IoTHubTrigger("%eventHubConnectionPath%", 
                                              Connection = "eventHubConnectionString")] EventData message, 
                               [CosmosDB(databaseName: "IoTData",
                                         collectionName: "Temperatures",
                                         ConnectionStringSetting = "cosmosDBConnectionString")] out TemperatureItem output,
                               ILogger log)
        {
            log.LogInformation($"C# IoT Hub trigger function processed a message: {Encoding.UTF8.GetString(message.Body.Array)}");

            var deviceId = message.SystemProperties["iothub-connection-device-id"].ToString();

            var jsonBody = Encoding.UTF8.GetString(message.Body);
            dynamic data = JsonConvert.DeserializeObject(jsonBody);
            double temperature = data.temperature;
            double threshold = data.threshold;

            output = new TemperatureItem
            {
                Temperature = temperature,
                Threshold = threshold,
                Id = deviceId
            };
        }

        [FunctionName("GetTemperature")]
        public static IActionResult GetTemperature([HttpTrigger(AuthorizationLevel.Anonymous, 
                                                                "get", 
                                                                Route = "temperature/{devicename}")] HttpRequest req,
                                                   [CosmosDB(databaseName: "IoTData",
                                                             collectionName: "Temperatures",
                                                             ConnectionStringSetting = "cosmosDBConnectionString",
                                                             Id = "{devicename}")] TemperatureItem temperatureItem,
                                                   ILogger log)
        {
            return new OkObjectResult(temperatureItem);
        }

        static readonly string connectionString = Environment.GetEnvironmentVariable("iotHubConnectionString");
        static readonly RegistryManager registryManager = RegistryManager.CreateFromConnectionString(connectionString);

        [FunctionName("SetTemperatureThreshold")]
        public static async Task<IActionResult> SetThreshold([HttpTrigger(AuthorizationLevel.Anonymous, 
                                                                          "get", 
                                                                          "post", 
                                                                          Route = "temperaturethreshold/{devicename}")] HttpRequest req,  // GET support for testing only
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
    }
}