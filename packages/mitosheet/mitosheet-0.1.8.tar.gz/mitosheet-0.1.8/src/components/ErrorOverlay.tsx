import React from 'react';
import { ErrorJSON } from '../widget';

const ErrorOverlay = (props : {errorJSON : ErrorJSON | undefined, onClick: () => void}): JSX.Element => {
    /*
        In the future, this will be a model that displays
        the error in an easy to consume manner.
    */

    return (
        <div onClick={props.onClick}>
            {
                props.errorJSON &&
                props.errorJSON.event + " ; " + props.errorJSON.type + " ; " + props.errorJSON.to_fix
            }
        </div>        
    );
};

export default ErrorOverlay;