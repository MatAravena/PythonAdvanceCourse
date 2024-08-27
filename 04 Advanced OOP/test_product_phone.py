import pytest
import datetime

from products import Phone

NoneType = type(None)


@pytest.fixture
def products():
    """Fixture to test both product variants"""
    out = [
        Phone('Test Product B 1'),
        Phone('Test Product B 2', 5.2)
    ]
    return out

        
def test_phone_init(products):
    """Test Product class initialisation, test assert statements for correct input."""
    assert products[0].price_per_week == 0
    assert products[1].price_per_week == 5.2   
    assert isinstance(products[1].product_id, str)
        
    with pytest.raises(AssertionError):
        Phone('Test Product C', '4')
        
    with pytest.raises(AssertionError):
        Phone(123)

    
def test_phone_rent(products):
    """Test rent() method of Laptop."""
    today = datetime.date.today()
    products[0].rent(8)
    assert products[0].rental_time == 8
    assert products[0].rental_start == today
    assert products[0].rental_end == today + datetime.timedelta(weeks=8)
       
        
def test_buyable(products):
    """Test buyable attribute of Phone"""
    assert products[0].buyable == True
    assert products[1].buyable == True


def test_phone_creation_from_dict():
    """Test initialisation through classmethod .from_dict()"""
    test_prod_a = Phone.from_dict({'name':'Test Product',
                                   'price_per_week': 3.5})
    test_prod_b = Phone.from_dict({'name':'Test Product 2',
                                   'price_per_week': 0})
    
    assert test_prod_a.name == 'Test Product'
    assert test_prod_a.price_per_week == 3.5
    assert test_prod_b.name == 'Test Product 2'
    assert test_prod_b.price_per_week == 0
    
    with pytest.raises(AssertionError):
        Phone.from_dict(['Test Product', 3.5])
    with pytest.raises(AssertionError):
        Phone.from_dict({'product_name':'Test Product', 
                         'price_per_week': 3.5})
    with pytest.raises(AssertionError):
        Phone.from_dict({'name':'Test Product', 
                         'price': 3.5})
    with pytest.raises(AssertionError):
        Phone.from_dict({'name':'Test Product'})