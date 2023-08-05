#!/usr/bin/env python
# coding: utf-8

# Copyright (c) Mito.
# Distributed under the terms of the Modified BSD License.

"""
Exports the evaluate function, which takes a list of edit events
as well as the original dataframe, and returns the current state 
of the sheet as a dataframe
"""

from .errors import EditError
from .topological_sort import topological_sort_columns, creates_circularity
from .utils import empty_column_python_code

def parse_formula(formula):
    """
    Returns a representation of the formula that is easy to handle.

    For now, the formula format we return in is a triple:
    (formula_type : string, arguments: list[column names])

    formula_type :== 'equals' | 'add' | 'zero'
    if formula_type == 'equals', arguments is a single column
    if formula_type == 'add', arguments is two columns
    if formula_type == 'zero', arguments is empty
    """

    # First, we remove all the whitespace from the string
    formula = "".join(formula.split())

    if len(formula) == len('=?'):
        if formula[0] != '=':
            raise EditError('invalid_formula_error')

        if formula[1] == '0': # zero
            return 'zero', []
        elif formula[1].isalpha():
            return 'equals', [formula[1].upper()]
        else:
            raise EditError('invalid_formula_error')

    elif (formula[0] == '=' and formula[1].isalpha() and formula[2] == '+' and formula[3].isalpha()):
        return 'add', [formula[1].upper(), formula[3].upper()]
    else:
        raise EditError('invalid_formula_error')


def get_dependencies(parsed_formula):
    """
    For a given parsed formula, returns a list of all the columns it 
    relies on.
    """
    formula_type, arguments = parsed_formula

    # TODO: change this to something that works when we implement better functions
    return arguments


def translate_parsed_formula(address, parsed_formula):
    """
    Given a parsed formula, this will translate it into 
    Python. 

    If it cannot translate, will raise an Exception - this
    should never happen if it can parse the formula.

    TODO: add a mapping from A -> column name, 
    TODO: add a mapping from A -> column type, maybe?
    """
    formula_type, arguments = parsed_formula

    if formula_type == 'zero':
        return f'df[\'{address}\'] = 0'
    elif formula_type == 'equals':
        return f'df[\'{address}\'] = df[\'{arguments[0]}\']'
    elif formula_type == 'add':
        return f'df[\'{address}\'] = df[\'{arguments[0]}\'] + df[\'{arguments[1]}\']'
    else:
        raise Exception("Error: should be able to translate any parsed function!")

def handle_edit_event(
        edit_event,
        original_dataframes, 
        column_metatype,
        column_spreadsheet_code,
        column_python_code,
        column_evaluation_graph
    ):
    if edit_event['type'] == 'cell_edit':
        address = edit_event['address']
        old_formula = edit_event['old_formula']
        new_formula = edit_event['new_formula']

        # If nothings changed, there's no work to do
        if (old_formula == new_formula):
            return

        # First, we check the column_metatype, and make sure it's a formula
        if column_metatype[address] != 'formula':
            raise EditError('wrong_column_metatype_error')

        # Then we try and parse the formula
        new_formula_parsed = parse_formula(new_formula)

        # Then, we get the list of old column dependencies and new dependencies
        # so that we can update the graph
        old_formula_parsed = parse_formula(old_formula) # Note: no error possible, as this must be valid
        old_dependencies = get_dependencies(old_formula_parsed)
        new_dependencies = get_dependencies(new_formula_parsed)

        # We also check that the formula doesn't reference any columns that 
        # don't exist
        if any(set(new_dependencies).difference(column_metatype.keys())):
            raise EditError('no_column_error')

        # Before changing any variables, we make sure this edit didn't
        # introduct any circularity
        circularity = creates_circularity(
            column_evaluation_graph, 
            address,
            old_dependencies,
            new_dependencies
        )
        if circularity:
            raise EditError('circular_reference_error')

        # Translate the column python code
        python_code = translate_parsed_formula(address, new_formula_parsed)

        # Update the variables based on this new formula
        column_spreadsheet_code[address] = new_formula
        column_python_code[address]['column_formula_changes'] = python_code

        # Update the column dependency graph
        for old_dependency in old_dependencies:
            column_evaluation_graph[old_dependency].remove(address)
        for new_dependency in new_dependencies:
            column_evaluation_graph[new_dependency].add(address)

    elif edit_event['type'] == 'add_column':
        column_header = edit_event['column_header']

        if column_header in column_metatype:
            raise EditError('column_exists_error', {'column_header': column_header})

        column_metatype[column_header] = 'formula'
        column_spreadsheet_code[column_header] = '=0'
        column_python_code[column_header] = empty_column_python_code()
        column_python_code[column_header]['column_formula_changes'] = f'df[\'{column_header}\'] = 0'
        column_evaluation_graph[column_header] = set()            
    else:
        print("Not cell edit!")

    return

def update_dataframes(
        original_dataframes, 
        column_python_code,
        column_evaluation_graph  
    ):
    """
    Updates the given dataframes with columns defined by the given
    column_python_code, in the order of a topological sort
    of the column_evaluation_graph
    """
    topological_sort = topological_sort_columns(column_evaluation_graph)

    for column in topological_sort:
        # Exec the code, where the df is the original dataframe
        # See explination here: https://www.tutorialspoint.com/exec-in-python
        exec(
            column_python_code[column]['column_formula_changes'],
            {'df': original_dataframes[0]}
        )


def evaluate(
        edit_event_list,
        original_dataframes, 
        column_metatype,
        column_spreadsheet_code,
        column_python_code,
        column_evaluation_graph  
    ):
    """
    Takes the most recent edit (assumes all other events have been processed),
    and updates the state of each variable with that edit. 
    """

    # For now, we just check the most recent edit event
    last_edit = edit_event_list[-1]

    if last_edit['event'] == 'edit_event':
        handle_edit_event(
            last_edit,
            original_dataframes, 
            column_metatype,
            column_spreadsheet_code,
            column_python_code,
            column_evaluation_graph
        )

        update_dataframes(
            original_dataframes, 
            column_python_code, 
            column_evaluation_graph
        )