
from products import Product, Laptop, Phone

NoneType = type(None) 

# Lösung:
class RentalStore():
    """
    Container to store products.
    
    Args:
        products (list): List of Products in store. Defaults to empty list.

    """

    def __init__(self, products=None):
        if isinstance(products, NoneType):
            products = []
            
        for product in products:
            assert isinstance(product, Product), 'Can only add Product Objects'
        self.products = products
        
    @staticmethod
    def display_impressum():
        """Display Impressum."""
        print('IMPRESSUM \nE-Rentor GmbH \nPfandweg 7 \n44321 Leihstadt')
        
    def display_products(self):
        """Display products with name, price per week and availability."""
        for product in self.products:
            print('{}: \t {:.2f}€ per week \t Available: {}'.format(product.name, 
                                                                    product.price_per_week,
                                                                    product.available))

    def __len__(self):
        """Display number of products when len() is called."""
        return len(self.products)
               
    def __add__(self, other): 
        """Add product to self.products via '+' operator."""
        assert isinstance(other, Product), 'Can only add Product Objects'
        self.products.append(other)
        print('{} added to store'.format(other.__repr__()))
        return self
    
    def __sub__(self, other):
        """Remove product from self.products via '-' operator."""
        assert isinstance(other, Product), 'Can only remove Product Objects'
        
        for product in self.products:
            if product.name == other.name:
                self.products.remove(product)
                return self
            
        print('{} cannot be removed, as it is not part of the store\'s products'.format(other.__repr__()))
        return self
            

