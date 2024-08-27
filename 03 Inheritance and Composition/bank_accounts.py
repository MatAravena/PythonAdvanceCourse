import random
import uuid


class Account():
    """Bank Account of a customer.

    Args:
        customer (str): Name of the customer.
        bank (Bank): Bank-Object where you want to register the account.
        init_balance(int, float): Optional. Starting balance of the account.
            Defaults to 0.

    """

    def __init__(self,
                 customer,
                 bank,
                 init_balance=0):
        assert isinstance(bank, Bank)
        self.bank_num = bank.bank_num
        self.IBAN = self._create_new_IBAN()
        self.customer = customer
        self.transactions = []
        self.credit_limit = 0

        self._init_balance(init_balance)
        bank.add_account(self)

    def _create_new_IBAN(self):
        return "DE00{}{}".format(
            self.bank_num, random.randrange(1000000000, 9999999999, 10)
        )

    def _init_balance(self, init_balance):
        """Run to give Customer some initial money."""
        
        if init_balance > 0:
            self.deposit(init_balance)

    def _get_balance(self):
        balance = sum(
            [
                transaction.get('amount')
                for transaction in self.transactions
                if transaction.get('executed') == True
            ]
        )
        return balance

    # Property is read only, if you only pass a getter method.
    balance = property(_get_balance)

    def _add_transaction(self, transaction):
        """Add a new transaction."""
        self.transactions.append(transaction)
        print("Added {}".format(transaction.__repr__()))
        return self

    def deposit(self, amount, sender = 'CASH'):
        """Add money to bank account.

        Args:
            amount: Amount of money to put on the account. Must be a positive number.
            sender: Optional. Account-Object if deposit comes from a Tranfer.
                "CASH" if a deposit is a cash deposit. Defaults to "CASH"

        """

        deposit_dict = {
                        'transaction_id': str(uuid.uuid1()),
                        'amount': amount,
                        'sender': sender,
                        'receiver': self,
                        'executed': True
                        }
        self._add_transaction(deposit_dict)
        return self

    def withdraw(self, amount, receiver = 'CASH'):
        """Withdraw money from bank account."""

        withdraw_dict = {
                        'transaction_id': str(uuid.uuid1()),
                        'amount': amount *-1,
                        'sender': self,
                        'receiver': receiver,
                        'executed': False
                        }
        
        if  abs(amount) <= (self.balance + self.credit_limit):
            withdraw_dict['executed'] = True
            self._add_transaction(withdraw_dict)
            return True
        else:
            print('Insufficient funds.')
            self._add_transaction(withdraw_dict)
            return False
        
    def transfer(self, amount, receiver):
        """Transfer money from this Account to another account.

        Args:
            amount: Amount of money to draw from the account. Must be a positive number.
            receiver(Account): Account-Object of recipient.

        """

        transfer_dict = {
                         'transaction_id': str(uuid.uuid1()),
                         'amount': amount,
                         'sender': self,
                         'receiver': receiver,
                         'executed': False
                        }
        
        if self.withdraw(amount, receiver = receiver):
            receiver.deposit(amount, sender = self)
        
        return self


class Bank():
    """Bank container for holding accounts

    Args:
        name (str): name of the bank.
    Attributes:
        name (str): name of the bank.
        bank_num (int): Bank number create as a random number betwen 10000000 and 99999999.
        _accounts (dict): Dictionary holding the accounts of the format {iban: Account object}.

    """

    def __init__(self, name: str):
        self.name = name
        self.bank_num = random.randrange(10000000, 99999999)
        self._accounts = {}

    def add_account(self, account):
        """Add bank account to this bank. For creating a new account use the Account class.

        Args:
            account (Account): Bank account to be added
        Raises:
            AssertionError: If account.IBAN is already in _accounts.

        """

        assert isinstance(account, Account)
        iban = account.IBAN
        assert iban not in self._accounts, "IBAN already registered"
        self._accounts.update({iban: account})
        return self

    def _get_accounts(self):
        """Getter for the property 'account'"""
        return self._accounts

    accounts = property(_get_accounts)
    
class Savings(Account):
    """Savings Account, adds interest to the normal Account."""

    interest_rate = 0.05

    def add_annual_interest(self):
        self.deposit(self.balance * Savings.interest_rate)
        return self


class CreditCard(Account):
    """CreditCard Account, extends Account with a credit limit"""

    credit_limit = 1000

    def __init__(self, customer, bank, init_balance=0):
        super().__init__(customer, bank, init_balance)
        self.credit_limit = CreditCard.credit_limit


class Premium(Savings, CreditCard):
    """Combine functionality of Savings and CreditCard"""

    pass
