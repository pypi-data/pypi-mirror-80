#!/usr/bin/env python
# coding: utf-8

# Copyright (c) Mito.
# Distributed under the terms of the Modified BSD License.

"""
Contains all functions that can be used in a sheet. 

All functions should describe their behavior in a doc string.

NOTE: This file is alphabetical order!
"""
from typing import List, Union
from functools import reduce
import pandas as pd


def AVG(*argv: List[Union[pd.Series, int, float]]) -> pd.Series:
    """
    Takes any number of pd.Series, integers, or floating point numbers
    and returns their average. 

    If there is _any_ series in the given arguments, will return a series.
    Otherwise, will return a single number representing the average. 

    Examples:
    - AVG(pd.Series(data=[3]), 4) = pd.Series(data=[3.5])
    - AVG(3, 4) = 3.5.

    TODO: errors when given a string?
    TODO: errors when there is an overflow?
    """
    return SUM(*argv) / len(argv)


def CLEAN(series: pd.Series) -> pd.Series:
    """
    Takes a Python series objects containing strings, 
    and returns a series objects with line breaks and other 
    non-printable characters removed.

    Examples:
    - CLEAN(pd.Series(data=["ABC\nABC\f"])) = pd.Series(data=["ABCABC"]))
    - CLEAN(pd.Series(data=["data\037\x1fdirty"])) = pd.Series(data=["datadirty"]))
    """
    return series.apply(lambda x:''.join([i if 32 < ord(i) < 126 else "" for i in x]))


def CONCATENATE(*argv: List[Union[pd.Series, str]]) -> pd.Series:
    """
    Takes any number of pd.Series and strings, and returns the result
    of concatenating these strings together. 

    If there is _any_ series in the given arguments, will return a series.
    Otherwise, will return a single string representing the concatenation. 

    Examples:
    - CONCATENATE(pd.Series(data=['h']), 'i') = pd.Series(data=['hi']), 
    - CONCATENATE('h', 'i') ='hi' 
    """

    def as_string(x):
        if isinstance(x, pd.Series):
            return x.astype('str')
        else:
            return str(x)

    return as_string(reduce((lambda x, y: as_string(x) + as_string(y)), argv))


def FIND(series: pd.Series, substring: str) -> pd.Series:
    """
    Takes a Python series object and a substring to search for.

    Returns a series objects that contains the left-most index
    this substring is found in each Series element. 1-indexed.

    Returns 0 if the substring cannot be found.

    Examples:
    - FIND(pd.Series(data=["Apple"]), "xxx") = 0
    - FIND(pd.Series(data=["Apple"]), "A") = 1
    - FIND(pd.Series(data=["Apple"]), "pp") = 2
    """
    # NOTE: we do not cast _back_ to the original type, as 
    # we always want to return numbers!

    if substring is None:
        raise Exception(f'Must pass a substring to FIND, {substring} is not valid.')
    str_series = series.astype('str')
    # We add 1 to match Excel's behavior
    return str_series.str.find(substring) + 1


def LEFT(series: pd.Series, num_chars: int = 1) -> pd.Series:
    """
    Takes a Python series object and an integer number of characters.

    Returns a series objects that extracts the number of characters from the left 
    side of the string.

    Examples:
    - LEFT("Apple", -1) results in an error (cannot be negative)
    - LEFT("Apple", 0) = ""
    - LEFT("Apple", 3) = "App"
    - LEFT("Apple", 100) = "Apple"

    NOTE: This function performs strangely on mixed data types!
    NOTE: this does not handle date objects well!
    TODO: note this function has weird behavior on booleans, as well
    as mixed data type series. See tests for examples...
    """
    series_dtype = series.dtype
    str_series = series.astype('str')
    if (num_chars < 0):
        raise ValueError(f'num_chars must be > 0, cannot be {num_chars}')
    elif (num_chars == 0):
        return str_series.str[0:0].astype(series_dtype)
    return str_series.str[0:num_chars].astype(series_dtype)


def LEN(series: pd.Series) -> pd.Series:
    """
    Takes a Python series objects, and returns a series object 
    with the length of the strings (or other objects as strings).

    Examples:
    - LEN(pd.Series(data=["nate"])) = pd.Series(data=[4]))
    - LEN(pd.Series(data=["aBc123"])) = pd.Series(data=[6]))
    - LEN(pd.Series(data=[123])) = pd.Series(data=[3]))

    TODO: Determine how to handle dates
    """
    return series.astype('str').str.len()


def LOWER(series: pd.Series) -> pd.Series:
    """
    Takes a Python series objects containing strings, and returns a series 
    object with the strings totally lower-case.

    Examples:
    - LOWER(pd.Series(data=["ABC"])) = pd.Series(data=["abc"]))
    - LOWER(pd.Series(data=["aBc 123"])) = pd.Series(data=["abc 123"]))

    TODO: Errors if the given series is not strings.
    """
    series_dtype = series.dtype
    str_series = series.astype('str')
    return str_series.str.lower().astype(series_dtype)


def MID(series: pd.Series, start_loc: int, num_chars: int) -> pd.Series:
    """
    Takes a Python series object, a starting location, and a number 
    of chars to return. It returns a series object that extracts the 
    given number of characters from the middle of the supplied series. 

    Examples:
    - MID(pd.Series(data=["apple"]), 2, 3) = pd.Series(data=["ppl"]))
    - MID(pd.Series(data=["xxYxx"]), 1, 10) = pd.Series(data=["xxYxx"]))
    - MID(pd.Series(data=[123]), 2, 1) = pd.Series(data=[2]))
    """
    series_dtype = series.dtype
    return series.astype('str').str.slice(start=(start_loc - 1), stop=(start_loc + num_chars - 1)).astype(series_dtype)


