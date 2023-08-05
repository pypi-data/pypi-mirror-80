import React from 'react';
import {AgGridReact} from 'ag-grid-react';
import { CellValueChangedEvent } from 'ag-grid-community';
import 'ag-grid-community/dist/styles/ag-grid.css';
import 'ag-grid-community/dist/styles/ag-theme-alpine.css';

// And functions for building components
import { buildGridData, buildGridColumns } from '../data-utils/gridData';

// Import types
import { SheetJSON } from '../widget';

// Import css
import "../../css/mitosheet.css"

const MitoSheet = (props: {sheetJSON: SheetJSON; send: any}): JSX.Element => {
    
    const cellValueChanged = (e : CellValueChangedEvent) => {
        const column = e.colDef.field;
        const newValue = e.newValue;
        
        props.send({
            'event': 'edit_event',
            'type': 'cell_edit',
            'id': '123',
            'timestamp': '456',
            'address': column,
            'new_formula': newValue
        })
    };

    const columns = buildGridColumns(props.sheetJSON.columns);
    const rowData = buildGridData(props.sheetJSON);
    
    return (
        <div>
            <div className="ag-theme-alpine ag-grid"> 
                <AgGridReact
                    rowData={rowData}
                    onCellValueChanged={cellValueChanged} >
                    {columns}
                </AgGridReact>
            </div>
        </div>
    );
};

export default MitoSheet;