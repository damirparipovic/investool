import yfinance as yf

FORM="""
-------------------
Stock ticker: {}
 - price: {}
 - units: {}
 - percent: {}
 - value: {}
-------------------
"""

class Stock:
    def __init__(self, ticker='', price=0.0, units=0, percent=0.0) -> None:
        self.ticker = ticker
        self.price = price
        self.units = units
        self.percent = percent
        self.stockValue = price * units

    def __str__(self) -> str:
        return FORM.format(self.ticker, self.price, self.units, self.percent, self.stockValue)

    def __repr__(self) -> str:
        return f"Stock(ticker={self.ticker}, \
                price={self.price}, \
                percent={self.percent}, \
                units: {self.units})"

    def getTicker(self) -> str:
        return self.ticker

    def getPrice(self) -> float | None:
        return self.price

    def setPercent(self, percent: float) -> None:
        self.percent = percent

    def getPercent(self) -> float:
        return self.percent

    def getUnits(self) -> int:
        return self.units

    def setUnits(self, units: int) -> None:
        self.units = units

    def setTicker(self, newTicker: str) -> None:
        self.ticker = newTicker

    def updatePrice(self) -> float | None:
        try:
            stock_info = yf.Ticker(self.getTicker()).info
            self.price = stock_info.get('regularMarketPrice')
            if self.price == None:
                raise ValueError
        except ValueError:
            print(f"Invalid ticker code {self.ticker}.")
            return None
        else:
            self.updateValue()
            return self.price

    def updateValue(self) -> None:
        self.stockValue = self.price * self.units

    def getlValue(self) -> float:
        return self.stockValue
