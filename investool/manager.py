import datetime
from pathlib import Path
import pickle

from portfolio import Portfolio
from stock import Stock

class PortfolioManager():

    MANAGER_LOCATION = Path(__file__).absolute().parent
    DEFAULTPATH = Path(MANAGER_LOCATION, "..", "portfolios")

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

    def removeStockFromPortfolio(self, ticker: str) -> None:
        if ticker not in self.currentPortfolio.getStockTickers():
            raise ValueError("Stock not in portfolio! Cannot remove stock.")
        stock = self.getStock(ticker)
        self.currentPortfolio.stocks.remove(stock)

    def renamePortfolio(self, newName: str) -> None:
        self.currentPortfolio.portfolioName = newName

    def getFilePath(self, fileName: str) -> Path:
        if not fileName.endswith('.pickle'):
            fileName = fileName + '.pickle'
        return Path(self.DEFAULTPATH, fileName)

    def loadPortfolio(self, fileName: str) -> bool:
        currFilePath = self.getFilePath(fileName)
        if not currFilePath.exists():
            raise FileNotFoundError("file does not exist.")
        try:
            with open(currFilePath, 'rb') as f:
                self.currentPortfolio = pickle.load(f)
        except IOError:
            return False
        return True

    def checkFileExists(self, fileName: str) -> bool:
        currFilePath = self.getFilePath(fileName)
        return currFilePath.exists()

    def savePortfolio(self, fileName: str, overwrite: bool=False) -> bool:
        currFilePath = self.getFilePath(fileName)
        if currFilePath.exists() and not overwrite:
            timeStamp = datetime.datetime.now().strftime("%Y-%m-%d-%H:%M:%S")
            newFileName = f"{fileName}_{timeStamp}"
            currFilePath = self.getFilePath(newFileName)

        try:
            with open(currFilePath, 'wb') as f:
                pickle.dump(self.currentPortfolio, f, pickle.HIGHEST_PROTOCOL)
            return True
        except IOError:
            return False

    def portfolioPercentValid(self) -> bool:
        currentPercentTotal = self.currentPortfolio.getTotalPercent()
        if currentPercentTotal > 1:
            return False
        # if round(currentPercentTotal) != 1:
        #     return False
        return True

    def changePercentage(self, stockTicker: str, percent: float) -> None:
        if percent > 100:
            raise ValueError("Percent for any one stock cannot be > 100.")
        self.currentPortfolio.getStock(stockTicker).percent = percent

    def _calculateAllocationDifference(self, liquidCash: float=0) -> dict[Stock, int]:
        # calculate how many units need to be sold (-ve val) and 
        # purchased (+ve val)
        self.currentPortfolio.updatePortfolio()

        totalValue = self.currentPortfolio.totalValue + liquidCash

        # for each stock find how many units we should have based on target
        # percent of totalValue
        stocksUnitDifference = {}
        for stock in self.currentPortfolio.stocks:
            newUnitCount = round((stock.percent * totalValue) / stock.price)
            stockUnitDiff = newUnitCount - stock.units
            stocksUnitDifference[stock] = stockUnitDiff
        return stocksUnitDifference

    def calculateRebalanceSellBuy(self, liquidCash: float = 0.0) -> dict[Stock, int]:
        '''
        Function will calculate how to rebalance a portfolio by selling and
        then buying stocks. If there is not enough cash there will be some
        cash remaining. If there is liquid Cash available before the rebalance
        then it will be used to allow for complete rebalancing.
        The function takes into consideration the fact that stocks can only
        be sold as in whole units.

        Returns a dictionary of stocks as keys and how many units to sell (-ve)
        and buy (+ve) for each stock
        '''
        stocksUnitDifference = self._calculateAllocationDifference(liquidCash)

        sellList = [stock for stock in stocksUnitDifference.items() if stock[1] < 0]
        sellList.sort(key=lambda x: x[1])
        buyList = [stock for stock in stocksUnitDifference.items() if stock[1] >= 0]
        buyList.sort(key=lambda x: x[1], reverse=True)

        totalCash = liquidCash
        for stock, units in sellList:
            totalCash += (-1 * units) * stock.price
            
        # need a new buyList because values could change, depending on price
        finalBuyList = []
        for stock, units in buyList:
            cost = units * stock.price
            if cost > totalCash:
                units = int(totalCash/stock.price)
            totalCash -= units * stock.price
            finalBuyList.append((stock, units))

        return dict(sellList + finalBuyList)

    def calculateRebalanceBuyOnly(self, liquidCash: float = 0.0) -> dict[Stock, int]:
        stocksUnitDifference = self._calculateAllocationDifference(liquidCash)

        # only purchase stocks that are most skewed away from target percentages
        buyList = [stock for stock in stocksUnitDifference.items() if stock[1] >= 0]
        buyList.sort(key=lambda x: x[1], reverse=True)
        
        modifiedBuyList = []

        for i in range(len(buyList)):
            stock = buyList[i][0]
            units = buyList[i][1]
            cashNeeded = units * stock.price
            
            if cashNeeded > liquidCash:
                units = int(liquidCash/stock.price)
            liquidCash -= units * stock.price
            modifiedBuyList.append((stock, units))

        return dict(modifiedBuyList)

    def cashRemaining(self, buySellMap: dict[Stock, int], liquidCash: float = 0.0) -> float:
        rem = liquidCash
        for stock, units in buySellMap.items():
            rem -= units * stock.price
        return rem

    def rebalanceSellBuy(self, liquidCash: float = 0.0):
        rebalanceMap = self.calculateRebalanceSellBuy(liquidCash)

        for stock, units in rebalanceMap.items():
            if units > 0:
                self.buyStock(stock.ticker, units)
            elif units < 0:
                self.sellStock(stock.ticker, units)

    def rebalanceOnlyBuy(self, liquidCash: float = 0.0):
        rebalanceMap = self.calculateRebalanceSellBuy(liquidCash)

        for stock, units in rebalanceMap.items():
            if units > 0:
                self.buyStock(stock.ticker, units)

    def getStock(self, stockTicker: str) -> Stock:
        for i, stock in enumerate(self.currentPortfolio.stocks):
            if stockTicker == stock.ticker:
                return self.currentPortfolio.stocks[i]
        raise ValueError("The provided ticker does not exist in the portfolio.")

    def buyStock(self, stockTicker: str, quantity: int) -> int:
        # when quantity < 0 we are selling
        if stockTicker not in self.currentPortfolio.getStockTickers(): 
            raise ValueError(f"stock {stockTicker} is not in the portfolio")

        stock = self.getStock(stockTicker)
        stock.units += quantity

    def sellStock(self, stockTicker: str, quantity) -> int:
        if stockTicker not in self.currentPortfolio.getStockTickers(): 
            raise ValueError(f"stock {stockTicker} is not in the portfolio")
        
        stock = self.getStock(stockTicker)
        if quantity > stock.units:
            stock.units = 0
        else:
            stock.units += quantity
