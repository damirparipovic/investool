import requests

from stock import Stock
from constants import API_URL
from datetime import date

class Portfolio:
    def __init__(self, portfolioName='', stocks=list(), totalValue=0.0, portfolioCurrency='CAD'):
        self._portfolioName: str = portfolioName
        self._stocks: list[Stock] = stocks
        self._totalValue: float = totalValue
        self._portfolioCurrency: str = portfolioCurrency
        self._currencyExchangeCache: dict = {}

    def __str__(self) -> str:
        form = "Portfolio: {}\n  - stocks: {}\n  - totalValue: {}\n  - currency: {}"
        return form.format(self._portfolioName, self._stocks, self._totalValue, self._portfolioCurrency)

    def __repr__(self) -> str:
        return f"Portfolio('{self.portfolioName}', {self._stocks}, {self._totalValue}, {self._portfolioCurrency})"

    def __eq__(self, other) -> bool:
        if not isinstance(other, Portfolio):
            return NotImplemented
        if (self._portfolioName == other._portfolioName and
            self._stocks == other._stocks and
            self._totalValue == other._totalValue and 
            self._portfolioCurrency == other._portfolioCurrency):
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

    @property
    def portfolioCurrency(self) -> str:
        return self._portfolioCurrency

    @portfolioCurrency.setter
    def portfolioCurrency(self, currency: str) -> None:
        if not isinstance(currency, str):
            raise TypeError("currency must be a str.")
        self._portfolioCurrency = currency

    def getTotalPercent(self) -> float:
        return sum(stock.percent for stock in self.stocks)

    def getStockTickers(self) -> list[str]:
        return [stock.ticker for stock in self._stocks]

    def addStock(self, stock: Stock) -> None:
        if stock.ticker not in self.getStockTickers():
            stock.updatePrice()
            stock.updateValue()
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
            if stock.currency != self.portfolioCurrency:
                exchangeRate = self.getCurrencyExchange(stock.currency, self.portfolioCurrency)
                stock.stockValue *= exchangeRate

    def currencyUpToDate(self, currency: str) -> bool:
        today = date.today().strftime("%Y-%m-%d")
        return self._currencyExchangeCache[currency.lower()]['date'] == today

    def getCurrencyExchange(self, currency1: str, currency2: str) -> float:
        currency1 = currency1.lower()
        currency2 = currency2.lower()
        # if cache isn't up to date, update it accordingly
        if currency1 not in self._currencyExchangeCache or not self.currencyUpToDate(currency1):
            inp2 = "currencies/" + currency1 + ".json"
            response = requests.get(API_URL.format(inp2))
            if response.status_code == 200: 
                data = response.json()
                self._currencyExchangeCache[currency1] = data
            else:
                raise requests.RequestException("There was an error with getting the request.")

        # return the correct currency exchange rate from currency1 to currency2
        # ex: USD -> CAD being 1.34 means for 1 USD you get 1.34 CAD
        exchangeRate = self._currencyExchangeCache[currency1][currency1][currency2]

        return exchangeRate

    def updateTotalPortfolioValue(self, updatePrices:bool=True, updateValues:bool=True) -> None:
        if updatePrices:
            self.updateAllStockPrices()
        if updateValues:
            self.updateAllStockValues()
        self._totalValue = sum(s.stockValue for s in self._stocks)

    def updatePortfolio(self) -> None:
        self.updateTotalPortfolioValue()
