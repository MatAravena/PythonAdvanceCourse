from scripts.bank_accounts import Bank, Account

banc = Bank('Banco Matu')

@pytest.fixture()
def test_withdraw_amount_negative():
    accountA = Account('Moi', banc, 5000)
    accountB = Account('Moi2', banc, 5000)

    # assert that withdraw of 50 from demo_account is possible -> returns True
    assert accountA.withdraw(50) == True

    # assert that withdraw of 50 from demo_account makes transaction with negative amount
    assert accountA.transactions[-1].get('amount') < 0

    # assert that withdraw of 50 from demo_account to demo_account2 is possible -> returns True
    assert accountA.withdraw(50, receiver = accountB) == True

    # assert that withdraw of 50 from demo_account to demo_account2 makes transaction with negative amount
    assert accountA.transactions[-1].get('amount') < 0

@pytest.fixture()
def test_withdraw_receiver_default():
    """Test the receiver default is 'CASH'."""
    accountA = Account('Tina Tester', banc, 100)
    accountA.withdraw(50)
    assert accountA.transactions[-1].get('receiver') == 'CASH'

@pytest.fixture()
def test_withdraw_insufficient_funds():
    """Test insufficient funds."""
    accountA = Account('Tina Tester', banc, 100)
    accountB = Account('Tareq Tester', banc, 40)
    assert accountA.withdraw(150) == False
    assert accountA.transactions[-1].get('executed') == False
    assert accountB.withdraw(50, receiver = accountA) == False
    assert accountB.transactions[-1].get('executed') == False
