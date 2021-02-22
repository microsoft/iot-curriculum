# TinyML Audio classifier

This folder contains a lab with multiple parts working towards an audio classifier running on an Arduino Nano 33 BLE Sense microcontroller, taking advantage of the built-in microphone.

> This lab was inspired by [Better word classification with Arduino Nano 33 BLE Sense and Machine Learning](https://eloquentarduino.github.io/2020/08/better-word-classification-with-arduino-33-ble-sense-and-machine-learning/) by [Eloquent Arduino](https://eloquentarduino.github.io/about-me/).

| Author | [Jim Bennett](https://github.com/JimBobBennett) |
|:---|:---|
| Target platform   | <ul><li>Arduino Nano 33 BLE Sense</li></ul> |
| Hardware required | <ul><li>Arduino Nano 33 BLE Sense</li><li>USB cable</li></ul> |
| Software required | <ul><li>[Visual Studio Code](http://code.visualstudio.com?WT.mc_id=academic-7372-jabenn)</li><li>[PlatformIO](https://marketplace.visualstudio.com/items?itemName=platformio.platformio-ide&WT.mc_id=academic-7372-jabenn)</li></ul>|
| Programming Language | <ul><li>C++</li><li>Python</li></ul> |
| Prerequisites | Basic proficiency in using VS Code, C++ and Python.<br>If you want to learn Python, check out these free resources:<br><ul><li>[Python for beginners video series on Channel9](https://channel9.msdn.com/Series/Intro-to-Python-Development?WT.mc_id=academic-7372-jabenn)</li><li>[Take your first steps with Python learning path on Microsoft Learn](https://docs.microsoft.com/learn/paths/python-first-steps/?WT.mc_id=academic-7372-jabenn)</li></ul> |
| Date | February 2021 |
| Learning Objectives | <ul><li>Capture audio data suitable for TinyML using an Arduino device</li><li>Train a TinyML model using Python</li><li>Classify audio using TinyML on an Arduino device</li></ul> |
| Time to complete | 1 hour |

## The lab parts

This lab has the following parts

1. Program the Arduino device for audio capture and capture training data
1. Train a ML model using the training data
1. Program the Arduino device to classify audio

## Audio classification

Audo classification is the process of classifying a sound based on labelled training data. For example - you could train a model by using multiple recordings of someone saying the word "Yes" labelled as `Yes`, and multiple recordings of someone saying the word "No" labelled as `No`. The model could then take a new sound recording and classify it as either `Yes` or `No`.

This lab starts by coding the Arduino to record multiple samples that are labelled, then these labelled samples are used to train a model, which is then add to device code that runs on the microcontroller to classify new audio data.

The classifier you will create here needs at least 2 labels in the model, and will pick the most probable one to classify the audio.

## TinyML

TinyML is the coming together of machine learning and embedded systems. It involves training ML models that are tiny - that is substantially smaller than the models historically created, and able to run on microcontrollers with limited memory and power. It was originally defined as ML models that can run using less than 1mW of power, but has become a general term for running ML on microcontrollers.

Microcontrollers have memory limits usually in the kilobytes, meaning traditional ML models that are many megabytes in size cannot even be installed on the device, let alone run. By using TinyML models you can bring the world of ML to a microcontroller. An audio classifier (a model that can distinguish between multiple sounds) or a wake word model (a model that can detect one specific sound, such as the command to wake a smart device up), for example, can be compressed to less than 20KB using TinyML.

There is a trade off - with smaller models you lose accuracy, but this is an acceptable tradeoff for the advantages of smaller, low powered models. For example, if you were creating a voice activated smart device you would want it to consume as little power as possible waiting for a wake word, and only then powering up to listen for more instructions and using bigger models, or even sending data to the cloud. If you are using audio to classify animal behavior on a smart collar, you want long battery life and the device to be as small and light-weight as possible to reduce the inconvenience to the animal being tracked.

In this lab, the device in question is an [Arduino Nano 33 BLE Sense microcontroller](https://store.arduino.cc/usa/nano-33-ble-sense) - a board that has a built in microphone that can be used to detect and classify audio signals. It has 256KB of memory available.

## Labs

1. [Create the audio capture tool](./steps/audio-capture.md)
1. [Train the TinyML model](./steps/train-model.md)
1. [Create the audio classifier](./steps/audio-classifier.md)
