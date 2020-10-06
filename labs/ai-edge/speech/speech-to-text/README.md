# Speech to text

This lab covers using a Raspberry Pi and a microphone to recognize speech and convert it to text using Azure Cognitive Services and Python.

| Authors | [Connor Hagen](https://github.com/chagen24), [Jim Bennett](https://github.com/JimBobBennett) |
|:---|:---|
| Target platform   | <ul><li>Raspberry Pi</li></ul> |
| Hardware required | <ul><li>Raspberry Pi 4</li><li>Micro SD Card</li><li>An SD card to USB converter that matches the USB ports on your device if your device doesn't have an SD card slot</li><li>Raspberry Pi 4 power supply (USB-C)</li><li>USB Microphone</li><li>keyboard, mouse and monitor</li><li>[micro-HDMI to HDMI adapter or cable](https://www.raspberrypi.org/products/micro-hdmi-to-standard-hdmi-a-cable/)</li></ul> |
| Software required | <ul><li>[Raspberry Pi Imager](https://www.raspberrypi.org/downloads/)</li></ul> |
| Azure Services | <ul><li>[Azure Cognitive Services Speech service](https://azure.microsoft.com/services/cognitive-services/speech-services/?WT.mc_id=iotcurriculum-github-jabenn)</li></ul>|
| Programming Language | <ul><li>Python</li></ul> |
| Prerequisites | Basic proficiency with Python.<br><br>You will also need an [Azure subscription](https://github.com/microsoft/iot-curriculum/tree/main/labs/ai-edge/ocr#azure-subscription) |
| Date | October 2020 |
| Learning Objectives | <ul><li>Set up Azure Cognitive Services</li><li>Convert speech to text with Azure Speech Services</li></ul> |
| Time to complete | 1 hour |

## Azure Cognitive Services

[Azure Cognitive Services](https://azure.microsoft.com/services/cognitive-services/?WT.mc_id=iotcurriculum-github-jabenn) is a comprehensive family of AI services and cognitive APIs to help you build intelligent apps.

This lab covers the [Azure Cognitive Services Speech service](https://azure.microsoft.com/services/cognitive-services/speech-services/?WT.mc_id=iotcurriculum-github-jabenn). This service has a free tier, so there will be no cost to run this lab.

> Note that you can only have one free tier instance of each resource per Azure subscription, so if you already have a free tier set up, you can re-use it or use a paid tier. You can find the current pricing on the [Azure cognitive services pricing page](https://azure.microsoft.com/pricing/details/cognitive-services/?WT.mc_id=iotcurriculum-github-jabenn).

To learn more about these services, and to try them out on a Mac or PC, work through the [Process and Translate Speech with Azure Cognitive Speech Services](https://docs.microsoft.com/learn/paths/process-translate-speech-azure-cognitive-speech-services/?WT.mc_id=iotcurriculum-github-jabenn) learning path on [Microsoft Learn](https://docs.microsoft.com/learn?WT.mc_id=iotcurriculum-github-jabenn).

### Azure subscription

This lab is designed for courses where Azure resources are provided to students by the institution. To try them out, you can use one of our free subscriptions. Head to the [Azure Subscriptions Guide](../../../azure-subscription.md) for from information on setting up a subscription.

### Create an Azure Cognitive Services Speech resource

To create an Azure Cognitive Services Speech resource, follow the instructions in one of the following guides, depending on if you want to use the Azure Portal, or the Azure Command-line interface (CLI). You will need to create a single-service resource for the speech service as at the time of writing speech is not included in a multi-service resource.

* [Create a Cognitive Services resource using the Azure portal](https://docs.microsoft.com/azure/cognitive-services/cognitive-services-apis-create-account?tabs=multiservice%2Cwindows&WT.mc_id=iotcurriculum-github-jabenn)
* [Create a Cognitive Services resource using the Azure Command-Line Interface(CLI)](https://docs.microsoft.com/azure/cognitive-services/cognitive-services-apis-create-account-cli?tabs=windows&WT.mc_id=iotcurriculum-github-jabenn)

You will need your Key and Endpoint to access the resource. If you used the Azure CLI to create the resource, the endpoint is in the form:

`https://<location>.api.cognitive.microsoft.com/`

Where `<location>` is the location you used to create the resource. For example, if the location you used was `westus2`, the Endpoint will be `https://westus2.api.cognitive.microsoft.com/`.

## Set up the Raspberry Pi

To run this lab, you will need to use the Pi using the full Raspberry Pi OS connected via a monitor/keyboard/mouse, or using screen sharing such as VNC.

Connect the Pi to a keyboard, mouse, and a monitor. Connect the USB microphone.

### OS setup

Ensure you are running the latest Raspberry Pi OS (full version, not Lite), with the latest updates, configured based on how you want to access the Pi (for example with VNC enabled if you are going to control it over VNC).

You can read instructions on how to configure an SD card with Raspberry Pi OS in the [Raspberry Pi Installing Operating System images documentation](https://www.raspberrypi.org/documentation/installation/installing-images/).

Once you boot up your Pi, follow the instructions on-screen to set up the Pi, including connecting to WiFi (or connect the Pi to an ethernet cable) and updating all the software.

Once it is set up, if you's rather connect remotely to the Pi, then follow the instructions in the [Microsoft Raspberry Pi headless setup guide](https://github.com/microsoft/rpi-resources/tree/master/headless-setup#remote-desktop) to configure VNC or Remote Desktop.

### Software installation

Once your Pi is set up, you will need to install Jupyter Notebooks, as this lab runs from a notebook.

Follow the instructions in the [Configure Jupyter Notebooks on a Raspberry Pi guide](../../../../devices/configure-jupyter-notebooks-raspberry-pi.md) to install and run Jupyter Notebooks.

## Run the Jupyter notebook

To run the notebook, you first need to clone this repo, then you can launch it in Jupyter Notebooks.

1. From the Pi Terminal, run the following command to clone this repo to get the Jupyter notebook:

    ```sh
    git clone https://github.com/microsoft/iot-curriculum.git
    ```

1. Navigate to the Notebook folder

    ```sh
    cd ./iot-curriculum/labs/ai-edge/speech/speech-to-text
    ```

1. Open the notebook

    ```sh
    jupyter notebook speech-to-text.ipynb
    ```

This will launch the Jupyter Notebook running in the Chromium browser. Read and follow the instructions in the Notebook to complete the lab.

## Clean up

Once you have finished this lab, you can clean up your resource group to delete any Azure resources that you have created, stopping you being billed for them. You can read about how to do this in the [Deleting Azure Resource Groups guide](https://docs.microsoft.com/azure/azure-resource-manager/management/manage-resource-groups-portal?WT.mc_id=iotcurriculum-github-jabenn#delete-resource-groups)
