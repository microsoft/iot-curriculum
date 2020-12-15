# Routing messages from Azure IoT Hub to an storage account
Azure IoT hub is intended to route messages, based on different conditions to different destionations. This capability is called message brokering. The following image shows this concept.
![Snapshot](../images/message-enrichments-flow.png "Azure VM")

In this lab, we will store data in the previously created storage account, which is intended for storing massive ammount of data from millions of devices.
The outcome of this module is competing the end to end architecture presented.
![Snapshot](../images/Lab.png "Storage")

## Creating a Custom Endpoint of type Storage under Azure IoT Hub routes

First we need to declare the previously created storage endpoint. 
1. Go to the IoT Hub instance created in module 1
2. Select **Message routing** (red), **Custom endpoints** (blue). Click **Add** (green) and select **Storage**, as shown in the diagram below.

![Snapshot](../images/routing-1.png "Storage")

3. Name the endpoint **storage** (internal name) as shown in red. 
4. Select **Encoding** in JSON for better human readability. 
5. Click **Pick a Container** (Storage Container) created in the previous module, as shown below in blue.

![Snapshot](../images/routing-2.PNG "Storage")

6. In the menu displayed, click **Storage account** then add a container **+ Container** and **Select** the previously created container, as shown below:

![Snapshot](../images/routing-3.PNG "Storage")

7. Once the container has been properly selected,  the container URL will be shown in the following window, as highlighted in blue. Click **Create** to proceed.

![Snapshot](../images/routing-4.png "Storage")

Once the task is completed, the **Custom endpoint** will be shown as highlighted in red in the image below:

![Snapshot](../images/routing-5.PNG "Storage")

## Creating a Custom Endpoint of type Storage under Azure IoT Hub routes

In the previous step, we declared an Azure Storage container as a potential destination for sending device messages, but did nothing with it yet. <br/> 
In this step, we are going to configure all messages to be sent to that endpoint.<br/> 

8. In the previous blade, select the **Routes** submenu, highlighted in red and click **+Add** for creating a route, as shown below:

![Snapshot](../images/routing-6.png "Storage")

The image below will display. <br/> 
9. Input a name, for example, **route**, in the **Endpoint** dropdown, select the previously created endpoint, named **storage** and make sure the field **Enable route** is set to **Enable**

![Snapshot](../images/routing-7.png "Storage")

Note in this case all messages will go to this endpoint, since the **Routing query** is set to **True**. A very powerful query language can be input in order to route messages based on various numerous fields. Please visit the Azure IoT Hub Query Syntax [documentation](https://docs.microsoft.com/en-us/azure/iot-hub/iot-hub-devguide-routing-query-syntax) for further details.

Once the route is active, the following information will be shown in the screen.

![Snapshot](../images/routing-8.png "Storage")

## Sending messages to Azure IoT hub from the simulated device.

Review module 2 in which we sent traffic to Azure IoT Hub from the simulated device.

`vmuser@simulated-device:~$ python3 Azure_IoT_Lab/iot-client/iot-hub-client.py `**`"HostName=icaiiotlabgroup1.azure-devices.net;DeviceId=simulatedDevice;SharedAccessKey=7VA3mGEaP8U8JiH899kFGJitTrGA3YuXsj8QcxGDnic="`**

Messages will not show up in the Storage instantaneously, as a default **Batch frequency** of 100 seconds, was configured while creating the Storage endpoint
![Snapshot](../images/simulated-10.png "Azure VM")


## Sending messages to Azure IoT hub from the simulated device.

After waiting for the period in the batch frequency field, device data will be stored in the storage account. Navigate to the storage account and see the messages stored in text, as shown in the next window path.

![Snapshot](../images/routing-9.png "Storage")


At this point, this module is done. Go to the next module for continuing the lab and do something useful with this data
[Go back to the main section](../README.md )
