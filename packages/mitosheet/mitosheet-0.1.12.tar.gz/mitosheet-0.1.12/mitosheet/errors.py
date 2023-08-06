#!/usr/bin/env python
# coding: utf-8

# Copyright (c) Mito.
# Distributed under the terms of the Modified BSD License.

"""
Exports an error box that can be used to pass the errors
we need. 

Note: errors are the Pythonic way of handling this sort of things,
but we should avoid going overboard on new classes. 

See here: https://stackoverflow.com/questions/16138232/is-it-a-good-practice-to-use-try-except-else-in-python
"""

# A mapping from error type -> format strings on how to fix those errors
TO_FIX_ERROR = {
    'param_type_error': 'TODO',
    'execution_error': 'TODO',
    'unsupported_function_error': 'TODO',
    'invalid_formula_error': 'TODO',
    'divide_by_zero_error': 'TODO',
    'missing_key_error': 'TODO',
    'execution_error': 'TODO',
    'no_undo_error': 'TODO',
    'no_redo_error': 'TODO',
    'circular_reference_error': 'TODO',
    'column_exists_error': 'Sorry, a column already exists with the name {column_header}. Please choose a different name.', 
    'wrong_column_metatype_error': 'TODO',
    'no_column_error': 'TODO'
} 


class CreationError(Exception):
    """
    An error that occurs during a mito.sheet call, on creation
    of the mito widget. 
    """
    def __init__(self, type_, params=None):
        """
        Creates a creation error. 

        type_: a string that is the error type. 
        params: a dictonary of information about the error used to
        construct good error messaging
        """
        if params is None:
            params = dict()
        self.type_ = type_ # we have an _ to avoid overwriting the build in type
        self.to_fix = TO_FIX_ERROR[type_].format(**params)

class EditError(Exception):
    """
    An error that occurs during the processing of an editing event.
    """
    def __init__(self, type_, params=None):
        """
        Creates a creation error. 

        type_: a string that is the error type. 
        params: a dictonary of information about the error used to
        construct good error messaging
        """
        if params is None:
            params = dict()
        self.type_ = type_ # we have an _ to avoid overwriting the build in type
        self.to_fix = TO_FIX_ERROR[type_].format(**params)


# TODO: might want to consider making an error creation function
# for each of these different types; that way, we can easily
# see what parameters are needed rather than being through params...
