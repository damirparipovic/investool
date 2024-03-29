import yfinance as yf
import re
import requests

FORM="""-------------------
Stock ticker: {}
 - price: {}
 - currecny: {}
 - units: {}
 - percent: {}
 - value: {}
-------------------"""

TICKER_PATTERN = "[a-zA-Z]{1,4}(\.[a-zA-Z]{0,2})?"

class Stock:
    def __init__(self, ticker='', price=0.0, currency='',  units=0, percent=0.0, stockValue=0.0) -> None:
        self._ticker: str = ticker
        self._price: float = price
        self._currency: str = currency
        self._units: int = units
        self._percent: float = percent
        self._stockValue: float = stockValue

    def __str__(self) -> str:
        return FORM.format(self._ticker, self._price, self._currency, self._units, self._percent, self._stockValue)

    def __repr__(self) -> str:
        return f"Stock('{self._ticker}', {self._price}, '{self._currency}', {self._units}, {self._percent}, {self._stockValue})"

    def __eq__(self, other) -> bool:
        if not isinstance(other, Stock):
            return NotImplemented
        if (self._ticker == other._ticker and
            self._price == other._price and
            self._currency == other._currency and
            self._units == other._units and
            self._percent == other._percent and
            self._stockValue == other._stockValue):
            return True
        return False

    def __hash__(self) -> int:
        return hash((self._ticker, self._price, self._currency, self._units, self._percent, self._stockValue))

    @property
    def ticker(self) -> str:
        return self._ticker

    @ticker.setter
    def ticker(self, ticker: str) -> None:
        if not self.validTicker(ticker):
            raise Exception("Ticker format is invalid.")
        self._ticker = ticker

    @property
    def price(self) -> float:
        return self._price

    @price.setter
    def price(self, value: float) -> None:
        if value < 0:
            raise ValueError("Price can't be set to less than 0.")
        self._price = value

    @property
    def currency(self) -> str:
        return self._currency

    @currency.setter
    def currency(self, currency: str) -> None:
        self._currency = currency

    @property
    def units(self) -> int:
        return self._units

    @units.setter
    def units(self, value: int) -> None:
        if value < 0:
            raise ValueError("Cannot have a value of less than 0 for number of units.")
        self._units = value

    @property
    def percent(self) -> float:
        return self._percent

    @percent.setter
    def percent(self, value: float) -> None:
        if value < 0:
            raise ValueError("Percent cannot be less than 0.")
        if value > 1:
            raise ValueError("Percent cannot be greater than 1.")
        self._percent = value

    @property
    def stockValue(self) -> float:
        return self._stockValue

    @stockValue.setter
    def stockValue(self, value: float) -> None:
        if value < 0:
            raise ValueError("Stock can't have a value less than 0.")
        self._stockValue = value

    def getCurrentPrice(self) -> float | None:
        currentPrice = None
        try:
            stockInfo = yf.Ticker(self.ticker).fast_info
            if stockInfo == None:
                return None
            else:
                currentPrice = stockInfo.get("lastPrice")
        except requests.HTTPError:
            raise requests.HTTPError(f"Invalid ticker code {self.ticker} or unable to get request.")
        except KeyError:
            return None
        else:
            stockCurrency = stockInfo.get("currency")
            if stockCurrency:
                self.currency = stockCurrency
            return currentPrice

    def updatePrice(self) -> None:
        currentPrice = self.getCurrentPrice()

        if currentPrice == None:
            return
        else:
            self.price = currentPrice

    def updateValue(self) -> None:
        self.stockValue = self._price * self._units

    @classmethod
    def validTicker(cls, ticker: str) -> bool:
        if len(ticker) < 1:
            return False
        res = re.match(TICKER_PATTERN, ticker)
        if res == None or res.group(0) != ticker:
            return False
        else:
            return True
