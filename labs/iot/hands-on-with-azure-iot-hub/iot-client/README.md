# Extending sensor metrics

In this module, we will extend the script sending data to the cloud for adding new measures. <br/>
You will get familiar with an example script structure so you can extend it for your own project. Note why this is called a simulated device. A real device will collect the values from sensors, but here we just make up that data. The rest of the script will be valid for a real device.

Please browse the script **iot-hub-client.py** in this repo un the Azure_IoT_Lab/iot-client/ folder. <br/>

Explore the main method structure. See it run a sample collection method that starts the Azure IoT Hub connection and starts an infinite loop in which it collects sensor data, sends it to the cloud and repeats the look forever after a sleep period.
In order to updating the code of the sensor, in a more professional model you should look at DevOps Continuous Deployment models. For this lab, you can connect to the VM using NotePad++ FTP plugin and adding an SFTP connection

![Snapshot](../images/simulated-13.PNG "Azure VM")

As an example, we added a new meassure called **blood_sugar** supposing we have a sensor we can read from. See the variable points to a new method you might also have to implement.

![Snapshot](../images/simulated-14.PNG "Azure VM")

After executing the script again, we can see the new metric being sent to the cloud.

![Snapshot](../images/simulated-15.PNG "Azure VM")

As explained in the previous module, navigate to the storage container and see the new field being stored

![Snapshot](../images/routing-9.png "Storage")

At this point, this module is done. Go to the next module for continuing the lab and do something useful with this data
[Go back to the main section](../README.md )
