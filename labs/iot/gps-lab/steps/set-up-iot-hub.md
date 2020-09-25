# Set Up IoT Hub

In this step you will set up IoT Hub and add a device in it.

## Steps

1. Go to [Azure portal]('https://portal.azure.com') and login to your subscription. 
2. Create a resource for IoT Hub  ![Azure IoT Hub](../images/azure-iot-hub-create-1.png)
3. Once created note down the Event Hub Compatible Endppoint and Consumer Group
![IoT Hub Keys](../images/azure-iot-hub-create-3.png)
    
4. Update The [application.py](../server/code/application.py) with the connection string and consumer group
    
```python
    CONNECTION_STR = '<Iot_Hub_Connection_String>'
```
```python
    def index():    
    client = EventHubConsumerClient.from_connection_string(
        conn_str=CONNECTION_STR,
        consumer_group="<Consumer_Group_Name>"
    )
```

## Create a device

1. Go to the IoT hub you have created earlier
2. Go to IoT Devices and add new device
![Create Azure Device](../images/azure-iot-hub-create-device-1.png)
3. Enter a device Id. Leave the "Auto Generate Keys" checked.
![Create Azure Device](../images/azure-iot-hub-create-device-2.png)
4. Once created, note down the Primary Connection String.
![Create Azure Device](../images/azure-iot-hub-create-device-3.png)
5. Update the [raspberry-pi-gps-tracker.py](../client/code/raspberry-pi-gps-tracker.py) with the connection string

```python
# The device connection string to authenticate the device with your IoT hub.
CONNECTION_STRING = "<Device_Connection_String>"
```