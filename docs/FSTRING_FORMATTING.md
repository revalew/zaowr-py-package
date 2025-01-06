# Comprehensive F-String Formatting in Python

F-strings in Python offer versatile and powerful options for formatting strings. This guide organizes examples into meaningful sections for easy reference and copying.

## Table of Contents

1. [Numbers](#1-numbers)  
   - [Alignment](#11-alignment)  
   - [Separators](#12-separators)  
   - [Precision](#13-precision)  
   - [Exponential Notation](#14-exponential-notation)  
   - [Locale-Specific Formatting](#15-locale-specific-formatting)  
   - [Percentage](#16-percentage)  
2. [Integers](#2-integers)  
   - [Binary, Octal, Hexadecimal](#21-binary-octal-hexadecimal)  
3. [Booleans](#3-booleans)  
4. [Strings](#4-strings)  
   - [Alignment](#41-alignment)  
   - [Padding Symbols](#42-padding-symbols)
5. [Dates and Times](#5-dates-and-times)  
6. [Custom Classes](#6-custom-classes)  
   - [Using `repr` and `str`](#61-using-repr-and-str)  

## 1. **Numbers**

### 1.1 Alignment
```python
var = 123456789.123456789

print(f"{var = :>20.2f}")  # Right-aligned in a 20-character field
# var =         123456789.12

print(f"{var = :<20.2f}")  # Left-aligned in a 20-character field
# var = 123456789.12       

print(f"{var = :^20.2f}")  # Centered in a 20-character field
# var =     123456789.12     
```

</br>
</br>

### 1.2 Separators
```python
var = 123456789.123456789

print(f"{var = :_}")  # Use underscores to separate digits
# var = 123_456_789.12345679

print(f"{var = :,}")  # Use commas to separate digits
# var = 123,456,789.12345679

print(f"{var = :>20_,.2f}")  # Combined: right-aligned, underscores, and commas
# var =    123_456,789.12
```

</br>
</br>

### 1.3 Precision
```python
var = 123456789.123456789

print(f"{var = :.2f}")  # 2 decimal places
# var = 123456789.12
```

</br>
</br>

### 1.4 Exponential Notation
```python
var = 123456789.123456789

print(f"{var = :e}")  # Exponential notation (lowercase)
# var = 1.234568e+08

print(f"{var = :E}")  # Exponential notation (uppercase)
# var = 1.234568E+08
```

</br>
</br>

### 1.5 Locale-Specific Formatting
```python
var = 123456789.123456789

print(f"{var = :n}")  # Locale-specific separators (e.g., commas for English)
# var = 123,456,789.12345679
```

</br>
</br>

### 1.6 Percentage
```python
var = 123456789.123456789

print(f"{var = :.2%}")  # Percentage format with 2 decimal places
# var = 12345678912.35%

print(f"{var = :.0%}")  # Percentage format without decimal places
# var = 12345678912%
```

</br>
</br>

## 2. **Integers**

### 2.1 Binary, Octal, Hexadecimal
```python
int_var = 123456789

print(f"{int_var = :b}")  # Binary format
# int_var = 111010110111100110100010101

print(f"{int_var = :o}")  # Octal format
# int_var = 726746425

print(f"{int_var = :x}")  # Hexadecimal (lowercase)
# int_var = 75bcd15

print(f"{int_var = :X}")  # Hexadecimal (uppercase)
# int_var = 75BCD15
```

</br>
</br>

## 3. **Booleans**
```python
var_bool = True

print(f"{var_bool = }")  # Default formatting
# var_bool = True

print(f"{var_bool = :b}")  # Binary format (1 for True, 0 for False)
# var_bool = 1
```

</br>
</br>

## 4. **Strings**

### 4.1 Alignment
```python
text = "hello"

print(f"{text:_<20}")  # Left-aligned, padded with underscores
# hello_______________

print(f"{text:_>20}")  # Right-aligned, padded with underscores
# _______________hello

print(f"{text:_^20}")  # Centered, padded with underscores
# ______hello_______
```

</br>
</br>

### 4.2 Padding symbols
```python
text = "hello"

# Default padding (spaces)
print(f"{text:>20}")  # Right-aligned with spaces
#                hello

# Padding with underscores
print(f"{text:_<20}")  # Left-aligned with underscores
# hello_______________

# Padding with hyphens
print(f"{text:-^20}")  # Centered with hyphens
# -------hello--------

# Padding with asterisks
print(f"{text:*^20}")  # Centered with asterisks
# *******hello*******

# Padding with dots
print(f"{text:.>20}")  # Right-aligned with dots
# ...............hello

# Padding with hashes
print(f"{text:#<20}")  # Left-aligned with hashes
# hello###############
```

</br>
</br>

## 5. **Dates and Times**
```python
from datetime import datetime

now = datetime.now()

print(f"{now = :%Y-%m-%d %H:%M:%S}")  # Custom date-time format
# now = 2025-01-06 14:53:30
```

</br>
</br>

## 6. **Custom Classes**

### 6.1 Using `repr` and `str`
```python
class MyClass:
    def __repr__(self):
        return "repr_format"
    def __str__(self):
        return "str_format"

obj = MyClass()

print(f"{obj!r}")  # Use repr
# repr_format

print(f"{obj!s}")  # Use str
# str_format
```