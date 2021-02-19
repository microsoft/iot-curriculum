# Train the TinyML model

In the [previous step](./audio-capture.md) you programed the Arduino device to capture audio data ready to classify to train the model. In this step you will use the output from the audio capture to train a TinyML model.

## Create the Python training script

The audio data can be used to train an ML model that can be used to classify new audio data. In this case, the model being trained is a [Support Vector Machine trained to do classification](https://scikit-learn.org/stable/modules/svm.html). This model will be trained using the [Scikit-Learn Python package](https://scikit-learn.org/).

To train the model, you will need Python, as well as a number of Python packages installed.

1. If you do not have an up-to-date version of Python installed, install it from the [Python downloads page](https://www.python.org/downloads/), or using your preferred method such as [the Windows store](https://www.microsoft.com/en-us/p/python-39/9p7qfqmjrfp7?WT.mc_id=academic-7372-jabenn) or [Homebrew on macOS](https://docs.python-guide.org/starting/install3/osx/).

1. Create a folder on your computer to hold the Python code

1. Open this folder in VS Code

### PyLance in Visual Studio Code

Python support with full debugging support and intellisense, can be added to VS Code via the [PyLance extension](https://devblogs.microsoft.com/python/announcing-pylance-fast-feature-rich-language-support-for-python-in-visual-studio-code/?WT.mc_id=academic-7372-jabenn).

1. Select the **Extensions** tab from the VS Code side menu

    ![the extension menu](../../../images/vscode-extensions-menu.png)

1. Search for `PyLance` and select the **Install** button to install the PyLance Python extension

    ![The PyLance install button](../../../images/vscode-extensions-pylance-install-button.png)

Visual Studio Code will now be configured to run Python.

### Create a Python Virtual Environment

Python comes in various versions, and Python apps can use external code in packages installed via a tool called `pip`. This can lead to problems if different apps need different package versions, or different Python versions. To make it easier to avoid issues with package or Python versions, it is best practice to use *virtual environments*, self-contained folder trees that contain a Python installation for a particular version of Python, plus a number of additional packages.

1. When the new Visual Studio Code window is opened, the terminal should be opened by default. If not, open a new terminal by selecting *Terminal -> New Terminal*.

1. Create a new file called `train_classifier.py`. This is the file that will contain the code for the model trainer, and by creating it the Python extension in Visual Studio Code will be activated.

1. The Python extension will activate, and you can see the progress in the status bar.

1. Create a new virtual environment called `.venv` using Python 3 by running the following command in the terminal

   ```sh
   python3 -m venv .venv
   ```

1. A dialog will pop up asking if you want to activate this virtual environment. Select **Yes**.

   ![The virtual environment dialog](../../../images/vscode-launch-venv-dialog.png)

1. The existing terminal will not have the virtual environment activated. Close it by selecting the trash can button

   ![The kill terminal button](../../../images/vscode-kill-terminal.png)

1. Create a new terminal by selecting *Terminal -> New Terminal*. The terminal will load the virtual environment

### Install pip packages

Pip packages can be installed one by one via the command line, but it's best practice to create a file that lists all the Pip packages needed by an application, so that they can all be installed at once. This file can also be checked in to source code control with your code allowing other developers to re-create your setup. This file is traditionally called `requirements.txt`.

1. Create a new file called `requirements.txt`

1. Add the following to this file. You can also find this code in the [requirements.txt](../code/model-trainer/requirements.txt) file in the [code/model-trainer](../code/model-trainer) folder.

    ```sh
    scikit-learn
    micromlgen
    ```

    * `scikit-learn` is the Pip package for the Scikit-Learn Machine learning library that can be used to train the model
    * `micromlgen` is a Pip package for a utility that can export a Scikit-Learn model as C++ code that can be run on a microcontroller

1. Save the file

1. Install these packages by running the following command in the terminal:

    ```sh
    pip install -r requirements.txt
    ```

> If you are using an M1 based Mac, at the time of writing Scikit-Learn is not available as a Pip package that runs on the M1 processor. You can find instructions on how to install it using Miniforge in [this blog post](https://dev.to/jimbobbennett/installing-scikit-learn-on-an-apple-m1-114d).

### Set up the data files with the training data

The training data captured in the previous step will be loaded by the training script to train the model.

1. Create a folder called `data` inside the folder opened in VS Code

1. Copy all the CSV files created in the previous part into this folder

### Write the code

1. Add the following code to the `train_classifier.py` file:

    ```python
    import numpy as np
    import os
    from micromlgen import port
    from sklearn.svm import SVC
    from sklearn.model_selection import train_test_split

    label_idx = 0

    # A map of label indexes to labels
    label_map = {}

    # Prepare a dataset to hold the CSV data
    dataset = None

    # Prepare an array to hold the labels
    dataset_labels = None

    # Make the random numbers predictable so the model is the same each time
    np.random.seed(0)

    # Iterate through the files in the data folder loading the data
    # This assumes the files are all valid csv files and the label
    # is the file name without the .csv extensiojn
    for file in os.listdir('data'):
        # Get the file name to use as the label
        file_name, ext = os.path.splitext(file)
        label_map[label_idx] = file_name

        # Load the data from the CSV files and build a dataset by concatenating
        # all the data into one big array
        file_contents = np.loadtxt('data/' + file, delimiter=',')
        dataset = file_contents if dataset is None else np.vstack((dataset, file_contents))

        # Create an array of labels containing one row for each row in the main dataset
        # with the value for each row the label index
        labels = np.full((len(file_contents), 1), label_idx)
        dataset_labels = labels if dataset_labels is None else np.vstack((dataset_labels, labels))

        # Increment the label index for the next file
        label_idx = label_idx + 1

    # Split the data into a training and testing set to test the accuracy of the model
    # If you are happy with the accuracy of the model, you can remove this split
    dataset_train, dataset_test, label_train, label_test = train_test_split(dataset, dataset_labels.ravel(), test_size=0.2)

    # Build the support vector classification for our data and train the model
    svc = SVC(kernel='poly', degree=2, gamma=0.1, C=100)
    svc.fit(dataset_train, label_train)

    # Test the accuracy of the model
    print('Accuracy:', svc.score(dataset_test, label_test))
    print()

    # Convert the model to C code and write to the classifier.h file
    c_code = port(svc, classmap=label_map)
    with open('classifier.h', 'w') as f:
        f.write(c_code)
        f.close()

    print('Classifier written to classifier.h.')
    ```

    This code loads all the audio data from all the files in the `data` folder, and stores in a large array. It also tracks the lables for the data using the file name as the data label by creating an array of numerical labels for each row in the data set, and a mapping from the numerical labels to the names.

    This dataset is split into 80% training data and 20% testing data. The 80% training data is used to train the model, and the testing data is used to get the accuracy of the model.

    > If you are happy with the accuracy of the model, you can remove the split and create the model just using the dataset and labels.

    Finally, the `micromlgen` package is used to convert the model to C++ code that can be run on the Arduino device.

1. Save the file

1. Run the code by running the following command in the terminal:

    ```sh
    python train_classifier.py
    ```

1. The code will run and create a file called `classifier.h` in the root of the folder. This file is needed in the next step to create the classifier.

## Next steps

In this step, you used the output from the audio capture to train a TinyML model. In the [next step](./audio-classifier.md) you will use this model to create an audio classifier.
