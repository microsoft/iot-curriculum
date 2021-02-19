// Copyright (c) Microsoft Corporation.
// Licensed under the MIT license.

#ifndef __SAMPLE_CAPTURE_H__
#define __SAMPLE_CAPTURE_H__

#include <PDM.h>
#include <arm_math.h>

// The size of the data coming in from the microphone
#define BUFFER_SIZE 512U

// 128 samples is enough for 2 seconds of audio - it's captured at 64 samples per second
#define SAMPLE_SIZE 128
#define GAIN (1.0f / 50)
#define SOUND_THRESHOLD 1000

/**
 * @brief The function signature for the callback function that is called when we have a full set of samples.
 */
typedef void (*samples_ready_callback)(float*);

/**
 * @brief A helper class for accessing the BLEs microphone.
 * 
 * Audio data is captured as a full 512 byte data buffer (1/64 second of audio data).
 * Each buffer is then converted into a root mean square value of the buffer to create a smaller
 * representation of the audio.
 * 
 * If this root mean square value is over a threshold (i.e. not silence), then the next SAMPLE_SIZE
 * buffers are captured and the RMS values calculated. Once a full set of samples is retrieved, a
 * callback function is invoked, passing this set of samples.
 * 
 * This essentially converts audio data to a smaller representation for use with training and inference 
 * with TinyML models.
 * For example - 2 seconds of audio * becomes 128 4-byte float values (512 bytes) instead of
 * 32,768 2-byte integerss (65,536 bytes).
 */
class SampleCapture
{
public:
    /**
     * @brief Setup the PDM library to access the microphone at a sample rate of 16KHz
     * @param callback A callback function to call when there is a full set of samples ready.
     * This callback will take the samples as a parameter as a SAMPLE_SIZE array of floats.
     * This array is owned by this class, so the callback will need to take a copy.
     */
    void init(samples_ready_callback callback)
    {
        // Set up the audio callback
        PDMHelper::setSampleCapture(this);

        // Set up the callback when a set of samples is ready
        _callback = callback;

        // Start listening on the microphone at a sample rate of 16KHz
        PDM.begin(1, 16000);
        PDM.setGain(20);
    }

private:
    /**
     * @brief A helper wrapper class that can connect a method on the SampleCapture object
     * to the PDM callback that expects a static method
     */
    class PDMHelper
    {
    public:
        /**
         * @brief Sets up the PDM callback to a method on the SampleCapture class
         */
        static void setSampleCapture(SampleCapture *sampleCapture)
        {
            // Store the sample capture
            _sampleCapture = sampleCapture;

            // Set up the callback
            PDM.onReceive(PDMHelper::onReceive);
        }

    private:
        /**
         * @brief The callback from the PDM class, calls the SampleCapture update method
         */
        static void onReceive()
        {
            _sampleCapture->onReceive();
        }

        inline static SampleCapture *_sampleCapture;
    };

    /**
     * @brief Reads the audio data from the PDM buffer and calculates the
     * root mean square value, adding it to the samples if needed.
     */
    void onReceive()
    {
        // Check we have a full buffers worth
        if (PDM.available() == BUFFER_SIZE)
        {
            // Read from the buffer
            PDM.read(_buffer, BUFFER_SIZE);

            // Calculate the root mean square value of the buffer
            int16_t rms;
            arm_rms_q15((q15_t *)_buffer, BUFFER_SIZE/sizeof(int16_t), (q15_t *)&rms);

            // If we are not currently collecting samples, check if the RMS value is
            // above our threshold - as in we've heard something, not just silence.
            // If we hear something, start collecting samples
            if (!_started)
            {
                if (rms > SOUND_THRESHOLD)
                {
                    _started = true;
                    _position = 0;
                }
            }

            // If were collecting data, either because we already were, or because we've
            // just detected audio that's not slience, add it to the next slot in the samples
            // array.
            if (_started)
            {
                // Add the RMS value to the samples array in the next slot, multiplied by a 
                // gain value to give the signal a boost
                _samples[_position] = rms * GAIN;

                // Move to the next slot in the samples
                _position++;

                // If we're filled the samples buffer, stop collecting data and call the callback
                if (_position >= SAMPLE_SIZE)
                {
                    _started = false;
                    _position = 0;

                    // Pass the samples to the callback
                    _callback(_samples);
                }
            }
        }
    }

    // The buffer to read from the PDM into - use this as a field to reduce overhead
    // creating and deleteing it every time the buffer is full
    int16_t _buffer[BUFFER_SIZE/sizeof(int16_t)];

    // The samples buffer- use this as a field to reduce overhead
    // creating and deleteing it every time the buffer is full
    float _samples[SAMPLE_SIZE];

    // Are we currently capturing data - we capture from when audio above the SOUND_THRESHOLD
    // is detected, for SAMPLE_SIZE samples
    bool _started;

    // The current position in the samples array to write the next sample to
    int _position;

    // The callback to call when we have a full set of samples
    samples_ready_callback _callback;
};

#endif __SAMPLE_CAPTURE_H__