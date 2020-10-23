# Raspberry Pi

The Raspberry Pi Foundation is a UK-based charity that manufactures small-board computers that were originally designed for children to use to code, but now are used in their millions as beginner IoT Devices, home computers, media servers, smart home controllers and games machines.

The model recommended for this cart is the [Raspberry Pi 4](https://www.raspberrypi.org/products/raspberry-pi-4-model-b/). This has a quad-core ARM 64 processor, up to 8GB RAM, 2 4K HDMI ports, WiFi, Gigabit Ethernet, USB-2 and 3 ports and GPIO (General Purpose Input Output) pins to allow you to connect a range of sensors and other hardware.

Raspberry Pis can run a range of operating systems, and the most common is Raspberry Pi OS - a version of Debian Linux customized for the Pi and available in 2 flavors, one that has a full desktop experience, and a Lite version that is terminal only. This allows the Pi to be connected to a keyboard/mouse/screen and used as a fully functioning computer, or connected to remotely.

Seeing as the Pi runs a full version of Linux, it can be programmed in a variety of languages. This is different to devices like Arduino boards that rely on C++ or possibly micro-python. The Pi comes with Python, C++, Java, Ruby and Scratch pre-installed in Raspberry Pi OS, and can run .NET in C# or F#, JavaScript, Node, Perl or Erlang amongst others.

The resources in this repo will focus on Python and C# only.

## Raspberry Pi Resources

Rather than duplicate existing labs or documentation, here are some links to existing Microsoft and external Raspberry Pi content.

* [Microsoft Raspberry Pi Resources](https://github.com/microsoft/rpi-resources) - guides on how to set up a Pi for remote access, how to connect remotely to code on the Pi using [Visual Studio Code](https://code.visualstudio.com?WT.mc_id=academic-7372-jabenn), and getting started with GPIO in Python.
* [Setting up Jupyter Notebooks on a Raspberry Pi](./configure-jupyter-notebooks-raspberry-pi.md)
* [Grove Python setup](https://wiki.seeedstudio.com/Grove_Base_Kit_for_Raspberry_Pi/) - guide from Seeed Studios on how to set up the Grove libraries on a Pi
* [Debugging Pi apps remotely using VS Code](https://github.com/gloveboxes/PyLab-0-Raspberry-Pi-Set-Up) - a hands on lab covering how to debug Python apps remotely on a Raspberry Pi using Visual Studio Code. This lab is designed for multiple students per Pi, supporting up to 20 students on one Raspberry Pi.
* [Building a Raspberry Pi based Kubernetes cluster](https://github.com/gloveboxes/Raspberry-Pi-Kubernetes-Cluster) - learn how to build a Kubernetes cluster using Raspberry Pis to run intelligent edge workloads
* [Get started with .NET core on Raspberry Pi](https://github.com/gloveboxes/Create-RaspberryPi-dotNET-Core-C-Sharp-IoT-Applications) - getting started lab using .NET core on a Raspberry Pi
* [Connecting a Raspberry Pi to Azure IoT Hub](https://github.com/jimbobbennett/Raspberry-Pi-And-Azure-IoT-Hub) - a guide to connecting a Raspberry Pi to Azure IoT Hub using Python to send data
* [AgroHack hands on digital agriculture lab](https://github.com/jimbobbennett/AgroHack) - a hands on lab showing how to monitor a plant using a Raspberry Pi and Grove sensors.
* [Create a talking image recognition solution with Azure IoT Edge and Azure Cognitive Services](https://github.com/gloveboxes/Create-a-talking-image-recognition-solution-with-Azure-IoT-Edge-Azure-Cognitive-Services) - A hands on lab where you build a solution that identifies a item scanned against a pre-trained machine learning model, tells the person what they have just scanned, then sends a record of the transaction to a central inventory system.
* [Developing C/C++ Apps on Raspberry Pi with Visual Studio Code Remote SSH](https://github.com/gloveboxes/Raspberry-Pi-with-Visual-Studio-Code-Remote-SSH-and-C-or-C-Development) - This tutorial explores using Visual Studio Code from Linux, macOS, or Windows to build C/C++ applications on the Raspberry Pi itself.
