const axios = require("axios");
const OPENAI_API_KEY = "YOUR_API_KEY";

// Function to generate an embedding for a given text using OpenAI's API
async function generateEmbedding(text) {
    try {
        const response = await axios.post(
            "https://api.openai.com/v1/embeddings",
            {
                model: "text-embedding-ada-002",
                input: text,
            },
            {
                headers: {
                    Authorization: `Bearer ${OPENAI_API_KEY}`,
                    "Content-Type": "application/json",
                },
            }
        );

        return response.data.data[0].embedding;
    } catch (error) {
        console.error("Error generating embedding:", error.message);
        throw error;
    }
}

// Function to calculate cosine similarity between two vectors
function cosineSimilarity(vecA, vecB) {
    const dotProduct = vecA.reduce((sum, a, idx) => sum + a * vecB[idx], 0);
    const magnitudeA = Math.sqrt(vecA.reduce((sum, a) => sum + a * a, 0));
    const magnitudeB = Math.sqrt(vecB.reduce((sum, b) => sum + b * b, 0));
    return dotProduct / (magnitudeA * magnitudeB);
}

module.exports = { generateEmbedding, cosineSimilarity };
