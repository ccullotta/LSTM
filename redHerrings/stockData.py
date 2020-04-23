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