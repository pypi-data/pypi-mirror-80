#!/usr/bin/env python
# coding: utf-8

# Copyright (c) Mito.
# Distributed under the terms of the Modified BSD License.

import pytest
import pandas as pd

from ..evaluate import parse_formula

# We mark this as expected to fail, and will fix it later!
@pytest.mark.xfail
def test_evaluate_cell_edit_event():
    formula_type, arguments = parse_formula("=AA + AB")

def test_evaluate_ignores_whitespace():
    assert parse_formula("=A + B") == ('add', ['A', 'B'])
    assert parse_formula("=A+ B") == ('add', ['A', 'B'])
    assert parse_formula("=A +B") == ('add', ['A', 'B'])
    assert parse_formula("=A+B") == ('add', ['A', 'B'])
    assert parse_formula("= A + B") == ('add', ['A', 'B'])