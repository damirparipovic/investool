import pytest
from requests import HTTPError
from investool import stock

MSFT_STOCK_PRICE = 123.45

@pytest.fixture()
def msft_stock():
    newStock = stock.Stock('msft', MSFT_STOCK_PRICE, 'usd', 10, 0.3, 0)
    return newStock

@pytest.fixture
def empty_stock():
    return stock.Stock()

def test_repr_print(msft_stock):
    assert repr(msft_stock) == "Stock('msft', 123.45, 'usd', 10, 0.3, 0)"

def test_str_print(msft_stock):
    assert str(msft_stock) == stock.FORM.format(msft_stock.ticker,
                                                msft_stock.price,
                                                msft_stock.currency,
                                                msft_stock.units,
                                                msft_stock.percent,
                                                msft_stock.stockValue)

def test_ticker(msft_stock):
    assert msft_stock.ticker == 'msft'

def test_set_ticker(empty_stock):
    empty_stock.ticker = 'goog'
    assert empty_stock.ticker == 'goog'

def test_invalid_ticker(empty_stock):
    with pytest.raises(Exception):
        empty_stock.ticker = ''
    with pytest.raises(Exception):
        empty_stock.ticker = 'al;ksdjf'
    with pytest.raises(Exception):
        empty_stock.ticker = '12345'

def test_equality(msft_stock):
    # equality assert empty_stock == stock.Stock()
    assert msft_stock == stock.Stock('msft', 123.45, 'usd', 10, 0.3, 0)

def test_inequality_type(msft_stock):
    # test if not same type
    assert msft_stock != "hello"
    assert msft_stock != 42

def test_equality_two_stocks(empty_stock, msft_stock):
    assert empty_stock != msft_stock

def test_equality_one_change(msft_stock):
    assert msft_stock != stock.Stock('m', 123.45, 'usd', 10, 0.3, 0)
    assert msft_stock != stock.Stock('msft', 1.45, 'usd', 10, 0.3, 0)
    assert msft_stock != stock.Stock('msft', 123.45, 'usd', 9, 0.3, 0)
    assert msft_stock != stock.Stock('msft', 123.45, 'usd', 10, 0.2, 0)
    assert msft_stock != stock.Stock('msft', 123.45, 'usd', 10, 0.3, 1)

def test_hash(msft_stock, empty_stock):
    assert hash(empty_stock) == hash(stock.Stock())
    assert hash(msft_stock) == hash(stock.Stock('msft', 123.45, 'usd', 10, 0.3, 0))
    assert hash(msft_stock) != hash(stock.Stock('msft', 123.00, 'usd', 10, 0.3, 0))
    assert hash(msft_stock) != hash(stock.Stock('msft', 123.45, 'usd', 9, 0.3, 0))

def test_price(msft_stock, empty_stock):
    assert msft_stock.price == MSFT_STOCK_PRICE

    empty_stock.price = 200.0
    assert empty_stock.price == 200.0

    with pytest.raises(ValueError):
        empty_stock.price = -20

def test_currency(msft_stock, empty_stock):
    pass

def test_units(msft_stock, empty_stock):
    assert msft_stock.units == 10

    empty_stock.units = 20
    assert empty_stock.units == 20

    with pytest.raises(ValueError):
        empty_stock.units = -10

def test_percent(msft_stock, empty_stock):
    assert msft_stock.percent == 0.3

    empty_stock.percent = 0.5
    assert empty_stock.percent == 0.5

    with pytest.raises(ValueError):
        empty_stock.percent = -1
    with pytest.raises(ValueError):
        empty_stock.percent = 2
    with pytest.raises(TypeError):
        empty_stock.percent = "msft"

def test_stockValue(msft_stock, empty_stock):
    assert msft_stock.stockValue == 0

    empty_stock.stockValue = 123
    assert empty_stock.stockValue == 123

    empty_stock.stockValue = 12.3
    assert empty_stock.stockValue == 12.3

    with pytest.raises(ValueError):
        empty_stock.stockValue = -2
    with pytest.raises(ValueError):
        empty_stock.stockValue = -3.2
    with pytest.raises(TypeError):
        empty_stock.stockValue = "abc"

def test_getCurrentPrice(msft_stock, empty_stock, mocker):
    # check that returned empty object returns None
    assert empty_stock.getCurrentPrice() == None

    # check if value returned is None
    mockTicker = mocker.patch("investool.stock.yf.Ticker")
    mockTicker.return_value.fast_info = None
    assert empty_stock.getCurrentPrice() == None

    # check if everything works as intended
    mockTicker.return_value.fast_info = {"lastPrice": MSFT_STOCK_PRICE}
    assert msft_stock.price == msft_stock.getCurrentPrice()

    # check that HTTPError occurs and raises an HTTPError with custom details
    with mocker.patch("investool.stock.yf.Ticker", side_effect=HTTPError):
        with pytest.raises(HTTPError):
            msft_stock.getCurrentPrice()

def test_updatePrice(msft_stock, empty_stock, mocker):
    empty_stock.updatePrice() 
    assert empty_stock.price == 0.0

    msft_stock.getCurrentPrice = mocker.MagicMock(return_value=42)
    msft_stock.updatePrice()
    assert msft_stock.price != MSFT_STOCK_PRICE
    assert msft_stock.price == 42

def test_updateValue(msft_stock):
    msft_stock.updateValue()
    assert msft_stock.stockValue == 1234.5
