#!/usr/bin/env python
# coding: utf-8

# Copyright (c) Mito.
# Distributed under the terms of the Modified BSD License.

"""
Exports the evaluate function, which takes a list of edit events
as well as the original dataframe, and returns the current state 
of the sheet as a dataframe
"""
import re

from .errors import EditError

def parse_formula(formula, address):
    """
    Returns a representation of the formula that is easy to handle.

    Specifically, this function returns the triple:
    (python_code, functions, dependencies).

    python_code : a string of Python code that executes
    this formula.
    functions : a set of a strings (function names) that 
    are called
    dependencies : a set of columns this formula references
    """

    # We remove the leading =, as we don't need it
    if not formula.startswith('='):
        raise EditError('invalid_formula_error')
    formula = formula[1:]

    functions = set()
    dependencies = set()
    def replace(match):
        """
        Each word match can be:
            1. A constant.
                - A number. Thus, all characters must be digits
                - A string. Must be surrounded by single or double quotes.
                    TODO: support strings with _no_ spaces
                - A boolean. True or False only.
            2. A function call. 
                - This MUST be followed by a '('
            3. A column_reference
                - Any word that isn't any of the above!
        """
        text = match.group()
        start = match.start()
        end = match.end() # this is +1 after the last char of the string

        print(text)

        # CONSTANTS

        # Number
        if text.isdigit():
            return text
        # String (check it's in quotes)
        if start - 1 >= 0 and (formula[start - 1] == '\"' or formula[start - 1] == '\'') \
            and end < len(formula) and (formula[end] == '\"' or formula[end] == '\''):
            return text
        # Boolean
        if text == 'True' or text == 'False':
            return text

        # Function
        if end < len(formula) and formula[end] == '(':
            # TODO: log formula
            functions.add(text)
            return text

        # Finially, columns
        dependencies.add(text)
        return f'df[\'{text}\']'
    
    # We match all words in formula, and send them through the replace function.
    # See documentation here: https://docs.python.org/3/library/re.html#re.sub
    formula = re.sub('\w+', replace, formula)
    
    # Finially, prepend the address to set the dataframe
    formula = f'df[\'{address}\'] = {formula}'

    return formula, functions, dependencies

def evaluate(
        edit_event_list,
        widget_state_container
    ):
    """
    Takes the most recent edit (assumes all other events have been processed),
    and updates the widget_state_container with that edit.
    """

    # For now, we just check the most recent edit event
    last_edit = edit_event_list[-1]

    if last_edit['event'] == 'edit_event':
        widget_state_container.handle_edit_event(last_edit)