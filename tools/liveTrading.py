
import requests, json
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