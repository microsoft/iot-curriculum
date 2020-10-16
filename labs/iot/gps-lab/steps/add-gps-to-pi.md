# Add the GPS sensor to Raspberry Pi

In this step you will set up the GPS sensor to Pi.

## Steps

1. Put the vcc to 2, ground to 6 tx and rx to 8 and 10
![Pin Reference](../images/raspberry-pi-pins.png)[Source](https://www.raspberrypi.org/documentation/usage/gpio/)
2. The GPS Module connected should look like following with a blinking red light when the satelite is available
![Pi with GPS](../images/raspberry-pi-connected.jpg)
3. Note that the GPS antenna should face the sky to get the GPS values

## Run the Python Code
1. Connect the Raspberry Pi to the computer
2. Open the Python Editor (Default Thonny) or Visual Studio Code
3. Run raspberry-pi-gps-tracker.py
4. Note that you have changed the connection string as specified in the previous steps
5. If everything is set up correctly you should see the GPS messages going to the IoT Hub
![Pi with GPS](../images/raspberry-pi-gps-messages.png)
