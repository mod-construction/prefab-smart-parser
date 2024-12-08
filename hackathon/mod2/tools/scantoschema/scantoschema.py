import json
import re
from PyPDF2 import PdfReader
from openai import OpenAI  # Replace with your GPT-4 or equivalent API


def extract_text_from_pdf(pdf_path):
    """
    Extracts all text from a given PDF file.
    """
    with open(pdf_path, 'rb') as file:
        reader = PdfReader(file)
        text = ""
        for page in reader.pages:
            text += page.extract_text()
        return text


def find_unique_keywords(pdf_text, datamodel):
    """
    Finds keywords in the PDF text that are not part of the datamodel.
    """

    def flatten_json(y):
        out = {}

        def flatten(x, name=''):
            if isinstance(x, dict):
                for key in x:
                    flatten(x[key], f"{name}{key}.")
            elif isinstance(x, list):
                for i, item in enumerate(x):
                    flatten(item, f"{name}{i}.")
            else:
                out[name[:-1]] = x

        flatten(y)
        return out

    datamodel_keys = set(flatten_json(datamodel).keys())
    pdf_keywords = set(re.findall(r'\b\w+\b', pdf_text.lower()))
    return pdf_keywords - datamodel_keys


def ask_ai_for_relevance(keyword, context, model="gpt-4"):
    """
    Uses AI to determine if a keyword is crucial for the AEC industry based on its context.
    """
    prompt = f"""
    You are an expert in the Architecture, Engineering, and Construction (AEC) industry. 
    Analyze the following information and determine if it is crucial for the AEC industry.
    If it is relevant, explain why; otherwise, indicate it is not relevant.

    Keyword: {keyword}
    Context: {context}
    """
    # Replace with your OpenAI API call
    response = OpenAI.Completion.create(
        model=model,
        prompt=prompt,
        temperature=0.3,
        max_tokens=150
    )
    return response['choices'][0]['text'].strip()


def extract_relevant_info(pdf_text, datamodel):
    """
    Extracts AEC-relevant information by comparing keywords in the PDF against the datamodel,
    and using AI to assess their relevance.
    """
    extra_info = {}
    unique_keywords = find_unique_keywords(pdf_text, datamodel)

    for keyword in unique_keywords:
        # Find sentences containing the keyword
        matches = re.findall(rf'([^.]*\b{keyword}\b[^.]*)\.', pdf_text, re.IGNORECASE)
        for match in matches:
            # Ask AI if this keyword and its context are relevant
            relevance = ask_ai_for_relevance(keyword, match)
            if "relevant" in relevance.lower():
                extra_info[keyword] = {
                    "context": match,
                    "aiAnalysis": relevance
                }
    return {"extra": extra_info}


def generate_json_with_ai_relevance(pdf_path, json_path, datamodel):
    """
    Reads a PDF, extracts AEC-relevant data using AI, and writes it to a JSON file.
    """
    # Extract text from the PDF
    pdf_text = extract_text_from_pdf(pdf_path)

    # Extract AEC-relevant information
    extracted_data = extract_relevant_info(pdf_text, datamodel)

    # Write the extracted data to a JSON file
    with open(json_path, 'w') as json_file:
        json.dump(extracted_data, json_file, indent=4)
    print(f"JSON file with extra information created at: {json_path}")


# Example datamodel (adjust to your needs)
datamodel = {
    "id": "4dd643ff-7ec7-4666-9c88-50b7d3da34e4",
    "name": "Structural Insulated Panel",
    "description": "SIP panel with OSB facings and insulating foam core for structural wall applications",
    "boundingBox": {
        "width": 1220,
        "height": 2440,
        "depth": 165
    },
    "material": {
        "finishMaterial": "Timber",
        "structuralMaterial": "Hybrid"
    },
    "structuralProperties": {
        "loadBearingCapacity": {
            "maximumLoad": 0,
            "unit": "kN"
        }
    }
}
import os

current_dir = r"C:\Users\Kaamil\OneDrive\Documents\AEC_Hackathon_MOD2\pdfs"
file_names = os.listdir(current_dir)

for file in file_names:
    try:
        input_pdf_path = os.path.join(current_dir, file)
        output_json_path = os.path.join(current_dir, file.split(".")[0] + ".json")
        generate_json_with_extra(input_pdf_path, output_json_path, datamodel)
    except:
        print(f"check this pdf{file}")

# print("its over")
## Example usage
# input_pdf_path = "/mnt/data/Datenblatt_Akustikschaumstoff.pdf"
# output_json_path = "/mnt/data/extra_aec_information.json"
# generate_json_with_ai_relevance(input_pdf_path, output_json_path, datamodel)
