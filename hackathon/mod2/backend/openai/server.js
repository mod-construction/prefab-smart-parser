const express = require("express");
const multer = require("multer");
const cors = require("cors");
const fs = require("fs");
const path = require("path");
const {
    preprocessAndIndexPDF,
    processChunks,
    mergeStructuredData,
    retrieveRelevantChunks,
} = require("./pdfProcessingScripts");
const { generateEmbedding } = require("./embedding_utils");
const examplePrefabElement = require("./schema");

const app = express();
const PORT = 5001;

app.use(cors());
app.use(express.json());

// Ensure uploads directory exists
if (!fs.existsSync("uploads")) {
    fs.mkdirSync("uploads");
}

// Set up multer for file uploads
const upload = multer({ dest: "uploads/" });

// Endpoint to handle PDF upload and processing
app.post("/upload", upload.single("pdf"), async (req, res) => {
    if (!req.file) {
        console.error("No file uploaded.");
        return res.status(400).json({ error: "No file uploaded" });
    }

    const pdfPath = req.file.path;

    try {
        console.log(`Processing file: ${req.file.filename}`);
        let documentIndex = []; // Define documentIndex locally to handle each upload independently

        // Step 1: Preprocess the PDF and index its content
        try {
            await preprocessAndIndexPDF(pdfPath, documentIndex);
            console.log(`PDF ${req.file.filename} indexed successfully.`);
        } catch (error) {
            console.error("Error during PDF preprocessing and indexing:", error.message);
            throw new Error("PDF preprocessing and indexing failed.");
        }

        // Step 2: Create an embedding for the schema query
        let queryEmbedding;
        try {
            const schemaQuery = `Extract data for building material usage for the document ${req.file.filename}`;
            queryEmbedding = await generateEmbedding(schemaQuery);
        } catch (error) {
            console.error("Error generating embedding for schema query:", error.message);
            throw new Error("Embedding generation failed.");
        }

        // Step 3: Retrieve relevant chunks from the indexed document
        let relevantChunks;
        try {
            relevantChunks = retrieveRelevantChunks(queryEmbedding, documentIndex, req.file.filename);
        } catch (error) {
            console.error("Error retrieving relevant chunks:", error.message);
            throw new Error("Retrieving relevant chunks failed.");
        }

        // Step 4: Process chunks to generate structured data
        let structuredDataList;
        try {
            structuredDataList = await processChunks(relevantChunks, examplePrefabElement);
        } catch (error) {
            console.error("Error processing chunks:", error.message);
            throw new Error("Processing chunks failed.");
        }

        // Step 5: Merge structured data and send response
        let mergedData;
        try {
            mergedData = mergeStructuredData(structuredDataList);
        } catch (error) {
            console.error("Error merging structured data:", error.message);
            throw new Error("Merging structured data failed.");
        }

        // Send JSON response back to the frontend
        res.json({ schema: mergedData });

        // Step 6: Delete the uploaded file to keep the server clean
        fs.unlink(pdfPath, (err) => {
            if (err) {
                console.error("Error deleting uploaded file:", err.message);
            } else {
                console.log(`Uploaded file ${req.file.filename} deleted.`);
            }
        });
    } catch (error) {
        console.error("Error processing PDF:", error.message);
        res.status(500).json({ error: "Error processing PDF: " + error.message });
    }
});

// Start the server
app.listen(PORT, () => {
    console.log(`Server is running on http://localhost:${PORT}`);
});
