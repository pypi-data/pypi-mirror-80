#!/usr/bin/env python
# coding: utf-8

# Copyright (c) Mito.
# Distributed under the terms of the Modified BSD License.

import pytest
import pandas as pd

from ..example import df_to_json, MitoWidget


def test_example_creation_blank():
    df = pd.DataFrame()
    sheet_json = df_to_json(df)
    w = MitoWidget(analysis_name='analysis', df=df)
    assert w.sheet_json == sheet_json
