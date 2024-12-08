from typing import Union
from .pdf_parser import PDFParser
from .web_parser import WebParser
from .image_parser import ImageParser
from .base import BaseParser

class ParserFactory:
    @staticmethod
    def get_parser(content_type: str) -> BaseParser:
        """
        Factory method to get appropriate parser based on content type
        
        Args:
            content_type: Type of content to parse ('pdf', 'web', 'image')
        Returns:
            Instance of appropriate parser
        """
        parsers = {
            'pdf': PDFParser,
            'web': WebParser,
            'image': ImageParser
        }
        
        parser_class = parsers.get(content_type.lower())
        if not parser_class:
            raise ValueError(f"Unsupported content type: {content_type}")
            
        return parser_class() 