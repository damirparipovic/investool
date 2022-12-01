from stock import Stock

class Portfolio:
    def __init__(self):
        self.stocks = list()
        self.totalValue = 0

    def getStockTickers(self) -> list[str]:
        return [x.getTicker() for x in self.stocks]

    def addStock(self, stock: Stock) -> None:
        if stock.getTicker() not in self.getStockTickers():
            stock.updatePrice()
            self.stocks.append(stock)
        else:
            print("Stock already exists in portfolio.")

    def getAllStocks(self) -> list[Stock]:
        return self.stocks

    def getStock(self, ticker: str) -> Stock:
        for i, stock in enumerate(self.stocks):
            if ticker == stock.getTicker():
                return self.stocks[i]
        raise ValueError("The provided ticker does not exist in the portfolio.")

    def updateAllPrices(self) -> None:
        for stock in self.stocks:
            stock.updatePrice()

    def updateTotalValue(self) -> None:
        for stock in self.stocks:
            self.totalValue = self.totalValue + stock.getValue()

    def printStocks(self) -> None:
        for stock in self.stocks:
            print(stock)
