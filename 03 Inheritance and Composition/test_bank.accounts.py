import pytest
from scripts.bank_accounts import Bank, Account


def test_add_account():
    """Test method add_account."""
    bank = Bank('test_bank')
    account = Account('Petra May', bank, 50)
    
    assert bank._accounts[account.IBAN] == account, 'Account IBAN {account.IBAN} not in bank._accounts' 
    assert bank._accounts == {account.IBAN: account}, 'Account storage not like {IBAN : Account object}.'


def test_no_duplicate_account():
    """Test that method add_account is not be able to overwrite existing accounts."""
    bank = Bank('test_bank')
    account = Account('Petra May', bank, 50)
    
    with pytest.raises(AssertionError):
        bank.add_account(account)


def test_get_account():
    """Test property accounts."""
    bank = Bank('test_bank')
    account1 = Account('Petra May', bank, 50)
    account2 = Account('Jim Gordon', bank, 200)
    assert bank.accounts == bank.__dict__['_accounts'] , 'Property "accounts" does not retrun the same data as the private Attribute "_accounts"'


def test_get_account_read_only():
    """"Test that property 'accounts' is read only."""
    bank = Bank('test_bank')
    account = Account('Petra May', bank, 50)
    with pytest.raises(AttributeError):
        bank.accounts = {account.IBAN: account}
