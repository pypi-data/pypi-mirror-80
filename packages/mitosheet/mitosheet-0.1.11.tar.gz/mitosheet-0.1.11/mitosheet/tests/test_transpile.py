#!/usr/bin/env python
# coding: utf-8

# Copyright (c) Mito.
# Distributed under the terms of the Modified BSD License.

import pytest
import pandas as pd

from ..transpile import transpile
from ..utils import empty_column_python_code


def test_transpile_single_column():
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
    code = transpile(
        column_python_code,
        column_evaluation_graph
    )

    assert code == 'df[\'C\'] = df[\'A\']'


def test_transpile_multiple_columns_no_relationship():
    column_python_code = {
        'A': empty_column_python_code(),
        'B': {
            'column_name_change': None,
            'column_type_change': None,
            'column_value_changes': {},
            'column_formula_changes': 'df[\'B\'] = df[\'A\']'
        },
        'C': {
            'column_name_change': None,
            'column_type_change': None,
            'column_value_changes': {},
            'column_formula_changes': 'df[\'C\'] = df[\'A\']'
        }
    }
    column_evaluation_graph = {'A': set(['B', 'C']), 'B': set([]), 'C': set([])}
    
    # Actually evaluate
    code = transpile(
        column_python_code,
        column_evaluation_graph
    )

    assert (code == 'df[\'C\'] = df[\'A\']\n\ndf[\'B\'] = df[\'A\']' or \
            code == 'df[\'B\'] = df[\'A\']\n\ndf[\'C\'] = df[\'A\']')


def test_transpile_multiple_columns_linear():
    column_python_code = {
        'A': empty_column_python_code(),
        'B': {
            'column_name_change': None,
            'column_type_change': None,
            'column_value_changes': {},
            'column_formula_changes': 'df[\'B\'] = df[\'A\']'
        },
        'C': {
            'column_name_change': None,
            'column_type_change': None,
            'column_value_changes': {},
            'column_formula_changes': 'df[\'C\'] = df[\'B\']'
        }
    }
    column_evaluation_graph = {'A': set(['B']), 'B': set(['C']), 'C': set([])}
    
    # Actually evaluate
    code = transpile(
        column_python_code,
        column_evaluation_graph
    )

    assert (code == 'df[\'B\'] = df[\'A\']\n\ndf[\'C\'] = df[\'B\']')