import React from 'react';

// Import CSS
import "../../css/mito-toolbar.css"

// Import Types
import { SheetJSON } from '../widget';

const MitoToolbar = (props: {sheetJSON: SheetJSON, send: any}): JSX.Element => {

    /* Adds a new column onto the end of a sheet, with A, B, C... as the name */
    const addColumn = () => {
        const newColumn = String.fromCharCode(65 + props.sheetJSON.columns.length);
        console.log(newColumn);
        // TODO: have to update these timestamps, etc to be legit
        props.send({
            'event': 'edit_event',
            'type': 'add_column',
            'id': '123',
            'timestamp': '456',
            'column_header': newColumn
        })
    }

    return (
        <div className='mito-toolbar-container'>
            <button className='mito-toolbar-item' onClick={addColumn}>
                Add Column
            </button>
            {/* add className mito-toolbar-item to a div below to add another toolbar item! */}
        </div>
    );
};

export default MitoToolbar;