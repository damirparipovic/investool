from portfolio import Portfolio
from stock import Stock
from pathlib import Path
import pickle

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

    def renamePortfolio(self, newName: str) -> None:
        self.currentPortfolio.portfolioName = newName

    def getFilePath(self, fileName: str) -> Path:
        return Path(self.DEFAULTPATH, fileName)

    def loadPortfolio(self, fileName: str) -> None:
        currFilePath = self.getFilePath(fileName)
        if not currFilePath.exists():
            raise FileNotFoundError("file does not exist.")
        with open(currFilePath, 'rb') as f:
            self.currentPortfolio = pickle.load(f)

    def checkFileExists(self, fileName: str) -> bool:
        currFilePath = self.getFilePath(fileName)
        return currFilePath.exists()

    def savePortfolio(self, fileName: str, confirmOverwrite: bool=False) -> None:
        currFilePath = self.getFilePath(fileName)
        if currFilePath.exists() and not confirmOverwrite:
            # so we want to save and not overwrite. So get the portfolioName
            # and append date to save file
            currFilePath.touch(exist_ok=False) # raises FileExistsError
            # need to create new file (ask for new filename or append date)
        else:
            currFilePath.touch()
        with open(currFilePath, 'wb') as f:
            pickle.dump(self.currentPortfolio, f, pickle.HIGHEST_PROTOCOL)

    # this should be in UI
    def confirmWrite(self) -> bool:
        confirmation = input("Are you sure you want to overwrite?[y/n]: ")
        if confirmation in self.VALIDCONFIRMATIONS:
            return True
        else:
            return False

    # rebalance portfolio
    def rebalanceSellBuy(self):
        pass

    def rebalanceOnlyBuy(self):
        pass
