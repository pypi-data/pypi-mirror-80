#!/usr/bin/env python
# coding: utf-8

# Copyright (c) Mito.
# Distributed under the terms of the Modified BSD License.

"""
Exports the transpile function, which takes the backend widget
container and generates transpiled Python code. 
"""

from .topological_sort import topological_sort_columns


def transpile(
        column_python_code,
        column_evaluation_graph
    ):

    # TODO: we have to handle the mito.sheet call, etc... in this code
    # We need to take all the existing code as input too!

    topological_sort = topological_sort_columns(column_evaluation_graph)

    code = ""
    for column in topological_sort:
        column_code = column_python_code[column]['column_formula_changes']
        if column_code != '':
            code += column_python_code[column]['column_formula_changes']
            code += "\n\n" # we add two new lines
            
    # remove any trailing whitespace
    return code.strip() 