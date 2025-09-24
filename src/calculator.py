"""
A simple calculator module for demonstration purposes.

This module contains basic mathematical operations to showcase
how docstrings can be automatically converted to documentation.
"""


def add(a: float, b: float) -> float:
    """
    Add two numbers together.
    
    Args:
        a (float): The first number
        b (float): The second number
        
    Returns:
        float: The sum of a and b
        
    Example:
        >>> add(2, 3)
        5.0
    """
    return a + b


def multiply(x: float, y: float) -> float:
    """
    Multiply two numbers.
    
    Args:
        x (float): The first number
        y (float): The second number
        
    Returns:
        float: The product of x and y
        
    Example:
        >>> multiply(4, 5)
        20.0
    """
    return x * y


def divide(dividend: float, divisor: float) -> float:
    """
    Divide one number by another.
    
    Args:
        dividend (float): The number to be divided
        divisor (float): The number to divide by
        
    Returns:
        float: The result of dividend / divisor
        
    Raises:
        ValueError: If divisor is zero
        
    Example:
        >>> divide(10, 2)
        5.0
    """
    if divisor == 0:
        raise ValueError("Cannot divide by zero")
    return dividend / divisor


class Calculator:
    """
    A simple calculator class.
    
    This class provides basic arithmetic operations and maintains
    a history of calculations.
    """
    
    def __init__(self):
        """Initialize a new Calculator instance."""
        self.history = []
    
    def calculate(self, operation: str, a: float, b: float) -> float:
        """
        Perform a calculation and store it in history.
        
        Args:
            operation (str): The operation to perform ('add', 'multiply', 'divide')
            a (float): The first operand
            b (float): The second operand
            
        Returns:
            float: The result of the calculation
            
        Raises:
            ValueError: If operation is not supported
            
        Example:
            >>> calc = Calculator()
            >>> calc.calculate('add', 2, 3)
            5.0
        """
        if operation == 'add':
            result = add(a, b)
        elif operation == 'multiply':
            result = multiply(a, b)
        elif operation == 'divide':
            result = divide(a, b)
        else:
            raise ValueError(f"Unsupported operation: {operation}")
        
        self.history.append(f"{operation}({a}, {b}) = {result}")
        return result
    
    def get_history(self) -> list:
        """
        Get the calculation history.
        
        Returns:
            list: A list of calculation strings
        """
        return self.history.copy()