import pytest
from ch3_scripts.bank_accounts import Bank, Account


@pytest.fixture()
def withdraw_setup():
    """Pytest fixture to set up bank and accounts."""
    print('\n============SetUp-Start==============')
    bank = Bank('test_bank')
    demo_account = Account('Tina Tester', bank, 100)
    demo_account2 = Account('Tareq Tester', bank, 40)
    print('============SetUp-End================')
    return [demo_account, demo_account2]


def test_withdraw_amount_negative(withdraw_setup):
    """Test withdraw method with negative amount."""
    demo_account = withdraw_setup[0]
    demo_account2 = withdraw_setup[1]
    assert demo_account.withdraw(50) == True
    assert demo_account.transactions[-1].get('amount') < 0
    assert demo_account.withdraw(50, receiver = demo_account2) == True
    assert demo_account.transactions[-1].get('amount') < 0



def test_withdraw_receiver_default(withdraw_setup):
    """Test the receiver default is 'CASH'."""
    demo_account = withdraw_setup[0]
    demo_account.withdraw(50)
    assert demo_account.transactions[-1].get('receiver') == 'CASH'


def test_withdraw_insufficient_funds(withdraw_setup):
    """Test insufficient funds."""
    demo_account = withdraw_setup[0]
    demo_account2 = withdraw_setup[1]
    assert demo_account.withdraw(150) == False
    assert demo_account.transactions[-1].get('executed') == False
    assert demo_account2.withdraw(50, receiver = demo_account) == False
    assert demo_account2.transactions[-1].get('executed') == False



