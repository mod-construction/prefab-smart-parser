from typing import Dict, Any
import aiohttp
from bs4 import BeautifulSoup
from .base import BaseParser
from processors.llm import LLMProcessor

class WebParser(BaseParser):
    def __init__(self):
        self.llm_processor = LLMProcessor()

    async def parse(self, url: str) -> Dict:
        """
        Parse web content and extract structured data
        
        Args:
            url: Web page URL to parse
        Returns:
            Dict containing extracted structured data
        """
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(url) as response:
                    html = await response.text()
                    
            # Parse HTML
            soup = BeautifulSoup(html, 'html.parser')
            
            # Remove script and style elements
            for script in soup(["script", "style"]):
                script.decompose()
                
            # Extract text
            text = soup.get_text(separator='\n', strip=True)
            
            # Process with LLM
            structured_data = await self.llm_processor.process(text)
            
            return structured_data
            
        except Exception as e:
            raise Exception(f"Web parsing error: {str(e)}")

    async def validate(self, data: Dict) -> bool:
        """
        Validate the parsed data structure
        
        Args:
            data: Parsed data dictionary
        Returns:
            bool indicating if data is valid
        """
        return await self.llm_processor.validate(data) 