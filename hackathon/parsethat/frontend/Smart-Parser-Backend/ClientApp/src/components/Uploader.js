import React, {useState} from "react";

export default function Uploader() {
    const [selectedFile, setSelectedFile] = useState(null);
    const [errorMessage, setErrorMessage] = useState("");
    const [uploadStatus, setUploadStatus] = useState("");

    const handleFileChange = (event) => {
        const file = event.target.files[0];

        // Validate file type
        if (file && file.type !== "application/pdf") {
            setErrorMessage("Only PDF files are allowed.");
            setSelectedFile(null);
        } else {
            setErrorMessage("");
            setSelectedFile(file);
        }
    };

    const handleFileUpload = async () => {
        if (!selectedFile) {
            alert("Please select a file before uploading.");
            return;
        }

        // Create a FormData object to send the file
        const formData = new FormData();
        formData.append("file", selectedFile);

        try {
            setUploadStatus("Uploading...");
            const response = await fetch("upload", {
                method: "POST",
                body: formData,
            });

            if (response.ok) {
                setUploadStatus("File uploaded successfully!");
            } else {
                setUploadStatus("Failed to upload file.");
            }
        } catch (error) {
            setUploadStatus("An error occurred during upload.");
            console.error("Upload error:", error);
        }
    };

    return (
        <div style={{padding: "20px", border: "1px solid #ccc", borderRadius: "5px"}}>
            <h2>Upload a PDF</h2>
            <div style={{margin: "20px 0"}}>
                <label htmlFor="fileInput" style={{display: "block", marginBottom: "10px"}}>
                    Select a PDF file:
                </label>
                <input
                    type="file"
                    id="fileInput"
                    accept=".pdf"
                    onChange={handleFileChange}
                />
                {errorMessage && (
                    <p style={{color: "red", marginTop: "10px"}}>{errorMessage}</p>
                )}
            </div>
            <button onClick={handleFileUpload} disabled={!selectedFile}>
                Upload
            </button>
            {uploadStatus && (
                <p style={{marginTop: "10px", color: uploadStatus.includes("successfully") ? "green" : "red"}}>
                    {uploadStatus}
                </p>
            )}
        </div>
    );
}
