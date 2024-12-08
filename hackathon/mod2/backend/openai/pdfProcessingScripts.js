const fs = require("fs");
const pdf = require("pdf-parse");
const { OpenAI } = require("openai");
const { generateEmbedding, cosineSimilarity } = require("./embedding_utils");
const examplePrefabElement = require("./schema");

const OPENAI_API_KEY = "YOUR_API_KEY";

const openai = new OpenAI({
  apiKey: OPENAI_API_KEY,
});

// Function to split text into manageable chunks
function splitTextIntoChunks(text, maxLength) {
    const chunks = [];
    let currentChunk = "";

    text.split("\n").forEach((line) => {
        if ((currentChunk + line).length > maxLength) {
            chunks.push(currentChunk);
            currentChunk = "";
        }
        currentChunk += line + "\n";
    });

    if (currentChunk) {
        chunks.push(currentChunk);
    }

    return chunks;
}

// Function to preprocess and generate embeddings for each chunk
async function preprocessAndIndexPDF(pdfPath, documentIndex) {
    try {
        const pdfBuffer = fs.readFileSync(pdfPath);
        const pdfData = await pdf(pdfBuffer);

        // Split text into chunks
        const chunks = splitTextIntoChunks(pdfData.text, 4000);
        const pdfFileName = pdfPath.split('/').pop(); // Extract the filename (e.g., "data01.pdf")

        for (const chunk of chunks) {
            try {
                const embedding = await generateEmbedding(chunk);
                // Store the chunk along with the embedding and the PDF name as metadata
                documentIndex.push({ chunk, embedding, pdfFileName });
            } catch (error) {
                console.error("Error generating embedding:", error.message);
            }
        }
    } catch (error) {
        console.error("Error in preprocessing and indexing PDF:", error.message);
        throw error;
    }
}

// Function to process each chunk and fetch structured data
async function processChunks(chunks, examplePrefabElement) {
    const structuredDataList = [];

    for (const chunk of chunks) {
        try {
            // Create a chat completion using OpenAI v4 API
            const response = await openai.chat.completions.create({
                model: "gpt-4-0613",
                messages: [
                    {
                        role: "system",
                        content: `
                            You are an assistant that processes PDF content into structured data.
                            Always respond with valid JSON that conforms to the following schema:
                            ${JSON.stringify(examplePrefabElement)}. 
                            Do not add any additional comments, explanations, or strings that are not part of the JSON itself.
                            Ensure the JSON structure is complete and valid.
                        `,
                    },
                    {
                        role: "user",
                        content: `Extract structured data from the following text: \n${chunk}`,
                    },
                ],
            });

            // Check if the response contains choices
            if (response && response.choices && response.choices.length > 0) {
                const aiOutput = response.choices[0].message.content;
                try {
                    const structuredData = JSON.parse(aiOutput);
                    structuredDataList.push(structuredData);
                } catch (parseError) {
                    console.error("Error parsing AI output as JSON:", parseError.message);
                    console.error("AI Output:", aiOutput);
                }
            } else {
                console.error("Unexpected response format:", response);
            }
        } catch (error) {
            console.error("Error processing chunk:", error.message);
            if (error.response) {
                console.error("Error details:", error.response.data);
            }
        }
    }

    return structuredDataList;
}

// Function to retrieve the most relevant chunks using cosine similarity
function retrieveRelevantChunks(queryEmbedding, documentIndex, pdfFileName, topK = 5) {
    if (!documentIndex || !Array.isArray(documentIndex)) {
        console.error("Error: documentIndex is undefined or not an array in retrieveRelevantChunks.");
        throw new Error("documentIndex is not defined.");
    }

    // Filter chunks by PDF name to only retrieve from the current PDF
    const filteredChunks = documentIndex.filter(chunk => chunk.pdfFileName === pdfFileName);

    // Calculate cosine similarity for each filtered chunk
    const similarities = filteredChunks.map(({ chunk, embedding }) => ({
        chunk,
        similarity: cosineSimilarity(queryEmbedding, embedding),
    }));

    // Sort by similarity score
    similarities.sort((a, b) => b.similarity - a.similarity);

    return similarities.slice(0, topK).map((item) => item.chunk);
}

// Function to merge structured data
function mergeStructuredData(structuredDataList) {
    const mergedData = { ...examplePrefabElement };

    structuredDataList.forEach((data) => {
        for (const key in data) {
            if (Array.isArray(data[key])) {
                mergedData[key] = [...(mergedData[key] || []), ...data[key]];
            } else if (typeof data[key] === "object" && data[key] !== null) {
                mergedData[key] = { ...(mergedData[key] || {}), ...data[key] };
            } else {
                mergedData[key] = data[key] || mergedData[key];
            }
        }
    });

    return mergedData;
}

module.exports = {
    splitTextIntoChunks,
    preprocessAndIndexPDF,
    processChunks,
    mergeStructuredData,
    retrieveRelevantChunks,
};
