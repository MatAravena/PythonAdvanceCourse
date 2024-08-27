#base
import pytest

from ch3_scripts.bank_accounts import Account, Bank


bank = Bank("Test-Bank")


@pytest.fixture
def accounts():
    """Pytest fixture to set up accounts."""
    out = [
        Account("Tina Test", bank, 100),
        Account("Tareq Test", bank, 40),
        Account("Tommy Test", bank),
    ]
    return out


def test_init_balance(accounts):
    """Test initial balance."""
    assert accounts[0].balance == 100
    assert accounts[1].balance == 40
    assert accounts[2].balance == 0


def test_withdraw(accounts):
    """Test withdraw method."""
    accounts[0].withdraw(10)
    assert accounts[0].balance == 90
    accounts[1].withdraw(40)
    assert accounts[1].balance == 0
    assert accounts[2].withdraw(10) == False


def test_transfer(accounts):
    """Test transfer method."""
    accounts[0].transfer(50, accounts[1])
    assert accounts[0].balance == 50
    assert accounts[1].balance == 90


# # Addition 1:
# import os
# from shutil import rmtree

# # Global scoped SetUp-Method
# @pytest.fixture(scope="module")
# def temp_folder():
#     path = "./temp_files"
#     os.mkdir(path)
#     return path

# # Revision 1:
# # Global scoped SetUp with TearDown   
# @pytest.fixture(scope="module")
# def temp_folder():
#     path = "./temp_files"
#     os.mkdir(path)
#     yield path
#     rmtree(path)

# # Addition 1
# def test_save_account_statement(temp_folder, accounts):
#     accounts[0].withdraw(10)
#     accounts[0].deposit(5)
#     accounts[0].transfer(50, accounts[1])
#     accounts[1].transfer(20, accounts[0])
#     accounts[0].save_account_statement(temp_folder)
#     temp_files = os.listdir(temp_folder)
#     assert "{}.csv".format(accounts[0].IBAN) in temp_files

