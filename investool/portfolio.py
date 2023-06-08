from stock import Stock

class Portfolio:
    def __init__(self):
        self.stocks = list()
        self.totalValue = 0

    def getStockTickers(self) -> list[str]:
        return [s.ticker for s in self.stocks]

    def addStock(self, stock: Stock) -> None:
        if stock.ticker not in self.getStockTickers():
            stock.updatePrice()
            self.stocks.append(stock)

    def getAllStocks(self) -> list[Stock]:
        return self.stocks

    def getStock(self, ticker: str) -> Stock:
        for i, stock in enumerate(self.stocks):
            if ticker == stock.ticker:
                return self.stocks[i]
        raise KeyError("The provided ticker does not exist in the portfolio.")

    def updateAllPrices(self) -> None:
        for stock in self.stocks:
            stock.updatePrice()

    def updateTotalValue(self) -> None:
            self.totalValue = sum(s.stockValue for s in self.stocks)

    def printStocks(self) -> None:
        for stock in self.stocks:
            print(stock)
