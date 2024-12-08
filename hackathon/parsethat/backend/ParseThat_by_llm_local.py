import json
from pydantic import ValidationError
from mod_dlm_schema import PrefabElement  # Importing schema
from transformers import AutoModelForCausalLM, AutoTokenizer
import bitsandbytes
import torch
from jsonformer import Jsonformer
from transformers import AutoTokenizer, AutoModelForCausalLM

class LLMAgent:
    def __init__(self, model_name: str = "meta-llama/Llama-3.2-1B-Instruct", output_file: str = "output.json"):
        """
        Initializes the LLMAgent with a Hugging Face model and tokenizer.

        :param model_name: The Hugging Face model to use.
        :param output_file: The file path to save the final JSON output.
        """
        
        self.output_file = output_file
        self.tokenizer = AutoTokenizer.from_pretrained(model_name)
        self.model = AutoModelForCausalLM.from_pretrained(  model_name,
                                                            device_map="auto",
                                                            load_in_4bit=True,
                                                            bnb_4bit_compute_dtype=torch.float16)
        self.json_schema  = {"type": "object",
                             "properties":[]
                            }

    def fill_schema_with_model(self, schema: str, markdown: str) -> dict:
        """
        Use a Hugging Face model to populate the schema based on the provided markdown content.

        :param schema: The JSON schema as a string.
        :param markdown: The markdown content to extract information from.
        :return: A dictionary representing the populated schema.
        """
        # First set the json schema
        try:
            self.json_schema["properties"] = json.loads(schema)
        except json.JSONDecodeError as e:
            print("Error loading the JSON schema. Please make sure it is formatted correctly.", e)
            return {}  # Return an empty dictionary on failure

        prompt = f"""
Generate a JSON object for the product specifications depicted as below. Convert the product sheet information provided in markdown into the structured JSON format as specified in the schema below. **Use the JSON fields exactly as described in the schema**. If a field is missing from the product sheet, omit it. Output only the JSON file without any comments or explanations. Use only the specified data types and options while filling in the JSON. Translate all fields to English if they are in a different language.
You are given the following JSON schema:
```json
{schema}
```

From the provided markdown content:
```
{markdown}
```
Fill out the schema fields based on the markdown information. If you cannot find any information about a field, you can skip it. Output the result strictly in JSON format matching the schema. Do not return a code output. Return a single JSON file.
"""
        ####
        # Alternative prompt:
        ####
#         prompt = f"""Generate a sample product information based on the following schema and product data sheet:
# {datasheet}"""


        jsonformer = Jsonformer(self.model, self.tokenizer, self.json_schema, prompt)
        response = jsonformer()
        # A sample response is available in ./llama.json
        # response = open("llama.json", "r").read()
        
        try:
            return json.loads(response)  # Parse the JSON output
        except json.JSONDecodeError as e:
            print("Error decoding JSON:", e)
            return {}  # Return an empty dictionary on failure

    def populate_and_validate_schema(self, markdown_content: str) -> dict:
        """
        Populate and validate the schema using the provided markdown content.

        :param markdown_content: The markdown content to extract information from.
        :return: A dictionary representing the validated schema.
        :raises: ValidationError if the data is invalid.
        """
        prefab_schema = json.dumps(PrefabElement.model_json_schema())

        try:
            # Fill missing schema data using the local model
            populated_data = self.fill_schema_with_model(prefab_schema, markdown_content)

            ## TODO: I haven't checked there unfortunately :\ that's a thing to do tomorrow.
            
            # Validate data against the PrefabElement schema
            validated_data = PrefabElement(**populated_data)
            print("Validation successful!")
            return validated_data.dict()
        except ValidationError as e:
            print("Validation Error:", e.json())
            return {}
        except Exception as e:
            print("Error during model processing:", e)
            return {}

    def save_json_to_file(self, data: dict):
        """
        Save the JSON data to the specified output file.

        :param data: The data to save.
        """
        with open(self.output_file, "w") as f:
            json.dump(data, f, indent=2)
        print(f"Schema populated and saved to {self.output_file}")

if __name__ == "__main__":
    # Initialize the agent with a Hugging Face model and output file path
    model_name = "meta-llama/Llama-3.2-1B-Instruct"  # Replace with your preferred model (e.g., "meta-llama/Llama-3.2-3B-Instruct")
    agent = LLMAgent(model_name=model_name, output_file="output.json")

    # Read markdown content
    markdown_file = "markup.md"
    with open(markdown_file, "r", encoding="utf-8") as f:
        markdown_content = f.read()

    # Populate, validate, and save the schema
    try:
        final_data = agent.populate_and_validate_schema(markdown_content)
        agent.save_json_to_file(final_data)
    except Exception as e:
        print(f"An error occurred: {e}")
