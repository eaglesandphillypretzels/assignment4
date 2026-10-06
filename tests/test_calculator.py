
# tests/test_calculator.py

"""
This test module contains unit tests for the 'app/calculator.py' module.
Each test demonstrates good testing practices using the Arrange-Act-Assert (AAA) pattern.
"""

import pytest
from io import StringIO

# Import the functions to be tested
from app.calculator import display_help, display_history, calculator

# -----------------------------------------------------------------------------------
# Parameterized Tests for Arithmetic Operations
# -----------------------------------------------------------------------------------

@pytest.mark.parametrize(
    "operation, num1, num2, expected_output",
    [
        ("add", 10, 5, "Result: AddCalculation: 10.0 Add 5.0 = 15.0"),
        ("subtract", 20, 5, "Result: SubtractCalculation: 20.0 Subtract 5.0 = 15.0"),
        ("multiply", 7, 8, "Result: MultiplyCalculation: 7.0 Multiply 8.0 = 56.0"),
        ("divide", 20, 4, "Result: DivideCalculation: 20.0 Divide 4.0 = 5.0"),
        ("power", 2, 3, "Result: PowerCalculation: 2.0 Power 3.0 = 8.0"),
        ("modulus", 10, 3, "Result: ModulusCalculation: 10.0 Modulus 3.0 = 1.0"),
    ],
    ids=["add", "subtract", "multiply", "divide", "power", "modulus"]
)
def test_calculator_arithmetic_operations(monkeypatch, capsys, operation, num1, num2, expected_output):
    """
    Parameterized test for all basic arithmetic operations including power and modulus.
    """
    # Arrange
    user_input = f"{operation} {num1} {num2}\nexit\n"
    monkeypatch.setattr('sys.stdin', StringIO(user_input))

    # Act
    with pytest.raises(SystemExit):
        calculator()

    # Assert
    captured = capsys.readouterr()
    assert expected_output in captured.out


# -----------------------------------------------------------------------------------
# Parameterized Tests for Zero Division/Modulus Errors
# -----------------------------------------------------------------------------------

@pytest.mark.parametrize(
    "operation, expected_error",
    [
        ("divide", "Cannot divide by zero."),
        ("modulus", "Modulus by zero is not allowed."),
    ],
    ids=["divide_by_zero", "modulus_by_zero"]
)
def test_calculator_zero_division_errors(monkeypatch, capsys, operation, expected_error):
    """
    Parameterized test for handling division and modulus by zero.
    """
    # Arrange
    user_input = f"{operation} 10 0\nexit\n"
    monkeypatch.setattr('sys.stdin', StringIO(user_input))

    # Act
    with pytest.raises(SystemExit):
        calculator()

    # Assert
    captured = capsys.readouterr()
    assert expected_error in captured.out


# -----------------------------------------------------------------------------------
# Parameterized Tests for Invalid Inputs
# -----------------------------------------------------------------------------------

@pytest.mark.parametrize(
    "invalid_input",
    [
        "invalid input",
        "add 5",
        "subtract",
        "add ten five"
    ],
    ids=["wrong_format_1", "missing_num2", "missing_nums", "non_numeric"]
)
def test_calculator_invalid_inputs(monkeypatch, capsys, invalid_input):
    """
    Parameterized test for handling various invalid input formats and non-numeric strings.
    """
    # Arrange
    user_input = f"{invalid_input}\nexit\n"
    monkeypatch.setattr('sys.stdin', StringIO(user_input))

    # Act
    with pytest.raises(SystemExit):
        calculator()

    # Assert
    captured = capsys.readouterr()
    # Check for either the format error or the float conversion error depending on the input
    assert ("Invalid input. Please follow the format: <operation> <num1> <num2>" in captured.out or
            "Invalid input. Please ensure numbers are valid." in captured.out or
            "could not convert string to float" in captured.out)
    assert "Type 'help' for more information." in captured.out


# -----------------------------------------------------------------------------------
# Parameterized Tests for Unsupported Operations
# -----------------------------------------------------------------------------------

@pytest.mark.parametrize(
    "unsupported_op",
    ["sqrt", "log", "foo"],
    ids=["sqrt", "log", "foo"]
)
def test_calculator_unsupported_operations(monkeypatch, capsys, unsupported_op):
    """
    Parameterized test for handling unsupported operations.
    """
    # Arrange
    user_input = f"{unsupported_op} 2 3\nexit\n"
    monkeypatch.setattr('sys.stdin', StringIO(user_input))

    # Act
    with pytest.raises(SystemExit):
        calculator()

    # Assert
    captured = capsys.readouterr()
    assert f"Unsupported calculation type: '{unsupported_op}'." in captured.out
    assert "Type 'help' to see the list of supported operations." in captured.out


# -----------------------------------------------------------------------------------
# Parameterized Tests for Display History
# -----------------------------------------------------------------------------------

@pytest.mark.parametrize(
    "history, expected_output",
    [
        ([], "No calculations performed yet."),
        (
            [
                "AddCalculation: 10.0 Add 5.0 = 15.0",
                "SubtractCalculation: 20.0 Subtract 3.0 = 17.0"
            ],
            "Calculation History:\n1. AddCalculation: 10.0 Add 5.0 = 15.0\n2. SubtractCalculation: 20.0 Subtract 3.0 = 17.0"
        )
    ],
    ids=["empty_history", "populated_history"]
)
def test_display_history(capsys, history, expected_output):
    """
    Parameterized test for display_history function (empty and populated states).
    """
    # Act
    display_history(history)

    # Assert
    captured = capsys.readouterr()
    assert captured.out.strip() == expected_output.strip()


