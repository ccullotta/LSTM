import requests, json
from stock import Stock
from config import *
import csv
from pprint import pprint
import pickle
from coin import *


def writeToCSV(input, fileName):
    with open(fileName,'w',newline='') as result_file:
        wr = csv.writer(result_file, dialect='excel')
        wr.writerows(input)
        return
def getAccount():
    r = requests.get(ACCOUNT_URL, headers=ALP_HEADERS)
    return json.loads(r.content)

def makeOrder(symbol, qty, side, type, time):
    data = {
        "symbol": symbol,
        "qty": qty,
        "side": side,
        "type": type,
        "time_in_force": time
    }
    r = requests.post(ORDERS_URL, json=data, headers=ALP_HEADERS)
    return json.loads(r.content)

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

def getDividend(symbol):
    url = STOCK_DIVIDEND_URL+symbol+'/dividends/1y'+"?token="+STOCK_DIVIDEND_KEY
    r = requests.get(url)
    return json.loads(r.content)

def readCSVFile(fileName):
    stocks = []
    with open(fileName, newline="") as csvfile:
        reader = csv.reader(csvfile)
        for row in reader:
            stocks.append(row)
    return stocks        

def removeDividends(list):
    for stock in list:
        stock_hist = getDividend(stock[0])
        if not stock_hist:
            print(stock[0] + ": yeilds no dividend")
        else:
            print("removing " + stock[0] + " as it pays dividend here! VVV")
            print(stock_hist[0]['amount'])
            list.remove(stock)
    return list

def createStockData(list):
    result = []
    for name in list:
        try:
            url = STOCK_DIVIDEND_URL+name[0]+'/quote?token='+STOCK_DIVIDEND_KEY
            r = requests.get(url)
            print(r)
            data = json.loads(r.content)
            print(data['symbol']+'\n')
            stock = Stock(data['symbol'],data['peRatio'],data['marketCap'],data['week52Low'],data['week52High'])
            result.append(stock)
        except:
            print("error!")
    return result

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

# s = getQuote("BTC")
def openBin(fileName):
    with open(fileName, 'rb') as Y:
        return pickle.load(Y)
# print(json.dumps(end, indent=2))
end = openBin("bitcoin.dat")
myBits = []
for day in end["Time Series (Digital Currency Daily)"]:
    myBits.append([day, end["Time Series (Digital Currency Daily)"][day]['4b. close (USD)'], end["Time Series (Digital Currency Daily)"][day]['5. volume']])

result = []
for i in range(0, 700):
    packet = []
    for x in range(0, 30):
        packet.append(CoinDataPoint("BTC", (myBits[i+x][0]),(myBits[i+x][1]),(myBits[i+x][2])))
    result.append(CoinPack(packet))

writeToBin(result[0],"coinPackArray.dat")


# ret = readCSVFile("stocks_no_dividend.csv")
# result = createStockData(ret)
# with open('test.dat', 'wb') as f:
    # pickle.dump(result, f)



# print(len(end))


# ret = readCSVFile("nasdaq stocks.csv")
# end = removeDividends(ret)
# writeToCSV(end, "stocks_no_dividend.csv")
# print(ret)
# ret = getDailyStockHistory("IBM", '30')
# print(json.dumps(ret, indent=4))
# print(ret["Time Series (Daily)"]["2020-04-17"])





