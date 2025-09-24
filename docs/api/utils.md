# utils.py

Utility functions for the code-to-docs demo.

This module contains helper functions that complement the main calculator module.

---

## Functions

### format_number
```python
format_number(num: float, decimals: int) -> str
```

Format a number to a specific number of decimal places.


**Arguments:**

- `num (float): The number to format`
- `decimals (int, optional): Number of decimal places. Defaults to 2.`


**Returns:**

str: The formatted number as a string


**Example:**

```python
>>> format_number(3.14159, 2)
```
'3.14'

---

### is_even
```python
is_even(number: int) -> bool
```

Check if a number is even.


**Arguments:**

- `number (int): The number to check`


**Returns:**

bool: True if the number is even, False otherwise


**Example:**

```python
>>> is_even(4)
```
True
```python
>>> is_even(3)
```
False

---

### find_max
```python
find_max(numbers)
```

Find the maximum value in a list of numbers.


**Arguments:**

- `numbers (List[float]): A list of numbers`


**Returns:**

Optional[float]: The maximum value, or None if the list is empty


**Example:**

```python
>>> find_max([1, 3, 2, 5, 4])
```
5.0
```python
>>> find_max([])
```
None

---
