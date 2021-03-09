from functools import reduce
from typing import Callable

# (1) 1) Write a normal function that accepts another function as an argument.
# Output the result of that other function in your “normal” function.


def with_logger(fn: Callable, *args: tuple):
    result = fn(*args)
    print('Result: {:-^20}'.format(result))

    return result


def add(num1: int, num2: int) -> int:
    return num1 + num2


with_logger(add, 3, 8)


# Call your “normal” function by passing a lambda function
# – which performs any operation of your choice – as an argument.

with_logger(lambda num1, num2: num1 * num2, 3, 24)

# Tweak your normal function by allowing an infinite amount of
# arguments on which your lambda function will be executed.


def multiply(num1: int, num2: int) -> int:
    return num1 * num2


with_logger(lambda *args: reduce(multiply, args, 1), 3, 24, 88, 22)

# Format the output of your “normal” function such that numbers look nice 
# and are centered in a 20 character column.

