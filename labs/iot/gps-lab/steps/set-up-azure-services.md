# Set up Azure services

In this part, you will set up all the Azure services needed to complete this lab.

The services you will use are Azure Maps and Azure IoT Hub.

## Azure Cloud Shell

The Azure Portal is the UI for Azure, and is available at [portal.azure.com](https://portal.azure.com?WT.mc_id=academic-7372-jabenn). As well as providing a UI for creating and managing Azure services, it also has a terminal you can run to interact with Azure via the command line. This is called the Azure Cloud Shell.

### Launch the cloud shell

1. Open the Azure Portal in your browser by heading to [portal.azure.com](https://portal.azure.com?WT.mc_id=academic-7372-jabenn)

1. Log in with your Azure account if necessary

1. Select the **Cloud Shell** button to launch the cloud shell

    ![The cloud shell button](../../../images/azure-portal-cloud-shell-button.png)

1. The Cloud Shell will appear at the bottom of the portal window. If it is the first time you've used the Cloud Shell, it will tell you that you need a storage account set up to store configuration and other cloud shell files. Select the **Create Storage** button.

    ![Create storage option](../../../images/azure-portal-cloud-shell-create-storage.png)

    > If you have multiple Azure Subscriptions, such as an Azure for Students subscription and a School one, select the appropriate subscription from the dialog

1. All the commands in this lab will use the Bash shell, so ensure that Bash is selected for the Cloud Shell, not Powershell

### Configure the cloud shell

The cloud shell has the [Azure CLI](https://docs.microsoft.com/cli/azure/?WT.mc_id=academic-7372-jabenn) pre-installed. This allows you to run commands using the `az` tool to create and manage Azure services.

The Azure Cloud Shell uses your default subscription. If you only have one, then that will be selected. If you have multiple Azure Subscriptions, such as an Azure for Students subscription and a School one, then you need to select the right one for this lab.

1. Follow the instructions in the [Use multiple Azure subscriptions documentation](https://docs.microsoft.com/cli/azure/manage-azure-subscriptions-azure-cli?WT.mc_id=academic-7372-jabenn) to select the subscription you want to use.

There are extensions available to give more capabilities with a wide range of Azure services, including IoT. The IoT extension needs to be installed.

1. From the cloud shell, run the following command to install the IoT extension:

    ```sh
    az extension add --name azure-iot
    ```

> If you have previously used the Cloud Shell with the previous version of this extension called `azure-cli-iot-ext`, then you will need to remove it first with the following command:
>
>    ```sh
>    az extension remove --name azure-cli-iot-ext
>    ```

## Get the closest Azure location

Azure consists of multiple regions made up of one or more data centers at different locations around the world. When you create a resource for most services, it needs to be created in a specific location.

You can find a list of locations in the [Azure geographies page](https://azure.microsoft.com/global-infrastructure/geographies/?WT.mc_id=academic-7372-jabenn). Each location has a name that is needed when creating most resources.

1. To get a list of all the locations, run the following command in the Azure Cloud Shell

    ```sh
    az account list-locations --output table
    ```

1. Find the location closest to you, and note down the value from the *Name* column, such as `westus2` or `southindia`.

## Azure Resource groups

In Azure, a *resource* is an instance of a service set up for you. For example, Azure Maps is a service but your Maps account, with your key that is for you to use is your resource.

Whenever you create a resource in Azure, such as a Maps resource, or an IoT hub, it has to belong to a Resource Group. A resource group is a logical grouping of resources, allowing you to keep all the resources for a project in the same resource group, and manage them as a group. For example, at the end of this lab you will delete the resource group, and that will delete any resources inside of it.

### Create a resource group

All the Azure resources you will use in this lab should belong to the same resource group.

1. Run the following command in the Azure Cloud Shell to create a resource group called `gps-lab`:

    ```sh
    az group create --name gps-lab --location <location>
    ```

    Replace `<location>` with the closest location to you.

## Azure Maps

Microsoft Azure Maps provides developers with powerful geospatial capabilities. Those geospatial capabilities are packed with the freshest mapping data. Azure Maps is available for both web and mobile applications. Azure Maps is an Azure One API compliant set of REST APIs. The following are only a high-level overview of the services which Azure Maps offers - Maps, Search, Routing, Traffic, Mobility, Weather, Time Zones, Geolocation, Geofencing, Map Data, Creator, and Spatial Operations. The Web and Android SDKs make development easy, flexible, and portable across multiple platforms.

### Set up an Azure Maps resource

To use Azure Maps, you need to set up and Azure Maps resource.

1. From the Azure Cloud Shell, run the following command:

    ```sh
    az maps account create --name gps-lab \
                           --resource-group gps-lab \
                           --accept-tos \
                           --sku S0
    ```

    This will create a [standard tier](https://docs.microsoft.com/azure/azure-maps/choose-pricing-tier?WT.mc_id=academic-7372-jabenn) Azure Maps account called `gps-lab` in the `gps-lab` resource group. These Maps accounts are global, and don't need a location set.

1. To use the Maps account, you will need a API key. To get this, run the following command:

    ```sh
    az maps account keys list --name gps-lab \
                              --resource-group gps-lab
    ```

1. Take a copy of the value of the `primaryKey` from the output as you will need this in a later step

## Azure IoT Hub

IoT Hub is a managed service, hosted in the cloud, that acts as a central message hub for bi-directional communication between your IoT application and the devices it manages. You can use Azure IoT Hub to build IoT solutions with reliable and secure communications between millions of IoT devices and a cloud-hosted solution backend. You can connect virtually any device to IoT Hub.

Azure IoT Hub is secure in that only authenticated devices can connect to it. These devices can either be pre-authenticated and set up inside IoT Hub up front by creating a device identity, or they can authenticate themselves later using a device provisioning service. For this lab, the device will be pre-authenticated up front.

### Set up an Azure IoT Hub resource

1. Run the following command in the Azure Cloud Shell to create an IoT Hub:

    ```sh
    az iot hub create --resource-group gps-lab \
                      --sku F1 \
                      --partition-count 2 \
                      --name <hub_name>
    ```

    Replace `<hub_name>` with the name for your IoT Hub. This names needs to be globally unique as it is used to generate a publicly visible endpoint that devices connect to. Use something like `gps-lab-<your-name>` replacing `<your-name>` with your name.

    The `--sku F1` parameter means the IoT Hub will be created using the [Free Tier](https://azure.microsoft.com/pricing/details/iot-hub/?WT.mc_id=academic-7372-jabenn), allowing you to send up to 8,000 messages a day without any cost. If you exceed this then messages are lost, rather than costing you money.

### Set up a device identity

For the GPS device to connect to IoT Hub, a device identity needs to be created in IoT Hub to identify the GPS device.

1. Run the following command in the Azure Cloud Shell to create an IoT Hub device identity:

    ```sh
    az iot hub device-identity create --device-id gps_device \
                                      --hub-name <hub_name>
    ```

    Replace `<hub_name>` with the name for your IoT Hub. This will create a device identity for a device called `gps_device`.

1. To configure the GPS device, it will need a connection string that contains the credentials for the device identity. Run the following command to get the connection string:

    ```sh
    az iot hub device-identity connection-string show --device-id gps_device \
                                                      --output table \
                                                      --hub-name <hub_name>
    ```

    Replace `<hub_name>` with the name for your IoT Hub. Take a copy of the value from the *ConnectionString* column.

    The connection string is made of three parts, separated by a semi-colon:

    * `HostName` - This is the host name of the IoT Hub and tells the device what IoT Hub to connect to
    * `DeviceId` - This is the Id of the device, used to identity it to the IoT Hub when it connects
    * `SharedAccessKey` - This is a secret key for this device to authenticate

    These connection strings are device specific - each new device will need a new connection string containing the relevant device Id as well as the devices shared access key.

1. Reading messages from the GPS device off the IoT Hub to display the location on a web page needs an Event Hub compatible endpoint. This is an end point that you can connect to to receive values as soon as they are sent to the IoT Hub. Run the following command to get the connection string for the Event Hub compatible end point:

    ```sh
    az iot hub connection-string show --default-eventhub \
                                      --output table \
                                      --hub-name <hub_name>
    ```

    Replace `<hub_name>` with the name for your IoT Hub. Take a copy of the value from the *ConnectionString* column.

    > [Event hubs](https://azure.microsoft.com/services/event-hubs/?WT.mc_id=academic-7372-jabenn) is an Azure service for streaming events between components of your application. Azure IoT Hub can act like an Event Hub and services can connect to IoT Hub to ingest IoT messages in the same way as they could connect to an Event Hub to ingest events.

## Next steps

In this step you set up all the Azure services needed to complete this lab.

In the [next step](./set-up-pi.md) you will set up the Raspberry Pi to receive GPS signals from the GPS receiver.
