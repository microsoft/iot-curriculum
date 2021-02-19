import numpy as np
import os
from glob import glob
from sklearn.svm import SVC
from micromlgen import port
from sklearn.model_selection import train_test_split

def load_features(folder):
    dataset = None
    classmap = {}
    for class_idx, filename in enumerate(glob('%s/*.csv' % folder)):
        class_name = os.path.splitext(filename)[0]
        classmap[class_idx] = class_name
        samples = np.loadtxt(filename, dtype=float, delimiter=',')
        labels = np.ones((len(samples), 1)) * class_idx
        samples = np.hstack((samples, labels))
        dataset = samples if dataset is None else np.vstack((dataset, samples))
    return dataset, classmap

np.random.seed(0)
dataset, classmap = load_features('data')
X, y = dataset[:, :-1], dataset[:, -1]

# this line is for testing your accuracy only: once you're satisfied with the results, set test_size to 1
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)

clf = SVC(kernel='poly', degree=2, gamma=0.1, C=100)
clf.fit(X_train, y_train)

print('Accuracy', clf.score(X_test, y_test))
print('Exported classifier to plain C')
print()
print(port(clf, classmap=classmap))