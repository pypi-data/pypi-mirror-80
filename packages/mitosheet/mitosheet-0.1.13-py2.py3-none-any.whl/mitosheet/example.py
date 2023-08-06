#!/usr/bin/env python
# coding: utf-8

# Copyright (c) Mito.
# Distributed under the terms of the Modified BSD License.

"""
TODO: Add module docstring
"""
import json
import analytics
import pandas as pd
from ipywidgets import DOMWidget
from traitlets import Unicode, List

from ._frontend import module_name, module_version
from .evaluate import evaluate
from .transpile import transpile
from .errors import EditError
from .utils import empty_column_python_code
from mitosheet.widget_state_container import WidgetStateContainer

# Write key taken from segement.com
analytics.write_key = '6I7ptc5wcIGC4WZ0N1t0NXvvAbjRGUgX' 
# For now, we identify users with the file location of their path 
# TODO: this probably isn't very good long-term
static_user_id = __file__
analytics.identify(static_user_id, {}) #TODO: get information to store as traits?


class MitoWidget(DOMWidget):
    """TODO: Add docstring here
    """
    _model_name = Unicode('ExampleModel').tag(sync=True)
    _model_module = Unicode(module_name).tag(sync=True)
    _model_module_version = Unicode(module_version).tag(sync=True)
    _view_name = Unicode('ExampleView').tag(sync=True)
    _view_module = Unicode(module_name).tag(sync=True)
    _view_module_version = Unicode(module_version).tag(sync=True)

    value = Unicode('Hello World').tag(sync=True)
    sheet_json = Unicode('').tag(sync=True)
    code_json = Unicode('').tag(sync=True)
    df_name = Unicode('').tag(sync=True)
    user_id = Unicode(static_user_id).tag(sync=True)
    column_spreadsheet_code_json = Unicode('').tag(sync=True)
    edit_event_list = List()

    def __init__(self, *args, **kwargs):
        # Call the DOMWidget constructor to set up the widget properly
        super(MitoWidget, self).__init__(*args, **kwargs)
        self.analysis_name = kwargs['analysis_name'] if 'analysis_name' in kwargs else ''
        self.df = kwargs['df'] if kwargs['df'] is not None else pd.DataFrame() # make a 

        # Set up starting shared state variables
        self.sheet_json = df_to_json(self.df)
        self.code_json = json.dumps({"code": "0"})
        self.df_name = ''
        self.column_spreadsheet_code_json = json.dumps({key: '' for key in self.df.keys()})

        # Set up the state container to hold private widget state
        self.widget_state_container = WidgetStateContainer(self.df)

        # Set up message handler
        self.on_msg(self.receive_message)

        
    def send(self, msg):
        """
        We overload the DOMWidget's send function, so that 
        we log all outgoing messages
        """
        # Send the message though the DOMWidget's send function
        super().send(msg)
        # Log the message as sent
        analytics.track(self.user_id, 'py_sent_msg_log_event', {'event': msg})

    def saturate(self, event):
        """
        Saturation is when the server fills in information that
        is missing from the event client-side. This is for consistency
        and because the client may not have easy access to the info
        all the time.
        """
        if event['event'] == 'edit_event':
            if event['type'] == 'cell_edit':
                address = event['address']
                event['old_formula'] = self.widget_state_container.column_spreadsheet_code[address]

        


    def receive_message(self, widget, content, buffers=None):
        """
        Handles all incoming messages from the JS widget. 

        TODO: we currently assume these are edit events, which
        may not be the case in the future!
        """
        # First, we saturate the event
        self.saturate(content)

        # Then log that we got this message
        analytics.track(self.user_id, 'py_recv_msg_log_event', {'event': content})

        self.edit_event_list.append(content)

        # First, we send this new edit to the evaluator
        try:
            analytics.track(self.user_id, 'evaluator_started_log_event')
            evaluate(
                self.edit_event_list,
                self.widget_state_container  
            )
            analytics.track(self.user_id, 'evaluator_finished_log_event')

            # update column spreadsheet code json
            self.column_spreadsheet_code_json = json.dumps(
                self.widget_state_container.column_spreadsheet_code
            )
            # Update the sheet json, and alert the frontend of the update
            self.sheet_json = df_to_json(self.widget_state_container.df)
            self.send({
                "event": "update_sheet"
            })
        except EditError as e:
            # If we hit an error during editing, log that it has occured
            analytics.track(
                self.user_id, 
                'error_log_event', 
                {'type': e.type_, 'to_fix': e.to_fix}
            )
            # Report it to the user, and then return
            self.send({
                'event': 'edit_error',
                'type': e.type_,
                'to_fix': e.to_fix
            })
            return

        # Then, we send these edits to the transpiler
        analytics.track(self.user_id, 'transpiler_started_log_event')
        code_container = transpile(
            self.widget_state_container
        )
        analytics.track(self.user_id, 'transpiler_finished_log_event')
        # update the code 
        self.code_json = json.dumps(code_container)
        # tell the front-end to render the new code
        self.send({"event": "update_code"})



def sheet(df: pd.DataFrame) -> MitoWidget:
    return MitoWidget(df=df)

def df_to_json(df=None):
    if df is None:
        return '{}'
    json_obj = json.loads(df.to_json(orient="split"))
    # Then, we go through and find all the null values (which are infinities),
    # and set them to undefined.
    for d in json_obj['data']:
        for idx, e in enumerate(d):
            if e is None:
                d[idx] = 'undefined'
    return json.dumps(json_obj)

