class ShoppingList():
    """
    Contains the information of items in the shopping cart and their price.
    """
    
    def __init__(self):
        self.items = {}
        
    def add_item(self, item):
        """
        Add item name and price to the items dictionary, if the item name is not yet in it.
        Print a confirmation that item was added.

        Args:
            item (Notebook): Notebook to be added to the list

        """

        assert not item.name in self.items.keys(), "Item names must be unique!, Please consider renaming your configuration."
        self.items.update({item.name: item.price})
        print('{} added.'.format(item.name))
    
    def _get_total(self):
        """Sum prices of all items. Getter method for the property 'total'."""
        return sum(self.items.values())
    
    total = property(_get_total)
    
    def display_items(self):
        """Print all items currently in the shopping list in the format: 'item     €price'"""
        for item, price in self.items.items():
            print('{} \t €{}'.format(item, price))
    
    def delete_item(self, item):
        """Remove item from items dictionary. Print a confirmation that item was deleted."""
        print('{} deleted.'.format(item.name))
        del self.items[item.name]

class Notebook():
    """
    Contains the information for a notebook configuration.

    Args:
        name (str): Notebooks unique name, required by ShoppingList.
        ram (str, optional): Notebook's RAM size from the available choices. 
            Defaults to '4GB'.
        battery (str, optional) Notebook's average battery time from the available choices.
            Defaults to '10h'.
        os (str, optional) Specifies whether Notebook comes with OS preinstalled. 
            Defaults to 'Yes'.
        ssd (str, optional): Notebook's SSD size from the available choices.
            Defaults to '120GB'. 
        screen (str, optional): Notebook's screen size from the available choices.
            Defaults to '15"'.

    """

    base_price = 500.00
    notebook_parts = {'ram': {'4GB': 20.0, '8GB': 40.0, '16GB': 90.0},
                      'battery': {'10h': 0.0, '16h': 50.0},
                      'os': {'Yes': 50.0, 'No': 0.0},
                      'ssd': {'120GB': 0.0, '500GB': 50.0, '1TB': 120.0},
                      'screen': {'15"': 0.0, '17"': 100.0}}
    valid_configuration_options = notebook_parts.keys()

    def __init__(self, name, ram='4GB', battery='10h',
                 os='Yes', ssd='120GB', screen='15"'):
        assert ram in Notebook.notebook_parts['ram'], "Please pick a valid RAM option ({})".format(
            ', '.join(Notebook.notebook_parts['ram'].keys()))
        assert battery in Notebook.notebook_parts['battery'], 'Please pick a valid battery option ({})'.format(
            ', '.join(Notebook.notebook_parts['battery'].keys()))
        assert os in Notebook.notebook_parts['os'], 'Please pick a valid OS option ({})'.format(
            ', '.join(Notebook.notebook_parts['os'].keys()))
        assert ssd in Notebook.notebook_parts['ssd'], 'Please pick a valid SSD option ({})'.format(
            ', '.join(Notebook.notebook_parts['ssd'].keys()))
        assert screen in Notebook.notebook_parts['screen'], 'Please pick a valid screen option ({})'.format(
            ', '.join(Notebook.notebook_parts['screen'].keys()))
        self.name = name
        self.ram = ram
        self.battery = battery
        self.os = os
        self.ssd = ssd
        self.screen = screen

    def list_components(self):
        """Print all components of the chosen configuration in the format: 'component     chosen option'."""
        for part, option in self.__dict__.items():
            print('{}\t{}'.format(part, option))

    def _get_price(self):
        """Sum prices of all valid notebook parts. Setter method for the property 'price'."""
        prices = [Notebook.notebook_parts[part][option]
                  for part, option in self.__dict__.items() if part in Notebook.valid_configuration_options]
        prices.append(self.base_price)
        return sum(prices)

    price = property(_get_price,doc="Sum of all parts' prices.")


shopping_list = ShoppingList()

default_notebook = Notebook('Standard Notebook')
default_notebook.list_components()
print('Price\t€{}'.format(default_notebook.price))



shopping_list.add_item(default_notebook)
shopping_list.display_items()



highend_notebook = Notebook('Highend Notebook', ram='16GB', battery='16h',
                            os='Yes', ssd='1TB', screen='17"')
highend_notebook.list_components()
assert highend_notebook.price == 910.0, 'The price is not correct'
print('Price\t€{}'.format(highend_notebook.price))

shopping_list.add_item(highend_notebook)


shopping_list.display_items()
print('Shopping Card Total\t€{}'.format(shopping_list.total))


# Should raise AssertionError.
dream_notebook = Notebook('Dream Notebook', ram='64GB', battery='24h',
                          os='Yes', ssd='2TB', screen='17"')


#Fetch list
shopping_list.display_items()