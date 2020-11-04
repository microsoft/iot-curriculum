# Machine Learning on Microcontrollers

This lab covers using an Arduino Nano 33 BLE Sense to recognize speech. This lab will utilize and explain machine learning techniques specialized for the memory constraints of microcontrollers.

| Authors | [Connor Hagen](https://github.com/chagen24) |
|:---|:---|
| Sponsor  | [Microsoft AI & IOT Insiders Lab](https://microsoftiotinsiderlabs.com/en) |
| Target platform   | <ul><li>Arduino Nano 33 BLE Sense</li></ul> |
| Hardware required | <ul><li>Arduino Nano 33 BLE Sense</li><li>Micro USB to USB cable</li><li>A PC with Windows or Ubuntu</li></ul> |
| Software required | <ul><li>[Arduino IDE](https://www.arduino.cc/en/Main/Software)</li></ul> |
| Programming Language | <ul><li>C++</li></ul> |
| Prerequisites | Basic understanding of C++ |
| Date | October 2020 |
| Learning Objectives | <ul><li>Interface with a microcontroller</li><li>Understand the basic concepts of machine learning given memory constraints</li></ul> |
| Time to complete | 1 hour |


## tinyML

Machine learning models are most often deployed to devices optimized with plenty of computational resources including GPUs, large amounts of RAM, and fast CPU's. But what about scenarios where these computational resources are restricted? This is when the concepts of [tinyML](https://www.tinyml.org/) must be employed.



## Set up the Arduino IDE

This lab will require you to install the Arduino IDE to interface with the device. Navigate to the [Arduino IDE Downloads](https://www.arduino.cc/en/Main/Software) and install the software appropriate for your PC.

### Install Arduino Nano 33 BLE Sense Board Tools

After downloading the Arduino IDE, open it and install the Arduino Nano 33 BLE Sense board tools with the following steps:

1. From the header menu select ```Tools --> Board --> Boards Manager..```
2. In the search bar type ```Arduino Nano 33 BLE```
3. Select ```Install``` for the first result in the list

### Install the Arduino_TensorFlowLite Library

Install the Arduino_TensorFlowLite library with the following steps:

1. From the header menu select ```Tools --> Manage Libraries```
2. Search for ```Arduino_TensorFlowLite```
3. Select ```Install``` for the first result in the list

### Connect the Arduino Nano 33 BLE Sense

Connect the device to the Arduino IDE with the following steps:

1. USB cable to the device and a USB port on your PC
2. From the header menu select ```Tools --> Board --> Arduino Mbed OS Boards (nRF52840 / STM32H747) --> Arduino Nano 33 BLE```
3. From the header menu navigate to ```Tools --> Port``` then select the serial port currently connected to the device
4. Test the device's connection by selecting ```Tools --> Get Board Info```

### Load the micro_speech example

Download the code for this lab by selecting from the header menu ```File --> Examples --> Arduino_TensorFlowLite --> micro_speech```

## Understanding the micro_speech code

To understand the micro_speech code, refer to the descriptions found in "micro_speech_explanations.md" and "support_libraries_explanations.md"

## Build, load, then run the example

The Arduino IDE can build, load, and run the example with the following steps:

1. Build the code by selecting from the header menu ```Sketch --> Verify and Compile```
2. Load the newly compiled binary by selecting from the header menu ```Sketch --> Upload```

After the code has been built and uploaded to the device, saying the word "yes" near the microphone will cause the green LED on the device to stay on for three seconds and a message will be displayed in the following format

```Heard yes (201) @4056ms```

The "201" in this case represents the model's certainty, and the "4056ms" represents how many milliseconds since bootup the word "yes" was detected in this instance.
