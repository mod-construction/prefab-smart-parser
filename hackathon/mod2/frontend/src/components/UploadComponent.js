import React from "react";
import { useDropzone } from "react-dropzone";

const UploadComponent = ({ onDrop, isLoading, pdfFile, allowMultiple }) => {
    const { getRootProps, getInputProps } = useDropzone({
        onDrop,
        multiple: allowMultiple,
        accept: "application/pdf",
    });

    return (
        <div
            {...getRootProps()}
            style={{
                height: pdfFile ? "100px" : "300px", // Smaller height if a PDF is uploaded
                padding: "20px",
                border: "2px dashed #ccc",
                textAlign: "center",
                display: "flex",
                alignItems: "center",
                justifyContent: "center",
                cursor: "pointer",
                transition: "height 0.3s ease-in-out", // Smooth transition when resizing
            }}
        >
            <input {...getInputProps()} />
            {isLoading ? (
                <p>Processing PDF...</p>
            ) : (
                <p>{pdfFile ? "Upload another PDF" : "Drag and drop a PDF file here, or click to select a file"}</p>
            )}
        </div>
    );
};

export default UploadComponent;
