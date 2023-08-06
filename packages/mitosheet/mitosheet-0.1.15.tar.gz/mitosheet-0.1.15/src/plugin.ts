// Copyright (c) Mito
// Distributed under the terms of the Modified BSD License.

import { Application, IPlugin } from '@phosphor/application';

import { Widget } from '@phosphor/widgets';

import { IJupyterWidgetRegistry } from '@jupyter-widgets/base';

import {
  INotebookTracker
} from '@jupyterlab/notebook';

import {
  ICellModel
} from "@jupyterlab/cells";

import * as widgetExports from './widget';

import { MODULE_NAME, MODULE_VERSION } from './version';

import {
  IObservableString,
  IObservableUndoableList
} from '@jupyterlab/observables';

const EXTENSION_ID = 'mitosheet:plugin';

/**
 * The example plugin.
 */
const examplePlugin: IPlugin<Application<Widget>, void> = ({
  id: EXTENSION_ID,
  requires: [IJupyterWidgetRegistry, INotebookTracker],
  activate: activateWidgetExtension,
  autoStart: true,
} as unknown) as IPlugin<Application<Widget>, void>;
// the "as unknown as ..." typecast above is solely to support JupyterLab 1
// and 2 in the same codebase and should be removed when we migrate to Lumino.

export default examplePlugin;


function getCellAtIndex(cells: IObservableUndoableList<ICellModel> | undefined, index: number): ICellModel | undefined {
  if (cells == undefined) {
    return undefined;
  }

  const cellsIterator = cells.iter();
  let cell = cellsIterator.next();
  let i = 0;
  while (cell) {
    if (i == index) {
      return cell;
    }

    i++;
    cell = cellsIterator.next();
  }

  
  return undefined;
}

function codeContainer(code: string): string {
  /*
  Returns the code block with
  # MITO CODE START
  and
  # MITO CODE END
  Same functions in utils.py
  */

  return `# MITO CODE START\n\n${code}\n\n# MITO CODE END`
}


/**
 * Activate the widget extension.
 */
function activateWidgetExtension(
  app: Application<Widget>,
  registry: IJupyterWidgetRegistry,
  tracker: INotebookTracker
): void {

  /*
    We define a command here, so that we can call it elsewhere in the
    app - and here is the only place we have access to the app (which we
    need to be able to add commands) and tracker (which we need to get
    the current notebook).
  */
  app.commands.addCommand('write-code-to-cell', {
    label: 'Write Mito Code to a Cell',
    execute: (args: any) => {
      console.log(args)
      // This is the code that was passed to write to the cell.
      const imports = (args.codeJSON as any).imports as string;
      const code = codeContainer(imports + '\n\n' + (args.codeJSON as any).code);

      // We get the current notebook (currentWidget)
      const notebook = tracker.currentWidget?.content;
      if (notebook) {
        // Then, we cell if this is the cell that is actually displaying the mito sheet
        const activeCell = notebook.activeCell;
        if (activeCell) {
          /*
            TODO: we need to fix all the bugs that arise because of the assumption 
            that the cell displaying the sheet actually contains the init call...
          */
          const value = activeCell.model.modelDB.get('value') as IObservableString;
          const currentCode = value.text;
          if (!currentCode.includes('mitosheet.sheet')) {
            return
          }
          /*
            Algorithm below:
            1. Figure out if we've already written Mito code, and if so just replace it
            2. If we haven't written code, then:
              a) Split the existing code at the last line (that displays the sheet)
              b) Put the code in the middle of this
          */

          if (currentCode.includes('MITO CODE')) {
            const preamble = currentCode.substring(0, currentCode.indexOf("# MITO CODE START"));
            const postamble = currentCode.substring(
              currentCode.indexOf("MITO CODE END") + "MITO CODE END".length
            );

            const newCode = preamble + code + postamble;
            value.text = newCode;
          } else {
            const lines = currentCode.split('\n');
            let displayLine = '';
            var i = lines.length - 1
            for (i; i >= 0; i--) {
              // Find the last non-whitespace line
              const currentLine = lines[i].trim();
              if (currentLine.length > 0) {
                displayLine = currentLine;
                break;
              }
            }

            // We rejoin all the lines that aren't the last line
            const preamble = lines.slice(0, i).join('\n');
            const newCode = `${preamble}\n\n${code}\n\n${displayLine}`;
            value.text = newCode;
          }
        }
      }
    }
  });

  app.commands.addCommand('read_df_name', {
    label: 'Read df name from mitoSheet call',
    execute: args => {

      // We get the current notebook (currentWidget)
      const notebook = tracker.currentWidget?.content;

      if (!notebook) return "";

      // If this is a cell displaying a widget, we get the next cell, and write code to it
      const activeCellIndex = notebook.activeCellIndex;

      const cells = notebook.model?.cells;
      const previousCell = getCellAtIndex(cells, activeCellIndex - 1); // TODO: change this to next cell model or something
      
      let dfName = ""
      if (previousCell) {
        // remove the df argument to mitosheet.sheet() from the cell's text
        const previousValue = previousCell.modelDB.get('value') as IObservableString;
        dfName = previousValue.text.split("mitosheet.sheet(")[1].split(")")[0];
      } 

      return dfName
    }
  });


  window.commands = app.commands; // so we can write to it elsewhere
  registry.registerWidget({
    name: MODULE_NAME,
    version: MODULE_VERSION,
    exports: widgetExports,
  });
}


