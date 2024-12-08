from typing import Dict, Any
import PyPDF2
from io import BytesIO
from .base import BaseParser
from processors.llm import LLMProcessor

class PDFParser(BaseParser):
    def __init__(self):
        self.llm_processor = LLMProcessor()

    async def parse(self, content: BytesIO) -> Dict:
        """
        Parse PDF content and extract structured data
        
        Args:
            content: PDF file as BytesIO object
        Returns:
            Dict containing extracted structured data
        """
        try:
            # Read PDF content
            pdf_reader = PyPDF2.PdfReader(content)
            extracted_text = []
            
            # Extract text from each page
            for page in pdf_reader.pages:
                text = page.extract_text()
                extracted_text.append(text)
            
            # Combine all text
            full_text = "\n".join(extracted_text)
            
            # Process with LLM
            structured_data = await self.llm_processor.process(full_text)
            
            return structured_data
            
        except Exception as e:
            raise Exception(f"PDF parsing error: {str(e)}")

    async def validate(self, data: Dict) -> bool:
        """
        Validate the parsed data structure
        
        Args:
            data: Parsed data dictionary
        Returns:
            bool indicating if data is valid
        """
        return await self.llm_processor.validate(data) 