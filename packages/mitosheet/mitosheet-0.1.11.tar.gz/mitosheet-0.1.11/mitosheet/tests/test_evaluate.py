#!/usr/bin/env python
# coding: utf-8

# Copyright (c) Mito.
# Distributed under the terms of the Modified BSD License.

from copy import deepcopy

import pytest
import pandas as pd

from ..evaluate import evaluate
from ..utils import empty_column_python_code
from ..errors import EditError

EDIT_EVENT_CELL_EDIT = {
    'event': 'edit_event',
    'type': 'cell_edit',
    'id': '123',
    'timestamp': '456',
    'address': 'C',
    'old_formula': '=A',
    'new_formula': '=B',
}

EDIT_EVENT_ADD_COLUMN = {
    'event': 'edit_event',
    'type': 'add_column',
    'id': '123',
    'timestamp': '456',
    'column_header': 'C'
}


def test_evaluate_cell_edit_event():
    d = {'A': [1], 'B': [2], 'C': [1]}
    df = pd.DataFrame(data=d)

    edit_event_list = [EDIT_EVENT_CELL_EDIT]
    original_dataframes = [df]
    column_metatype = {'A': 'values', 'B': 'values', 'C': 'formula'}
    column_spreadsheet_code = {'A': None, 'B': None, 'C': '=A'}
    column_python_code = {
        'A': empty_column_python_code(),
        'B': empty_column_python_code(),
        'C': {
            'column_name_change': None,
            'column_type_change': None,
            'column_value_changes': {},
            'column_formula_changes': 'df[\'C\'] = df[\'A\']'
        }
    }
    column_evaluation_graph = {'A': set(['C']), 'B': set([]), 'C': set([])}
    
    # Actually evaluate
    evaluate(
        edit_event_list,
        original_dataframes,
        column_metatype,
        column_spreadsheet_code,
        column_python_code,
        column_evaluation_graph
    )

    # Check all the intermediate values have been updated correctly
    assert column_metatype == {'A': 'values', 'B': 'values', 'C': 'formula'}
    assert column_spreadsheet_code == {'A': None, 'B': None, 'C': '=B'}
    assert column_evaluation_graph == {'A': set([]), 'B': set(['C']), 'C': set([])}
    assert column_python_code == {
        'A': empty_column_python_code(),
        'B': empty_column_python_code(),
        'C': {
            'column_name_change': None,
            'column_type_change': None,
            'column_value_changes': {},
            'column_formula_changes': 'df[\'C\'] = df[\'B\']'
        }
    }
    # Finially, check that the dataframe has been updated correctly
    assert original_dataframes[0].equals(pd.DataFrame(data={'A': [1], 'B': [2], 'C': [2]}))


def test_evaluate_add_column_event():
    d = {'A': [1], 'B': [2]}
    df = pd.DataFrame(data=d)

    edit_event_list = [EDIT_EVENT_ADD_COLUMN]
    original_dataframes = [df]
    column_metatype = {'A': 'values', 'B': 'values'}
    column_spreadsheet_code = {'A': None, 'B': None}
    column_python_code = {
        'A': empty_column_python_code(),
        'B': empty_column_python_code(),
    }
    column_evaluation_graph = {'A': set([]), 'B': set([])}
    
    # Actually evaluate
    evaluate(
        edit_event_list,
        original_dataframes,
        column_metatype,
        column_spreadsheet_code,
        column_python_code,
        column_evaluation_graph
    )

    # Check all the intermediate values have been updated correctly
    assert column_metatype == {'A': 'values', 'B': 'values', 'C': 'formula'}
    assert column_spreadsheet_code == {'A': None, 'B': None, 'C': '=0'}
    assert column_evaluation_graph == {'A': set([]), 'B': set([]), 'C': set([])}
    assert column_python_code == {
        'A': empty_column_python_code(),
        'B': empty_column_python_code(),
        'C': {
            'column_name_change': None,
            'column_type_change': None,
            'column_value_changes': {},
            'column_formula_changes': 'df[\'C\'] = 0'
        }
    }
    # Finially, check that the dataframe has been updated correctly
    assert original_dataframes[0].equals(pd.DataFrame(data={'A': [1], 'B': [2], 'C': [0]}))


