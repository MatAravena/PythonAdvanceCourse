import pytest
from experimental.exp_products import Product, Laptop, Phone
from experimental.exp_store import RentalStore
from experimental.exp_customer import Customer

from collections import Counter


@pytest.fixture
def store():
    """Fixture for RentalStore instance"""
    out = RentalStore([
        Laptop('Test Product A 1'),
        Laptop('Test Product A 2', 10),
        Phone('Test Product B 1', 5.2)
    ])
    return out

@pytest.fixture
def customer(store):
    """Fixture for Customer instance"""
    out = Customer('Timothy Test', store=store)
    return out


def test_product_counts(store):
    """Test product counts property and most common method"""
    assert store.product_counts == Counter({Laptop: 2, Phone: 1})
    assert store.get_most_common_product() == [(Laptop, 2)]


def test_search_products(customer):
    """Test product search through customer method"""
    assert customer.search_products('Test Product') == ['Test Product B 1',
                                                        'Test Product A 2',
                                                        'Test Product A 1']
    assert customer.search_products('XYZ') == []


def test_rent_random_product(customer):
    """Test random product rental based on product type"""
    
    customer.rent_random_product(Laptop, 12)
    assert len(customer.current_items) == 1
    with pytest.raises(AssertionError):
        customer.rent_random_product(Product, 12)