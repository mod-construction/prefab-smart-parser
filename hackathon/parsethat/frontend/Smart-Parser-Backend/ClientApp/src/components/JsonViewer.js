import React, {useState, useEffect} from "react";
import ReactJson from "react-json-view";

const JsonViewer = ({jsonData}) => {
    if (!jsonData) {
        return <div></div>;
    }

    return (
        <div style={{padding: "20px",maxHeight: "650px", overflowY: "scroll", fontFamily: "monospace", backgroundColor: "#f4f4f4", borderRadius: "8px"}}>
            <h3>JSON Data</h3>
            <ReactJson
                src={jsonData}
                collapsed={3} 
                enableClipboard={true} // Enable copy to clipboard
                displayDataTypes={false} // Hide data types
                displayObjectSize={true} // Show object size
                theme="monokai" // Set a theme
                style={{fontFamily: "monospace"}}
            />
        </div>
    );
};

export default JsonViewer;
