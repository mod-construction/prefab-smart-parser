import os
import time
import openai
from flask import Flask, request, jsonify
from dotenv import load_dotenv
from openai import OpenAI
from flask_cors import CORS

# Load environment variables
load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")
app = Flask(__name__)
CORS(app)
client = OpenAI()
assistant_id = None
assistant_thread_id = None
json_file_id=0
pdf_file_id=0
vector_Store_id=0
vector_store = client.beta.vector_stores.create(name="Json Format")

@app.route('/upload_json', methods=['POST'])
def upload_json():
    json_file = request.files['json_file']
    json_path = os.path.join('uploads', json_file.filename)
    json_file.save(json_path)

    with open(json_path, "rb") as file_data:
        file = client.files.create(file=file_data, purpose="assistants")
        file_batch = client.beta.vector_stores.file_batches.upload_and_poll(vector_store_id=vector_store.id, files=file)
        json_file_id=file.id
        vector_Store_id=file_batch.id

    return jsonify({"message": "JSON file uploaded", "file_id": file.id})


@app.route('/upload_pdf', methods=['POST'])
def upload_pdf():
    pdf_file = request.files['pdf_file']
    pdf_path = os.path.join('uploads', pdf_file.filename)
    pdf_file.save(pdf_path)
    with open(pdf_path, "rb") as file_data:
        file = client.files.create(file=file_data, purpose="assistants")
        pdf_file_id=file.id
    return jsonify({"message": "PDF file uploaded", "file_id": file.id})
@app.route('/process_files', methods=['POST'])
def process_files():
    purpose = """Your job is to extract the data from PDF and fill the provided JSON format with only the information in the PDF provided.
    No invention and elaboration of data is acceptable.
    1. First, classify each datasheet into high-level categories (buildingSystem and productCategory) as per the schema to make sure it's relevant to the schema.
    2. Ensure accuracy by adhering strictly to the schema and PDF content only.
    """
    assistant = client.beta.assistants.create(
        name=f"mod test 1",
        instructions=purpose,
        model="gpt-4o-mini",
        tools=[{"type": "file_search"}],
        tool_resources={"file_search": {"vector_store_ids": [vector_store.id]}}
    )
    assistant_id = assistant.id
    new_thread = client.beta.threads.create()
    assistant_thread_id = new_thread.id
    instructions = """process the data in the attached PDF and add it to the attached JSON Format, please stick to the same data types and schema of the json format and to the data that's in the PDF,
    your output should be JSON only with no additional text, and please translate all the values to english if it's not English,
    for the ID please use an online UUID generator to fill it"""
    client.beta.threads.messages.create(
         thread_id=assistant_thread_id,
         role="user",
         content=instructions,
         attachments=[
            {"file_id": pdf_file_id, "tools": [{"type": "file_search"}]},
            {"file_id": json_file_id, "tools": [{"type": "file_search"}]}
        ]
    )
    run = client.beta.threads.runs.create(thread_id=assistant_thread_id, assistant_id=assistant_id)
    run = client.beta.threads.runs.retrieve(thread_id=assistant_thread_id, run_id=run.id)
    while run.status not in ["completed", "failed", "canceled"]:
        time.sleep(5)
        run = client.beta.threads.runs.retrieve(thread_id=assistant_thread_id, run_id=run.id)
    messages = client.beta.threads.messages.list(thread_id=assistant_thread_id)
    for message in reversed(messages.data):
        print(message.role + ": " + message.content[0].text.value)
    answer = messages.data[0].content[0].text.value
    return jsonify({"result": answer})
if not os.path.exists('uploads'):
    os.makedirs('uploads')


if __name__ == '__main__':
    #app.run(debug=True)
    port = int(os.environ.get("PORT", 8081))
    app.run(host="0.0.0.0", port=port)
