import numpy as np
from sense_hat import SenseHat
from pyod.models.iforest import IForest
from pyod.utils.data import generate_data
from pyod.utils.data import evaluate_print
import pickle


clf =  pickle.load( open( "IForrest.p", "rb" ) )

def transform(arr):
    ret = []
    for z in arr:
        for a in z:
            ret.append(a)
    return ret


O = (10, 10, 10) # Black
X = (255, 0 ,0) # red

alert = transform([
        [X, X, O, O, O, O, X, X],
        [X, X, X, O, O, X, X, X],
        [O, X, X, X, X, X, X, O],
        [O, O, X, X, X, X, O, O],
        [O, O, X, X, X, X, O, O],
        [O, X, X, X, X, X, X, O],
        [X, X, X, O, O, X, X, X],
        [X, X, O, O, O, O, X, X]
        ])


clear = transform([
        [O, O, O, O, O, O, O, O],
        [O, O, O, O, O, O, O, O],
        [O, O, O, O, O, O, O, O],
        [O, O, O, O, O, O, O, O],
        [O, O, O, O, O, O, O, O],
        [O, O, O, O, O, O, O, O],
        [O, O, O, O, O, O, O, O],
        [O, O, O, O, O, O, O, O]
        ])

while True:
    dat = np.array([gyro['x'],gyro['y'],gyro['z'],accel['x'],accel['y'],accel['z']])
    pred = clf.predict(X)
    if pred[0] == 1:
        sense.set_pixels(alert)
    else:
        sense.set_pixels(clear)
   
    time.sleep(0.1)
