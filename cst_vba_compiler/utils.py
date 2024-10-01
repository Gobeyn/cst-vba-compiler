""" 
Collection of useful functions that are used throughout the module.

author: Aaron Gobeyn
date: 01-10-2024
"""

from .writer import VbaWriter


def wrap_nonstr_in_double_quotes(value) -> str:
    """Wrap any given `value` that implements `repr` in double quotes,
    except when `value` is a string.

    :param value: Value that implements the `__repr__` dunder method.
    :type value: Any that implements `__repr__`
    """
    return value if isinstance(value, str) else VbaWriter.wrap_double_quotes(value)


def num_or_list_of_nums_to_str(nums: int | list[int]) -> str:
    """Given an integer, or a list of integers, return the integer
    or the integers separated by commas, with double quotes.
    In other words 1 -> "1" and [1,2,3] -> "1,2,3".

    :param nums: Integer or list thereof which we want to convert into the
        VBA appropriate format.
    :type nums: int | list[int]
    """
    if isinstance(nums, int):
        return wrap_nonstr_in_double_quotes(value=nums)
    else:
        string: str = ""
        for num in nums:
            string += repr(num)
            string += ","
        return VbaWriter.string_repr(text=string)
