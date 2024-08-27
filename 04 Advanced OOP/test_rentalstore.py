import pytest
from store import RentalStore
from products import Product, Laptop, Phone


@pytest.fixture
def store():
    """Fixture for RentalStore instance"""
    out = RentalStore([
        Laptop('Test Product A 1'),
        Laptop('Test Product A 2', 10),
        Phone('Test Product B 1', 5.2)
    ])
    return out


def test_rentalstore_init():
    """Test assert statement to allow only Product-type to be in rental store."""
    with pytest.raises(AssertionError):
        RentalStore(['Product', 'Product 2.0'])
        
        
def test_rentalstore_len(store):
    """Test __len__() method."""
    assert len(store) == 3


def test_rentalstore_add_product(store):
    """Test adding (only) Product-type to rental store via '+' operator."""
    new_product = Laptop('New Product')
    store + new_product
    
    assert store.products[-1].name == 'New Product'
    assert store.products[-1].product_id == new_product.product_id
    assert len(store) == 4
    

def test_rentalstore_add_product_returns_store(store):
    """Test return when adding (only) Product-type to rental store via '+' operator."""
    new_product = Laptop('New Product')
    result = store + new_product
    assert isinstance(result, RentalStore)
    assert store.products[-1].name == 'New Product'
    assert store.products[-1].product_id == new_product.product_id
    assert len(store) == 4    
    
    
def test_rentalstore_add_product_errors(store):
    """Test errors when adding non-Product-type to rental store via '+' operator."""    
    with pytest.raises(AssertionError):
        store + 'New Product 2.0'
        
    with pytest.raises(AssertionError):
        store + store
        
        
def test_rentalstore_substract_product(store):
    """Test removing products via '-' operator."""
    removed_product = store.products[0]
    
    new_product = Laptop('New Product')
    
    # len should be 2 now instead of 3
    store - removed_product
    assert len(store) == 2
    
    # len should be unchanged
    store - new_product
    assert len(store) == 2
    
    
def test_rentalstore_substract_product_errors(store):
    """Test errors when substracting non-Product-type to rental store via '-' operator."""    
    with pytest.raises(AssertionError):
        store - 'New Product 2.0'
        
    with pytest.raises(AssertionError):
        store - store
        
        
def test_rentalstore_substract_product_returns_store(store):
    """Test return when substracting (only) Product-type to rental store via '-' operator."""
    removed_product = store.products[0]
    
    result = store - removed_product
    assert isinstance(result, RentalStore)
    assert len(result) == 2
    
