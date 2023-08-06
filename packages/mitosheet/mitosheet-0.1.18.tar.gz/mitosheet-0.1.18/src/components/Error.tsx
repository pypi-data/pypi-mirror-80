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
            <div className="error">
                {/* Note: we close whenever you click anywhere on the header! */}
                <div className='error-header' onClick={props.onClick}>
                    <div className='error-header-text'>{props.errorJSON.header}</div>
                    <div className='error-header-close'>X</div>
                </div>
                <div className='error-message'>
                    {props.errorJSON.to_fix} 
                </div>
            </div>        
        );
    } else {
        return (
            <div></div>
        )
    }
    
};

export default Error;