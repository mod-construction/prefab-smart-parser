import PdfViewer from "./PdfViewer";
import JsonViewer from "./JsonViewer";
import DragAndDropUploader from "./DragAndDropUploader";
import React, {useState} from "react";
import ComboBox from "./ComboBox";
import {PrefabElement, PrefabElementSchema} from "@mod-construction/mod-dlm";
import {v4 as uuidv4} from "uuid";
import LoadingSpinner from "./LoadingSpinner";

export default function Dashboard() {
    const [jsonData, setJsonData] = useState({});
    const [pdfUrl, setPdfUrl] = useState(null);
    const [loading, setLoading] = useState(false);
    const [validationError, setValidationError] = useState([]);

    const handleFileUpload = async (file) => {
        // const file = event.target.files[0];
        const formData = new FormData();
        formData.append("file", file);

        try {
            // Upload the file using fetch
            const response = await fetch("/upload", {
                method: "POST",
                body: formData,
            });

            if (response.ok) {
                setPdfUrl(`http://localhost:44434/${process.env.PUBLIC_URL}/${file.name}`);
                setLoading(true);
                const url = new URL("/upload", window.location.origin);
                url.searchParams.append("fileName", file.name);
                const jsonResponse = await fetch(url, {
                    method: "GET",
                });

                if (jsonResponse.ok) {
                    const data = await jsonResponse.json();
                    data.result.id = uuidv4();
                    setJsonData(data);
                    debugger;
                    // Validate the element using the PrefabElementSchema
                    validate(data?.result);

                } else {
                    console.error("Error with the request:", jsonResponse.status);
                }

            } else {
                console.error("File upload failed:", response.statusText);
            }
        } catch (error) {
            console.error("Error uploading the file:", error);
        }
    };

    const validate = (result) => {
        if (!result) {
            setValidationError(false);
        }
        const validation = PrefabElementSchema.safeParse(result);

        if (validation.success) {
            setValidationError([]);
            // console.log('Element is valid:', validation.data);
        } else {
            debugger;
            const error = validation.error;
            setValidationError(error);
            console.error('Element validation failed:', error);
        }

        setLoading(false);
    }

    return (
        <div className={"row h-700px"} style={{backgroundColor: "#B8BFB6"}}>
            <div className={"col-6 border-1 border-dark"}>
                <div className={"row"}>
                    <div className={"row p-0 m-0 p-2"}>
                        <DragAndDropUploader onFileUpload={handleFileUpload}/>
                    </div>
                    <div className={"row p-0 m-0 p-2"}>
                        <div className={"mb-2 actionBox row p-0 m-0"}
                             style={{
                                 padding: "20px",
                                 marginTop: "10px",
                                 border: "2px dashed #aaa",
                                 borderRadius: "10px",
                                 textAlign: "center",
                                 backgroundColor: "#ACD79E",
                                 transition: "background-color 0.2s"
                             }}
                        >
                            <ComboBox/>
                            <div className={"col-4 checkbox-container"}>
                                <input type="checkbox" id="multi-Products" name="multi-Products"/>
                                <label htmlFor="multi-Products">Multi-Products</label>
                            </div>
                            <div className={"col-4 checkbox-container"}>
                                <input type="checkbox" id="allow" name="allow"/>
                                <label htmlFor="allow">Allow Assumption</label>
                            </div>
                        </div>
                        <br/>
                        <div className={"col-12"}><PdfViewer pdfUrl={pdfUrl}/></div>
                    </div>
                </div>
            </div>
            {loading ? <div className={"col-6"}><LoadingSpinner/></div> :
                (Array.isArray(validationError) && validationError.length > 0 ? <div>data is not valid!</div> :
                        <div className={"col-6 p-3 border-1 border-dark max-height-600px overflow-scroll-y"}>
                            <div> Data is Valid.</div>
                            <JsonViewer jsonData={jsonData}/>
                        </div>
                )
            }
        </div>
    );
}