# calculator.py

A simple calculator module for demonstration purposes.

This module contains basic mathematical operations to showcase
how docstrings can be automatically converted to documentation.

---

## Functions

### add
```python
add(a: float, b: float) -> float
```

Add two numbers together.


**Arguments:**

- `a (float): The first number`
- `b (float): The second number`


**Returns:**

float: The sum of a and b


**Example:**

```python
>>> add(2, 3)
```
5.0

---

### multiply
```python
multiply(x: float, y: float) -> float
```

Multiply two numbers.


**Arguments:**

- `x (float): The first number`
- `y (float): The second number`


**Returns:**

float: The product of x and y


**Example:**

```python
>>> multiply(4, 5)
```
20.0

---

### divide
```python
divide(dividend: float, divisor: float) -> float
```

Divide one number by another.


**Arguments:**

- `dividend (float): The number to be divided`
- `divisor (float): The number to divide by`


**Returns:**

float: The result of dividend / divisor


**Raises:**

ValueError: If divisor is zero


**Example:**

```python
>>> divide(10, 2)
```
5.0

---

### calculate
```python
calculate(self, operation: str, a: float, b: float) -> float
```

Perform a calculation and store it in history.


**Arguments:**

- `operation (str): The operation to perform ('add', 'multiply', 'divide')`
- `a (float): The first operand`
- `b (float): The second operand`


**Returns:**

float: The result of the calculation


**Raises:**

ValueError: If operation is not supported


**Example:**

```python
>>> calc = Calculator()
```
```python
>>> calc.calculate('add', 2, 3)
```
5.0

---

### get_history
```python
get_history(self) -> list
```

Get the calculation history.


**Returns:**

list: A list of calculation strings

---

## Classes

### Calculator

A simple calculator class.

This class provides basic arithmetic operations and maintains
a history of calculations.


#### Methods

##### calculate
```python
calculate(self, operation: str, a: float, b: float) -> float
```

Perform a calculation and store it in history.


**Arguments:**

- `operation (str): The operation to perform ('add', 'multiply', 'divide')`
- `a (float): The first operand`
- `b (float): The second operand`


**Returns:**

float: The result of the calculation


**Raises:**

ValueError: If operation is not supported


**Example:**

```python
>>> calc = Calculator()
```
```python
>>> calc.calculate('add', 2, 3)
```
5.0


##### get_history
```python
get_history(self) -> list
```

Get the calculation history.


**Returns:**

list: A list of calculation strings


---
