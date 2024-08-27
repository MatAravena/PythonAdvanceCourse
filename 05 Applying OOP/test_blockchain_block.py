import time
import json
import hashlib
import pytest
import copy

from blockchain import Block


@pytest.fixture()
def now():
    return time.time()

@pytest.fixture()
def transaction():
    return {
        'sender': 'Alice',
        'receiver': 'Bob',
        'amount': 10.0
    }

@pytest.fixture()
def block(transaction, now):
    return Block(
        index=0,
        timestamp=now,
        previous_hash='0123456789abcdef',
        transaction=transaction
    )

@pytest.fixture()
def block_hash(block):
    json_encoded = json.dumps(block.__dict__, sort_keys=True).encode()
    return hashlib.sha256(json_encoded).hexdigest()


def test_block_init(transaction, now):
    """Test init of Block class."""
    block = Block(
        index=0,
        timestamp=now,
        previous_hash='0123456789abcdef',
        transaction=transaction
    )
    assert block.index == 0
    assert block.timestamp == now
    assert block.previous_hash == '0123456789abcdef'
    assert block.transaction == transaction
    assert block.nonce == 0


def test_block_init_errors(transaction, now):
    """Test various init errors of Block class."""
    
    # missing arguments
    with pytest.raises(TypeError):
        block = Block()
        
    # index not integer
    with pytest.raises(AssertionError):
        block = Block(
            index=0.5,
            timestamp=now,
            previous_hash='0123456789abcdef',
            transaction=transaction
        )
        
    # index negative
    with pytest.raises(AssertionError):
        block = Block(
            index=-1,
            timestamp=now,
            previous_hash='0123456789abcdef',
            transaction=transaction
        )
        
    # timestamp not float
    with pytest.raises(AssertionError):
        block = Block(
            index=0,
            timestamp='now',
            previous_hash='0123456789abcdef',
            transaction=transaction
        )
        
    # previous_hash not string
    with pytest.raises(AssertionError):
        block = Block(
            index=0,
            timestamp=now,
            previous_hash=123456789,
            transaction=transaction
        )
        
    # previous_hash not string
    with pytest.raises(AssertionError):
        block = Block(
            index=0,
            timestamp=now,
            previous_hash=123456789,
            transaction='Alice sends Bob 10 EUR'
        )
        
        
def test_block_dict(block):
    """Test __dict__ attribute of Block class."""
    
    # test after init
    assert isinstance(block.__dict__, dict)
    assert 'index' in block.__dict__
    assert 'transaction' in block.__dict__
    assert 'timestamp' in block.__dict__
    assert 'previous_hash' in block.__dict__
    assert 'nonce' in block.__dict__
    assert len(block.__dict__) == 5
    
    # test after hash property has been called
    current_hash = block.hash
    assert isinstance(block.__dict__, dict)
    assert 'index' in block.__dict__
    assert 'transaction' in block.__dict__
    assert 'timestamp' in block.__dict__
    assert 'previous_hash' in block.__dict__
    assert 'nonce' in block.__dict__
    assert len(block.__dict__) == 5    
        

def test_block_hash(block, block_hash):
    """Test property hash of Block class."""
    
    # should have expected hash
    assert block.hash == block_hash
    
    # changing any attribute should change hash
    new_block = copy.deepcopy(block)
    new_block.index += 1
    assert not new_block.hash == block_hash

    new_block = copy.deepcopy(block)
    new_block.timestamp = time.time()
    assert not new_block.hash == block_hash
    
    new_block = copy.deepcopy(block)
    new_block.previous_hash = 'fedcba9876543210'
    assert not new_block.hash == block_hash
    
    new_block = copy.deepcopy(block)
    new_block.previous_hash = 'fedcba9876543210'
    assert not new_block.hash == block_hash
    
    new_block = copy.deepcopy(block)
    new_block.nonce += 1
    assert not new_block.hash == block_hash
    
    # adding attributes should change hash
    new_block = copy.deepcopy(block)
    new_block.new_attribute = 'my new attribute'
    assert not new_block.hash == block_hash
    
    
def test_block_hash_read_only(block):
    """Test that the hash property is read-only."""
    with pytest.raises(AttributeError):
        block.hash = '0123456789abcdef'
        
        
def test_block_hash_consistent(block, block_hash):
    """Test that the hash property is robust to method calls."""
    
    # hash does not change after calling property
    block.hash
    assert block.hash == block_hash
    
    # hash does not change after calling __repr__
    block.__repr__()
    assert block.hash == block_hash
    
    
def test_block_repr(block, block_hash):
    """Test method __repr__() of Block class"""
    return_str = block.__repr__()
    assert block_hash in return_str
    
    
    
    
