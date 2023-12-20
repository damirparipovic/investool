from stock import Stock

class Portfolio:
    def __init__(self, portfolioName='', stocks=list(), totalValue=0.0):
        self._portfolioName: str = portfolioName
        self._stocks: list[Stock] = stocks
        self._totalValue: float = totalValue

    def __str__(self) -> str:
        form = "Portfolio: {}\n  - stocks: {}\n  - totalValue: {}"
        return form.format(self._portfolioName, self._stocks, self._totalValue)

    def __repr__(self) -> str:
        return f"Portfolio('{self.portfolioName}', {self._stocks}, {self._totalValue})"

    def __eq__(self, other) -> bool:
        if not isinstance(other, Portfolio):
            return NotImplemented
        if (self._portfolioName == other._portfolioName and
            self._stocks == other._stocks and
            self._totalValue == other._totalValue):
            return True
        else:
            return False

    @property
    def portfolioName(self) -> str:
        return self._portfolioName

    @portfolioName.setter
    def portfolioName(self, portfolioName: str) -> None:
        if not isinstance(portfolioName, str):
            raise TypeError("portfolioName must be a string")
        self._portfolioName = portfolioName

    @property
    def stocks(self) -> list[Stock]:
        return self._stocks

    @stocks.setter
    def stocks(self, stocks: list[Stock]) -> None:
        if not isinstance(stocks, list):
            raise TypeError("stocks must be a list")
        self._stocks = stocks

    @property
    def totalValue(self) -> float:
        return self._totalValue

    @totalValue.setter
    def totalValue(self, totalValue: float) -> None:
        if not isinstance(totalValue, float):
            raise TypeError("totalValue must be a float.")
        if totalValue < 0.0:
            raise ValueError("totalValue cannot be negative. Must be at least 0.")
        self._totalValue = totalValue

    def getStockTickers(self) -> list[str]:
        return [stock.ticker for stock in self._stocks]

    def addStock(self, stock: Stock) -> None:
        if stock.ticker not in self.getStockTickers():
            stock.updatePrice()
            self._stocks.append(stock)

    def removeStock(self, ticker: str) -> None:
        for stock in self._stocks:
            if stock.ticker == ticker:
                self._stocks.remove(stock)
                return
        raise ValueError(f"{ticker} not in portfolio.")

    def updateAllStockPrices(self) -> None:
        for stock in self._stocks:
            stock.updatePrice()

    def updateAllStockValues(self) -> None:
        for stock in self._stocks:
            stock.updateValue()

    def updateTotalPortfolioValue(self, updatePrices:bool=True, updateValues:bool=True) -> None:
        if updatePrices:
            self.updateAllStockPrices()
        if updateValues:
            self.updateAllStockValues()
        self._totalValue = sum(s.stockValue for s in self._stocks)

    def updatePortfolio(self) -> None:
        self.updateTotalPortfolioValue()
