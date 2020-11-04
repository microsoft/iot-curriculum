# micro_speech

```micro_speech``` is the main function of the micro_speech program. This file will load/allocate all of the necessary libraries and resources then execute the main detection loop.

### TfLiteStatus

As a general note- many operations performed in this code will have a return value of a ```TfLiteStatus``` object. This is an object designed exclusively to report any errors during a process.

## namespace

```namespace``` defines the global variables used for the micro_speech program. Also notably, this block of code defines the size of any intermediate tensors this model will be working with in the ```tensor_arena``` and defines the area of memory for the input features with the ```feature_buffer```.

## setup()

```setup()``` is a standard Arduino function necessary for Arduino builds such as this. This function will setup all of the resources which will be needed for execution. Notable sections of code include:

```model = tflite::GetModel(g_model)``` 

This will load the model which has been predefined in hex as ```g_model``` found in "micro_features_model.cpp".

```static tflite::MicroMutableOpResolver<4> micro_op_resolver(error_reporter);```

This object helps minimize the memory footprint of the model interpreter. In the tflite paradigm, the model and the model interpreter are seperate objects. By default, the model interpreter loads all of the most common operations a model could perform, but when dealing with the memory restrictions of a microcontroller, it is useful to only load in the necessary operations for a particular model. In this case, the model only contains the following four operations:

1. ```DEPTHWISE_CONV_2D```. This will perform a depthwise 2D convolution which is a 2D convolution performed on each layer of depth for a 3D tensor.
2. ```FULLY_CONNECTED```. This will perform a fully connected matrix multiplication between two tensors at successive levels.
3. ```SOFTMAX```. This will perform the final softmax activation function on the output tensor as defined here: https://en.wikipedia.org/wiki/Softmax_function
4. ```RESHAPE```. This will reshape the dimensions of a tensor.

```static tflite::MicroInterpreter static_interpreter(model, micro_op_resolver, tensor_arena, kTensorArenaSize, error_reporter);```

This instantiates the model interpreter with the previously defined tensor sizes from ```namespace``` and operation definitions from ```micro_op_resolver```.

```TfLiteStatus allocate_status = interpreter->AllocateTensors();```

This allocates the appropriate amount of memory for the tensors that will be used during the model's inference.

```model_input = interpreter->input(0);```
```...```
```model_input_buffer = model_input->data.int8;```

This defines the input buffer used to feed the collected speech data into the model through the model interpreter using the previously allocated memory.

```static FeatureProvider static_feature_provider(kFeatureElementCount, feature_buffer);```

This instantiates the object which will create the speech features as defined in "feature_provider.cpp".

```static RecognizeCommands static_recognizer(error_reporter);```

This instantiates the object which will take the output tensor of the model and interpret the results.


## loop()

```loop()``` is another standard Arduino function necessary. This is the main loop function that ```micro_speech``` will execute indefinitely after ```setup()```. Notable sections of code include:

```TfLiteStatus feature_status = feature_provider->PopulateFeatureData(error_reporter, previous_time, current_time, &how_many_new_slices);```

This will collect the features to be input into the model through the interpreter for inference.

```TfLiteStatus invoke_status = interpreter->Invoke();```

This will prompt the model interpreter to run the collected features as an inference through the model for this iteration of the loop. This ultimately results as the output tensor located in the interpreter as ```interpreter->output(0)```.

```TfLiteStatus process_status = recognizer->ProcessLatestResults(output, current_time, &found_command, &score, &is_new_command);```

This will prompt the recognizer to process the interpreter's output tensor and determine if any of the model's detectable words have been detected.

```RespondToCommand(error_reporter, current_time, found_command, score, is_new_command);```

This will call the function from "arduino_command_responder.cpp" to respond to any commands detected. In the case of this lab, this function will cause the green light to stay on for three seconds as well as output a message to the serial port reporting the detection of the word "yes" and the time it was detected.