# Audio model trainer

This Python program takes the output from the [audio capture program](../audio-capture) and uses it to train a TinyML model that can then be used in the the [audio classifier program](../audio-classifier).

## Setting up the Python environment

* Create a virtual environment for this folder using Python 3.8 or above
* Install the pip packages in the `requirements.txt` file

    > If you are using a new Apple Silicon based Mac, then the packages may not install as at the time of writing there is no supported Scikit-Learn package for the Mac. Instead you will need to use MiniForge. Refer to [this blog post](https://dev.to/jimbobbennett/installing-scikit-learn-on-an-apple-m1-114d) for instructions.
* Copy the CSV files created from the [audio capture program](../audio-capture) into the [`data`](./data) folder. These files should be named for the relevant label for the audio data.
* Run the `train_classifier.py` file

The model will be trained, and the output sent to the console.

```output
(.venv) ➜  model-trainer git:(master) ✗ python train_classifier.py 
Accuracy 1.0
Exported classifier to plain C
#pragma once
#include <cstdarg>
namespace Eloquent {
}
```

Copy everything from `#pragma once` to the end of the output and paste it into the [`classifier.h`](../audio-classifier/src/classifier.h) header file in the audio classifier project.