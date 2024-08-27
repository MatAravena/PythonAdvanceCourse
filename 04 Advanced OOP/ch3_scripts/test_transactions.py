import pytest
from ch3_scripts.bank_accounts import Bank, Account


bank = Bank('test_bank')


def test_withdraw_amount_negative():
    """Test withdraw method with negative amount."""
    demo_account = Account('Tina Tester', bank, 100)
    demo_account2 = Account('Tareq Tester', bank, 40)
    # assert that withdraw of 50 from demo_account is possible -> returns True
    assert demo_account.withdraw(50) == True
    # assert that withdraw of 50 from demo_account makes transaction with negative amount
    assert demo_account.transactions[-1].get('amount') < 0
    # assert that withdraw of 50 from demo_account to demo_account2 is possible -> returns True
    assert demo_account.withdraw(50, receiver = demo_account2) == True
    # assert that withdraw of 50 from demo_account to demo_account2 makes transaction with negative amount
    assert demo_account.transactions[-1].get('amount') < 0


def test_withdraw_receiver_default():
    """Test the receiver default is 'CASH'."""
    demo_account = Account('Tina Tester', bank, 100)
    demo_account.withdraw(50)
    assert demo_account.transactions[-1].get('receiver') == 'CASH'



def test_withdraw_insufficient_funds():
    """Test insufficient funds."""
    demo_account = Account('Tina Tester', bank, 100)
    demo_account2 = Account('Tareq Tester', bank, 40)
    assert demo_account.withdraw(150) == False
    assert demo_account.transactions[-1].get('executed') == False
    assert demo_account2.withdraw(50, receiver = demo_account) == False
    assert demo_account2.transactions[-1].get('executed') == False


