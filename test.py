import requests, json
from config import *
from tools.bin import*
import numpy as np
from keras.models import Sequential
from keras.layers import Dense, Activation
from keras.layers import LSTM
from keras.models import model_from_json
from sklearn.model_selection import train_test_split
import matplotlib.pyplot as plt
import math
import os
os.environ["CUDA_VISIBLE_DEVICES"] = "-1"

def getQuote(symbol):
    data = {
        "function":"DIGITAL_CURRENCY_DAILY",
        "symbol":symbol,
        "market":'USD',
        "apikey": STOCK_DATA_KEY
    }
    r = requests.get(STOCK_DATA_URL, params=data)
    return json.loads(r.content)

def normalizeBtc(num, big, small):
    num = (num - small)/(big-small)
    # num = num/big
    # 1/(1+math.exp(-num))
    return num
    
def normalizeVol(num, big, small):
    num = num/big
    1/(1+math.exp(-num))
    return num

data = openBin("btcClosingData3")
targei = openBin("btcTraining")

npData = np.array(data, dtype=float)
suma = np.sum(npData)
print(np.isnan(suma))
npTarget = np.array(targei, dtype=float)

print(npData.shape) #shape is 700,30,2 meaning 700 samples of 30 sets of 2 data 
x_train,x_test,y_train,y_test = train_test_split(npData, npTarget, test_size = 0.2, random_state = 4)
model = Sequential()
model.add(LSTM((32),batch_input_shape=(None,60,1),return_sequences=False))

model.add(Dense(1))
model.add(Activation('sigmoid'))
model.compile(loss="binary_crossentropy", optimizer='adam', metrics=['accuracy'])
print(model.summary())

history = model.fit(x_train, y_train, epochs=1, validation_data=(x_test,y_test))
print(history)

# plt.scatter(range(len(y_test)), y_test, c = 'r')
# plt.scatter(range(len(y_test)), results, c = 'g')
# plt.show()
# plt.plot(history.history['loss'])

# modeldata = model.to_json()
# saveModel(modeldata, "firstmodel")
# model.save_weights("firstModelWeights.h5")







