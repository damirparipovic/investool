from .portfolio import Portfolio
from .stock import Stock
from pathlib import Path
import json

class PortfolioManager():

    DEFAULTPATH = Path("..", "portfolios")

    def __init__(self, portfolio=Portfolio()):
        self._currentPortfolio = portfolio

    @property
    def currentPortfolio(self) -> Portfolio:
        return self._currentPortfolio
    
    @currentPortfolio.setter
    def currentPortfolio(self, newPortfolio:Portfolio) -> None:
        self._currentPortfolio = newPortfolio

    def createStock(self, ticker: str, units: int, percent: float) -> Stock:
        newStock = Stock(ticker, 0, units, percent, 0);
        newStock.updatePrice()
        newStock.updateValue()
        return newStock

    def addStockToPortfolio(self, ticker: str, units: int, percent: float) -> None:
        newStock = self.createStock(ticker, units, percent)
        self.currentPortfolio.addStock(newStock)

    # load a portfolio
    def loadPortfolio(self, portfolioName: str) -> None:
        currFilePath = Path(self.DEFAULTPATH, portfolioName)
        if not currFilePath.exists():
            raise FileNotFoundError("file does not exist.")
        self.currentPortfolio = json.loads(currFilePath.read_text())

    # save a portfolio
    def savePortfolio(self, portfolioName: str) -> None:
        currFilePath = Path(self.DEFAULTPATH, portfolioName)
        if currFilePath.exists() and self.confirmWrite():
            print("Portfolio not saved (overwritten).")
            return
        else:
            currFilePath.touch(exist_ok=False)
        currFilePath.write_text(json.dumps(self.currentPortfolio))

    # this should be in UI
    def confirmWrite(self) -> bool:
        confirmation = input("Are you sure you want to overwrite?[y/n]: ")
        if confirmation in self.VALIDCONFIRMATIONS:
            return True
        else:
            return False


    # check for dir and files
    # might not need
    def fileExists(self, portfolioName: str) -> bool:
        pass

    # rebalance portfolio
    def rebalanceSellBuy(self):
        pass

    def rebalanceOnlyBuy(self):
        pass
