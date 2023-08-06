import React from 'react';
import {AgGridReact} from 'ag-grid-react';
import { CellValueChangedEvent, CellFocusedEvent } from 'ag-grid-community';
import 'ag-grid-community/dist/styles/ag-grid.css';
import 'ag-grid-community/dist/styles/ag-theme-alpine.css';
import '../../css/mitosheet.css';

// And functions for building components
import { buildGridData, buildGridColumns } from '../data-utils/gridData';

// Import types
import { SheetJSON } from '../widget';

const MitoSheet = (props: {
    sheetJSON: SheetJSON; 
    send: any; 
    sendCellValueUpdate: any; 
    cellFocused: (arg0: CellFocusedEvent) => void
}): JSX.Element => {
    
    const cellValueChanged = (e : CellValueChangedEvent) => {
        const column = e.colDef.field;
        const newValue = e.newValue;
        
        props.sendCellValueUpdate(column, newValue);
    };

    const columns = buildGridColumns(props.sheetJSON.columns);
    const rowData = buildGridData(props.sheetJSON);

    return (
        <div>
            <div className="ag-theme-alpine ag-grid"> 
                <AgGridReact
                    onCellFocused={(e : CellFocusedEvent) => props.cellFocused(e)}
                    rowData={rowData}
                    onCellValueChanged={cellValueChanged} >
                    {columns}
                </AgGridReact>
            </div>
        </div>
    );
};

export default MitoSheet;