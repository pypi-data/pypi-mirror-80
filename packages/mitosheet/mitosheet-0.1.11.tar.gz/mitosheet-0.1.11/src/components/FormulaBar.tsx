import React from 'react';

// Import css
import "../../css/formula-bar.css"

const FormulaBar = (props: {
    formulaBarValue: string, 
    handleFormulaBarEdit: any,
    handleFormulaBarSubmit: any
}): JSX.Element => {

    return(
        <div className="toolbar formula-bar">
            <p>Fx:</p>
            <form onSubmit={props.handleFormulaBarSubmit}>
                <input 
                    value={props.formulaBarValue} 
                    onChange={(e) => props.handleFormulaBarEdit(e)}
                    />
            </form>
        </div>
    )
}

export default FormulaBar
