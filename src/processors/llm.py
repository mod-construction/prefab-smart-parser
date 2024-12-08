from typing import Dict, Optional, List
from langchain.chat_models import ChatOpenAI, ChatAnthropic
from langchain.prompts import ChatPromptTemplate
from langchain.output_parsers import PydanticOutputParser
from langchain.chains import LLMChain
from core.config import settings
from pydantic import BaseModel, Field

class ProductSpecification(BaseModel):
    name: str = Field(description="Product name")
    manufacturer: str = Field(description="Manufacturer name")
    dimensions: Dict = Field(description="Product dimensions")
    materials: List[str] = Field(description="List of materials used")
    technical_specs: Dict = Field(description="Technical specifications")
    certifications: List[str] = Field(description="Product certifications")

class LLMProcessor:
    def __init__(self):
        # Primary LLM for complex understanding
        self.primary_llm = ChatAnthropic(
            model="claude-3-opus-20240229",
            temperature=0.1,
            anthropic_api_key=settings.ANTHROPIC_API_KEY
        )
        
        # Secondary LLM for simpler tasks
        self.secondary_llm = ChatOpenAI(
            model="gpt-3.5-turbo",
            temperature=0.1,
            api_key=settings.OPENAI_API_KEY
        )

        self.output_parser = PydanticOutputParser(pydantic_object=ProductSpecification)

    async def process(self, text: str, use_primary: bool = True) -> Dict:
        """
        Process text using LLM to extract structured information
        
        Args:
            text: Input text to process
            use_primary: Whether to use primary (more powerful) LLM
        """
        prompt = ChatPromptTemplate.from_messages([
            ("system", """You are a construction industry expert specialized in prefab products. 
            Extract structured information from the provided text into a standardized format.
            Focus on technical specifications, dimensions, materials, and certifications.
            Format the output according to the specified schema."""),
            ("human", f"Text: {text}\nSchema: {self.output_parser.get_format_instructions()}")
        ])

        # Choose LLM based on complexity
        llm = self.primary_llm if use_primary else self.secondary_llm
        
        chain = LLMChain(llm=llm, prompt=prompt)
        
        try:
            # Process with error handling and retry logic
            result = await chain.arun(text)
            parsed_data = self.output_parser.parse(result)
            return parsed_data.dict()
        except Exception as e:
            # Fallback to secondary LLM if primary fails
            if use_primary:
                return await self.process(text, use_primary=False)
            raise Exception(f"LLM processing error: {str(e)}")

    async def validate(self, data: Dict) -> bool:
        """
        Validate extracted information using LLM
        
        Args:
            data: Extracted data to validate
        """
        validation_prompt = ChatPromptTemplate.from_messages([
            ("system", """You are a construction data validation expert.
            Verify that the provided data meets these criteria:
            1. All required fields are present and non-empty
            2. Dimensions and measurements are in standard units
            3. Technical specifications are complete and valid
            4. Material information is specific and clear
            Respond with a boolean indicating if the data is valid."""),
            ("human", f"Data to validate: {data}")
        ])

        # Use secondary LLM for validation to save costs
        chain = LLMChain(llm=self.secondary_llm, prompt=validation_prompt)
        result = await chain.arun(data)
        
        return "true" in result.lower()

    async def detect_language(self, text: str) -> str:
        """
        Detect the language of the input text
        
        Args:
            text: Input text
        Returns:
            ISO language code
        """
        # Use secondary LLM for language detection
        prompt = ChatPromptTemplate.from_messages([
            ("system", "Detect the language of the following text and respond with the ISO language code."),
            ("human", text[:500])  # Use first 500 chars for efficiency
        ])
        
        chain = LLMChain(llm=self.secondary_llm, prompt=prompt)
        return await chain.arun(text)