from pathlib import Path
import manager
from portfolio import Portfolio
from stock import Stock
import os

class UI:
    def __init__(self):
        self.manager = manager.PortfolioManager()

    def loadPortfolio(self, filename) -> bool:
        try:
            self.manager.loadPortfolio(filename)
        except FileNotFoundError:
            print("File was not loaded properly.")
            return False
        return True

    def choosePortfolio(self) -> None:
        # list all portfolios in portfolios directory
        # if the dir doesn't exist create it (Shouldn't not exist)
        # if it is empty, only option 0 allowed which is name and
        # create new portfolio
        listOfOptions = self.listPortfolios()
        if len(listOfOptions) == 0:
            # create new portfolio
            print("There seem to be 0 portfolios in the directory.")
            print("Please create a portfolio.")
            self.createNewPortfolio()
        else:
            # ask user which portfolio they want to use and load it
            while True:
                try:
                    choice = int(input("Please choose a portfolio (the number):"))
                except ValueError:
                    print("Provided number is not a value. Please try again.")
                    continue
                if choice >= len(listOfOptions) or choice < 0:
                    print("Please provide a valid selection.")
                    continue
                # make sure choice exists and load it 
                res = self.loadPortfolio(listOfOptions[choice])
                if res:
                    break
                else:
                    print("There was an error loading the portfolio. Please try again.")

    def listPortfolios(self) -> list[str]:
        # shows list of portfolios and returns the list
        listOfPortfolios = os.listdir(self.manager.DEFAULTPATH)
        print("List of portfolios available:")
        if len(listOfPortfolios) == 0:
            print(" empty")
        else:
            for i, p in enumerate(listOfPortfolios):
                print(f" {i} - {p}")
        return listOfPortfolios

    def createNewPortfolio(self) -> None:
        # should ask for a new name for portfolio
        while True:
            newPortfolioName = input("Provide a portfolio name: ")
            if self.manager.checkFileExists(newPortfolioName):
                print("A portfolio with this name already exists. Please try again.")
                continue
            else:
                self.manager.renamePortfolio(newPortfolioName)
                break

    def UIprintCurrentPortfolioInformation(self) -> None:
        stockList = self.manager.currentPortfolio.stocks
        # if no portfolio chosen and currently have new portfolio
        if self.manager.currentPortfolio == Portfolio():
            return
        print(f" -- Portfolio: {self.manager.currentPortfolio.portfolioName} -- ")
        print("Stocks:")
        for stock in stockList:
            print(stock)
        print(f"Total portfolio value: {self.manager.currentPortfolio.totalValue:.2f}")

    def getConfirmation(self, inputMessage) -> bool:
        while True:
            try:
                inp = str(input(inputMessage)).lower()
            except (TypeError, ValueError):
                print("The input provided is invalid. Please try again.")
                continue
            else:
                if inp == 'y' or inp == 'yes':
                    return True
                else:
                    return False

    def getValidType(self, inputMessage: str, wantedType: type, lowerLimit: float=float('-inf'), upperLimit: float=float('inf')) -> float:
        while True:
            try:
                inputValue = input(inputMessage)
                if inputValue == '' or inputValue == '\n':
                    print("You did not provide a value. Please try again.")
                    continue
                else:
                    inputValue = wantedType(inputValue)
            except (ValueError, TypeError):
                print(f"The provided value is not input. Provide a valid value of type {wantedType.__name__}.")
                continue
            else:
                isNumberType = type(inputValue) == float or type(inputValue) == int
            if isNumberType and (inputValue < lowerLimit or inputValue > upperLimit):
                print(f"Provided value is not within limits of {lowerLimit} to {upperLimit} (both inclusive).")
                continue
            break
        return inputValue

    def printHowUnitsHaveToChange(self, stockUnitMap: dict[Stock, int]) -> None:
        print()
        print("Showing how many units of each stock need to be sold or bought:")
        # sell stocks
        for stock, units in stockUnitMap.items():
            if units < 0:
                print(f"  - {stock.ticker} sell {units} units.")
        # buy stocks
        for stock, units in stockUnitMap.items():
            if units >= 0:
                print(f"  - {stock.ticker} buy {units} units.")

    def UIrebalancePortfolioBuySell(self) -> None:
        print(" -- Rebalancing Portfolio (sell then buy) -- ")
        print()
        inputMessage = "Provide how much liquid cash is available for rebalancing: "
        liquidCash = self.getValidType(inputMessage, float, lowerLimit=0)

        while not self.manager.portfolioPercentValid():
            print("The portfolio target allocation percentages are not valid.")
            self._resetTargetPercentAllocation()

        stocksUnitDifferences = self.manager.calculateRebalanceSellBuy(liquidCash)
        self.printHowUnitsHaveToChange(stocksUnitDifferences)

        if self.getConfirmation("Would you like to continue with this rebalancing? (y/N): "):
            self.manager.rebalanceSellBuy(liquidCash)
            remainingCash = self.manager.cashRemaining(stocksUnitDifferences, liquidCash)
            print(f"Cash Remaining is after rebalancing is: {remainingCash:.2f}")
        else:
            print("Did not rebalance.")
        print("Returning to previous menu.")
        
    def UIrebalancePortfolioBuyOnly(self) -> None:
        print(" -- Rebalancing Portfolio (buy only) -- ")
        print()
        inputMessage = "Provide how much liquid cash is available for rebalancing: "
        liquidCash = self.getValidType(inputMessage, float, lowerLimit=0)

        while not self.manager.portfolioPercentValid():
            print("The portfolio target allocation percentages are not valid.")
            self._resetTargetPercentAllocation()

        stocksUnitDifferences = self.manager.calculateRebalanceBuyOnly(liquidCash)
        self.printHowUnitsHaveToChange(stocksUnitDifferences)

        if self.getConfirmation("Would you like to continue with this rebalancing? (y/N): "):
            self.manager.rebalanceOnlyBuy(liquidCash)
            remainingCash = self.manager.cashRemaining(stocksUnitDifferences, liquidCash)
            print(f"Cash Remaining is after rebalancing is: {remainingCash:.2f}")
        else:
            print("Did not rebalance.")
        print("Returning to previous menu.")

    def getValidTicker(self, inputMessage) -> str:
        while True:
            validStr = self.getValidType(inputMessage, str)
            if Stock.validTicker(validStr):
                return validStr
            else:
                print("The provided ticker format is not valid.")
                continue

    def getStockThatExists(self, currTicker: str) -> Stock:
        while True:
            try:
                stock = self.manager.getStock(currTicker)
            except ValueError:
                print(f"The ticker provided ({currTicker}) does not exist in the portfolio.")
                print("Here are the stocks currently in the portfolio.")
                allTickers = self.manager.currentPortfolio.getStockTickers()
                for ticker in allTickers:
                    print(f"{ticker} ", end='')
                currTicker = self.getValidTicker("Please choose a ticker from the list above: ")
                continue
            else:
                return stock

    def UIaddStock(self) -> None:
        print("  -- Add Stock -- ")
        # get ticker
        while True:
            ticker = self.getValidTicker("Please provide the ticker for the stock you would like to add: ")
            if ticker in self.manager.currentPortfolio.getStockTickers():
                print("The provided ticker already exists in the portfolio.")
                if self.getConfirmation("Would you like to add a different stock? (y/N) (N returns to previous menu.): "):
                    continue
                else:
                    print("Did not add the stock, returning to previous menu.")
                    return
            break
        # get units
        units = self.getValidType("Please provide how many units of the stock you own: ", int, lowerLimit=0)
        # get target allocation percent
        percent = self.getValidType("Please provide the target percent allocation for this stock (0 to 1): ", float, lowerLimit=0, upperLimit=1)

        if self.getConfirmation(f"Would you like to add this stock ({ticker}) (y/N)? "):
            print(f"Stock {ticker} successfully added!")
            self.manager.addStockToPortfolio(ticker, units, percent)
        else:
            print("Did not add the stock, returning to previous menu.")

    def _resetTargetPercentAllocation(self) -> None:
        while not self.manager.portfolioPercentValid():
            print("Please provide new target percentages for each stock.")
            for stock in self.manager.currentPortfolio.stocks:
                newTargetPercent = self.getValidType(f"Please provide a new target allocation percent for {stock.ticker} (0 to 1): ", float)
                stock.percent = newTargetPercent
            print(f"New total percent is {round(self.manager.currentPortfolio.getTotalPercent(), 2)}")

    def UIremoveStock(self) -> None:
        print(" -- Remove Stock -- ")
        # get ticker
        ticker = self.getValidTicker("Please provide a ticker of a stock to remove from portoflio: ")
        if self.getConfirmation(f"Would you like to remove this stock ({ticker}) (y/N)?:"):
            print(f"Removing stock {ticker}")
            try:
                self.manager.removeStockFromPortfolio(ticker)
            except ValueError as e:
                print(e)
                print("Did not remove stock, returning to previous menu.")
        else:
            print("Did not remove stock, returning to previous menu.")

    def UIchangeTargetAllocations(self) -> None:
        print(" -- Changing stock target allocations percentages -- ")
        self._resetTargetPercentAllocation()

    def UIbuyStock(self) -> None:
        print(" -- Buy stock -- ")
        ticker = self.getValidTicker("Please provide the ticker for the stock you would like to buy: ")
        stock = self.manager.getStock(ticker)

        newUnits = self.getValidType("How many new units are you purchasing?: ", int)
        stock.units += newUnits
        print(f"New units added to stock {ticker}.")

    def UIsellStock(self) -> None:
        print(" -- Sell Stock -- ")
        ticker  = self.getValidTicker("Please provide the ticker for the stock you would like to sell: ")
        stock = self.manager.getStock(ticker)

        unitsToSell = self.getValidType("How many units would you like to sell?: ", int)
        if unitsToSell > stock.units:
            print("The number of units you would like to sell are more than what you have currently.")
            print("This will cause the stock to be removed from the portfolio.")
            if self.getConfirmation(f"Would you like to remove the stock {ticker}"):
                self.manager.removeStockFromPortfolio(ticker)
            else:
                print("No changes made. Returning to previous menu.")
        else:
            stock.units -= unitsToSell
            print(f"Removed {unitsToSell} from {stock.ticker}. Have {stock.units} units remaining.")

    def UIsaveAllChanges(self) -> None:
        if self.getConfirmation("Would you like to save all changes? (y/N): "):
            print("Not overwritting the file will cause a new one to be created using the current date.")
            overwrite = self.getConfirmation("Would you like to overwrite the current file? (y/N): ")
            self.manager.savePortfolio(Path(__file__).name, overwrite)
        self.clearScreen()

    def clearScreen(self) -> None:
        command = 'cls' if os.name == 'nt' else 'clear'
        os.system(command)

    def startupMenu(self) -> int:
        # choose option and setup the self.manager accordingly
        validChoices = [1,2,3,4]
        print("Select an option below:")
        print(" - 1) list all portfolios")
        print(" - 2) load existing portfolio")
        print(" - 3) create new portfolio")
        print(" - 4) exit application")

        while True:
            try:
                choice = int(input("provide your choice (1, 2, 3 or 4): "))
            except (TypeError, ValueError):
                print("Input is not a number. Please try again.")
                continue
            if choice not in validChoices:
                print("The provided choice is invalid (not 1, 2, 3 or 4). Please try again.")
                continue
            else:
                break
        return choice

    def mainMenu(self) -> int:
        print("---- Portfolio Management  ----")
        print("Please choose an option below:")
        print(" 1 - portfolio information")
        print(" 2 - rebalance portfolio (sell/buy)")
        print(" 3 - rebalance portfolio (buy only)")
        print(" 4 - add stock")
        print(" 5 - remove stock")
        print(" 6 - change target allocations")
        print(" 7 - buy stock")
        print(" 8 - sell stock")
        print(" 9 - go back (save optional)")
        print(" 10 - Exit")

        getValidChoice = self.getValidType("Provide your choice: ", int, lowerLimit=1, upperLimit=10)

        return getValidChoice

    def introPrompt(self) -> None:
        print("##########################")
        print("## Welcome to investool ##")
        print("##########################")

    def run(self) -> None:
        self.introPrompt()
        mainLoop = True
        # Need to decide what to do on startup. After choice made go to main section
        while mainLoop:
            while True:

                startupChoice = self.startupMenu()
                match startupChoice:
                    case 1:
                        self.listPortfolios()
                    case 2:
                        self.choosePortfolio()
                        break
                    case 3:
                        self.createNewPortfolio()
                        break
                    case 4:
                        print("Exiting application!")
                        exit(0)
                    case _:
                        exit(1) #should never execute
                input("Press any key to continue.")
                self.clearScreen()

            # main section where changes are made to portfolio.
            self.clearScreen()
            while True:
                # main loop. Show main menu and perform action based on choice
                self.manager.currentPortfolio.updateTotalPortfolioValue()
                mainChoice = self.mainMenu()

                self.clearScreen()
                match mainChoice:
                    case 1:
                        self.UIprintCurrentPortfolioInformation()
                    case 2:
                        self.UIrebalancePortfolioBuySell()
                    case 3:
                        self.UIrebalancePortfolioBuyOnly()
                    case 4:
                        self.UIaddStock()
                    case 5:
                        self.UIremoveStock()
                    case 6:
                        self.UIchangeTargetAllocations()
                    case 7:
                        self.UIbuyStock()
                    case 8:
                        self.UIsellStock()
                    case 9:
                        print("Exiting to previous menu.")
                        self.UIsaveAllChanges()
                        break
                    case 10:
                        print("Exiting Application (no saves)")
                        exit(0)
                    case _:
                        exit(1)
                input("Press any key to continue.")
                self.clearScreen()
        return
