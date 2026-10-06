# tests/test_calculation.py

"""
Unit tests for the calculator_calculations module using pytest.

This test suite covers both positive and negative scenarios for the Calculation
classes and the CalculationFactory. It ensures that calculations execute correctly,
the factory creates appropriate instances, and error handling behaves as expected.

Tests are organized following the AAA (Arrange, Act, Assert) pattern and adhere
to PEP8 standards for code style and formatting.
"""

import pytest
from unittest.mock import patch
from app.operation import Operation
from app.calculation import (
    CalculationFactory,
    AddCalculation,
    SubtractCalculation,
    MultiplyCalculation,
    DivideCalculation,
    PowerCalculation,
    ModulusCalculation,
    Calculation
)

# -----------------------------------------------------------------------------------
# Parameterized Tests for Execute Method (Positive Scenarios)
# -----------------------------------------------------------------------------------

@pytest.mark.parametrize(
    "calc_class, operation_method, a, b, expected_result",
    [
        (AddCalculation, 'addition', 10.0, 5.0, 15.0),
        (SubtractCalculation, 'subtraction', 10.0, 5.0, 5.0),
        (MultiplyCalculation, 'multiplication', 10.0, 5.0, 50.0),
        (DivideCalculation, 'division', 10.0, 5.0, 2.0),
        (PowerCalculation, 'power', 2.0, 3.0, 8.0),
        (ModulusCalculation, 'modulus', 10.0, 3.0, 1.0),
    ],
    ids=["add", "subtract", "multiply", "divide", "power", "modulus"]
)
def test_calculation_execute_positive(calc_class, operation_method, a, b, expected_result):
    """
    Parameterized test for the execte method of Calculation subclasses (Positive).
    Verifies that the correct Operation method is called and the result is returned.
    """
    # Arrange & Act
    with patch.object(Operation, operation_method, return_value=expected_result) as mock_op:
        calc = calc_class(a, b)
        result = calc.execute()

    # Assert
    mock_op.assert_called_once_with(a, b)
    assert result == expected_result


# -----------------------------------------------------------------------------------
# Parameterized Tests for Execute Method (Negative Scenarios)
# -----------------------------------------------------------------------------------

@pytest.mark.parametrize(
    "calc_class, operation_method, a, b",
    [
        (AddCalculation, 'addition', 10.0, 5.0),
        (SubtractCalculation, 'subtraction', 10.0, 5.0),
        (MultiplyCalculation, 'multiplication', 10.0, 5.0),
        (DivideCalculation, 'division', 10.0, 5.0),
        (PowerCalculation, 'power', 2.0, 3.0),
        (ModulusCalculation, 'modulus', 10.0, 3.0)
    ],
    ids=["add", "subtract", "multiply", "divide", "power", "modulus"]
)
def test_calculation_execute_negative(calc_class, operation_method, a, b):
    """
    Parameterized test for the execute method of Calculation subclasses (Negative).
    Verifies that exceptions from the Operation layer are propagated correctly.
    """
    # Arrange
    error_message = f"{operation_method} error"
    
    # Act & Assert
    with patch.object(Operation, operation_method, side_effect=Exception(error_message)):
        calc = calc_class(a, b)
        
        with pytest.raises(Exception) as exc_info:
            calc.execute()

    assert str(exc_info.value) == error_message


# -----------------------------------------------------------------------------------
# Specialized Edge Case Tests
# -----------------------------------------------------------------------------------

def test_divide_calculation_execute_division_by_zero():
    """
    Test that DivideCalculation.execute raises ZeroDivisionError when dividing by zero.
    """
    # Arrange
    a = 10.0
    b = 0.0
    divide_calc = DivideCalculation(a, b)

    # Act & Assert
    with pytest.raises(ZeroDivisionError) as exc_info:
        divide_calc.execute()

    assert str(exc_info.value) == "Cannot divide by zero."


# -----------------------------------------------------------------------------------
# Parameterized Tests for CalculationFactory
# -----------------------------------------------------------------------------------

