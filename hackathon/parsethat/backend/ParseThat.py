import os
from ParseThat_pdf import ParseThat_PDF_Agent
from ParseThat_by_llm import LLMAgent
import secret as shh  # For accessing API key

class ParseThat:
    def __init__(self):
        """
        Initializes the ParseThat workflow.
        """
        self.pdf_agent = ParseThat_PDF_Agent()
        self.llm_agent = LLMAgent(api_key=shh.OPENAI_API_KEY)

    def process_pdf(self, pdf_path: str):
        """
        Processes a PDF file: converts it to Markdown, passes it to the LLMAgent,
        and generates a JSON output with the same name as the PDF.

        :param pdf_path: Path to the input PDF file.
        """
        # Step 1: Parse the PDF and extract content
        print(f"Processing PDF: {pdf_path}")
        self.pdf_agent.parse(pdf_path)

        # Step 2: Save the extracted content as Markdown
        markdown_folder = os.path.splitext(pdf_path)[0]
        markdown_file = os.path.join(markdown_folder, f"{os.path.basename(markdown_folder)}.md")
        self.pdf_agent.save(pdf_path, save_fulltext=True, save_images=False, save_metadata=False)

        # Step 3: Read the generated Markdown content
        print(f"Reading generated Markdown file: {markdown_file}")
        with open(markdown_file, "r", encoding="utf-8") as md_file:
            markdown_content = md_file.read()

        # Step 4: Pass the Markdown content to LLMAgent for JSON generation
        print("Using LLMAgent to generate JSON output.")
        output_json_path = os.path.splitext(pdf_path)[0] + ".json"
        try:
            json_data = self.llm_agent.populate_and_validate_schema(markdown_content)
            self.llm_agent.save_json_to_file(json_data)
            print(f"JSON output saved at: {output_json_path}")
            return json_data
        except Exception as e:
            print(f"An error occurred during JSON generation: {e}")

def wrapper(pdf_fp):
    # Example usage
    pdf_file_path = pdf_fp # Replace with the actual path to the PDF
    parser = ParseThat()
    response= parser.process_pdf(pdf_file_path)
    print(response)
    return response

if __name__ == "__main__":
    wrapper("LORENZ_Datenblatt_DD18_60_2210.pdf")
