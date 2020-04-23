import requests, json
from redHerrings.stock import Stock
from config import *
import csv
from pprint import pprint
import pickle
from coin import *
import numpy as np
from keras.models import Sequential
from keras.layers import Dense
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

def sigmize(num, big):
    num = num/big
    1/(1+math.exp(-num))
    return num
end = openBin("bitcoin.dat")
myBits = []
for day in end["Time Series (Digital Currency Daily)"]:
    myBits.append(float(end["Time Series (Digital Currency Daily)"][day]['4b. close (USD)']))

big = float(max(myBits[:730]))
print(big)
data = [[[sigmize(myBits[i+j], big)] for i in range(30)] for j in range(700)]
targei = [sigmize(myBits[30 + i], big) for i in range(700)]



npData = np.array(data, dtype=float)
npTarget = np.array(targei, dtype=float)

print(npData.shape) #shape is 700,30,1 meaning 700 samples of 30 sets of 1 datum 
x_train,x_test,y_train,y_test = train_test_split(npData, npTarget, test_size = 0.2, random_state = 4)
model = Sequential()
model.add(LSTM((1),batch_input_shape=(None,30,1),return_sequences=False))
model.compile(loss="mean_absolute_error", optimizer='adam', metrics=['accuracy'])

print(model.summary())

print(x_test.shape)
print(y_test.shape)
history = model.fit(x_train, y_train, epochs=200, validation_data=(x_test,y_test))
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






