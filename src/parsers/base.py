from abc import ABC, abstractmethod
from typing import Any, Dict

class BaseParser(ABC):
    """Abstract base class for all parsers"""
    
    @abstractmethod
    async def parse(self, content: Any) -> Dict:
        """Parse the input content and return structured data"""
        pass

    @abstractmethod
    async def validate(self, data: Dict) -> bool:
        """Validate the parsed data"""
        pass 