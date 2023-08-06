import React, { FormEvent } from 'react';

// Import types
import { CellFocusedEvent } from 'ag-grid-community';
import { SheetJSON, CodeJSON, ErrorJSON } from '../widget';

// Import sheet and code components
import MitoSheet from './MitoSheet';
import SheetTab from './SheetTab';
import Error from './Error';
import FormulaBar from './FormulaBar';
import MitoToolbar from './MitoToolbar';

// Import css
import "../../css/mito.css"

interface ColumnSpreadsheetCodeJSON {
    [Key: string]: String;
}


type MitoProps = {
    dfName: string;
    columnSpreadsheetCodeJSON: ColumnSpreadsheetCodeJSON;
    sheetJSON: SheetJSON;
    codeJSON: CodeJSON;
    send: any
};

type MitoState = {
    dfName: string;
    columnSpreadsheetCodeJSON: ColumnSpreadsheetCodeJSON;
    sheetJSON: SheetJSON;
    codeJSON: CodeJSON;
    formulaBarValue: string;
    selectedColumn: string;
    selectedRowIndex: number;
    errorJSON: ErrorJSON | undefined;
};


class Mito extends React.Component<MitoProps, MitoState> {

    constructor(props: MitoProps) {
        super(props);
        this.state = {
            columnSpreadsheetCodeJSON: this.props.columnSpreadsheetCodeJSON,
            dfName: this.props.dfName,
            sheetJSON: this.props.sheetJSON,
            codeJSON: this.props.codeJSON,
            formulaBarValue: '',
            selectedColumn: '',
            selectedRowIndex: 0,
            errorJSON: undefined
        };

        this.cellFocused = this.cellFocused.bind(this);
        this.handleFormulaBarEdit = this.handleFormulaBarEdit.bind(this);
        this.handleFormulaBarSubmit = this.handleFormulaBarSubmit.bind(this);
        this.sendCellValueUpdate = this.sendCellValueUpdate.bind(this);
    }

    cellFocused(event : CellFocusedEvent) {
        const column = event.column.getColId();
        const columnIndex = this.state.sheetJSON.columns.indexOf(column);
        const rowIndex = event.rowIndex;

        const columnFormula = this.state.columnSpreadsheetCodeJSON[column];
        let formulaBarValue = '';
        if (columnFormula !== '') {
            // if the cell has a formula, then display the formula
            formulaBarValue = columnFormula.toString()

        } else {
            // if the cell does not have a formula, display the value
            formulaBarValue = this.state.sheetJSON.data[rowIndex][columnIndex];
        }

        // update state
        this.setState({
            selectedColumn: column,
            selectedRowIndex: rowIndex,
            formulaBarValue: formulaBarValue
        });
    }

    handleFormulaBarEdit(e: FormEvent<HTMLInputElement>) {
        this.setState({
            formulaBarValue: e.currentTarget.value
        });
    }

    // TODO: do we want a different type of edit for a value change and a formula change or will 
    // we just detect that in the backend and apply the correct edit rules?
    handleFormulaBarSubmit(e : React.FormEvent<HTMLFormElement>) {
        e.preventDefault();
        this.sendCellValueUpdate(this.state.selectedColumn, this.state.formulaBarValue);
    }

    // TODO: this event should be broken out into a formula edit and a value edit
    sendCellValueUpdate(column : string, newValue : string) {
        this.props.send({
            'event': 'edit_event',
            'type': 'cell_edit',
            'id': '123',
            'timestamp': '456',
            'address': column,
            'new_formula': newValue
        });
    }

    render() {

        return (
            <div className="mito-container">
                <div className="mitosheet">
                    <FormulaBar
                        formulaBarValue={this.state.formulaBarValue}
                        handleFormulaBarEdit={this.handleFormulaBarEdit}
                        handleFormulaBarSubmit={this.handleFormulaBarSubmit} 
                    />
                    <MitoToolbar sheetJSON={this.state.sheetJSON} send={this.props.send}/>
                    <MitoSheet 
                        sheetJSON={this.state.sheetJSON} 
                        cellFocused={this.cellFocused}
                        send={this.props.send}
                        sendCellValueUpdate={this.sendCellValueUpdate} />
                    <div key={this.state.dfName} className="sheet-tab-bar">
                        <SheetTab sheetName={this.state.dfName}></SheetTab>
                    </div>
                </div>
                <div className="modal">
                        <Error
                            errorJSON={this.state.errorJSON}
                            onClick={() => {this.setState({errorJSON: undefined})}} />
                </div>
            </div>
        );
    }

}


export default Mito;