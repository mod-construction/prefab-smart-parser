import json
from mod_dlm_schema import PrefabElement  # Importing schema
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
from langchain_community.chat_models import ChatOpenAI
from pydantic import ValidationError
import secret as shh

class LLMAgent:
    def __init__(self, api_key: str, output_file: str = "output.json"):
        """
        Initializes the LLMAgent with the OpenAI API key and output file.

        :param api_key: The API key for OpenAI.
        :param output_file: The file path to save the final JSON output.
        """
        self.api_key = api_key
        self.output_file = output_file

    def fill_schema_with_openai(self, schema: str, markdown: str) -> dict:
        """
        Use OpenAI GPT-4 to populate the schema based on the provided markdown content.

        :param schema: The JSON schema as a string.
        :param markdown: The markdown content to extract information from.
        :return: A dictionary representing the populated schema.
        """
        llm = ChatOpenAI(
            model="gpt-4",
            temperature=0,
            openai_api_key=self.api_key
        )

        # Define the prompt template
        # prompt = PromptTemplate(
        #     template="""
        #     You are given the following schema:
        #     {schema}

        #     From the provided markdown content:
        #     {markdown}

        #     Fill out the schema fields based on the markdown information. If any fields are missing, infer them logically, keeping the schema constraints in mind. Output the result strictly in JSON format matching the schema and put "unknown" for string fields, and for enum fields use the last of the available option, and for numerical fields put -1 if there is no information found.
        #     """,
        #     input_variables=["schema", "markdown"],
        # )

        prompt = PromptTemplate(
            template="""
            You are given the following schema:
            {schema}

            From the provided markdown content:
            {markdown}

            Fill out the schema fields based on the markdown information. If any fields are missing, infer them logically, keeping the schema constraints in mind. Output the result strictly in JSON format matching the schema.
            """,
            input_variables=["schema", "markdown"],
        )

        # Use RunnableSequence to chain the prompt and LLM
        sequence = prompt | llm

        # Generate the result
        result = sequence.invoke({"schema": schema, "markdown": markdown})
        return json.loads(result.content)

    def populate_and_validate_schema(self, markdown_content: str) -> dict:
        """
        Populate and validate the schema using the provided markdown content.

        :param markdown_content: The markdown content to extract information from.
        :return: A dictionary representing the validated schema.
        :raises: ValidationError if the data is invalid.
        """
        # Convert the PrefabElement schema to JSON for GPT-4
        prefab_schema = json.dumps(PrefabElement.model_json_schema())

        validated_data={}

        try:
            # Fill missing schema data using GPT-4
            populated_data = self.fill_schema_with_openai(prefab_schema, markdown_content)

            # Validate data against the PrefabElement schema
            validated_data = PrefabElement(**populated_data)

            print("Validation successful!")
        except ValidationError as e:
            print("Validation Error:", e.json())
           # raise e
            pass        
        except Exception as e:
            print("Error during GPT-4 processing:", e)
            #raise e
            pass

        return validated_data.dict()
       

    def save_json_to_file(self, data: dict):
        """
        Save the JSON data to the specified output file.

        :param data: The data to save.
        """
        with open(self.output_file, "w") as f:
            json.dump(data, f, indent=2)
        print(f"Schema populated and saved to {self.output_file}")

if __name__ == "__main__":
    # Initialize the agent with OpenAI API key and output file path
    api_key = shh.OPENAI_API_KEY
    agent = LLMAgent(api_key=api_key, output_file="output.json")

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