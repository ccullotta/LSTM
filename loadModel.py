from tools.bin import*
from keras.models import Sequential
from keras.layers import Dense, Activation
from keras.layers import LSTM
from keras.models import model_from_json
from sklearn.model_selection import train_test_split
import math
import numpy as np
import matplotlib.pyplot as plt


import os
os.environ["CUDA_VISIBLE_DEVICES"] = "-1"
data = openBin("btcClosingData3")

targei = openBin("btcTraining")

data = data[:(len(data) - 1)]
npData = np.array(data, dtype=float)
suma = np.sum(npData)
print(np.isnan(suma))
npTarget = np.array(targei, dtype=float)

print(npData.shape) #shape is 700,30,2 meaning 700 samples of 30 sets of 2 data 
x_train,x_test,y_train,y_test = train_test_split(npData, npTarget, test_size = 0.2, random_state = 4)



json_obj = open('firstmodel', 'r')
loaded_model = json_obj.read()
json_obj.close()
model = model_from_json(loaded_model)
model.load_weights("firstModelWeights.h5")
results = model.predict(x_test)
model.compile(loss="binary_crossentropy", optimizer='adam', metrics=['accuracy'])
print(model.evaluate(x_test,y_test, verbose=0))