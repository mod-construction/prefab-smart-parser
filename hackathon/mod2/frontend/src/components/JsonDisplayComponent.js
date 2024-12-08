import React from "react";
import JSONPretty from "react-json-pretty";
import "react-json-pretty/themes/monikai.css";

const JsonDisplayComponent = ({ jsonSchema }) => {
    return (
        <div style={{ flex: 1, padding: "20px", overflow: "auto" }}>
            {jsonSchema ? (
                <JSONPretty data={jsonSchema} theme={JSONPretty.monikai}></JSONPretty>
            ) : (
                <p>No JSON schema generated yet. Please upload a PDF.</p>
            )}
        </div>
    );
};

export default JsonDisplayComponent;
