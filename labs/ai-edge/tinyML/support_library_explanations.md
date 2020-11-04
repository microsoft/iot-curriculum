# Other components of micro_speech

The code from micro_speech uses libraries from other files included in the code base. Here is an explanation of the most important components of this lab's code.

## arduino_audio_provider.cpp

"arduino_audio_provider.cpp" defines the logic necessary to interface with the microphone and capture the features to be fed into the "FeatureProvider" which the model will ultimately use as an input tensor. 

```namespace``` will define and allocate the buffers used to capture the audio samples.

```CaptureSamples()``` defines the raw function to read in the audio from the on-board microphone. This function utilizes the "PMD" (Pulse-density modulation) library to interface with the microphone.

```TfLiteStatus InitAudioRecording(tflite::ErrorReporter* error_reporter)```

This is a wrapper function around ```CaptureSamples()``` which allows errors to be caught and returned at the "PMD" level.

```TfLiteStatus GetAudioSamples(tflite::ErrorReporter* error_reporter, int start_ms, int duration_ms, int* audio_samples_size, int16_t** audio_samples)```

This is an abstraction of the ```InitAudioRecording``` function which allows the microphone to capture audio for the desired length of time. This function will ultimately be called by "feature_provider.cpp".


## arduino_command_responder.cpp

"arduino_command_responder.cpp" defines the ```RespondToCommand``` function which will take the output tensor from the model as input and light the on-board LEDs depending on the results as well as write to the serial port the message:

```Heard [yes or no] [score] [time]```

The "score" for this model is a scalar number greater than 0. For this particular model to detect the word "yes" or "no", the model must have a score greater than 200.

```RespondToCommand``` will ultimately be called by ```loop()``` function in "micro_speech".


## feature_provider.cpp

"feature_provider.cpp" utilizes the functions from "arduino_audio_provider.cpp" to capture audio from the on-board microphone and encapsulate it as features in the format digestable by the inference model.

```PopulateFeatureData(tflite::ErrorReporter* error_reporter, int32_t last_time_in_ms, int32_t time_in_ms, int* how_many_new_slices)```

This function takes as input the window of time starting at ```last_time_in_ms``` and ending at ```time_in_ms```. The variable ```how_many_new_slices``` is assigned based on the length of time during this window divided by the variable ```kFeatureSliceStrideMs``` which represents the static length of each slice of time in this window.

Side-note: The variables such as ```kFeatureSliceCount``` and ```kFeatureSliceStrideMs``` are all values derived from values used during the model's training process. The values can be found in "micro_features_micro_model_settings.h".

The rest of the logic in ```PopulateFeatureData``` takes the audio captured from the ```GetAudioSamples``` function defined in "arduino_audio_provider.cpp" and transforms it into the appropriate features for the model using the ```GenerateMicroFeatures``` function defined in "micro_features_micro_features_generator.cpp"


## micro_features_micro_features_generator.cpp

"micro_features_micro_features_generator.cpp" defines the ```GenerateMicroFeatures``` function which takes as input an audio sample and transforms it into a tensor of features fit to the specifications of those which the inference model has been trained on.


## micro_features_model.cpp

"micro_features_model.cpp" defines the hardcoded parameters of the tflite model as an array of hex values.