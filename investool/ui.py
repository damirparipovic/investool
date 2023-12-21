import manager
from portfolio import Portfolio
from stock import Stock
import os

class UI:
    def __init__(self):
        self.manager = manager.PortfolioManager()

    def introPrompt(self) -> None:
        print("##########################")
        print("## Welcome to investool ##")
        print("##########################")

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
        newPortfolioName = input("Provide a portfolio name: ")
        while True:
            if self.manager.checkFileExists(newPortfolioName):
                print("A portfolio with this name already exists. Please try again.")
                continue
            else:
                self.manager.renamePortfolio(newPortfolioName)

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
        print(" 6 - buy stock")
        print(" 7 - sell stock")
        print(" 8 - go back to startup menu")
        print(" 9 - Exit")

        while True:
            try: 
                choice = int(input("Provide your choice:"))
            except (TypeError, ValueError):
                print("Input is not a valid number. Please Try again.")
                continue
            if choice < 1 or choice > 9:
                print("The provided choice is invalid. Not within option range. Please Try Again.")
                continue
            else:
                break
        return choice

    def printCurrentPortfolioInformation(self) -> None:
        stockList = self.manager.currentPortfolio.stocks
        # if no portfolio chosen and currently have new portfolio
        if self.manager.currentPortfolio == Portfolio():
            return
        print(f" -- Portfolio: {self.manager.currentPortfolio.portfolioName} -- ")
        print("Stocks:")
        for stock in stockList:
            print(stock)
        print(f"Total portfolio value: {self.manager.currentPortfolio.totalValue}")

    def getConfirmation(self) -> bool:
        while True:
            try:
                inp = str(input("Would you like to continue with this rebalancing? (y/n): ")).lower()
            except (TypeError, ValueError):
                print("The input provided is invalid. Please try again.")
                continue
            else:
                if inp == 'y' or inp == 'yes':
                    return True
                else:
                    return False

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
        print(" -- Rebalancing Portfolio -- ")
        print()
        while True:
            try:
                liquidCash = input("Provide how much liquid cash is available for rebalancing: ")
                if liquidCash == '' or liquidCash == '\n':
                    liquidCash = 0
                    break
                else:
                    liquidCash = int(liquidCash)
            except (ValueError, TypeError):
                print("The provided value is not valid.")
                continue
            if liquidCash < 0:
                print("Cannot have negative values of liquidCash.")
            else:
                break

        stocksUnitDifferences = self.manager.calculateRebalanceSellBuy(liquidCash)
        print(stocksUnitDifferences)
        self.printHowUnitsHaveToChange(stocksUnitDifferences)

        if self.getConfirmation():
            self.manager.rebalanceSellBuy(liquidCash)
            remainingCash = self.manager.cashRemaining(stocksUnitDifferences, liquidCash)
            print(f"Cash Remaining is after rebalancing is: {remainingCash}")
        else:
            print("Did not rebalance.")
        print("Returning to previous menu.")
        
    def UIrebalancePortfolioBuyOnly(self) -> None:
        pass

    def UIaddStock(self) -> None:
        pass

    def UIremoveStock(self) -> None:
        pass

    def UIbuyStock(self) -> None:
        pass

    def UIsellStock(self) -> None:
        pass

    def clearScreen(self) -> None:
        command = 'cls' if os.name == 'nt' else 'clear'
        os.system(command)

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
                        self.printCurrentPortfolioInformation()
                    case 2:
                        self.UIrebalancePortfolioBuySell()
                    case 3:
                        self.UIrebalancePortfolioBuyOnly()
                    case 4:
                        self.UIaddStock()
                    case 5:
                        self.UIremoveStock()
                    case 6:
                        self.UIbuyStock()
                    case 7:
                        self.UIsellStock()
                    case 8:
                        break # break out and go back to startupMenu
                    case 9:
                        print("Exiting Application")
                        exit(0)
                    case _:
                        exit(1)
                input("Press any key to continue.")
                self.clearScreen()
        return
