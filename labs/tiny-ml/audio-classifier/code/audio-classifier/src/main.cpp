// Copyright (c) Microsoft Corporation.
// Licensed under the MIT license.

/**
 * Audio Classifier
 * 
 * This program listens on the microphone capturing audio data.
 * Instead of capturing raw data, it captures root mean squared values allowing
 * audio to be reduced to a few values instead of thousands of values every second.
 * These values are then output to the serial port - one line per audio sample.
 * 
 * This data is then run through a TinyML classifier to classify the sound based on
 * a trained model using code pasted into the classifier.h header file.
 */

#include "mic.h"
#include "classifier.h"

// Settings for the audio
// These need to match the settings you used in the audio capture program
// 128 samples is enough for 2 seconds of audio - it's captured at 64 samples per second
#define SAMPLES 128
#define GAIN (1.0f / 50)
#define SOUND_THRESHOLD 1000

// An array of the audio samples
float features[SAMPLES];

// A wrapper for the microphone
Mic mic;

// The classifier
Eloquent::ML::Port::SVM clf;

/**
 * @brief PDM callback to update the data in the mic object
 */
void onAudio()
{
    mic.update();
}

/**
 * @brief Read given number of samples from mic
 * @return True if there is enough data captured from the microphone,
 * otherwise False
 */
bool recordAudioSample()
{
    // Check the microphone class as captured enough data
    if (mic.hasData() && mic.pop() > SOUND_THRESHOLD)
    {
        // Loop through the samples, waiting to capture data if needed
        for (int i = 0; i < SAMPLES; i++)
        {
            while (!mic.hasData())
                delay(1);

            // Add the features to the array
            features[i] = mic.pop() * GAIN;
        }

        // Return that we have features
        return true;
    }

    // Return that we don't have enough data yet
    return false;
}

/**
 * @brief Sets up the serial port and the microphone
 */
void setup()
{
    // Start the serial connection so the captured audio data can be output
    Serial.begin(115200);

    // Set up the microphone callback
    PDM.onReceive(onAudio);

    // Start listening
    mic.begin();

    // Wait 3 seconds for everything to get started
    delay(3000);
}

/**
 * @brief Runs continuously capturing audio data and classifying it,
 * writing the predicted label to the serial port
 */
void loop()
{
    // wait for audio data
    if (recordAudioSample())
    {
        // Write out the classification to the serial port
        Serial.print("Sound number: ");
        Serial.println(clf.predictLabel(features));

        // Wait between samples
        delay(1000);
    }

    // Sleep to allow background microphone processing
    delay(20);
}
