import React from 'react';
import { ErrorJSON } from '../widget';

// import css
import "../../css/error.css"
import "../../css/margins.css"

const Error = (props : {errorJSON : ErrorJSON | undefined, onClick: () => void}): JSX.Element => {
    /*
        In the future, this will be a model that displays
        the error in an easy to consume manner.
    */


    if (props.errorJSON) {
        return (
            <div className="error" onClick={props.onClick}>
                <div>An error occured -- {props.errorJSON.type} </div>
                <div className="mt-4">click to exit</div>
            </div>        
        );
    } else {
        return (
            <div></div>
        )
    }
    
};

export default Error;