import React, { useState, useRef } from "react";
import axios from "axios";
import UploadComponent from "./components/UploadComponent";
import PdfViewerComponent from "./components/PdfViewerComponent";

// Function to apply basic syntax highlighting to JSON
const syntaxHighlight = (json) => {
    if (typeof json !== "string") {
        json = JSON.stringify(json, undefined, 2);
    }
    json = json
        .replace(/&/g, "&amp;")
        .replace(/</g, "&lt;")
        .replace(/>/g, "&gt;");
    return json.replace(
        /("(\\u[a-zA-Z0-9]{4}|\\[^u]|[^\\"])*"(\s*:)?|\b(true|false|null)\b|\b-?\d+(?:\.\d*)?(?:[eE][+-]?\d+)?\b)/g,
        (match) => {
            let cls = "number";
            if (/^"/.test(match)) {
                if (/:$/.test(match)) {
                    cls = "key";
                } else {
                    cls = "string";
                }
            } else if (/true|false/.test(match)) {
                cls = "boolean";
            } else if (/null/.test(match)) {
                cls = "null";
            }
            return `<span class="${cls}">${match}</span>`;
        }
    );
};

function App() {
    const [pdfFiles, setPdfFiles] = useState([]); // Store PDF files
    const [schemas, setSchemas] = useState({}); // Store JSON schemas for each PDF
    const [isLoading, setIsLoading] = useState(false);
    const jsonDivRefs = useRef({}); // Refs for each JSON div to handle cursor positions

    // Handle multiple file uploads
    const onDrop = async (acceptedFiles) => {
        if (acceptedFiles.length === 0) return;

        // Immediately add PDF files to state for viewing
        const newPdfFiles = [];
        acceptedFiles.forEach((file) => {
            newPdfFiles.push(file);
            setPdfFiles((prevFiles) => [...prevFiles, file]);
        });

        // Continue to process each file for JSON schema
        setIsLoading(true);
        for (const file of newPdfFiles) {
            const formData = new FormData();
            formData.append("pdf", file);

            try {
                const response = await axios.post("http://localhost:5001/upload", formData, {
                    headers: {
                        "Content-Type": "multipart/form-data",
                    },
                });

                // Update the state with the received JSON schema for each file
                if (response.data && response.data.schema) {
                    setSchemas((prevSchemas) => ({
                        ...prevSchemas,
                        [file.name]: {
                            schema: response.data.schema,
                            jsonEditValue: JSON.stringify(response.data.schema, null, 2),
                        },
                    }));
                }
            } catch (error) {
                console.error("Error uploading PDF:", error);
            }
        }

        setIsLoading(false);
    };

    // Handle changes to the editable JSON text area for each PDF
    const handleJsonEditChange = (pdfName, event) => {
        const selection = window.getSelection();
        const range = selection.getRangeAt(0);
        const startOffset = range.startOffset;

        const updatedJsonEditValue = event.target.textContent;

        setSchemas((prevSchemas) => ({
            ...prevSchemas,
            [pdfName]: {
                ...prevSchemas[pdfName],
                jsonEditValue: updatedJsonEditValue,
            },
        }));

        // Restore cursor position after updating the content
        setTimeout(() => {
            if (jsonDivRefs.current[pdfName]) {
                const newRange = document.createRange();
                newRange.setStart(jsonDivRefs.current[pdfName].childNodes[0], startOffset);
                newRange.collapse(true);
                selection.removeAllRanges();
                selection.addRange(newRange);
            }
        }, 0);
    };

    // Function to download the JSON schema for each PDF
    const downloadJson = (pdfName) => {
        const schemaData = schemas[pdfName]?.schema;
        if (!schemaData) return;

        // Create a Blob with the JSON data
        const jsonString = JSON.stringify(schemaData, null, 2);
        const blob = new Blob([jsonString], { type: "application/json" });

        // Create an anchor element and trigger a download
        const url = URL.createObjectURL(blob);
        const link = document.createElement("a");
        link.href = url;
        link.download = `${pdfName.replace(".pdf", "_schema.json")}`; // Generate filename
        document.body.appendChild(link);
        link.click();
        document.body.removeChild(link);
    };

    return (
        <div style={{ display: "flex", height: "100vh" }}>
            {/* Left Side - Upload PDFs & PDF Viewer */}
            <div style={{ width: "50%", padding: "20px", borderRight: "1px solid #ccc", overflowY: "auto" }}>
                {/* Upload Component */}
                <UploadComponent onDrop={onDrop} isLoading={isLoading} allowMultiple={true} />

                {/* PDF Viewer for each uploaded file */}
                {pdfFiles.map((file) => (
                    <div key={file.name} style={{ marginTop: "20px" }}>
                        <h4 style={{ color: "#000" }}>{file.name}</h4>
                        <PdfViewerComponent pdfFile={file} />
                    </div>
                ))}
            </div>

            {/* Right Side - Highlighted JSON Schema Editors */}
            <div style={{ width: "50%", padding: "20px", overflowY: "auto" }}>
                {pdfFiles.map((file) => {
                    const pdfName = file.name;
                    const schema = schemas[pdfName]?.jsonEditValue;

                    return (
                        <div key={pdfName} style={{ marginBottom: "30px" }}>
                            <h3 style={{ color: "#000" }}>Highlighted JSON Schema Preview for {pdfName}</h3>
                            {schema && (
                                <>
                                    {/* Highlighted JSON Schema */}
                                    <div
                                        ref={(el) => (jsonDivRefs.current[pdfName] = el)}
                                        contentEditable
                                        onInput={(e) => handleJsonEditChange(pdfName, e)}
                                        dangerouslySetInnerHTML={{ __html: syntaxHighlight(schema) }}
                                        style={{
                                            width: "100%",
                                            padding: "15px",
                                            fontFamily: "monospace",
                                            fontSize: "14px",
                                            border: "1px solid #ccc",
                                            borderRadius: "4px",
                                            backgroundColor: "#2b2b2b",
                                            color: "#ffffff",
                                            overflow: "auto",
                                            whiteSpace: "pre",
                                            outline: "none",
                                            marginBottom: "10px",
                                            resize: "vertical", // Allows resizing vertically
                                        }}
                                    ></div>

                                    {/* Button Container */}
                                    <div style={{ display: "flex", gap: "10px", marginBottom: "20px" }}>
                                        {/* Save Edited JSON Button */}
                                        <button
                                            onClick={() => {
                                                try {
                                                    const parsedJson = JSON.parse(schemas[pdfName].jsonEditValue);
                                                    setSchemas((prevSchemas) => ({
                                                        ...prevSchemas,
                                                        [pdfName]: {
                                                            ...prevSchemas[pdfName],
                                                            schema: parsedJson,
                                                        },
                                                    }));
                                                    alert("JSON updated successfully!");
                                                } catch (error) {
                                                    alert("Invalid JSON format. Please correct it before saving.");
                                                }
                                            }}
                                            style={{
                                                padding: "10px",
                                                backgroundColor: "#007bff",
                                                color: "#fff",
                                                border: "none",
                                                borderRadius: "4px",
                                                cursor: "pointer",
                                            }}
                                        >
                                            Save Edited JSON
                                        </button>

                                        {/* Download JSON Button */}
                                        <button
                                            onClick={() => downloadJson(pdfName)}
                                            style={{
                                                padding: "10px",
                                                backgroundColor: "#28a745",
                                                color: "#fff",
                                                border: "none",
                                                borderRadius: "4px",
                                                cursor: "pointer",
                                            }}
                                        >
                                            Download JSON
                                        </button>
                                    </div>
                                </>
                            )}
                        </div>
                    );
                })}
            </div>
        </div>
    );
}

export default App;
