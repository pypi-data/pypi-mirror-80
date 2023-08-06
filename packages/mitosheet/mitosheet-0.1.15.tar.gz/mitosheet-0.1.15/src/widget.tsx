// Copyright (c) Mito
// Distributed under the terms of the Modified BSD License.

import {
  DOMWidgetModel,
  DOMWidgetView,
  ISerializers,
  WidgetView,
} from '@jupyter-widgets/base';

import { MODULE_NAME, MODULE_VERSION } from './version';

// Import the CSS
import '../css/widget.css';

// React
import React from 'react';
import ReactDOM from 'react-dom';

// Components
import Mito from './components/Mito';

// Logging
import Analytics from 'analytics-node';

export class ExampleModel extends DOMWidgetModel {

  defaults() {
    return {
      ...super.defaults(),
      _model_name: ExampleModel.model_name,
      _model_module: ExampleModel.model_module,
      _model_module_version: ExampleModel.model_module_version,
      _view_name: ExampleModel.view_name,
      _view_module: ExampleModel.view_module,
      _view_module_version: ExampleModel.view_module_version,
      df_json: '',
    };
  }

  static serializers: ISerializers = {
    ...DOMWidgetModel.serializers,
    // Add any extra serializers here
  };

  static model_name = 'ExampleModel';
  static model_module = MODULE_NAME;
  static model_module_version = MODULE_VERSION;
  static view_name = 'ExampleView'; // Set to null if no view
  static view_module = MODULE_NAME; // Set to null if no view
  static view_module_version = MODULE_VERSION;
}

// We save a Mito component in the global scope, so we
// can set the state from outside the react component
declare global {
  interface Window { 
    Mito: any; 
    commands: any;
  }
}

export interface SheetJSON {
  columns: (string|number)[];
  index: string[];
  data: string[][];
}

export interface CodeJSON {
  imports: string;
  code: string;
}

export interface ErrorJSON {
  event: string;
  type: string;
  to_fix: string;
}

export class ExampleView extends DOMWidgetView {

  // The logger instance for this view
  // TODO: do we want to put this in the model as well?
  logger: Analytics;
  user_id: string; 

  /*
    We override the DOMWidgetView constructor, so that we can
    create a logging instance for this view. 
  */
  initialize(parameters : WidgetView.InitializeParameters) {
    super.initialize(parameters);

    // Get df name from code block
    window.commands?.execute('read_df_name').then((dfName : string) => {
      // set the data frame name in the model state
      this.model.set('df_name', dfName);

      // set the data frame name in the widget
      window.Mito?.setState({dfName: dfName});
    });

    // We get the user id from the client side
    this.user_id = this.model.get('user_id');

    // Write key taken from segment.com
    this.logger = new Analytics('L4FqIZ3qB4C2FBitK4gUn073vv3lyWXm');
    // Identify the user
    this.logger.identify({userId: this.user_id});

  }

  /* 
    We override the sending message utilities, so that we can log all
    outgoing messages
  */
  send(msg: {}) {
    // Log the out-going message
    this.logger.track({
      userId: this.user_id,
      event: 'js_sent_msg_log_event',
      properties: {
        event: msg
      }
    })
    super.send(msg);
  }

  render() {    
    // Capture the send, to pass to the component
    const send = (msg: {}) => {
      this.send(msg);
    }

    // TODO: there is a memory leak, in the case where
    // we rerender the component (e.g. we run the mito.sheet)
    // cell again. We need to clean up the component somehow!
    ReactDOM.render(
      <Mito 
        dfName={this.model.get('df_name')}
        sheetJSON={this.getSheetJSON()}
        columnSpreadsheetCodeJSON={JSON.parse(this.model.get('column_spreadsheet_code_json'))}
        codeJSON={this.getCodeJSON()}
        send={send}
        ref={(Mito : any) => { window.Mito = Mito }}
        />,
      this.el
    )
    this.model.on('msg:custom', this.handleMessage, this);
    
    // Log that this view was rendered
    this.logger.track({
      userId: this.user_id,
      event: 'sheet_view_creation_log_event',
      properties: {}
    });
  }

  getSheetJSON(): SheetJSON {
    let sheetJSON: SheetJSON = {
      columns: [],
      index: [],
      data: []
    };

    const unparsedSheetJSON = this.model.get('sheet_json');
    try {
      sheetJSON['columns'] = JSON.parse(unparsedSheetJSON)['columns'];
      sheetJSON['index'] = JSON.parse(unparsedSheetJSON)['index'];
      sheetJSON['data'] = JSON.parse(unparsedSheetJSON)['data'];
    } catch (e) {
      // Suppress error
    }

    return sheetJSON;
  }

  getCodeJSON(): CodeJSON {
    let codeJSON: CodeJSON = {
      imports: '# No imports',
      code: '# No code has been written yet!'
    };

    const unparsedCodeJSON = this.model.get('code_json');
    try {
      codeJSON['imports'] = JSON.parse(unparsedCodeJSON)['imports'];
      codeJSON['code'] = JSON.parse(unparsedCodeJSON)['code'];
    } catch (e) {
      // Suppress error
    }
    return codeJSON;
  }



  handleMessage(message : any) {
    /* 
      This route handles the messages sent from the Python widget
    */
  
    // Log that we received this message
    this.logger.track({
      userId: this.user_id,
      event: 'js_recv_msg_log_event',
      properties: {
        event: message
      }
    })

    console.log("Got a message, ", message);
    if (message.event === 'update_sheet') {
      console.log("Updating sheet");
      window.Mito.setState({
        sheetJSON: this.getSheetJSON(),
        columnSpreadsheetCodeJSON: JSON.parse(this.model.get('column_spreadsheet_code_json'))
      });
    } else if (message.event === 'update_code') {
      console.log('Updating code.');
      window.commands?.execute('write-code-to-cell', {codeJSON: this.getCodeJSON()});
    } else if (message.event === 'edit_error') {
      console.log("Updating edit error.");
      window.Mito.setState({errorJSON: message});
    }
  }
}
