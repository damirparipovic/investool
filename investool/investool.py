import ui
from manager import PortfolioManager
import os

def setup() -> bool:
    # add portfolios directory if its missing
    try:
        if not PortfolioManager.checkDirectoryExists():
            os.mkdir(PortfolioManager.DEFAULT_DIRECTORY)
    except OSError:
        print("There was an error creating or checking for directory. Exiting.")
        exit(1)
    return True
    

def main() -> None:
    setup()
    investoolUI = ui.UI()
    investoolUI.run()
    return

if __name__ == "__main__":
    main()
