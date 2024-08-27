import pytest
import datetime
from customer import Customer
from store import RentalStore
from products import Laptop, Phone

NoneType = type(None)


@pytest.fixture
def products():
    """Fixture to test both products"""
    out = [
        Laptop('Test Product A 1'),
        Laptop('Test Product A 2', 10),
        Phone('Test Product B 1', 5.2)
    ]
    return out

@pytest.fixture
def store(products):
    """Fixture for RentalStore instance"""
    out = RentalStore(products)
    return out


@pytest.fixture
def demo_customer(store):
    """Fixture for Customer instance"""
    out = Customer('Tina Tester', store)
    return out


def test_customer_init(demo_customer, store):
    """Test Customer initialization."""
    assert demo_customer.name == 'Tina Tester'
    assert demo_customer.store == store
    assert demo_customer.invoice == 0.0
    assert demo_customer.current_items == []
    assert demo_customer.due_items == []
    assert demo_customer.paid_items == []
    assert demo_customer.owned_items == []
    
def test_customer_init_errors(demo_customer):
    """Test Customer initialization errors."""
    with pytest.raises(AssertionError):
        test_customer = Customer('Tobias Tester', 'MyStore')
    with pytest.raises(AssertionError):
        test_customer = Customer('Tobias Tester',
                                 RentalStore(), 
                                 current_items = ['MyProduct'])
    

def test_customer_repr(demo_customer):
    """Test __repr__ for Customer."""
    assert demo_customer.__repr__() == 'Customer: Tina Tester, 0 items rented.'

    
def test_customer_str(demo_customer, products):
    """Test __str__ for Customer."""
    base_str = """Tina Tester
Owned items: [{}]
Rented items: [{}]
Due items: [{}]
Amount payable: {}"""
    
    demo_product = products[0]
    demo_buyable_product = products[2]
    
    # check empty representation
    not_rented_str = base_str.format('', '', '', 0)
    assert str(demo_customer) == not_rented_str
    
    # check representation when renting 
    demo_customer.rent(demo_product.name, 2)
    
    product_rented_str = base_str.format('', demo_product.__repr__(), '', 0)
    assert str(demo_customer) == product_rented_str
    
    # check representation when buying and renting
    demo_customer.buy(demo_buyable_product.name)
    
    product_rented_and_bought_str = base_str.format(
        demo_buyable_product.__repr__(),
        demo_product.__repr__(),
        '',
        0
    )
    
    assert str(demo_customer) == product_rented_and_bought_str


def test_customer_rent(demo_customer, products):
    """Test method rent() for Customer."""
    demo_product = products[0]
    demo_id = demo_product.product_id
    demo_customer.rent(demo_product.name, 2)
    
    current_ids = [item.product_id for item in demo_customer.current_items]
    due_ids = [item.product_id for item in demo_customer.due_items]
    paid_ids = [item.product_id for item in demo_customer.paid_items]
    
    assert demo_id in current_ids
    assert demo_id not in due_ids
    assert demo_id not in paid_ids
    
    
def test_customer_rent_errors(demo_customer):
    """Test errors of method rent() for Customer."""
    with pytest.raises(AssertionError):
        demo_customer.rent('Toaster', 2)
        
        
def test_customer_due_items(demo_customer, products):
    demo_product = products[1]
    demo_customer.rent(demo_product.name, 2)
    demo_product._rental_start = datetime.date.today() - datetime.timedelta(weeks=3)
    
    assert demo_product in demo_customer.due_items


def test_customer_pay_invoice(demo_customer, products):
    """Test invoice property for Customer"""
    
    # rent product
    demo_product = products[1]
    rental_time = 2
    demo_customer.rent(demo_product.name, rental_time)
    
    # calculate amount to pay
    amount_to_pay = demo_product.price_per_week * rental_time
    
    # backdate rental
    demo_product._rental_start = datetime.date.today() - datetime.timedelta(weeks=3)
    
    # pay invoice
    demo_customer.pay_invoice(amount_to_pay)
    
    assert demo_product in demo_customer.paid_items
    

def test_customer_buy(demo_customer, products):
    """Test buy() method for Customer"""
    demo_product = products[2]
    demo_customer.buy(demo_product.name)
    assert demo_product in demo_customer.owned_items
    # test add to owned items
    assert len(demo_customer.owned_items) == 1
    # test removal from store
    assert len(demo_customer.store.products) == 2
        
        
#def test_customer_buy_errors(demo_customer, products):
#    """Test errors of method buy() for Customer"""
#    
#    demo_product_1 = products[1]
#    demo_product_2 = products[2]
#    demo_customer.rent(demo_product_2.name, 2)
#    
#    print(demo_product_1.price_per_week)
#    
#    # test non-buyable items
#    with pytest.raises(AssertionError):
#        demo_customer.buy(demo_product_1.name)
#        
#    # test already rented items
#    with pytest.raises(AssertionError):
#        demo_customer.buy(demo_product_2.name)    