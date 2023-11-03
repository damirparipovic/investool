import manager
import portfolio
import os
from pathlib import Path

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
                try:
                    res = self.loadPortfolio(listOfOptions[choice])
                except FileNotFoundError:
                    print("The file does not exist.") #should happen
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

    def startupMenu(self) -> None:
        # choose option and setup the self.manager accordingly
        validChoices = [1,2,3]
        print("Would you like to laod a saved portfolio or create a new portfolio?")
        print(" - 1) load existing portfolio")
        print(" - 2) create new portfolio")
        print(" - 3) exit application")
        while True:
            try:
                choice = int(input("provide your choice (1, 2, or 3): "))
            except TypeError:
                print("Input is not a number. Please try again.")
                continue
            if choice not in validChoices:
                print("The provided choice is invalid (not 1, 2 or 3). Please try again.")
                continue
            else:
                break
        
        match choice:
            case 1:
                self.choosePortfolio()
            case 2:
                self.createNewPortfolio()
            case 3:
                exit(0)
            case _:
                exit(1) #should never execute

    def mainMenu(self) -> int:
        print("---- Main Menu ----")
        print("Please choose an option below:")
        print(" 0 - info")
        print(" 1 - rebalance (only buy)")
        print(" 2 - add stock")
        print(" 3 - remove stock")
        print(" 4 - buy stock")
        print(" 5 - sell stock")
        pass
    
    def clearScreen(self) -> None:
        command = 'cls' if os.name == 'nt' else 'clear'
        os.system(command)

    def printPortfolio(self) -> None:
        stockList = self.manager.currentPortfolio.stocks
        print(f"Portfolio: {self.manager.currentPortfolio.portfolioName}")
        print("Stocks:")
        for stock in stockList:
            print(stock)
        print(f"Total portfolio value: {self.manager.currentPortfolio.totalValue}")

    def run(self):
        self.introPrompt()
        self.startupMenu()
        self.printPortfolio()
        input("Press any key to continue.")
        self.clearScreen()
        while True:
            # main loop. Show main menu and perform action based on choice
            break

        return
