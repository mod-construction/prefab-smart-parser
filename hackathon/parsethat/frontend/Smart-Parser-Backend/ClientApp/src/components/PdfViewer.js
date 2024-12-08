import React from "react";
import "react-pdf/dist/esm/Page/AnnotationLayer.css";
import "@react-pdf-viewer/core/lib/styles/index.css";
import "@react-pdf-viewer/default-layout/lib/styles/index.css";

function PdfViewer({pdfUrl}) {
    return (
        <div>
            <iframe
                className={"col-md-12"}
                src={pdfUrl}
                width="100%"
                height="480px"
                title="PDF Viewer"
            ></iframe>
        </div>
    );

}

export default PdfViewer;
