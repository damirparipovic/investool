import pytest
from investool.stock import Stock
from investool.portfolio import Portfolio

@pytest.fixture(scope="session")
def standard_portfolio():
    stocks = []
    stocks.append(Stock('msft', 10, 10, 0.5, 0))
    stocks.append(Stock('appl', 20, 10, 0.25, 0))
    stocks.append(Stock('zag.to', 30, 10, 0.25, 0))
    port = Portfolio('test', stocks, 100.0)
    return port

@pytest.fixture()
def empty_portfolio(scope="session"):
    return Portfolio()

def test_portfolio_creation(standard_portfolio, empty_portfolio):
    assert empty_portfolio.portfolioName == ''
    assert empty_portfolio.stocks == []
    assert empty_portfolio.totalValue == 0.0
    assert standard_portfolio.portfolioName == 'test'
    assert standard_portfolio.stocks == [Stock('msft', 10, 10, 0.5, 0), 
                                         Stock('appl', 20, 10, 0.25, 0),
                                         Stock('zag.to', 30, 10, 0.25, 0)]
    assert standard_portfolio.totalValue == 100.0

def test_portfolio_repr(empty_portfolio):
    assert repr(empty_portfolio) == "Portfolio('', [], 0.0)"

def test_portfolio_str(empty_portfolio):
    assert str(empty_portfolio) == "Portfolio: \n  - stocks: []\n  - totalValue: 0.0"

def test_equality(standard_portfolio):
    stocks = []
    stocks.append(Stock('msft', 10, 10, 0.5, 0))
    stocks.append(Stock('appl', 20, 10, 0.25, 0))
    stocks.append(Stock('zag.to', 30, 10, 0.25, 0))
    assert standard_portfolio == Portfolio('test', stocks, 100.0)

def test_inequality_properties(standard_portfolio):
    assert standard_portfolio != '42'
    assert standard_portfolio != 42
    assert standard_portfolio != Stock("msft", 10, 10, 0.5, 0)

def test_inequality_two_portfolios(empty_portfolio, standard_portfolio):
    assert empty_portfolio != standard_portfolio

def test_portfolio_name(standard_portfolio):
    assert standard_portfolio.portfolioName == "test"

def test_empty_portfolio_name(empty_portfolio):
    assert empty_portfolio.portfolioName == ""

def test_portfolio_name_setter(empty_portfolio):
    new_name = "abcd123"
    empty_portfolio.portfolioName = new_name
    assert empty_portfolio.portfolioName == new_name

def test_stocks(standard_portfolio):
    assert standard_portfolio.stocks == [Stock('msft', 10, 10, 0.5, 0),
                                          Stock('appl', 20, 10, 0.25, 0),
                                          Stock('zag.to', 30, 10, 0.25, 0)]

def test_empty_stocks(empty_portfolio):
    assert empty_portfolio.stocks == []
    
def test_stocks_setter(empty_portfolio):
    new_stocks = [Stock('not_stock', 1, 2, 3, 4)]
    empty_portfolio.stocks = new_stocks
    assert empty_portfolio.stocks == [Stock('not_stock', 1, 2, 3, 4)]
