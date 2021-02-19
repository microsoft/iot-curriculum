# Audio Capture

This folder contains a [PlatformIO](https://platformio.org/platformio-ide) project to build an audio capture app that runs on an [Arduino Nano 33 BLE Sense](https://store.arduino.cc/usa/nano-33-ble-sense) board.

You can read more about this project in the [top level README.md file](../README.md).

To build and deploy this project, you will need to open this folder in [Visual Studio Code](https://code.visualstudio.com/?WT.mc_id=academic-7372-jabenn) with the [PlatformIO extension](https://platformio.org/platformio-ide) installed. You will then be able to build the project and upload to a Arduino Nano 33 BLE Sense board.

## Building this project

This project has a library dependency on the ARM CMSIS static library. You will need to download this from the ARM GitHub repo.

* Head to [the CMSIS GCC libs folder in the GitHub repo](https://github.com/ARM-software/CMSIS_5/tree/5.7.0/CMSIS/DSP/Lib/GCC)
* Download `libarm_cortexM4l_math.a` from that repo page
* Add the file to the root folder of this project
* Build and upload as normal

## Running the project

Once the project is running on the board, it will listen for audio and output RMS values to the serial port.

* Connect to the serial monitor to view the audio values
* Make the one of the relevant noises into the microphone of the board. Pause after each noise and you will see a line output to the serial monitor.
* Repeat 15-30 times for that one noise
* Copy the values from the serial monitor into a CSV file named using the name of the label (for eample if you were capturing numbers you would put the data for one into `one.csv`, for two into `two.csv` and so on).
* Clear the serial output and repeat the above steps for all the noises you are interested in

## Processing the output

Refer to the [top level README.md file](../README.md) for instructions on how to process and use the output to classify noises.
