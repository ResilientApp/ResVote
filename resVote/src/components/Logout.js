import React from 'react';
import '../App.css';

export default function Logout(params){
    const { onLogout } = params;
  return (
    <>
        <button
            type="button"
            className="btn btn-danger logout-button"
            onClick={() => onLogout()}
        >
            Logout
        </button>
        {/* <div className="page-container">
            <div className="form-container">
                <div className="d-flex justify-content-between align-items-center mb-4">
                        <button
                            type="button"
                            className="btn btn-danger logout-button"
                            onClick={() => onLogout()}
                        >
                            Logout
                        </button>
                    </div>
                </div>
            </div> */}
        </>
    )
}