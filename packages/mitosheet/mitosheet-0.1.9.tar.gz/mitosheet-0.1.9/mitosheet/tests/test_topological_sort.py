#!/usr/bin/env python
# coding: utf-8

# Copyright (c) Mito.
# Distributed under the terms of the Modified BSD License.

import pytest
import pandas as pd

from ..errors import EditError, TO_FIX_ERROR
from ..topological_sort import topological_sort_columns

def test_no_cell_relationships_no_error():
    column_evaluation_graph = {'A': set([]), 'B': set([]), 'C': set([])}
    topological_sort_columns(column_evaluation_graph)

def test_simple_linear_topological_sort():
    column_evaluation_graph = {'A': set(['B']), 'B': set(['C']), 'C': set([])}
    sort = topological_sort_columns(column_evaluation_graph)
    assert sort == ['A', 'B', 'C']

def test_simple_linear_topological_sort_options():
    column_evaluation_graph = {'A': set(['B']), 'B': set([]), 'C': set([])}
    sort = topological_sort_columns(column_evaluation_graph)
    assert (sort == ['A', 'B', 'C'] or sort == ['A', 'C', 'B'] or sort == ['C', 'A', 'B'])

def test_out_of_order_topological_sort_options():
    column_evaluation_graph = {
        'A': set([]), 
        'B': set(['A']), 
        'C': set(['A'])
    }
    sort = topological_sort_columns(column_evaluation_graph)
    assert (sort == ['C', 'B', 'A'] or sort == ['B', 'C', 'A'])

def test_out_of_order_linear_topological_sort_options():
    column_evaluation_graph = {
        'A': set([]), 
        'B': set(['A']), 
        'C': set(['B'])
    }
    sort = topological_sort_columns(column_evaluation_graph)
    assert sort == ['C', 'B', 'A']

def test_strong_linear_prder():
    column_evaluation_graph = {
        'A': set(['B', 'C']), 
        'B': set(['C']), 
        'C': set([])
    }
    sort = topological_sort_columns(column_evaluation_graph)
    assert sort == ['A', 'B', 'C']

# Errors with cyles

def test_simple_cycle_is_cycle_error():
    column_evaluation_graph = {'A': set(['B']), 'B': set(['C']), 'C': set(['A'])}
    with pytest.raises(EditError) as edit_error_info:
        sort = topological_sort_columns(column_evaluation_graph)
    assert edit_error_info.value.type_ == 'circular_reference_error'

def test_self_reference_is_cycle_error():
    column_evaluation_graph = {'A': set(['B']), 'B': set(['C']), 'C': set(['C'])}
    with pytest.raises(EditError) as edit_error_info:
        sort = topological_sort_columns(column_evaluation_graph)
    assert edit_error_info.value.type_ == 'circular_reference_error'

def test_simple_nested_cycleis_cycle_error():
    column_evaluation_graph = {'A': set(['B']), 'B': set(['C']), 'C': set(['B'])}
    with pytest.raises(EditError) as edit_error_info:
        sort = topological_sort_columns(column_evaluation_graph)
    assert edit_error_info.value.type_ == 'circular_reference_error'
