import datetime
from experimental.exp_store import RentalStore
from experimental.exp_products import Laptop, Phone

NoneType = type(None)

import difflib
import random

class Customer():
    """
    Serves as the main interface of the rental system. Stores information about customers 
    and allows interactions with store and products.
    
    Args:
        name (str): Customer name.
        store (RentalStore): Store to which customer belongs.
        current_items (list): Currently rented items. Defaults to empty list.
        
    Attributes:
        name (str): Customer name.
        store (RentalStore): Store to which customer belongs.
        
    Properties:
        invoice (float):  Outstanding amount to pay by customer for due items.
        current_items (list): Currently rented items.
        owned_items (list): Items bought from store.
        due_items (list): Rented, unpaid items after their rental period has ended.
        paid_items (list): Rented, paid items after their rental period has ended.
        invoice (float): Outstanding amount to pay by customer for rented items. Defaults to 0.0.

    """

    def __init__(self,
                 name,
                 store,
                 current_items=None):
        if isinstance(current_items, NoneType):
            current_items = []
        assert isinstance(store, RentalStore), 'Customer needs to be linked to a valid RentalStore'
        for item in current_items:
            assert isinstance(item, Product), 'Can only rent Product Objects'
        self.name = name
        self.store = store
        self._rented_items = []
        self._paid = {}
        self._owned_items = [] # for purchased items
        
    @property
    def invoice(self):
        """float: Outstanding amount to pay by customer for due items."""
        return sum([item.rental_time * item.price_per_week for item in self.due_items])
    
    @property
    def current_items(self):
        return [item for item in self._rented_items if item.rental_end > datetime.date.today()]
    
    @property
    def due_items(self):
        return [item for item in self._rented_items
                if item.rental_end <= datetime.date.today()
                and not self._paid[item.product_id]]
    
    @property
    def paid_items(self):
        return [item for item in self._rented_items
                if item.rental_end <= datetime.date.today()
                and self._paid[item.product_id]]
    
    @property
    def owned_items(self):
        return self._owned_items
    
    def pay_invoice(self, amount_paid):
        """Pay invoice and reset it to 0.0. Removes payed for items from current_items.
        
        Args:
            amount_paid (float): Amount to pay to settle invoice.

        """

        assert isinstance(amount_paid, (int, float)), 'amount_paid must be int or float'
        assert amount_paid > 0, 'amount_paid must be positive'
        assert self.invoice == amount_paid, 'Whole bill must be paid, no partial payments possible'

        # delete old items
        for item in self.due_items:
            self._paid[item.product_id] = True
        
    def rent(self, item_name, rental_time):
        """Rent item for specific amount of time.
        
        Args:
            item_name (str): Item name as given by Product.__repr__().
            rental_time (int): Rental time in weeks.
        
        Raises:
            AssertionError: If item_name not in self.store.products.

        """

        #check if item in Store
        assert item_name in [item.name for item in self.store.products], 'item must be in store'
        #check if item available
        rental_item = [item for item in self.store.products
                      if item.name == item_name][0]
        
        # if item available in store, set rental time and start rental today
        if rental_item.rent(rental_time):
            self._rented_items.append(rental_item)
            self._paid[rental_item.product_id] = False
            
        # if not available, display message and all store items
        else:
            print('Sorry, {} is currently not available'.format(item_name))
            print('Here is a list of products and their availability:')
            self.store.display_products()

    def buy(self, item_name): 
        """Buy item from store. Remove item from products in store. Does not handle monetary transactions.
        
        Args:
            item_name (str): Item name as given by Product.__repr__().
            
        Raises:
            AssertionError: If item_name not in self.store.products.

        """

        #check if item in Store
        assert item_name in [item.name for item in self.store.products], 'item must be in store'
        #check if item available
        purchased_item = [item for item in self.store.products
                          if item.name == item_name][0]
        if purchased_item.available and purchased_item.buyable:
            # delete from rental store
            self.store.products.remove(purchased_item)
            self._owned_items.append(purchased_item)
        else:
            print('Sorry, {} is currently not available for purchase'.format(item_name))
            print('Please be aware that only some product types are available for purchase')
            print('Here is a list of products and their availability:')
            self.store.display_products()

    def __repr__(self):
        """Return __repr__ as 'Customer: NAME, NUMBER OF ITEMS items rented'"""
        return 'Customer: {}, {} items rented.'.format(self.name, len(self.current_items))

    def __str__(self):
        """
        Return __str__ as five rows containing name, owned items,
        current items, items due and invoice amount.
        
        """
        
        base_str = """{}
Owned items: {}
Rented items: {}
Due items: {}
Amount payable: {}"""

        return base_str.format(self.name,
                               self.owned_items,
                               self.current_items,
                               self.due_items,
                               self.invoice)           
            
    def search_products(self, search_query, n_results = 5, _diff_cutoff = 0.6):
        """
        Search similar product names in store for a given search query.
        
        Args:
            search_query (str): String to search for similar strings in product names.
            store (RentalStore): RentalStore to search product names in.
            n_results (int): Maximum number of results to return. Defaults to 5.
            _diff_cutoff (float): Difference cutoff for the sequence matching algorithm. 
                Defaults to 0.6. Change with caution.

        Returns:
            result (list): List of product names (str) that match the given query.

        """

        product_names = [product.name for product in self.store.products]
        result = difflib.get_close_matches(search_query, 
                                           product_names, 
                                           n=n_results, 
                                           cutoff=_diff_cutoff) 
        return result
    
    def rent_random_product(self, product_type, rental_time):
        """Rents a random Product from a given product type"""
        assert product_type in [type(product) for product 
                                in self.store.products], 'Product Type must be in Store'
        available_products = [product for product 
                              in self.store.products 
                              if type(product) == product_type 
                              and product.available]
        chosen_product = random.choice(available_products)
        
        print('{} rented for {} weeks'.format(chosen_product.name, 
                                              rental_time))
        self.rent(chosen_product.name,rental_time)