TOKEN="ABCDEFGHIJKLMNOPQRSTUV"

"""
Utility functions for the code-to-docs demo.

This module contains helper functions that complement the main calculator module.
"""

from typing import List, Optional


def format_number(num: float, decimals: int = 2) -> str:
    """
    Format a number to a specific number of decimal places.
    
    Args:
        num (float): The number to format
        decimals (int, optional): Number of decimal places. Defaults to 2.
        
    Returns:
        str: The formatted number as a string
        
    Example:
        >>> format_number(3.14159, 2)
        '3.14'
    """
    return f"{num:.{decimals}f}"


def is_even(number: int) -> bool:
    """
    Check if a number is even.
    
    Args:
        number (int): The number to check
        
    Returns:
        bool: True if the number is even, False otherwise
        
    Example:
        >>> is_even(4)
        True
        >>> is_even(3)
        False
    """
    return number % 2 == 0


def find_max(numbers: List[float]) -> Optional[float]:
    """
    Find the maximum value in a list of numbers.
    
    Args:
        numbers (List[float]): A list of numbers
        
    Returns:
        Optional[float]: The maximum value, or None if the list is empty
        
    Example:
        >>> find_max([1, 3, 2, 5, 4])
        5.0
        >>> find_max([])
        None
    """
    if not numbers:
        return None
    return max(numbers)