@pytest.mark.parametrize(
    "calc_type, expected_class, a, b",
    [
        ('add', AddCalculation, 10.0, 5.0),
        ('subtract', SubtractCalculation, 10.0, 5.0),
        ('multiply', MultiplyCalculation, 10.0, 5.0),
        ('divide', DivideCalculation, 10.0, 5.0),
        ('power', PowerCalculation, 2.0, 3.0),
        ('modulus', ModulusCalculation, 10.0, 3.0),
    ],
    ids=["add", "subtract", "multiply", "divide", "power", "modulus"]
)
def test_factory_creates_correct_calculation(calc_type, expected_class, a, b):
    """
    Parameterized test to verify the Factory creates the correct subclass instance
    and correctly assigns the operands.
    """
    # Act
    calc = CalculationFactory.create_calculation(calc_type, a, b)

    # Assert
    assert isinstance(calc, expected_class)
    assert calc.a == a
    assert calc.b == b


def test_factory_create_unsupported_calculation():
    """
    Test that CalculationFactory raises ValueError when an unsupported calculation type is requested.
    """
    # Arrange
    a = 10.0
    b = 5.0
    unsupported_type = 'exponent'  # Changed from 'modulus' since modulus is now supported!

    # Act & Assert
    with pytest.raises(ValueError) as exc_info:
        CalculationFactory.create_calculation(unsupported_type, a, b)

    assert f"Unsupported calculation type: '{unsupported_type}'" in str(exc_info.value)


def test_factory_register_calculation_duplicate():
    """
    Test that registering a calculation type that's already registered raises ValueError.
    """
    # Arrange & Act
    with pytest.raises(ValueError) as exc_info:
        @CalculationFactory.register_calculation('add')
        class AnotherAddCalculation(Calculation):
            def execute(self) -> float:
                return Operation.addition(self.a, self.b)

    # Assert
    assert "Calculation type 'add' is already registered." in str(exc_info.value)


# -----------------------------------------------------------------------------------
# Parameterized Tests for String Representation (__str__)
# -----------------------------------------------------------------------------------

@pytest.mark.parametrize(
    "calc_class, operation_method, a, b, expected_result, expected_str",
    [
        (AddCalculation, 'addition', 10.0, 5.0, 15.0, "AddCalculation: 10.0 Add 5.0 = 15.0"),
        (SubtractCalculation, 'subtraction', 10.0, 5.0, 5.0, "SubtractCalculation: 10.0 Subtract 5.0 = 5.0"),
        (MultiplyCalculation, 'multiplication', 10.0, 5.0, 50.0, "MultiplyCalculation: 10.0 Multiply 5.0 = 50.0"),
        (DivideCalculation, 'division', 10.0, 5.0, 2.0, "DivideCalculation: 10.0 Divide 5.0 = 2.0"),
        (PowerCalculation, 'power', 2.0, 3.0, 8.0, "PowerCalculation: 2.0 Power 3.0 = 8.0"),
        (ModulusCalculation, 'modulus', 10.0, 3.0, 1.0, "ModulusCalculation: 10.0 Modulus 3.0 = 1.0"),
    ],
    ids=["add", "subtract", "multiply", "divide", "power", "modulus"]
)
def test_calculation_str_representation(calc_class, operation_method, a, b, expected_result, expected_str):
    """
    Parameterized test for the __str__ method of Calculation subclasses.
    """
    # Arrange & Act
    with patch.object(Operation, operation_method, return_value=expected_result):
        calc = calc_class(a, b)
        calc_str = str(calc)

    # Assert
    assert calc_str == expected_str


# -----------------------------------------------------------------------------------
# Parameterized Tests for Repr Representation (__repr__)
# -----------------------------------------------------------------------------------

@pytest.mark.parametrize(
    "calc_class, a, b",
    [
        (AddCalculation, 10.0, 5.0),
        (SubtractCalculation, 10.0, 5.0),
        (MultiplyCalculation, 10.0, 5.0),
        (DivideCalculation, 10.0, 5.0),
        (PowerCalculation, 2.0, 3.0),
        (ModulusCalculation, 10.0, 3.0),
    ],
    ids=["add", "subtract", "multiply", "divide", "power", "modulus"]
)
def test_calculation_repr_representation(calc_class, a, b):
    """
    Parameterized test for the __repr__ method of Calculation subclasses.
    """
    # Arrange
    calc = calc_class(a, b)
    expected_repr = f"{calc_class.__name__}(a={a}, b={b})"

    # Act & Assert
    assert repr(calc) == expected_repr