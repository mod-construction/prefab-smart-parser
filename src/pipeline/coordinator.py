from typing import Dict, Union, BinaryIO
import json
from pathlib import Path
from fastapi import UploadFile
from parsers.factory import ParserFactory
from processors.llm import LLMProcessor
from processors.nlp import NLPProcessor
from transformers.mod_dlm import ModDLMTransformer
from core.config import settings
import logging

logger = logging.getLogger(__name__)

class PipelineCoordinator:
    def __init__(self):
        self.parser_factory = ParserFactory()
        self.llm_processor = LLMProcessor()
        self.nlp_processor = NLPProcessor()
        self.transformer = ModDLMTransformer()

    async def process_document(
        self,
        content: Union[UploadFile, str, bytes, BinaryIO],
        content_type: str
    ) -> Dict:
        """
        Process a document through the complete pipeline
        
        Args:
            content: Document content (file, URL, or raw content)
            content_type: Type of content ('pdf', 'web', 'image')
        Returns:
            JSON-compatible dictionary in mod-dlm format
        """
        try:
            # 1. Parse the document
            parser = self.parser_factory.get_parser(content_type)
            parsed_data = await parser.parse(content)
            logger.info(f"Document parsed successfully: {len(parsed_data)} characters extracted")

            # 2. Process with NLP
            nlp_results = await self.nlp_processor.process(parsed_data)
            logger.info("NLP processing completed")

            # 3. Process with LLM
            llm_results = await self.llm_processor.process(parsed_data)
            logger.info("LLM processing completed")

            # 4. Combine results
            extracted_data = self._merge_results(nlp_results, llm_results)
            logger.info("Results merged successfully")

            # 5. Transform to mod-dlm format
            mod_dlm_object = await self.transformer.transform(extracted_data)
            logger.info("Transformation to mod-dlm completed")

            # 6. Convert to JSON-compatible dictionary
            result = mod_dlm_object.model_dump(exclude_none=True)
            
            # 7. Save result if configured
            if settings.SAVE_RESULTS:
                await self._save_result(result)

            return result

        except Exception as e:
            logger.error(f"Pipeline error: {str(e)}")
            raise

    def _merge_results(self, nlp_results: Dict, llm_results: Dict) -> Dict:
        """
        Merge results from NLP and LLM processors
        
        Args:
            nlp_results: Results from NLP processing
            llm_results: Results from LLM processing
        Returns:
            Merged dictionary of results
        """
        merged = {}

        # Prefer LLM results for overlapping keys
        merged.update(nlp_results)
        merged.update(llm_results)

        # Merge measurements
        if 'measurements' in nlp_results and 'measurements' in llm_results:
            merged['measurements'] = {
                **nlp_results['measurements'],
                **llm_results['measurements']
            }

        # Merge materials
        if 'materials' in nlp_results and 'materials' in llm_results:
            merged['materials'] = list({
                *nlp_results['materials'],
                *llm_results['materials']
            })

        return merged

    async def _save_result(self, result: Dict) -> None:
        """
        Save the result to a file
        
        Args:
            result: Processed result dictionary
        """
        output_dir = Path(settings.OUTPUT_DIR)
        output_dir.mkdir(exist_ok=True)
        
        filename = f"mod_dlm_{result.get('id', 'unknown')}.json"
        output_path = output_dir / filename
        
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(result, f, indent=2, ensure_ascii=False)
        
        logger.info(f"Result saved to {output_path}") 