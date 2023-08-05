

def empty_column_python_code():
    """
    Helper functions for creating an empty entry
    for column_python_code - which can then be filled 
    in later (or left empty for an unedited column)
    """
    return {
        'column_name_change': None,
        'column_type_change': None,
        'column_value_changes': {},
        'column_formula_changes': ''
    }

def code_container(code):
    """
    Returns the code block with
    # MITO CODE START
    and
    # MITO CODE END

    SAME FUNCTION IN PLUGIN.ts
    """

    return f'# MITO CODE START\n\n{code}\n\n# MITO CODE END'