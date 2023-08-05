import React from 'react';

// Import types
import { SheetJSON, CodeJSON, ErrorJSON } from '../widget';

// Import sheet and code components
import MitoSheet from './MitoSheet';
import SheetTab from './SheetTab';
import ErrorOverlay from './ErrorOverlay';
import MitoToolbar from './MitoToolbar';

// Import css
import "../../css/mito.css"

type MitoProps = {
    dfName: string;
    sheetJSON: SheetJSON;
    codeJSON: CodeJSON;
    send: any
};
type MitoState = {
    dfName: string;
    sheetJSON: SheetJSON;
    codeJSON: CodeJSON;
    errorJSON: ErrorJSON | undefined;
};




class Mito extends React.Component<MitoProps, MitoState> {

    constructor(props: MitoProps) {
        super(props);
        this.state = {
            dfName: this.props.dfName,
            sheetJSON: this.props.sheetJSON,
            codeJSON: this.props.codeJSON,
            errorJSON: undefined
        };
    }

    render() {
        return (
            <div className="sheet-container">
                <MitoToolbar sheetJSON={this.state.sheetJSON} send={this.props.send}/>
                <MitoSheet 
                    sheetJSON={this.state.sheetJSON} 
                    send={this.props.send} />
                {/* For now, we just place the error overlay below; we can make it a modal later. */}
                <ErrorOverlay
                    errorJSON={this.state.errorJSON}
                    onClick={() => {this.setState({errorJSON: undefined})}} />
                <div key={this.state.dfName} className="sheet-tab-bar">
                    <SheetTab sheetName={this.state.dfName}></SheetTab>
                </div>
            </div>
        );
    }

}


export default Mito;