def MULTIPLY(*argv: List[Union[pd.Series, int, float]]) -> pd.Series:
    """
    Takes any number of pd.Series, integers, or floating point numbers
    and returns the result of muliplying them together. 

    If there is _any_ series in the given arguments, will return a series.
    Otherwise, will return a single number representing the product. 

    Examples:
    - MULTIPLY(pd.Series(data=[3]), 4) = pd.Series(data=[12])
    - MULTIPLY(3, 4) = 12.

    TODO: errors when given a string?
    TODO: errors when there is an overflow?
    """
    return reduce((lambda x, y: x * y), argv) 


def PROPER(series: pd.Series) -> pd.Series:
    """
    Takes a Python series objects containing strings, and returns a 
    series objects with strings in proper case. 

    Examples:
    - PROPER(pd.Series(data=["nate rush"])) = pd.Series(data=["Nate Rush"]))
    - PROPER(pd.Series(data=["aBc 123"])) = pd.Series(data=["Abc 123"]))
    """
    return series.astype('str').str.title()

def RIGHT(series: pd.Series, num_chars: int = 1) -> pd.Series:
    """
    Takes a Python series object and an integer number of characters.

    Returns a series objects that extracts the number of characters from the right 
    side of the string.

    Examples:
    - RIGHT("Apple", -1) results in an error (cannot be negative)
    - RIGHT("Apple", 0) = ""
    - RIGHT("Apple", 3) = "ple"
    - RIGHT("Apple", 100) = "Apple"

    NOTE: This function performs strangely on mixed data types!
    NOTE: this does not handle date objects well!
    TODO: note this function has weird behavior on booleans, as well
    as mixed data type series. See tests for examples...
    """
    series_dtype = series.dtype
    str_series = series.astype('str')
    if (num_chars < 0):
        raise ValueError(f'num_chars must be > 0, cannot be {num_chars}')
    elif (num_chars == 0):
        return str_series.str[0:0].astype(series_dtype)
    return str_series.str[-(num_chars):].astype(series_dtype)


def SUBSTITUTE(series: pd.Series, old_text: str, new_text: str, instance: int = -1):
    """
    Takes a Python series object, a string of old text to replace with a string of new text, and 
    optionally an instance number of the old text to replace. 
    
    Returns a series object with all occurances of the old text 
    replaced with the new text, the first instance times it appears. 
    
    If instance is not given, replaces all occurences.

    Examples:
    =SUBSTITUTE(pd.Series('Apple'),'p','x') = pd.Series('Axxle')
    =SUBSTITUTE(pd.Series('Apple'),'p','x', 1) = pd.Series('Axple')
    =SUBSTITUTE(pd.Series('Apple'),'d','x') = pd.Series('Apple')
    """

    series_dtype = series.dtype
    return series.astype('str').str.replace(old_text, new_text, n=instance).astype(series_dtype)


def SUM(*argv: List[Union[pd.Series, int, float]]) -> pd.Series:
    """
    Takes any number of pd.Series, integers, or floating point numbers
    and returns the result of adding them together. 

    If there is _any_ series in the given arguments, will return a series.
    Otherwise, will return a single number representing the sum. 

    Examples:
    - SUM(pd.Series(data=[3]), 4) = pd.Series(data=[7])
    - SUM(3, 4) = 7.

    TODO: errors when given a string?
    TODO: errors when there is an overflow?
    """
    return reduce((lambda x, y: x + y), argv) 


def TRIM(series: pd.Series) -> pd.Series:
    """
    Takes a Python series objects containing strings, and returns a 
    series object with the leading and trailing whitespace removed.

    Examples:
    - LEN(pd.Series(data=["   nate"])) = pd.Series(data=["nate"]))
    - LEN(pd.Series(data=["  aBc  123  "])) = pd.Series(data=["aBc  123"]))
    - LEN(pd.Series(data=[123])) = pd.Series(data=[123]))

    TODO: Only operate on strings
    """
    def trim_string(x):
        if isinstance(x, str):
            return x.strip()
        else:
            return x
    
    return series.apply(lambda x: trim_string(x))


def UPPER(series: pd.Series) -> pd.Series:
    """
    Takes a Python series objects containing strings, and returns a series 
    object with the strings totally upper-case.

    Examples:
    - UPPER(pd.Series(data=["abc"])) = pd.Series(data=["ABC"]))
    - UPPER(pd.Series(data=["aBc 123"])) = pd.Series(data=["ABC 123"]))

    NOTE: performs strangely in the case of a mixed
    data type series. See tests.
    """
    series_dtype = series.dtype
    str_series = series.astype('str')
    return str_series.str.upper().astype(series_dtype)


# TODO: we should see if we can list these automatically!
FUNCTIONS = {
    'AVG': AVG,
    'CLEAN': CLEAN,
    'CONCATENATE': CONCATENATE,
    'FIND': FIND,
    'LEFT': LEFT,
    'LEN': LEN,
    'LOWER': LOWER,
    'MID': MID,
    'MULTIPLY': MULTIPLY,
    'PROPER': PROPER,
    'RIGHT': RIGHT,
    'SUBSTITUTE': SUBSTITUTE,
    'SUM': SUM,
    'TRIM': TRIM,
    'UPPER': UPPER,
}