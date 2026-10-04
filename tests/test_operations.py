import pytest
from typing import Union
from app.operation import Operation

Number = Union[int, float]

# -----------------------------------------------------------------------------------
# Unit Tests for the 'addition' method in the Operation class
# -----------------------------------------------------------------------------------

@pytest.mark.parametrize(
    "a, b, expected_result",
    [
        (10, 5, 15),            # Test with two positive integers
        (0, 5, 5),              # Test with a zero and a postive integer
        (10, -5, 5),            # Test with one positive and one negative integer
        (-12.0, 5.0, -7.0),     # Test with a negative float and a positive float
        (10.0, 5.0, 15.0),      # Test with two positive floats
    ],
    ids=[
        "add_two_positive_integers",
        "add_zero_and_positive_integer",
        "add_positive_and_negative_integer",
        "add_zero_and_positive_float",
        "add_positive_float_and_zero",
    ]
)
def test_addition(a: Number, b: Number, expected_result: Number) -> None:
    """
    Test the addition method with various combinations of numbers.
    
    This test verifies that adding two numbers returns the correct sum for different scenarios.
    """
    # Act: Call the addition method from the Operation class
    result = Operation.addition(a, b)

    # Assert: The result should match the expected result
    assert result == expected_result, f"Expected {a} + {b} to be {expected_result}, got {result}"   

# -----------------------------------------------------------------------------------
# Unit Tests for the 'subtraction' method in the Operation class
# -----------------------------------------------------------------------------------
@pytest.mark.parametrize(
    "a, b, expected_result",
    [
        (10.0, 5.0, 5.0),               # Test with two positive numbers
        (-10.0, -5.0, -5.0),            # Test with two negative numbers
        (10.0, -5.0, 15.0),             # Test with one positive and one negative number
        (0.0, 5.0, -5.0),               # Test with zero and a positive number
        (10.0, 0.0, 10.0),              # Test with a positive number and zero
    ],
    ids=[
        "subtract_two_positive_floats",
        "subtract_two_negative_floats",
        "subtract_positive_and_negative_float",
        "subtract_zero_and_positive_float",
        "subtract_positive_float_and_zero",
    ]
)
def test_subtraction(a: Number, b: Number, expected_result: Number) -> None:
    """
    Test the subtraction method with various combinations of numbers.
    
    This test verifies that subtracting two numbers returns the correct difference for different scenarios.
    """
    # Act: Call the subtraction method from the Operation class
    result = Operation.subtraction(a, b)

    # Assert: The result should match the expected result
    assert result == expected_result, f"Expected {a} - {b} to be {expected_result}, got {result}"   

# -----------------------------------------------------------------------------------
# Unit Tests for the 'multiplication' method in the Operation class
# -----------------------------------------------------------------------------------   

@pytest.mark.parametrize(
    "a, b, expected_result",
    [
        (10, 5, 50),              # Test with two positive integers
        (-10, -5, 50),            # Test with two negative integers
        (10, -5, -50),            # Test with one positive and one negative integer
        (0.0, 5.0, 0.0),          # Test with zero and a positive float
        (10.0, -5.0, -50.0),      # Test with one positive and one negative float
    ],
    ids=[
        "multiply_two_positive_integers",
        "multiply_two_negative_integers",
        "multiply_positive_and_negative_integers",
        "multiply_zero_and_positive_float",
        "multiply_two_negative_floats",
    ]
)
def test_multiplication(a: Number, b: Number, expected_result: Number) -> None:
    """
    Test the multiplication method with various combinations of numbers.
    
    This test verifies that multiplying two numbers returns the correct product for different scenarios.
    """
    # Act: Call the multiplication method from the Operation class
    result = Operation.multiplication(a, b)

    # Assert: The result should match the expected result
    assert result == expected_result, f"Expected {a} * {b} to be {expected_result}, got {result}"

# -----------------------------------------------------------------------------------
# Unit Tests for the 'division' method in the Operation class
# -----------------------------------------------------------------------------------   
@pytest.mark.parametrize(
    "a, b, expected_result",
    [
        (10, 5, 2),               # Test with two positive integers
        (-10, -5, 2),             # Test with two negative integers
        (10, -5, -2),             # Test with one positive and one negative integer
        (0.0, 5.0, 0.0),          # Test with zero and a positive float
        (10.0, -5.0, -2.0),      # Test with one positive and one negative float
    ],
    ids=[
        "divide_two_positive_integers",
        "divide_two_negative_integers",
        "divide_positive_and_negative_integers",
        "divide_zero_and_positive_float",
        "divide_positive_and_negative_float",
    ]
)
def test_division(a: Number, b: Number, expected_result: Number) -> None:
    """
    Test the division method with various combinations of numbers.
    
    This test verifies that dividing two numbers returns the correct quotient for different scenarios.
    """
    # Act: Call the division method from the Operation class
    result = Operation.division(a, b)

    # Assert: The result should match the expected result
    assert result == expected_result, f"Expected {a} / {b} to be {expected_result}, got {result}"
