from langchain_core.output_parsers import JsonOutputParser
from langchain_core.prompts import PromptTemplate
from langchain_core.pydantic_v1 import BaseModel, Field
from langchain_openai import ChatOpenAI
from dotenv import load_dotenv
from preprocess.py import extract_text_from_pdf, split_into_sentences, create_overlapping_chunks

import PyPDF2

def extract_text_from_pdf(pdf_path):
    with open(pdf_path, "rb") as file:
        pdf_reader = PyPDF2.PdfReader(file)
        all_text = ""
        for page_num in range(len(pdf_reader.pages)):
            page = pdf_reader.pages[page_num]
            page_text = page.extract_text()
            all_text += page_text if page_text else ""
    
    return all_text

pdf_file_path = "Data/2024_Glossary_Template.pdf"
pdf_text = extract_text_from_pdf(pdf_file_path)
print(pdf_text)

def split_into_sentences(text):
    # Use regex to split text at sentence-ending punctuation marks followed by a space
    sentence_list = re.split(r'(?<=[.!?]) +', text)
    return sentence_list

# sente
# print(sentence_list)

load_dotenv()

model = ChatOpenAI(temperature=1)

# Define your desired data structure.
class Joke(BaseModel):
    individual_related: str = Field(description="Just write individual related information like university name etc")
    #punchline: str = Field(description="answer to resolve the joke")

# And a query intented to prompt a language model to populate the data structure.
joke_query = "Tell me a joke."

# Set up a parser + inject instructions into the prompt template.
parser = JsonOutputParser(pydantic_object=Joke)

prompt = PromptTemplate(
    template="Answer the user query.\n{format_instructions}\n{query}\n",
    input_variables=["query"],
    partial_variables={"format_instructions": parser.get_format_instructions()},
)

chain = prompt | model | parser

result = chain.invoke({"query": pdf_text})

print(result)

setup = result['setup']

print("Setup value from dict: ", setup)

if __name__ == "__main__":
    pdf_file_path = "Data/2024_Glossary_Template.pdf"
    pdf_text = extract_text_from_pdf(pdf_file_path)
    sentences_list = split_into_sentences(pdf_text)
    chunks = create_overlapping_chunks(sentences_list)

    for index, chunk in enumerate(chunks):
        print(f"Chunk {index}: {chunk}")