import React from "react";
import { Worker, Viewer } from "@react-pdf-viewer/core";
import "@react-pdf-viewer/core/lib/styles/index.css";
import "@react-pdf-viewer/default-layout/lib/styles/index.css";

const PdfViewerComponent = ({ pdfFile }) => {
    if (!pdfFile) {
        return <p>No PDF selected for visualization. Please upload a PDF.</p>;
    }

    const fileUrl = URL.createObjectURL(pdfFile);

    return (
        <div style={{ flex: 1, padding: "20px", overflow: "auto" }}>
            <Worker workerUrl={`https://unpkg.com/pdfjs-dist@3.4.120/build/pdf.worker.min.js`}>
                <Viewer fileUrl={fileUrl} />
            </Worker>
        </div>
    );
};

export default PdfViewerComponent;
