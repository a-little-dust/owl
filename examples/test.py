import dotenv
print("Hello, World!")
from camel.toolkits import FunctionTool

def add(a: int, b: int) -> int:
    r"""Adds two numbers.

    Args:
        a (int): The first number to be added.
        b (int): The second number to be added.

    Returns:
        integer: The sum of the two numbers.
    """
    return a + b

# Wrap the function with FunctionTool
add_tool = FunctionTool(add)
print(add_tool.get_function_name())