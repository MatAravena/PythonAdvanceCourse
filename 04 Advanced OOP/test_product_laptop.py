import pytest
import datetime

from products import Laptop

NoneType = type(None)


@pytest.fixture
def products():
    """Fixture to test both product variants"""
    out = [
        Laptop('Test Product A 1'),
        Laptop('Test Product A 2', 10)
    ]
    return out


def test_laptop_init(products):
    """Test Laptop class initialisation, test assert statements for correct input."""
    assert products[0].price_per_week == 0
    assert products[1].buyable == False    
    assert isinstance(products[1].product_id, str)
        
    with pytest.raises(AssertionError):
        Laptop('Test Product C', '4')
        a
    with pytest.raises(AssertionError):
        Laptop(123)
        
        
def test_laptop_rent(products):
    """Test rent() method of Laptop."""
    today = datetime.date.today()
    products[0].rent(8)
    assert products[0].rental_time == 8
    assert products[0].rental_start == today
    assert products[0].rental_end == today + datetime.timedelta(weeks=8)
    
    
def test_laptop_has_max_rental_time():
    """Test that Laptop has class attribute max_rental_time."""
    assert Laptop.max_rental_time == 12
    
    
def test_laptop_rent_over_max_rental_time(products):
    """Test rent() method of Laptop for longer rental times."""
    max_rental_time = Laptop.max_rental_time
    with pytest.raises(AssertionError):
        products[0].rent(max_rental_time + 1)


# rental_time needs to be tested again for Laptop due to new def of property
def test_laptop_set_rental_time(products):
    """Test setting rental_time property of Laptop."""
    
    # rental_time is None when initialized
    assert isinstance(products[0].rental_time, NoneType)
    
    # rental_time can be extended
    products[0].rent(8)
    products[0].rental_time = 10
    assert products[0].rental_time == 10
    

def test_laptop_set_rental_time_errors(products):
    """Test erros when setting the rental_time property of Laptop."""
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
        
    # cannot be extended beyond max_rental_time
    with pytest.raises(AssertionError):
        products[0].rental_time = Laptop.max_rental_time + 1   

        
def test_laptop_creation_from_list():
    """Test initialisation through classmethod .from_list()"""
    test_prod_a = Laptop.from_list(['Test Product', 3.5])
    test_prod_b = Laptop.from_list(['Test Product 2'])
        
    assert test_prod_a.name == 'Test Product'
    assert test_prod_a.price_per_week == 3.5
    assert test_prod_b.name == 'Test Product 2'
    assert test_prod_b.price_per_week == 0
    
    with pytest.raises(AssertionError):
        Laptop.from_list(('Test Product', 3.5, 'third variable'))
    with pytest.raises(AssertionError):
        Laptop.from_list(['Test Product', 3.5, 'third variable'])
