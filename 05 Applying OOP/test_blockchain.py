import time
import json
import hashlib
import pytest
import copy

from blockchain import Block, Blockchain


@pytest.fixture()
def blockchain():
    return Blockchain()

@pytest.fixture()
def transaction():
    return {
        'sender': 'Alice',
        'receiver': 'Charlie',
        'amount': 50.0
    }

@pytest.fixture()
def now():
    return time.time()

@pytest.fixture()
def new_block(blockchain, transaction, now):
    return Block(
        index=1,
        timestamp=now,
        previous_hash=blockchain.chain[-1].hash,
        transaction=transaction
    )


def test_blockchain_init(blockchain):
    """Test blockchain initialization."""
    assert hasattr(blockchain, 'chain')
    assert len(blockchain.chain) == 1
    assert isinstance(blockchain.chain[0], Block)
    
    
def test_blockchain_genesis_block(blockchain):
    """Test genesis block creation."""
    genesis_block = blockchain.chain[0]
    assert hasattr(genesis_block, 'index')
    assert genesis_block.index == 0
    assert hasattr(genesis_block, 'timestamp')
    assert hasattr(genesis_block, 'previous_hash')
    assert hasattr(genesis_block, 'nonce')
    assert hasattr(genesis_block, 'transaction')
    
    
def test_blockchain_create_block_from_transation(blockchain, transaction, new_block):
    """Test creating new blocks."""
    last_block = blockchain.chain[-1]
    
    this_new_block = blockchain.create_block_from_transaction(transaction)
    
    assert isinstance(this_new_block, Block)
    assert this_new_block.index == 1
    assert this_new_block.transaction == transaction
    assert this_new_block.previous_hash == last_block.hash
    # not yet added
    assert len(blockchain.chain) == 1
    
    # compare to pre-computed new block
    assert this_new_block.index == new_block.index
    assert this_new_block.previous_hash == new_block.previous_hash
    assert this_new_block.transaction == new_block.transaction


def test_blockchain_add_block(blockchain, new_block):
    """Test adding new blocks."""
    blockchain.add_block(new_block)
    assert len(blockchain.chain) == 2
    assert blockchain.chain[-1] == new_block


def test_blockchain_add_block_errors(blockchain, new_block, now):
    """Test adding new blocks."""
    blockchain.add_block(new_block)
    
    new_new_block = Block(
        index=5,
        timestamp=now,
        previous_hash='0123456789abcdef',
        transaction={}
    )
    
    with pytest.raises(AssertionError):
        blockchain.add_block('Alice sends Bob 50 EUR')
        
    with pytest.raises(AssertionError):
        blockchain.add_block(new_new_block)

    
def test_blockchain_last_block(blockchain, new_block):
    """Test blockchain's last_block property."""
    assert isinstance(blockchain.last_block, Block)
    
    blockchain.add_block(new_block)
    assert isinstance(blockchain.last_block, Block)
    assert blockchain.last_block.index == new_block.index
    assert blockchain.last_block.timestamp == new_block.timestamp
    assert blockchain.last_block.previous_hash == new_block.previous_hash
    assert blockchain.last_block.transaction == new_block.transaction
    
    
def test_blockchain_len(blockchain, new_block):
    """Test method __len__() of blockchain."""
    assert len(blockchain) == 1
    blockchain.add_block(new_block)
    assert len(blockchain) == 2


def test_blockchain_repr(blockchain):
    """Test method __repr__() of blockchain."""
    return_str = blockchain.__repr__()
    
    for block in blockchain.chain:
        assert block.hash in return_str
    