# -----------------------------------------------------------------------------------
# Standard Tests (Kept separate for clarity due to unique control flows)
# -----------------------------------------------------------------------------------

def test_display_help(capsys):
    """
    Test the display_help function. 
    Note: Updated expected output to include power and modulus to prevent assertion errors.
    """
    # Act
    display_help()

    # Assert
    captured = capsys.readouterr()
    expected_output = """
Calculator REPL Help
--------------------
Usage:
    <operation> <number1> <number2>
    - Perform a calculation with the specified operation and two numbers.
    - Supported operations:
        add       : Adds two numbers.
        subtract  : Subtracts the second number from the first.
        multiply  : Multiplies two numbers.
        divide    : Divides the first number by the second.
        power     : Raises the first number to the power of the second.
        modulus   : Returns the remainder of the division of the first by the second.

Special Commands:
    help      : Display this help message.
    history   : Show the history of calculations.
    exit      : Exit the calculator.

Examples:
    add 10 5
    subtract 15.5 3.2
    multiply 7 8
    divide 20 4
    power 2 3
    modulus 10 3
"""
    assert captured.out.strip() == expected_output.strip()

def test_calculator_exit(monkeypatch, capsys):
    """Test the calculator function's ability to handle the 'exit' command."""
    # Arrange
    user_input = 'exit\n'
    monkeypatch.setattr('sys.stdin', StringIO(user_input))

    # Act
    with pytest.raises(SystemExit) as exc_info:
        calculator()

    # Assert
    captured = capsys.readouterr()
    assert "Exiting calculator. Goodbye!" in captured.out
    assert exc_info.type == SystemExit
    assert exc_info.value.code == 0

def test_calculator_help_command(monkeypatch, capsys):
    """Test the calculator function's ability to handle the 'help' command."""
    # Arrange
    user_input = 'help\nexit\n'
    monkeypatch.setattr('sys.stdin', StringIO(user_input))

    # Act
    with pytest.raises(SystemExit):
        calculator()

    # Assert
    captured = capsys.readouterr()
    assert "Calculator REPL Help" in captured.out
    assert "Exiting calculator. Goodbye!" in captured.out

def test_calculator_history(monkeypatch, capsys):
    """Test the calculator's ability to display calculation history."""
    # Arrange
    user_input = 'add 10 5\nsubtract 20 3\nhistory\nexit\n'
    monkeypatch.setattr('sys.stdin', StringIO(user_input))

    # Act
    with pytest.raises(SystemExit):
        calculator()

    # Assert
    captured = capsys.readouterr()
    assert "Result: AddCalculation: 10.0 Add 5.0 = 15.0" in captured.out
    assert "Result: SubtractCalculation: 20.0 Subtract 3.0 = 17.0" in captured.out
    assert "Calculation History:" in captured.out
    assert "1. AddCalculation: 10.0 Add 5.0 = 15.0" in captured.out
    assert "2. SubtractCalculation: 20.0 Subtract 3.0 = 17.0" in captured.out

def test_calculator_keyboard_interrupt(monkeypatch, capsys):
    """Test the calculator's handling of KeyboardInterrupt (Ctrl+C)."""
    # Arrange
    def mock_input(prompt):
        raise KeyboardInterrupt()
    monkeypatch.setattr('builtins.input', mock_input)

    # Act
    with pytest.raises(SystemExit) as exc_info:
        calculator()

    # Assert
    captured = capsys.readouterr()
    assert "\nKeyboard interrupt detected. Exiting calculator. Goodbye!" in captured.out
    assert exc_info.value.code == 0

def test_calculator_eof_error(monkeypatch, capsys):
    """Test the calculator's handling of EOFError (Ctrl+D)."""
    # Arrange
    def mock_input(prompt):
        raise EOFError()
    monkeypatch.setattr('builtins.input', mock_input)

    # Act
    with pytest.raises(SystemExit) as exc_info:
        calculator()

    # Assert
    captured = capsys.readouterr()
    assert "\nEOF detected. Exiting calculator. Goodbye!" in captured.out
    assert exc_info.value.code == 0

def test_calculator_unexpected_exception(monkeypatch, capsys):
    """Test the calculator's handling of unexpected exceptions during calculation execution."""
    # Arrange
    class MockCalculation:
        def execute(self):
            raise Exception("Mock exception during execution")
        def __str__(self):
            return "MockCalculation"

    def mock_create_calculation(operation, a, b):
        return MockCalculation()

    monkeypatch.setattr('app.calculation.CalculationFactory.create_calculation', mock_create_calculation)
    user_input = 'add 10 5\nexit\n'
    monkeypatch.setattr('sys.stdin', StringIO(user_input))

    # Act
    with pytest.raises(SystemExit):
        calculator()

    # Assert
    captured = capsys.readouterr()
    assert "An error occurred during calculation: Mock exception during execution" in captured.out
    assert "Please try again." in captured.out