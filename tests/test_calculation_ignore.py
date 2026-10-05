# tests/test_calculations.py

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
    Calculation
)

# -----------------------------------------------------------------------------------
# Unit Tests for the CalculationFactory class
# -----------------------------------------------------------------------------------
@pytest.mark.parametrize(
    "operation_type, expected_class",
    [
        ("add", AddCalculation),
        ("subtract", SubtractCalculation),
        ("multiply", MultiplyCalculation),
        ("divide", DivideCalculation),
    ],
    ids=[
        "create_add_calculation",
        "create_subtract_calculation",
        "create_multiply_calculation",
        "create_divide_calculation",
    ]
)
def test_calculation_factory_creates_correct_instance(operation_type: str, expected_class: type) -> None:
    """
    Test that the CalculationFactory creates the correct Calculation subclass
    based on the provided operation type.
    """
    # Act: Create a calculation instance using the factory
    calculation_instance = CalculationFactory.create_calculation(operation_type)

    # Assert: The instance should be of the expected class
    assert isinstance(calculation_instance, expected_class), (
        f"Expected instance of {expected_class.__name__}, "
        f"got {type(calculation_instance).__name__}"
    )


