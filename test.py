import requests, json
from redHerrings.stock import Stock
from config import *
import csv
from pprint import pprint
import pickle
from coin import *
import numpy as np
from keras.models import Sequential
from keras.layers import Dense, Activation
from keras.layers import LSTM
from sklearn.model_selection import train_test_split
import matplotlib.pyplot as plt
import math

def getQuote(symbol):
    data = {
        "function":"DIGITAL_CURRENCY_DAILY",
        "symbol":symbol,
        "market":'USD',
        "apikey": STOCK_DATA_KEY
    }
    r = requests.get(STOCK_DATA_URL, params=data)
    return json.loads(r.content)

def writeToBin(data, fileName):
    with open(fileName, 'wb') as f:
        pickle.dump(data, f)

def openBin(fileName):
    with open(fileName, 'rb') as Y:
        return pickle.load(Y)

def normalizeBtc(num, big, small):
    num = (num - small)/(big-small)
    # num = num/big
    # 1/(1+math.exp(-num))
    return num
# def normalizeVol(num)
# end = openBin("bitcoin.dat")
# print(end)
# btcQuotes = []
# VolumeOfDay = []
# for day in end["Time Series (Digital Currency Daily)"]:
#     btcQuotes.append(float(end["Time Series (Digital Currency Daily)"][day]['4b. close (USD)']))
#     VolumeOfDay.append(float(end["Time Series (Digital Currency Daily)"][day]['5. volume']))
# baseData = [btcQuotes, VolumeOfDay]

# writeToBin(baseData, "inputData.dat")

baseData = openBin("inputData.dat")
data = [
    [
        [
            normalizeBtc(baseData[0][i+j], float(max(baseData[0][j:j+30])), float(min(baseData[0][j:j+30]))),
            normalizeBtc(baseData[1][i+j], float(max(baseData[1][j:j+30])), float(min(baseData[1][j:j+30])))
            ] for i in range(30)
        ] for j in range(700) 

        ]
print(data[0][0])
targei = []
for i in range(700):
    if baseData[0][30+i] > baseData[0][i-1]:
        targei.append(1) 
    else:
        targei.append(0)



npData = np.array(data, dtype=float)
npTarget = np.array(targei, dtype=float)

print(npData.shape) #shape is 700,30,2 meaning 700 samples of 30 sets of 2 data 
x_train,x_test,y_train,y_test = train_test_split(npData, npTarget, test_size = 0.2, random_state = 4)
model = Sequential()
model.add(LSTM((16),batch_input_shape=(None,30,2),return_sequences=False))
model.add(Activation('relu'))
model.add(Dense(1))
model.add(Activation('sigmoid'))
model.compile(loss="binary_crossentropy", optimizer='adam', metrics=['accuracy'])

print(model.summary())

print(x_test.shape)
print(y_test.shape)
print(x_train)
history = model.fit(x_train, y_train, epochs=100, validation_data=(x_test,y_test))
print(history)
results = model.predict(x_test)


plt.scatter(range(140), y_test, c = 'r')
plt.scatter(range(140), results, c = 'g')
plt.show()
plt.plot(history.history['loss'])
plt.show()
# result = []
# for i in range(0, 700):
#     packet = []
#     for x in range(0, 30):
#         packet.append(CoinDataPoint("BTC", (myBits[i+x][0]),(myBits[i+x][1]),(myBits[i+x][2])))
#     result.append(CoinPack(packet))

# writeToBin(result[0],"coinPackArray.dat")

# packs = openBin("coinPackArray.dat")
# #array of array of 30 floats 

# Data = [[[packs[i].days] for i in range(700)]]]






