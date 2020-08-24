from pyod.models.iforest import IForest
from pyod.utils.data import generate_data
from pyod.utils.data import evaluate_print
import numpy as np
import pickle


X_train = np.loadtxt('X_train.txt', dtype=float)
y_train = np.loadtxt('y_train.txt', dtype=float)
X_test = np.loadtxt('X_test.txt', dtype=float)
y_test = np.loadtxt('y_test.txt', dtype=float)


clf = IForest()
clf.fit(X_train)

y_test_pred = clf.predict(X_test)  # outlier labels (0 or 1)
y_test_scores = clf.decision_function(X_test)  # outlier scores
print(y_test_pred)

print("\nOn Test Data:")
evaluate_print('IForest', y_test[:len(y_test_scores)], y_test_scores)

pickle.dump( clf, open( "IForest.p", "wb" ) )