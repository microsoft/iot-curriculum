// Copyright (c) Microsoft Corporation.
// Licensed under the MIT license.
#include <PDM.h>
#include <arm_math.h>

// The size of the data coming in from the microphone
#define MICROPHONE_BUFFER_SIZE_IN_WORDS (256U)
#define MICROPHONE_BUFFER_SIZE_IN_BYTES (MICROPHONE_BUFFER_SIZE_IN_WORDS * sizeof(int16_t))

/**
 * @brief A helper class for accessing the BLEs microphone. This reads
 * samples from the microphone at 16KHz and computes the root mean squared value.
 * This value is then retrieved which resets the value so it can be recalculated
 * from more incomng data.
 * 
 * This allows for a small data set that represents a few seconds of sound data.
 * This is not enough to reproduce the audio, but is enough to train or use a
 * TinyML model.
 */
class Mic
{
public:
    /**
     * @brief Initializes the Mic class
     */
    Mic() : _hasData(false)
    {
    }

    /**
     * @brief Setup the PDM library to access the microphone at a sample rate of 16KHz
     */
    void begin()
    {
        PDM.begin(1, 16000);
        PDM.setGain(20);
    }

    /**
     * @brief Gets if the microphone has new data
     * @return true if the microphone has new data, otherwise false
     */
    bool hasData()
    {
        return _hasData;
    }

    /**
     * @brief Get the root mean squared data value from the microphone
     * @return The root mean square value of the last data point from the microphone
     */
    int16_t data()
    {
        return _rms;
    }

    /**
     * @brief Gets the last root mean squared value and resets the calculation
     * @return The last root mean square value
     */
    int16_t pop()
    {
        int16_t rms = data();

        reset();

        return rms;
    }

    /**
     * @brief Reads the audio data from the PDM object and calculates the
     * root mean square value
     */
    void update()
    {
        // Get the available bytes from the microphone
        int bytesAvailable = PDM.available();

        // Check we have a full buffers worth
        if (bytesAvailable == MICROPHONE_BUFFER_SIZE_IN_BYTES)
        {
            // Read from the buffer
            int16_t _buffer[MICROPHONE_BUFFER_SIZE_IN_WORDS];

            _hasData = true;
            PDM.read(_buffer, bytesAvailable);

            // Calculate a running root mean square value
            arm_rms_q15((q15_t *)_buffer, MICROPHONE_BUFFER_SIZE_IN_WORDS, (q15_t *)&_rms);
        }
    }

    /**
     * @brief Mark data as read
     */
    void reset()
    {
        _hasData = false;
    }

private:
    int16_t _rms;
    bool _hasData;
};