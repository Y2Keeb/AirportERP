# ~*~*~ DA RULEZ ~*~*~

In this section, we outline the coding conventions that will be followed throughout the project. 
These conventions help maintain consistency, readability, and quality across the codebase. 


<details>  
<summary>Function and Method Docstrings:</summary>
A short description of what the function does needs to be added at the start of a function/method.

```python
def add_numbers(a, b):
    """
    Adds two numbers together and returns the result.

    Args:
        a (int): The first number to add.
        b (int): The second number to add.

    Returns:
        int: The sum of a and b.
    """
    return a + b
```
</details>
<details>  
<summary>Imports </summary>
Write imports on one line when possible to prevent typing the same line twice.

```python
from tkinter import messagebox, Menu
```
instead of 

```python
from tkinter import messagebox
from tkinter import Menu
```
</details>  
<details>
<summary>Indentation</summary>
Use 4 spaces per indentation level.

```python
def long_function_name(
        var_one, var_two, var_three,
```
</details>
<details>
<summary>Variables:</summary>
Use snake_case (lowercase with underscores)

```python
user_name = "John Doe"
email_address = "john@example.com"
```
</details>
<details>
<summary>Functions & Methods:</summary>
Use snake_case for function and method names

```python
def calculate_total_price(cart_items):
```
</details>
<details>
<summary>Classes</summary>
Use PascalCase for class names

```python
class UserProfile:
```
</details>
<details>
<summary>Buttons:</summary>
Prefix with btn_ and use descriptive names

```python
btn_submit = Button(text="Submit")
```
</details>
<details>
<summary>Labels:</summary>
Prefix with lbl_ and use descriptive names

```python
lbl_username = Label(text="Submit")
```
</details>
