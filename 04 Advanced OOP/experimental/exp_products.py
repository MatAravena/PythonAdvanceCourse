import datetime
import uuid

NoneType = type(None)

# Lösung:

class Product():
    """
    Contains basic attributes and properties of a product.
    
    Args:
        name (str): Product's name.
        price_per_week (float, optional): Product's rental price per week.
            Defaults to 0.
    
    Attributes:
        name (str): Product's name.
        product_id (str): Unique product ID given by uuid.uuid1().
        buyable (bool): Product's status regarding purchases. Defaults to False.
    
    """

    def __init__(self, 
                 name,
                 price_per_week=0):
        #assert statements to check types
        assert isinstance(name, str), 'name must be string'
        assert isinstance(price_per_week, (int, float)), 'price_per_week must be int or float'
        
        self.name = name
        self.product_id = str(uuid.uuid1())
        self.buyable = False
        self._price_per_week = price_per_week
        self._rental_time = None
        self._rental_start = None
        
    @property
    def price_per_week(self):
        """int, float: Product's rental price per week."""
        return self._price_per_week
    
    @price_per_week.setter
    def price_per_week(self, new_price):
        assert isinstance(new_price, (int, float)), 'New price must be int or float'
        assert new_price > 0, 'New price must be positive'
        self._price_per_week = new_price
        
    def rent(self, rental_time):
        """
        Rent product for given rental time.
        
        Args:
            rental_time (int): Time to rent the product in weeks.
                Must be strictly positive.
                
        Returns:
            True if Product is available, False otherwise.
            
        """

        assert isinstance(rental_time, int), 'rental_time must be int'
        assert rental_time > 0, 'rental_time must be positive'
        if self.available:
            self._rental_time = rental_time
            self._rental_start = datetime.date.today()
            return True
        else:
            return False
              
    @property
    def rental_start(self):
        """datetime.date: Product's rental start date. Read-only."""
        return self._rental_start
    
    @property
    def rental_end(self):
        """datetime.date: Product's rental end date. Read-only."""
        return self.rental_start + datetime.timedelta(weeks=self.rental_time)
    
    @property
    def rental_time(self):
        """int: Product's rental time in weeks. Can be increased to extend rental."""
        return self._rental_time    
        
    @rental_time.setter
    def rental_time(self, rental_time):
        assert not isinstance(self._rental_time, NoneType), 'Product has not been rented yet'
        assert isinstance(rental_time, int), 'rental_time must be int'
        assert rental_time >= self._rental_time, 'Rental can only be extended, not shortened'
        self._rental_time = rental_time

    @property
    def available(self):
        """bool: Product's availability."""
        if isinstance(self._rental_time, NoneType):
            return True
        elif datetime.date.today() > self.rental_end:
            return True
        else:
            return False
        
    def product_description(self):
        """Display product name and price per week."""
        print('Product: {}\nPrice per week: {}'.format(self.name, self.price_per_week))
        
    def __repr__(self):
        """Returns objects __repr__ as name of object"""
        return self.name
    
    def __str__(self):
        """Returns objects str representation"""
        return '{}\nPrice per week: {}'.format(self.name, self.price_per_week)
    
    
class Laptop(Product):
    """
    Contains basic attributes of a Laptop. Subclass of Product.
    
    Args:
        name (str): Product's name.
        price_per_week (float): Product's rental price per week. Defaults to None.
    
    Attributes:
        name (str): Product's name.
        product_id (str): Unique product ID given by uuid.uuid1().
        buyable (bool): Product's status regarding purchases. Defaults to False.
    
    """
    
    # int: maximal rental time
    max_rental_time = 12
    
    def rent(self, rental_time):
        """
        Rent product for given rental time.
        
        Args:
            rental_time (int): Time to rent the product in weeks.
                Must be strictly positive and less or equal than
                Laptop.max_rental_time.
                
        Returns:
            True if Product is available, False otherwise.
            
        """

        assert isinstance(rental_time, int), 'rental_time must be int'
        assert rental_time > 0, 'rental_time must be positive'
        assert rental_time <= Laptop.max_rental_time, 'Rental time must be below {} weeks'.format(Laptop.max_rental_time)
        if self.available:
            self._rental_time = rental_time
            self._rental_start = datetime.date.today()
            return True
        else:
            return False
        
    @property
    def rental_time(self):
        """int: Product's rental time in weeks. Can be increased to extend rental."""
        return self._rental_time
    
    # define property setter newly to check against max_rental_time
    # for this property must be redefined completely, only setter doesn't work   
    @rental_time.setter
    def rental_time(self, rental_time):
        assert not isinstance(self._rental_time, NoneType), 'Product has not been rented'
        assert isinstance(rental_time, int), 'rental_time must be int'
        assert rental_time >= self.rental_time, 'Rental can only be extended, not shortened'
        assert rental_time <= Laptop.max_rental_time, 'Rental time must be below {} weeks'.format(Laptop.max_rental_time)
        self._rental_time = rental_time
        
    @classmethod
    def display_max_rental_time(cls):
        """Displays maximum rental time for product."""
        return cls.max_rental_time
    
    @classmethod
    def from_list(cls, param_list):
        """Allows class creation from list of parameters."""
        # assert list
        assert type(param_list) == list, "list must be passed to method"
        # assert list length
        assert len(param_list) <= 2, 'param_list should not have more than 2 elements'
        try:
            name, price_per_week = param_list
            return cls(name, price_per_week)
        except ValueError: #catch if list has only one parameter
            return cls(param_list[0])
        
    
    
class Phone(Product):
    """
    Contains basic attributes of a Phone. Subclass of Product.
    
    Args:
        name (str): Product's name.
        price_per_week (float): Product's rental price per week.
            Defaults to 0.
    
    Attributes:
        name (str): Product's name.
        product_id (str): Unique product ID given by uuid.uuid1().
        buyable (bool): Product's status regarding purchases. Defaults to True.
        price_per_week (float): Product's rental price per week.
    
    """
    
    def __init__(self,name,
                 price_per_week=0):
        super().__init__(name, price_per_week)
        self.buyable = True
            
    @classmethod #task
    def from_dict(cls, param_dict):
        """Allows class creation from dict of parameters."""
        # assert dict
        assert type(param_dict) == dict, "dict must be passed to method"
        # assert dict keys
        assert list(param_dict.keys()) == ['name','price_per_week'], "param_dict should contain 'name' and 'price_per_week' keys (and no others)"
        name = param_dict.get('name')
        price_per_week = param_dict.get('price_per_week')
        return cls(name, price_per_week)