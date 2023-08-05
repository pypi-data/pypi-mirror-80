import React from 'react';

// import css
import "../../css/sheet-tab.css"

type SheetTabProps = {
    sheetName: string;
};


export default function SheetTab(props : SheetTabProps) {

    const sheetName = props.sheetName ? props.sheetName : "sheet1";

    return (
        <div className="tab">
            <div>
                <p>
                    {sheetName}
                </p>
                <hr className="selected-tab-indicator"></hr>
            </div>  
        </div>
    );
}
