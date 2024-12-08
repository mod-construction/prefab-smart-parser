from flask import Flask, request, jsonify
import base64
from flask_cors import CORS
import os
import json
from llm import define_model, llm_stack, extract_text_from_pdf, split_into_sentences, create_overlapping_chunks

app = Flask(__name__)
CORS(app)

def process_pdf_content(pdf_content):
    """
    Process the base64-encoded PDF content using the pipeline defined in llm.py.
    """
    try:
        decoded_pdf = base64.b64decode(pdf_content)
        temp_pdf_path = "temp.pdf"
        with open(temp_pdf_path, "wb") as f:
            f.write(decoded_pdf)

        pdf_text = extract_text_from_pdf(temp_pdf_path)
        sentences_list = split_into_sentences(pdf_text)
        chunks = create_overlapping_chunks(sentences_list)

        model = define_model()

        schema_outputs = []
        for index, chunk in enumerate(chunks):
            print(f"Processing chunk {index + 1}/{len(chunks)}...")
            llm_response = llm_stack(model, chunk)
            if llm_response:
                schema_outputs.append(llm_response)

        os.remove(temp_pdf_path)

        return schema_outputs
    except Exception as e:
        print(f"Error processing PDF content: {e}")
        raise

@app.route('/process_pdf', methods=['POST'])
def process_pdf_endpoint():
    """
    Endpoint to process PDF content and return the extracted JSON schema.
    """
    try:
        data = request.json
        file_content = data.get("fileContent", "")
        if file_content.startswith("data:application/pdf;base64,"):
            file_content = file_content.split(",", 1)[1]  # Remove the prefix
        if 'fileContent' not in data:
            #print('received data', data)
            return jsonify({"error": "Missing 'fileContent' in the request"}), 400

        pdf_content = file_content
        print("First 100 characters of the encoded text: \n",pdf_content[:100])  
        #print("Pdf content here:", pdf_content )
        schema_outputs = process_pdf_content(pdf_content)

        result_folder = "result"
        os.makedirs(result_folder, exist_ok=True)  # Ensure the folder exists
        result_file_path = os.path.join(result_folder, "output.json")
        with open(result_file_path, "w") as result_file:
            json.dump(schema_outputs, result_file, indent=4)
        print("schema output content here:", schema_outputs)
        return jsonify(schema_outputs), 200
    except Exception as e:
        print(f"Error processing PDF request: {e}")
        return jsonify({"error": "Failed to process PDF", "details": str(e)}), 500

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8080))
    app.run(host="0.0.0.0", port=port)