def test_evaluate_add_column_change_formula():
    d = {'A': [1], 'B': [2]}
    df = pd.DataFrame(data=d)

    add_column_edit_event_list = [EDIT_EVENT_ADD_COLUMN]
    original_dataframes = [df]
    column_metatype = {'A': 'values', 'B': 'values'}
    column_spreadsheet_code = {'A': None, 'B': None}
    column_python_code = {
        'A': empty_column_python_code(),
        'B': empty_column_python_code(),
    }
    column_evaluation_graph = {'A': set([]), 'B': set([])}
    
    # Actually evaluate
    evaluate(
        add_column_edit_event_list,
        original_dataframes,
        column_metatype,
        column_spreadsheet_code,
        column_python_code,
        column_evaluation_graph
    )

    # Add the change formula column here
    add_column_edit_event_list.append({
        'event': 'edit_event',
        'type': 'cell_edit',
        'id': '123',
        'timestamp': '456',
        'address': 'C',
        'old_formula': '=0',
        'new_formula': '=A',
    })

    evaluate(
        add_column_edit_event_list,
        original_dataframes,
        column_metatype,
        column_spreadsheet_code,
        column_python_code,
        column_evaluation_graph
    )

    # Check all the intermediate values have been updated correctly
    assert column_metatype == {'A': 'values', 'B': 'values', 'C': 'formula'}
    assert column_spreadsheet_code == {'A': None, 'B': None, 'C': '=A'}
    assert column_evaluation_graph == {'A': set(['C']), 'B': set([]), 'C': set([])}
    assert column_python_code == {
        'A': empty_column_python_code(),
        'B': empty_column_python_code(),
        'C': {
            'column_name_change': None,
            'column_type_change': None,
            'column_value_changes': {},
            'column_formula_changes': 'df[\'C\'] = df[\'A\']'
        }
    }
    # Finially, check that the dataframe has been updated correctly
    assert original_dataframes[0].equals(pd.DataFrame(data={'A': [1], 'B': [2], 'C': [1]}))


def test_error_reference_non_existant_column():
    d = {'A': [1], 'B': [2], 'C': [1]}
    df = pd.DataFrame(data=d)

    edit_event_list = [{
        'event': 'edit_event',
        'type': 'cell_edit',
        'id': '123',
        'timestamp': '456',
        'address': 'C',
        'old_formula': '=A',
        'new_formula': '=D',
    }]
    original_dataframes = [df]
    column_metatype = {'A': 'values', 'B': 'values', 'C': 'formula'}
    column_spreadsheet_code = {'A': None, 'B': None, 'C': '=A'}
    column_python_code = {
        'A': empty_column_python_code(),
        'B': empty_column_python_code(),
        'C': {
            'column_name_change': None,
            'column_type_change': None,
            'column_value_changes': {},
            'column_formula_changes': 'df[\'C\'] = df[\'A\']'
        }
    }
    column_evaluation_graph = {'A': set(['C']), 'B': set([]), 'C': set([])}

    _original_dataframes = deepcopy(original_dataframes)
    _column_metatype = deepcopy(column_metatype)
    _column_spreadsheet_code = deepcopy(column_spreadsheet_code)
    _column_spreadsheet_code = deepcopy(column_spreadsheet_code)
    _column_python_code = deepcopy(column_python_code)
    _column_evaluation_graph = deepcopy(column_evaluation_graph)
    
    # Actually evaluate
    with pytest.raises(EditError) as e:
        evaluate(
            edit_event_list,
            _original_dataframes,
            _column_metatype,
            _column_spreadsheet_code,
            _column_python_code,
            _column_evaluation_graph
        )

    # Check all the intermediate values have not been updated
    assert column_metatype == _column_metatype
    assert column_spreadsheet_code == _column_spreadsheet_code
    assert column_evaluation_graph == _column_evaluation_graph
    assert column_python_code == _column_python_code
    # Finially, check that the dataframe has been updated correctly
    assert original_dataframes[0].equals(_original_dataframes[0])