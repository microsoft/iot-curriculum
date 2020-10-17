# Set up a Raspberry Pi

In the [previous step](./set-up-iot-hub.md) you set up a IoT Hub in Microsoft Azure Portal.

In this step you will set up a Raspberry Pi.

## Raspberry Pi

The [Raspberry Pi](https://raspberrypi.org) is a low-priced, small form factor computer that can run a full version of Linux. It's popular with hobbyists and kids - it was originally designed to be a cheap computer for kids to learn to code on. It has the same standard USB and HDMI ports that a PC or Mac would have, as well as GPIO (General Purpose Input Output) pins that can be used to work with a wide array of external electronic components, devices, sensors, machinery and robotics.

Raspberry Pi's can run a wide range of programing languages. In this lab you will use Python, and program the Pi using Visual Studio Code (VS Code), an open-source developer text editor that can remotely program on a Pi from your PC or Mac. When connected to the Pi remotely from your PC or Mac you can write and debug code from your device, with the code running on the Pi. You will also get a terminal that runs on the Pi.

The temperature data will come from a temperature sensor attached to the Pi. The sensor required is a Grove Temperature Humidity sensor and is part of the [Grove Pi+ Starter Kit](https://www.seeedstudio.com/GrovePi-Starter-Kit-for-Raspberry-Pi-A-B-B-2-3-CE-certified.html). These kits are designed to lower the barrier to entry when using sensors - providing a controller board, sensors with standard cables, and Python libraries.

## Hardware requirements

You will need the following hardware:

* A Raspberry Pi 4
* A micro SD Card
* An SD card to USB converter that matches the USB ports on your device if you r device doesn't have an SD card slot
* A Raspberry Pi 4 power supply (USB-C)
* A keyboard, mouse and monitor
* A [micro-HDMI to HDMI adapter or cable](https://www.raspberrypi.org/products/micro-hdmi-to-standard-hdmi-a-cable/)

### Set up the software

1. Insert the SD card into your PC or laptop using an adapter if necessary

1. Using the [Raspberry Pi imager](https://www.raspberrypi.org/downloads/), image the SD card with the default Raspberry Pi OS image. You can find instructions on how to do this in the [Raspberry Pi installing images documentation](https://www.raspberrypi.org/documentation/installation/installing-images/).

1. Insert the SD card into the Pi

1. Connect the Pi to your keyboard, mouse and monitor. If you are using ethernet for internet access then connect the Pi to an ethernet cable connected to your network. Then connect it to the power supply.

    > If you don't have a keyboard, monitor and mouse available, you can set up your Pi for headless access - check out the [Microsoft Raspberry Pi headless setup docs](https://github.com/microsoft/rpi-resources/tree/master/headless-setup) for details on how to set this up.

1. Work through the setup wizard on the Pi:

    1. Set your country, language and timezone

    1. Change your password from the default - when a new Raspberry Pi is set up it creates an account with a username of `pi` and a password of `raspberry`, so set a new password

    1. Set up the screen if necessary

    1. If you want to use Wifi, select your wireless network and enter the password if needed.

        > If you are using enterprise security you may need to launch Chromium, the Pi's browser after selecting your wireless network to log in to your Wifi

    1. Update the Pis software

    1. Reboot the Pi

Once the Pi has rebooted, you will need to change the hostname. All newly setup Pis are configured with a hostname of `raspberrypi`, so if you have more than one Pi on your network you won't be able to distinguish between them by name unless you rename them. You will also need to enable SSH (Secure SHell) access so you can control the Pi later remotely from Visual Studio Code.

1. From the Raspberry Pi select the **Raspberry Pi** menu, then select **Preferences -> Raspberry Pi Configuration**

    ![The pi configuration tool in the menu](../../environment-monitor/images/raspberry-pi-menu-configuration-app.png)

1. Change the value of the *Hostname* in the *General* tab to be something unique, such as by using your name

    ![Setting the hostname](../../environment-monitor/images/raspberry-pi-configuration-app-hostname.png)

1. In the **Interfaces** tab, ensure **SSH** is set to *Enable*

    ![enabling SSH](../../environment-monitor/images/raspberry-pi-configuration-enable-ssh.png)

1. Select the **OK** button

1. When prompted, select **Yes** to reboot the Pi

# Prepare Pi for python packages
1. Open a terminal
2. Run
```sh
    sudo apt install python3-pip
```

> Note that we will use the default python editor Thonny that comes with Raspberry Pi to program the client side code.
## Next steps

In this step you have set up the Raspberry Pi.

In the [next step](./add-gps-to-pi.md) you will add the GPS receiver to the pi and run the client side code.