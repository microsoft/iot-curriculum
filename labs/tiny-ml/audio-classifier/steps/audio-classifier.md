# Create the audio classifier

In the [previous step](./train-model.md), you used the output from the audio capture to train a TinyML model. In this step you will use this model to create an audio classifier.

## Use the classifier

The classifier created in the last step is ready to be added to a PlatformIO project to classify audio data captured by the Arduino device.

### Create the project

The bulk of the classifier project is identical to the audio capture project you created in an earlier step, so the easiest way to get started is to duplicate the project.

1. Create a copy of the `audio-capture` folder you created in the earlier step. Name the new folder `audio-classifier`.

1. Open the `audio-classifier` folder in VS Code

1. Copy the `classifier.h` file created by the training script in the last step into the `src` folder.

1. Open the `main.cpp` file to add the code to classify the audio

1. Add the following code below the `#include` statement for the `sample_capture.h` header file:

    ```cpp
    #include "classifier.h"

    // The classifier
    Eloquent::ML::Port::SVM clf;
    ```

    This code imports the new classifier header file and creates an instance of the classifier object.

1. Change the `procesSamples` function to classify the samples using the classifier created by the training script by replacing the function with the following code:

    ```cpp
    /**
    * @brief Classify the samples, writing the label to the serial port
    */
    void procesSamples()
    {
        // Write out the classification to the serial port
        Serial.print("Label: ");
        Serial.println(clf.predictLabel(_samples));
    }
    ```

    This code calls the classifier object to classify the audio sample, writing the output to the serial port.

1. Save the file

## Run the code

Now the code is written, it can be deployed to the Arduino device and run to capture data.

### Upload the code to the device

 1. Connect your Arduino board to your PC or Mac using a USB cable

1. From Visual Studio Code, launch the Command Palette. This is a pop-up menu that allows you to run actions from VS Code as well as any extensions installed.

    1. If you are using Windows or Linux, press `Ctrl+Shift+p`
    1. If you are using macOS, press `Command+Shift+p`

1. Search for `PlatformIO: Upload` by typing in the box, then select that option

    ![The upload option](../../../images/vscode-command-palette-platformio-upload.png)

The relevant tooling will be installed, and the code will be compiled for the device. Once built, it will be uploaded to the Arduino. You will see the progress in the VS Code terminal.

```output
Linking .pio/build/nano33ble/firmware.elf
Checking size .pio/build/nano33ble/firmware.elf
Building .pio/build/nano33ble/firmware.bin
Advanced Memory Usage is available via "PlatformIO Home > Project Inspect"
RAM:   [==        ]  17.2% (used 45112 bytes from 262144 bytes)
Flash: [=         ]   9.2% (used 90732 bytes from 983040 bytes)
================================================ [SUCCESS] Took 12.28 seconds ================================================
```

### Monitor the output

The serial output of the Arduino is the USB cable that is used to connect it to your PC or Mac. You can monitor the data being sent using the PlatformIO serial monitor.

1. Launch the serial monitor using one of these methods:
    * Open the VS Code Command Palette, search for `PlatformIO: Serial Monitor` and select this option

        ![The serial monitor command palette option](../../../images/vscode-command-palette-platformio-serial-monitor.png)

    * Select the Serial Monitor button from the status bar

        ![The serial monitor button](../../../images/vscode-status-bar-platformio-serial-monitor-button.png)

The serial monitor will listen for all messages from the device. You'll see nothing in the output to start with.

### Classify audio data

1. Make the relevant sound into the microphone on the Arduino device, either by speaking in to it, or playing the relevant audio.

1. The audio will be classified and the relevant output sent to the serial monitor. The example below shows a model trained on the words 'yes' and 'no' classifying the word 'yes' said twice, and 'no' said once.

    ```output
    > Executing task: pio device monitor <

    --- Available filters and text transformations: colorize, debug, default, direct, hexlify, log2file, nocontrol, printable, send_on_enter, time
    --- More details at http://bit.ly/pio-monitor-filters
    --- Miniterm on /dev/cu.usbmodem101  9600,8,N,1 ---
    --- Quit: Ctrl+C | Menu: Ctrl+T | Help: Ctrl+T followed by Ctrl+H ---
    Label: yes
    Label: yes
    Label: no
    ```


## Next steps

In this step you used the model create an audio classifier.
