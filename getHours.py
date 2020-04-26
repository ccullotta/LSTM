import requests, json
from tools.bin import *
from config import *
import csv
import numpy as np
import math

def getDailyStockHistory(symbol, qty):
    data = {
        "function":"TIME_SERIES_DAILY_ADJUSTED",
        "symbol":symbol,
        "outputsize":qty,
        "apikey": STOCK_DATA_KEY
    }
    r = requests.get(STOCK_DATA_URL, params=data)
    # print(r)
    return json.loads(r.content)

def writeToCSV(input, fileName):
    with open(fileName,'w',newline='') as result_file:
        wr = csv.writer(result_file, dialect='excel')
        wr.writerows(input)
        return

def readCSVFile(fileName):
    stocks = []
    with open(fileName, newline="") as csvfile:
        reader = csv.reader(csvfile)
        for row in reader:
            stocks.append(row)
    return stocks  


lis = [[1,2],[3,4]]
print(lis)

del(lis[0])
print(lis)
end = openBin('btcClosingData')


print(len(end))
i = 0
length = len(end)
while i < length:
    for j in range(60):
        if math.isnan(end[i][j]):
            del end[i]
            length -= 1
            print(str(i)+" "+str(j))
            i = i - 2
            break
    i += 1
arr = np.array(end)
suma = np.sum(arr)
print(np.isnan(suma))
print(len(end))
print(len(end))
writeToBin(end, 'btcClosingData2')
