# Clean up you Azure resources

In the [previous step](./set-up-web-app.md) you run the python website to show the current location in Azure Maps using GPS sensor data.

In this step you will clean up your Azure resources.

## Clean up resources

Every Azure service you use either costs you money (either paid for or reduces your available credit for free subscriptions), or uses up one of your available free tier resources. It's good practice when you are finished with a resource to delete it - to either save money or to allow you to spin up new free tier resources.

### Delete the Azure Resource Group

Azure has the concept of Resource Groups, logical groupings of resources that you can manage together. All resources, such as IoT Hubs or Azure Maps accounts have to live in a resource group. Deleting the resource group deletes all the services inside it.

1. From the [Azure Portal](https://portal.azure.com/?WT.mc_id=academic-7372-jabenn), head to the *gps-lab* resource group that you created earlier.

1. To delete the resource group, follow the instructions in the [Azure Resource Manager resource group and resource deletion documentation](https://docs.microsoft.com/azure/azure-resource-manager/management/delete-resource-group?tabs=azure-portal&WT.mc_id=academic-7372-jabenn)

### Delete the Azure App Service web app

If you deployed your web app to Azure App Service, you will need to delete the resource group that was created automatically by the deployment. The tutorial contains the steps to do this.

## Next steps

You have completed this lab to show current GPS location using a Raspberry Pi, GPS receiver and Azure Maps. You detected GPS location coordinates and sent this data to Azure IoT Hub, and from there you visualized it on Azure Maps.

If you want to learn more about Azure IoT Services, then check out the following:

* [IoT learning paths on Microsoft Learn](https://docs.microsoft.com/learn/browse/?term=IOT&WT.mc_id=academic-7372-jabenn)
* [The IoT show on Channel9](https://channel9.msdn.com/Shows/Internet-of-Things-Show/?WT.mc_id=academic-7372-jabenn)

Once you have upskilled as an IoT developer, why not get certified with our AZ-220 Azure IoT Developer certification. Check out the details on our [certification page](https://docs.microsoft.com/learn/certifications/azure-iot-developer-specialty?WT.mc_id=academic-7372-jabenn)
