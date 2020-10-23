# Speech to text

This lab covers using a Raspberry Pi and a microphone/speaker to use the Azure Cognitive Speech Services and Python. This lab covers speech to text, text to speech and speech translation.

| Authors | [Connor Hagen](https://github.com/chagen24), [Jim Bennett](https://github.com/JimBobBennett) |
|:---|:---|
| Target platform   | <ul><li>Raspberry Pi</li></ul> |
| Hardware required | <ul><li>Raspberry Pi 4</li><li>Micro SD Card</li><li>An SD card to USB converter that matches the USB ports on your device if your device doesn't have an SD card slot</li><li>Raspberry Pi 4 power supply (USB-C)</li><li>[USB Microphone/Speaker](https://www.amazon.com/USB-Speakerphone-Conference-Business-Microphones/dp/B07Q3D7F8S)</li><li>keyboard, mouse and monitor</li><li>[micro-HDMI to HDMI adapter or cable](https://www.raspberrypi.org/products/micro-hdmi-to-standard-hdmi-a-cable/)</li></ul> |
| Software required | <ul><li>[Raspberry Pi Imager](https://www.raspberrypi.org/downloads/)</li></ul> |
| Azure Services | <ul><li>[Azure Cognitive Services Speech service](https://azure.microsoft.com/services/cognitive-services/speech-services/?WT.mc_id=academic-7372-jabenn)</li><li>[Azure Cognitive Services Translator service](https://azure.microsoft.com/services/cognitive-services/translator/?WT.mc_id=academic-7372-jabenn)</li></ul>|
| Programming Language | <ul><li>Python</li></ul><br>If you want to learn Python, check out these free resources:<br><ul><li>[Python for beginners video series on Channel9](https://channel9.msdn.com/Series/Intro-to-Python-Development?WT.mc_id=academic-7372-jabenn)</li><li>[Take your first steps with Python learning path on Microsoft Learn](https://docs.microsoft.com/learn/paths/python-first-steps/?WT.mc_id=academic-7372-jabenn)</li></ul> |
| Prerequisites | Basic proficiency with Python.<br><br>You will also need an [Azure subscription](https://github.com/microsoft/iot-curriculum/tree/main/labs/ai-edge/ocr#azure-subscription) |
| Date | October 2020 |
| Learning Objectives | <ul><li>Set up Azure Cognitive Services</li><li>Convert speech to text with Azure Speech Services</li><li>Convert text to speech with Azure Speech Services</li><li>Convert speech to translated speech with Azure Speech and Translator Services</li></ul> |
| Time to complete | 2 hours |

## Azure Cognitive Services

[Azure Cognitive Services](https://azure.microsoft.com/services/cognitive-services/?WT.mc_id=academic-7372-jabenn) is a comprehensive family of AI services and cognitive APIs to help you build intelligent apps.

This lab covers the [Azure Cognitive Services Speech service](https://azure.microsoft.com/services/cognitive-services/speech-services/?WT.mc_id=academic-7372-jabenn) and [Azure Cognitive Services Translator service](https://azure.microsoft.com/services/cognitive-services/translator/?WT.mc_id=academic-7372-jabenn). Thess services have a free tier, so there will be no cost to run this lab.

> Note that you can only have one free tier instance of each resource per Azure subscription, so if you already have a free tier set up, you can re-use it or use a paid tier. You can find the current pricing on the [Azure cognitive services pricing page](https://azure.microsoft.com/pricing/details/cognitive-services/?WT.mc_id=academic-7372-jabenn).

To learn more about these services, and to try them out on a Mac or PC, work through the [Process and Translate Speech with Azure Cognitive Speech Services](https://docs.microsoft.com/learn/paths/process-translate-speech-azure-cognitive-speech-services/?WT.mc_id=academic-7372-jabenn) learning path on [Microsoft Learn](https://docs.microsoft.com/learn?WT.mc_id=academic-7372-jabenn).

### Azure subscription

This lab is designed for courses where Azure resources are provided to students by the institution. To try them out, you can use one of our free subscriptions. Head to the [Azure Subscriptions Guide](../../../azure-subscription.md) for from information on setting up a subscription.

### Create the Azure Cognitive Services resources

To create an Azure Cognitive Services Speech resource, follow the instructions in one of the following guides, depending on if you want to use the Azure Portal, or the Azure Command-line interface (CLI).

For the speech service, create a single-service resource, and use the `F0` tier, which is free.

For the translator service, create a single-service resource, set the location to `Global`, and use the `F0` tier, which is free.

* [Create a Cognitive Services resource using the Azure portal](https://docs.microsoft.com/azure/cognitive-services/cognitive-services-apis-create-account?tabs=multiservice%2Cwindows&WT.mc_id=iotcurriculum-github-jabenn)
* [Create a Cognitive Services resource using the Azure Command-Line Interface(CLI)](https://docs.microsoft.com/azure/cognitive-services/cognitive-services-apis-create-account-cli?tabs=windows&WT.mc_id=iotcurriculum-github-jabenn)

You will need your Key and Endpoint for the Speech resource, and the key for the Translator resource to use them in this lab.

## Set up the Raspberry Pi

To run this lab, you will need to use the Pi using the full Raspberry Pi OS connected via a monitor/keyboard/mouse, or using screen sharing such as VNC.

Connect the Pi to a keyboard, mouse, and a monitor. Connect the USB microphone/speaker.

### OS setup

Ensure you are running the latest Raspberry Pi OS (full version, not Lite), with the latest updates, configured based on how you want to access the Pi (for example with VNC enabled if you are going to control it over VNC).

You can read instructions on how to configure an SD card with Raspberry Pi OS in the [Raspberry Pi Installing Operating System images documentation](https://www.raspberrypi.org/documentation/installation/installing-images/).

Once you boot up your Pi, follow the instructions on-screen to set up the Pi, including connecting to WiFi (or connect the Pi to an ethernet cable) and updating all the software.

Once it is set up, if you'd rather connect remotely to the Pi, then follow the instructions in the [Microsoft Raspberry Pi headless setup guide](https://github.com/microsoft/rpi-resources/tree/master/headless-setup#remote-desktop) to configure VNC or Remote Desktop.

### Speaker setup

This lab will playback audio. To do this playback, you will need a speaker connected, such as using a USB microphone/speaker all in one unit. If there is only one microphone connected it will be the default and used, but the Raspberry Pi HDMI connection also supports audio out, so you can use the speakers in your monitor if you have them.

To configure the audio output source, right click on the speaker icon on the Raspberry Pi toolbar, then select *Audio Outputs*, then select your preferred audio output.

### Software installation

Once your Pi is set up, you will need to install Jupyter Notebooks, as this lab runs from a notebook. You will also need some libraries to be able to access the microphone.

1. Follow the instructions in the [Configure Jupyter Notebooks on a Raspberry Pi guide](../../../../devices/configure-jupyter-notebooks-raspberry-pi.md) to install and run Jupyter Notebooks. You don't need to run the last step that launches Jupyter Notebooks.

1. From the terminal, run the following command to install needed libraries

    ```sh
    sudo apt install libffi-dev libportaudio2 python3-scipy --yes
    ```

1. Some Python libraries need to be installed before the notebook is launched. Use the following command to install them:

    ```sh
    pip3 install cffi pyaudio sounddevice
    ```

## Run the relevant Jupyter Notebook

This lab contains 3 Jupyter Notebooks:

* [speech-to-text.ipynb](./speech-to-text.ipynb) - Converting speech to text
* [text-to-speech.ipynb](./text-to-speech.ipynb) - Converting text to speech
* [speech-translation.ipynb](./speech-translation.ipynb) - Translating speech to a different language

To run the notebooks, you first need to clone this repo, then you can launch them in Jupyter Notebooks.

1. From the Pi Terminal, run the following command to clone this repo to get the Jupyter notebook:

    ```sh
    git clone https://github.com/microsoft/iot-curriculum.git
    ```

1. Navigate to the Notebook folder

    ```sh
    cd ./iot-curriculum/labs/ai-edge/speech
    ```

1. Open the notebook. This will launch the Jupyter Notebook running in the Chromium browser.

    To open the speech to text notebook, run:

    ```sh
    jupyter notebook speech-to-text.ipynb
    ```

    To open the text to speech notebook, run:

    ```sh
    jupyter notebook text-to-speech.ipynb
    ```

    To open the speech translation notebook, run:

    ```sh
    jupyter notebook speech-translation.ipynb
    ```

1. Work through the notebook - read the directions and follow the instructions and running each cell. Make sure to set the `KEY`, `ENDPOINT`, `LANGUAGE`, and any other value in the first code cell!

> These samples are not production quality - they have no error trapping and assume all calls work. When using these in your own apps, ensure you handle any errors correctly.

## Clean up

Once you have finished this lab, you can clean up your resource group to delete any Azure resources that you have created, stopping you being billed for them. You can read about how to do this in the [Deleting Azure Resource Groups guide](https://docs.microsoft.com/azure/azure-resource-manager/management/manage-resource-groups-portal?WT.mc_id=academic-7372-jabenn#delete-resource-groups)
