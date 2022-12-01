from portfolio import Portfolio
from stock import Stock
from pathlib import Path
import json

class PortfolioManager():

    DEFAULTPATH = Path("..", "portfolios")
    VALIDCONFIRMATIONS = {"yes", "y"}

    def __init__(self):
        self.currentPortfolio = Portfolio()

    def createStock(self, ticker: str, units: int, percent: float,) -> Stock:
        newStock = Stock(ticker, 0, units, percent);
        newStock.updatePrice()
        newStock.updateValue()
        return newStock

    # load a portfolio
    def loadPortfolio(self, portfolioName: str) -> None:
        currFilePath = Path(self.DEFAULTPATH, portfolioName)
        if not currFilePath.exists():
            print("given portfolio doesn't exist. Nothing loaded")
            return
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

    def confirmWrite(self) -> bool:
        confirmation = input("Are you sure you want to overwrite?[y/n]: ")
        if confirmation in self.VALIDCONFIRMATIONS:
            return True
        else:
            return False


    # check for dir and files

    # rebalance portfolio
