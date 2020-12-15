# Creating an Azure Blob Storage
In previous modules, we have set-up a simulated client sending traffic to an [Azure IoT Hub](https://docs.microsoft.com/en-us/azure/iot-hub/)  instance. <br/>
At this point, Azure IoT Hub is not doing anything with that data, which obviously is not very useful. <br/>
Azure IoT Hub, apart from supporting device security and management, is a message broker capable of sending those IoT device messages to other services for consuming them. <br/>
In this module, we will create an [Azure Blob Storage](https://docs.microsoft.com/en-us/azure/storage/blobs/storage-blobs-overview). <br/>
The outcome of this module, added to what has been done in the previous 2 modules is summarized in the following image

![Snapshot](../images/Lab-3.png?style=centerme)

In the next module, we will configure Azure IoT Hub for storing device messages in the storage created in this module.

Blob storage is a highly scalable cloud storage service, allowing massive data ingest at very low price 

## Create an Storage Account in the Azure portal

1. Look for **Storage Account** in the Azure Portal. 
2. Click **Add** in order to create your Storage Account. 
3. Use the **Resource Group** previously used 
4. Name the storage account **icaiiotlabgroupXY**, where **X** is your double digit group ID and **Y** is **c** or **h** whether you are at class or at home 
5. Select **LRS** as Replication option and leave other options as default

![Snapshot](../images/storage-3.PNG)

Once you click **Review + create**, a window similar to the one that follows will show up.
If the Validated message in green is displayed, press **Create**

![Snapshot](../images/storage-4.PNG "Azure Storage")

## Create an Storage Container in the Storage Account

We are going to use blobs for storing sensor data. Blobs are stored in Containers. For this, we need to create a container. <br/>
1. Select **Containers** as highlighted in red in the image below and click **+ Container** as shown in purple. 
2. Name the container **sensordata** as shown in blue. Set access level to Container (see in orange).

*For simplicity for this lab, considering we are not storing personal data, we can put access policy to anonymous.* *Never use anonymous access to a container hosting* **personal data** 

![Snapshot](../images/storage-5.PNG "Azure Storage")

After clicking OK, this module is done. Go to the next module for continuing the lab and store sensor data in blobs in this storage account.
[Go back to the main section](../README.md )
