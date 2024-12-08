from typing import Dict, Any
import pytesseract
from PIL import Image
from io import BytesIO
from .base import BaseParser
from processors.llm import LLMProcessor

class ImageParser(BaseParser):
    def __init__(self):
        self.llm_processor = LLMProcessor()

    async def parse(self, content: BytesIO) -> Dict:
        """
        Parse image content and extract structured data
        
        Args:
            content: Image file as BytesIO object
        Returns:
            Dict containing extracted structured data
        """
        try:
            # Open image
            image = Image.open(content)
            
            # Perform OCR
            extracted_text = pytesseract.image_to_string(image)
            
            # Process with LLM
            structured_data = await self.llm_processor.process(extracted_text)
            
            return structured_data
            
        except Exception as e:
            raise Exception(f"Image parsing error: {str(e)}")

    async def validate(self, data: Dict) -> bool:
        """
        Validate the parsed data structure
        
        Args:
            data: Parsed data dictionary
        Returns:
            bool indicating if data is valid
        """
        return await self.llm_processor.validate(data) 