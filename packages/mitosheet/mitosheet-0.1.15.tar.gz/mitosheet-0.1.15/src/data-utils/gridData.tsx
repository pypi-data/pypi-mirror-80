import React from 'react';
import { AgGridColumn } from 'ag-grid-react';
import { SheetJSON } from '../widget';

interface RowDict<T> {
    [Key: string]: T;
}

// convert json formatted data frame into Ag-Grid data structure 
export function buildGridData(sheet_json : SheetJSON) : RowDict<String>[] {
    let gridData = [];
    let columns = sheet_json.columns;

    // iterate through the data frame to get each row
    for (let i = 0; i < sheet_json.data.length; i++) {
        let rowDict : RowDict<String> = {};
        // set the index column of the Ag-Grid
        rowDict["index"] = `${i + 1}`;
        // iterate through the column to get each element
        for (let j = 0; j < sheet_json.data[i].length; j++) {
            // create dict entry for row
            let rowDictKey = columns[j];
            rowDict[rowDictKey] = sheet_json.data[i][j];
        }
        gridData.push(rowDict);
    }
    return gridData;
}


// create columns from data frame columns
export function buildGridColumns(df_columns : (string|number)[]) : JSX.Element[] {
    let gridColumns = [];
    
    // create index column
    gridColumns.push(<AgGridColumn key={"index"} headerName={""} field={"index"} width={10} lockPosition={true}></AgGridColumn>);

    // iterate through columns of df_columns to create Ag-Grid columns
    df_columns.forEach((column_header : string|number)  => {
        gridColumns.push(
            <AgGridColumn 
                key={column_header} 
                field={column_header.toString()} 
                lockPosition={true} 
                editable={true} />
        );
    });

    return gridColumns;
}