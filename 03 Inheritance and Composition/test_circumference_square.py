import pytest
from circumference_square import circumference_square

def test_circumference_square_a_is_number():
    with pytest.raises(TypeError):
        circumference_square('1')

def test_circumference_square_negative_number():
    with pytest.raises(ValueError):
        circumference_square(-1)

@pytest.mark.parametrize('test_input, expected_output', [(1, 4), (4, 16), (2.5, 2.5*4)])
def test_circumference_square_output(test_input, expected_output):
    assert circumference_square(test_input) == expected_output
    
    
 