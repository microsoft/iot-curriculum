// Copyright (c) Microsoft Corporation.
// Licensed under the MIT license.

/**
 * Audio Capture
 * 
 * This program listens on the microphone capturing audio data, classifying it and outputting the
 * classification label to the Serial port.
 * 
 * Audio data is captured as a full 512 byte data buffer (1/64 second of audio data).
 * Each buffer is then converted into a root mean square value of the buffer to create a smaller
 * representation of the audio.
 * 
 * If this root mean square value is over a threshold (i.e. not silence), then the next SAMPLE_SIZE
 * buffers are captured and the RMS values calculated. Once a full set of samples is retrieved, a
 * callback function is invoked, passing this set of samples.
 * 
 * The default for SAMPLE_SIZE is 128 - 2 seconds of audio data. You can configure this in the 
 * sample_capture.h header file.
 * 
 * This essentially converts audio data to a smaller representation for use with training TinyML models.
 * For example - 2 seconds of audio * becomes 128 4-byte float values (512 bytes) instead of
 * 32,768 2-byte integerss (65,536 bytes).
 * 
 * Once a sample is colected, it is classified.
 * 
 */

#include "sample_capture.h"
#include "classifier.h"

// The classifier
Eloquent::ML::Port::SVM clf;

// A helper class that captures audio from the microphone
SampleCapture sampleCapture;

// A buffer used to store data read from the Sample Capture class
float _samples[SAMPLE_SIZE];

// Tracks if we have samples ready to log to the serial port
bool _ready;

/**
 * @brief A callback that is called whenever the sample capture object has a full buffer of audio
 * RMS values ready for processing
 */
void onSamples(float *samples)
{
	memcpy(_samples, samples, SAMPLE_SIZE * sizeof(float));
	_ready = true;
}

/**
 * @brief Classify the samples, writing the label to the serial port
 */
void procesSamples()
{
	// Write out the classification to the serial port
	Serial.print("Label: ");
	Serial.println(clf.predictLabel(_samples));
}

/**
 * @brief Sets up the serial port and the sample capture object
 */
void setup()
{
	// Start the serial connection so the captured audio data can be output
	Serial.begin(115200);

	// Start the sample capture object to listen for audio and callback when
	// it has a full set of samples
	sampleCapture.init(onSamples);

	// Wait 3 seconds for everything to get started
	delay(3000);
}

/**
 * @brief Runs continuously capturing audio data and writing it to
 * the serial port
 */
void loop()
{
	// check to see if we have audio data
	if (_ready)
	{
		// If we do, mark it as read ready for the next loop
		_ready = false;

		// Process the samples
		procesSamples();
	}

	// Sleep to allow background microphone processing
	// Each sample is 2 seconds, so sleeping for 1 second is fine
	delay(1000);
}
