import pytest
from investool.portfolio import Portfolio
from investool.stock import Stock

@pytest.fixture()
def standard_portfolio():
    stocks = []
    stocks.append(Stock('msft', 10, 10, 0.5, 0))
    stocks.append(Stock('appl', 20, 10, 0.25, 0))
    stocks.append(Stock('zag.to', 30, 10, 0.25, 0))
    port = Portfolio('test', stocks, 100.0)
    return port

@pytest.fixture()
def empty_portfolio():
    return Portfolio()

def test_portfolio_creation(standard_portfolio, empty_portfolio):
    assert empty_portfolio.portfolioName == 'new'
    assert empty_portfolio.stocks == []
    assert empty_portfolio.totalValue == 0.0
    assert standard_portfolio.portfolioName == 'test'
    assert standard_portfolio.stocks == [Stock('msft', 10, 10, 0.5, 0), 
                                         Stock('appl', 20, 10, 0.25, 0),
                                         Stock('zag.to', 30, 10, 0.25, 0)]
    assert standard_portfolio.totalValue == 100.0

def test_portfolio_prints(empty_portfolio):
    assert repr(empty_portfolio) == "Portfolio('new', [], 0.0)"
