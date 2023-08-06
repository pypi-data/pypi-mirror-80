#!/usr/bin/env python
# coding: utf-8

# Copyright (c) Mito.
# Distributed under the terms of the Modified BSD License.

import pytest

from ..evaluate import parse_formula

CONSTANT_TEST_CASES = [
    (
        '=100',
        'B',
        'df[\'B\'] = 100',
        set([]),
        set([])
    ),
    (
        '=True',
        'B',
        'df[\'B\'] = True',
        set([]),
        set([])
    ),
    (
        '=\'StringSingleQuotes\'',
        'B',
        'df[\'B\'] = \'StringSingleQuotes\'',
        set([]),
        set([])
    ),
    (
        '=\"StringDoubleQuotes\"',
        'B',
        'df[\'B\'] = \"StringDoubleQuotes\"',
        set([]),
        set([])
    )
]
"""
TODO: add these tests in, when we support strings with spaces!
(
    '=\'String Single Quotes\'',
    'B',
    'df[\'B\'] = \'String Single Quotes\'',
    set([]),
    set([])
),
(
    '=\"String Double Quotes\"',
    'B',
    'df[\'B\'] = \"String Double Quotes\"',
    set([]),
    set([])
)
"""

# Tests cases to ensure operators are parsed correctly
OPERATOR_TEST_CASES = [
    # Simple add operation
    (
        '=A + B',
        'C',
        'df[\'C\'] = df[\'A\'] + df[\'B\']',
        set(),
        set(['A', 'B'])
    ),
    # Simple subtract operation
    (
        '=A - B',
        'C',
        'df[\'C\'] = df[\'A\'] - df[\'B\']',
        set(),
        set(['A', 'B'])
    ),
    # Simple multiply operation
    (
        '=A * B',
        'C',
        'df[\'C\'] = df[\'A\'] * df[\'B\']',
        set(),
        set(['A', 'B'])
    ),
    # Simple divide operation
    (
        '=A / B',
        'C',
        'df[\'C\'] = df[\'A\'] / df[\'B\']',
        set(),
        set(['A', 'B'])
    ),
    # Handles multi-char columns
    (
        '=AAA + BBB + CCC + DDD',
        'E',
        'df[\'E\'] = df[\'AAA\'] + df[\'BBB\'] + df[\'CCC\'] + df[\'DDD\']',
        set(),
        set(['AAA', 'BBB', 'CCC', 'DDD'])
    ),
    # Maintains parens and constants
    (
        '=(A + B) / C + A * 100',
        'D',
        'df[\'D\'] = (df[\'A\'] + df[\'B\']) / df[\'C\'] + df[\'A\'] * 100',
        set(),
        set(['A', 'B', 'C'])
    ),
    # Operator in functions
    (
        '=FUNC(A + B / C + A * 100)',
        'D',
        'df[\'D\'] = FUNC(df[\'A\'] + df[\'B\'] / df[\'C\'] + df[\'A\'] * 100)',
        set(['FUNC']),
        set(['A', 'B', 'C'])
    )
]

# Tests proper function parsing
FUNCTION_TEST_CASES = [
    # Simple, singular function call
    (
        '=FUNC(A)',
        'B',
        'df[\'B\'] = FUNC(df[\'A\'])',
        set(['FUNC']),
        set(['A'])
    ),
    # Simple, singular function call that has the name of a column
    (
        '=C(A)',
        'B',
        'df[\'B\'] = C(df[\'A\'])',
        set(['C']),
        set(['A'])
    ),
    # Nested functions with different names
    (
        '=FUNCA(FUNCB(FUNCC(FUNCD(FUNCE(FUNCF(FUNCG(FUNCH(A))))))))',
        'B',
        'df[\'B\'] = FUNCA(FUNCB(FUNCC(FUNCD(FUNCE(FUNCF(FUNCG(FUNCH(df[\'A\']))))))))',
        set(['FUNCA', 'FUNCB', 'FUNCC', 'FUNCD', 'FUNCE', 'FUNCF', 'FUNCG', 'FUNCH']),
        set(['A'])
    ),
    # Nested functions with basic operators
    (
        '=RIGHT(A, LEN(B) - 10)',
        'C',
        'df[\'C\'] = RIGHT(df[\'A\'], LEN(df[\'B\']) - 10)',
        set(['RIGHT', 'LEN']),
        set(['A', 'B'])
    ),
    # More nested functions with columns
    (
        '=FUNC(A, FUNC(B, FUNC(C)))',
        'D',
        'df[\'D\'] = FUNC(df[\'A\'], FUNC(df[\'B\'], FUNC(df[\'C\'])))',
        set(['FUNC']),
        set(['A', 'B', 'C'])
    ),
    # Lots of column references
    (
        '=FUNC(A, B, C, D, E, F, G, H, I)',
        'J',
        'df[\'J\'] = FUNC(df[\'A\'], df[\'B\'], df[\'C\'], df[\'D\'], df[\'E\'], df[\'F\'], df[\'G\'], df[\'H\'], df[\'I\'])',
        set(['FUNC']),
        set(['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I'])
    ) 
]


"""
PARSE_TESTS contains a variety of tests that make sure
formula parsing is working properly; it is passed as 
a parameter into the test_parse test below.

Order of params is: formula, address, python_code, functions, columns

See documentation here: https://docs.pytest.org/en/latest/parametrize.html#parametrize-basics
"""
PARSE_TESTS = CONSTANT_TEST_CASES + OPERATOR_TEST_CASES + FUNCTION_TEST_CASES
@pytest.mark.parametrize("formula,address,python_code,functions,columns", PARSE_TESTS)
def test_parse(formula, address, python_code, functions, columns):
    assert parse_formula(formula, address) == \
        (
            python_code, 
            functions, 
            columns
        )