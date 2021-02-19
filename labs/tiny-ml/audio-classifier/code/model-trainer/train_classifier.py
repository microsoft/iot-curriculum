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
