# PDF Table Extraction and JSON Generation

## **Description**

[This Python script](DataframesFromCharts3.py) extracts product tables from a PDF file, processes them into JSON files, and fills the JSON structure of based on an example template. It also utilizes OpenAI's GPT model to infer and generate the required JSON data.

## **Features**

Extract Tables from PDFs: Uses pdfplumber to extract tabular data from a PDF file.
Dynamic Prompt Generation: Creates prompts dynamically based on an example JSON structure and extracted table data.
Integration with OpenAI: Leverages OpenAI GPT models to fill JSON templates with inferred values.
Save JSON Outputs: Generates and saves a JSON file for each row in the extracted tables.
There is a  template json

## **Requirements**

Python 3.11 or later
Required Python libraries:

- pdfplumber
- pandas
- openai
- json