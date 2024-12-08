import React, {useState} from "react";

export default function DragAndDropUploader({onFileUpload}) {
    const [isDragging, setIsDragging] = useState(false);
    const [fileName, setFileName] = useState("");

    const handleDragOver = (event) => {
        event.preventDefault();
        setIsDragging(true);
    };

    const handleDragLeave = () => {
        setIsDragging(false);
    };

    const handleDrop = async (event) => {
        event.preventDefault();
        setIsDragging(false);

        const file = event.dataTransfer.files[0];
        if (file) {
            setFileName(file.name);
            await onFileUpload(file);
        }
    };

    const handleFileChange = async (event) => {
        const file = event.target.files[0];
        if (file) {
            setFileName(file.name);
            await onFileUpload(file);
        }
    };

    return (
        <div
            onDragOver={handleDragOver}
            onDragLeave={handleDragLeave}
            onDrop={handleDrop}
            style={{
                padding: "20px",
                marginTop: "10px",
                border: "2px dashed #aaa",
                borderRadius: "10px",
                textAlign: "center",
                backgroundColor: isDragging ? "#f0f8ff" : "#ACD79E",
                transition: "background-color 0.2s",
            }}
        >
            <input
                type="file"
                accept="application/pdf"
                onChange={handleFileChange}
                style={{display: "none"}}
                id="file-upload"
            />
            <label
                htmlFor="file-upload"
                style={{
                    display: "block",
                    fontSize: "18px",
                    color: "#555",
                    cursor: "pointer",
                }}
            >
                {fileName || "Drag and drop a PDF file here, or click to upload"}
            </label>
        </div>
    );
};
