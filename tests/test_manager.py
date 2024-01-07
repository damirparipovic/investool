import pytest
from investool.manager import PortfolioManager, Portfolio, Stock
from tests.test_portfolio import standard_portfolio

@pytest.fixture
def standard_manager(standard_portfolio):
    return PortfolioManager(standard_portfolio)

@pytest.fixture(scope="function")
def standard_manager_path(tmp_path, standard_manager):
    test_dir = "temp_portfolios"
 
    d = tmp_path / test_dir
    d.mkdir()

    standard_manager.DEFAULT_PATH = d
    return standard_manager

@pytest.fixture
def standard_manager_fixed_prices(standard_manager, mocker):
    stockPrices = [10, 20, 30]

    for i in range(len(standard_manager.currentPortfolio.stocks)):
        stock = standard_manager.currentPortfolio.stocks[i]
        stock.getCurrentPrice = mocker.MagicMock(return_value=stockPrices[i])

    return standard_manager

@pytest.fixture
def real_stock_portfolio():
    msft = Stock('msft', 0, 5, 0.25, 0)
    aapl = Stock('aapl', 0, 5, 0.25, 0)
    amzn = Stock('amzn', 0, 5, 0.25, 0)
    nvda = Stock('nvda', 0, 5, 0.25, 0)
    stonks = [msft, aapl, amzn, nvda]
    return Portfolio("realStonks", stonks)

@pytest.fixture
def real_stock_manager(real_stock_portfolio):
    return PortfolioManager(real_stock_portfolio)

@pytest.fixture
def real_stock_manager_fixed(real_stock_manager, mocker):
    stockPrices = [10, 20, 30, 40]

    for i in range(len(real_stock_manager.currentPortfolio.stocks)):
        stock = real_stock_manager.currentPortfolio.stocks[i]
        stock.getCurrentPrice = mocker.MagicMock(return_value=stockPrices[i])

    return real_stock_manager

def test_manager_creation(standard_manager, standard_portfolio):
    assert standard_manager.currentPortfolio == standard_portfolio

def test_calculateAllocationDifference(standard_manager_fixed_prices):
    expectedResults = [20, -2, -5]
    expectedResultsDict = {}

    res = standard_manager_fixed_prices._calculateAllocationDifference()

    for i, stock in enumerate(standard_manager_fixed_prices.currentPortfolio.stocks):
        expectedResultsDict[stock] = expectedResults[i]

    for k, v in res.items():
        assert expectedResultsDict[k] == v

def test_calculateRebalanceSellBuy_no_cash_added(standard_manager_fixed_prices):
    expectedResults = [19, -2, -5]
    expectedResultsDict = {}

    diffs = standard_manager_fixed_prices.calculateRebalanceSellBuy()

    for i, stock in enumerate(standard_manager_fixed_prices.currentPortfolio.stocks):
        expectedResultsDict[stock] = expectedResults[i]

    for k, v in diffs.items():
        assert expectedResultsDict[k] == v

def test_calculateRebalanceSellBuy_with_cash(standard_manager_fixed_prices):
    expectedResults = [24, -1, -4]
    expectedResultsDict = {}

    diffs = standard_manager_fixed_prices.calculateRebalanceSellBuy(100)

    for i, stock in enumerate(standard_manager_fixed_prices.currentPortfolio.stocks):
        expectedResultsDict[stock] = expectedResults[i]

    for k, v in diffs.items():
        assert expectedResultsDict[k] == v

def test_cashRemaining(standard_manager_fixed_prices):
    expectedResult = 0
    liquidCash = 100
    diffs = standard_manager_fixed_prices.calculateRebalanceSellBuy(liquidCash)
    print(diffs)
    print(liquidCash)
    print(standard_manager_fixed_prices.cashRemaining(diffs, liquidCash))
    assert expectedResult == standard_manager_fixed_prices.cashRemaining(diffs, liquidCash)

def test_calculateRebalanceBuyOnly(real_stock_manager_fixed):
    liquidCash = 200
    expectedResult = [13, 3, 0, 0]
    expectedResultsDict = {}

    res = real_stock_manager_fixed.calculateRebalanceBuyOnly(liquidCash)

    for i, stock in enumerate(real_stock_manager_fixed.currentPortfolio.stocks):
        expectedResultsDict[stock] = expectedResult[i]

    for k, v in res.items():
        assert expectedResultsDict[k] == v

def test_buyStock(standard_manager_fixed_prices):
    quantity_to_buy = 3

    stock = standard_manager_fixed_prices.getStock("msft")
    current_quantity = stock.units
    standard_manager_fixed_prices.buyStock(stock.ticker, quantity_to_buy)

    assert current_quantity + quantity_to_buy == standard_manager_fixed_prices.getStock("msft").units

def test_sellStock(standard_manager_fixed_prices):
    quantity_to_sell = 4

    stock = standard_manager_fixed_prices.getStock("msft")
    current_quantity = stock.units
    standard_manager_fixed_prices.sellStock(stock.ticker, quantity_to_sell)

    assert current_quantity + quantity_to_sell == standard_manager_fixed_prices.getStock("msft").units

def test_sellStock_sell_too_many(standard_manager_fixed_prices):
    quantity_to_sell = 100

    stock = standard_manager_fixed_prices.getStock("msft")
    current_quantity = stock.units
    standard_manager_fixed_prices.sellStock(stock.ticker, quantity_to_sell)

    assert 0 == standard_manager_fixed_prices.getStock("msft").units

def test_savePortfolio(standard_manager_path):
    test_file = "test_save_portfolio"
    res = standard_manager_path.savePortfolio(test_file)
    assert res == True
    assert standard_manager_path.checkFileExists(test_file) == True

def test_loadPortfolio(standard_manager_path):
    test_file = "test_save_portfolio"
    with pytest.raises(FileNotFoundError):
        res = standard_manager_path.loadPortfolio(test_file)
        assert 0
        assert res == False

    res = standard_manager_path.savePortfolio(test_file)
    assert res == True

    new_manager = PortfolioManager()
    new_manager.DEFAULT_PATH = standard_manager_path.DEFAULT_PATH
    new_manager.loadPortfolio(test_file)

    assert new_manager.currentPortfolio == standard_manager_path.currentPortfolio
