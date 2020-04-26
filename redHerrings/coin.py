class CoinDataPoint:
    def __init__(self, name, date, volume, closingPrice):
        self.name = name
        self.date = date
        self.volume = float(volume)
        self.closingPrice = float(closingPrice)

class CoinPack:
    def __init__(self, list):
        self.CoinName = list[0].name
        self.days = list
        self.startDate = list[0].date
        self.size = len(list);
