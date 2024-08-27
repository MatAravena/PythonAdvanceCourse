import pytest
import datetime

from products import Product

NoneType = type(None)


@pytest.fixture
def products():
    """Fixture to test different product configurations."""
    out = [
        Product('Test Product A'),
        Product('Test Product B', 10),
        Product('Test Product C', 5.2)
    ]
    return out


def test_product_init(products):
    """Test Product class initialisation, test assert statements for correct input."""
    assert products[0].price_per_week == 0
    assert products[1].buyable == False
    assert isinstance(products[1].product_id, str)
    with pytest.raises(AssertionError):
        Product('Test Product C', '4')
    with pytest.raises(AssertionError):
        Product(123)
        
        
def test_product_rent(products):
    """Test rent() method."""
    today = datetime.date.today()
    products[0].rent(8)
    assert products[0].rental_time == 8
    assert products[0].rental_start == today
    assert products[0].rental_end == today + datetime.timedelta(weeks=8)
    
    
def test_product_rent_errors(products):
    """Test errors of rent() method."""
    # must be positive rental_time
    with pytest.raises(AssertionError):
        products[0].rent(-2)
        
    # must be int (weeks)
    with pytest.raises(AssertionError):
        products[1].rent('4 weeks')
    
    
def test_product_rent_available(products):
    """Test whether the property available changes when rented."""
    assert products[0].available
    products[0].rent(8)
    assert not products[0].available
    
    
def test_product_available_read_only(products):
    """Test whether the property available is read-only."""
    with pytest.raises(AttributeError):
        products[0].available = False
    with pytest.raises(AttributeError):
        products[1].rent(8)
        products[1].available = True


def test_product_price_per_week(products):
    """Test the price_per_week property."""
    # matches args
    assert products[0].price_per_week == 0
    assert products[1].price_per_week == 10
    assert products[2].price_per_week == 5.2
    
    # can be updated
    products[2].price_per_week = 6.3
    assert products[2].price_per_week == 6.3
    
    
def test_product_set_price_per_week_errors(products):
    """Test erros when setting the price_per_week property."""
    # must be int or float
    with pytest.raises(AssertionError):
        products[0].price_per_week = '4 EUR'
    
    # must be positive
    with pytest.raises(AssertionError):
        products[1].price_per_week = -2
        
        
def test_product_set_rental_time(products):
    """Test setting the rental_time property."""
    
    # rental_time is None when initialized
    assert isinstance(products[0].rental_time, NoneType)
    
    # rental_time can be extended
    products[0].rent(8)
    products[0].rental_time = 10
    assert products[0].rental_time == 10


def test_product_set_rental_time_errors(products):
    """Test erros when setting the rental_time property."""
    # should not be settable when initialized
    with pytest.raises(AssertionError):
        products[0].rental_time = 2
        
    # can only be extended
    products[0].rent(8)
    with pytest.raises(AssertionError):
        products[0].rental_time = 6
        
    # must be int
    with pytest.raises(AssertionError):
        products[0].rental_time = '4 Weeks'
    

def test_product_rental_start_read_only(products):
    """Test whether rental_start property is read-only."""
    with pytest.raises(AttributeError):
        products[0].rental_start = datetime.date(2020, 1, 1)

        
def test_product_rental_end_read_only(products):
    """Test whether rental_end property is read-only."""
    with pytest.raises(AttributeError):
        products[0].rental_end = datetime.date(2020, 1, 1)
        
