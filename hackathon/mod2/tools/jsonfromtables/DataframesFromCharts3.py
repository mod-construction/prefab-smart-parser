import pdfplumber
import pandas as pd
import openai
import json
import os

# OpenAI key
openai.api_key = 'YOUR_OPENAI_KEY'

# PDF Location
pdf_path = 'PdfTable/Test.pdf'

# Output folder
output_path = r"C:\Users\carme\Desktop\AEC Hackathon Munich\JsonOutputs" 

# Load JSON template from file
with open('examplejson.json', 'r') as file:
    jsonT = json.load(file)  # Load the JSON into a Python dictionary

def extract_tables_from_pdf(pdf_path):
    dataframes = {}
    
    # Open the PDF file
    with pdfplumber.open(pdf_path) as pdf:
        for page_number, page in enumerate(pdf.pages):
            # Extract tables from each page
            tables = page.extract_tables()
            
            if tables:
                for table_index, table in enumerate(tables):
                    table_name = f"page_{page_number + 1}_table_{table_index + 1}"
                    # Convert the extracted table into a pandas DataFrame
                    df = pd.DataFrame(table[1:], columns=table[0])
                    dataframes[table_name] = df
    
    return dataframes

# Usage
tables = extract_tables_from_pdf(pdf_path)
print(tables)
# Accessing a specific table
#print(tables.get("page_1_table_1").head())
testtable = tables.get("page_1_table_1")
#print(tables)

# GENERATE PROMPT
def generate_dynamic_prompt(json_sample, dataframe_sample):
    # Convert the JSON sample to a string for the prompt
    json_sample_str = json.dumps(json_sample, indent=4)

    # Convert the pandas DataFrame to a string
    if isinstance(dataframe_sample, pd.DataFrame):
        dataframe_str = dataframe_sample.to_string(index=False)  # Convert to string without row index
    else:
        dataframe_str = str(dataframe_sample)

    # Create the dynamic prompt
    prompt = f"Here is a sample JSON structure:\n{json_sample_str}\n"
    prompt = "Please generate a similar JSON object with the same structure as the example, but trying to fill the values extracted from the dataframe (translate attributes into english for cross reference) where possible, try to infer the values that can be used like measures to bounding box...etc , and the rest of the values empty. Your response should be just the json file, nothing else."
    prompt += f"\n\nHere is a sample table from the DataFrame:\n{dataframe_str}\n\n"

    return prompt


# Generate the dynamic prompt using a specific table (e.g., page_1_table_1)
#prompt = generate_dynamic_prompt(jsonT, tables.get("page_1_table_1"))

# Call the OpenAI API to generate similar data
#response = call_openai_api(prompt)

#print(response)

# Convert the JSON sample to a string for the prompt
json_sample_str = json.dumps(jsonT, indent=4)

def call_openai_api(txt_prompt):
    completion = openai.chat.completions.create(
        model="gpt-4",
        messages=[
            {
                "role": "system",
                "content": f"You are an assistant that processes PDF content into structured data. Always respond with valid JSON that conforms to the following schema:\n{json_sample_str}\nDo not add any additional comments, explanations, or strings that are not part of the JSON itself. Ensure the JSON structure is complete and valid."
            },
            {
                "role": "user",
                "content": txt_prompt,
            },
        ],
    )
    
    return(completion.choices[0].message.content)


#response = call_openai_api(prompt)
#print(response)


#Generate a json per row
def generate_jsons(df, jsons_path):
    counter = 0
    for _, row in df.iloc[1:].iterrows():
        
        print(row)
        #Generate prompt
        prompt = generate_dynamic_prompt(jsonT,row)

        #Generate json
        json_content= call_openai_api(prompt)
        # Parse the JSON string to a Python dictionary
        json_data = json.loads(json_content)

        # Format the JSON data into a properly indented string
        #formatted_json = json.dumps(json_data, indent=4)

        #Save Json
        extension = '.json'
        filename = str(counter) + extension

        # Ensure the folder exists
        os.makedirs(jsons_path, exist_ok=True)

        # Combine the folder path and file name to create the full file path
        file_path = os.path.join(jsons_path, filename)

        # Save the data as a JSON file
        with open(file_path, "w") as json_file:
            json.dump(json_data, json_file, indent=4)

        counter += 1

        print(f"JSON file saved at {file_path}")


# Iterate through each table in the dictionary
for table_name, df in tables.items():
    print(f"Processing table: {table_name}")
    
    # Call generate_jsons for each DataFrame
    generate_jsons(df, output_path)
