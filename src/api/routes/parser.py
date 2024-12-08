from fastapi import APIRouter, UploadFile, File, HTTPException
from typing import Dict
from pipeline.coordinator import PipelineCoordinator
import logging

router = APIRouter()
logger = logging.getLogger(__name__)

@router.post("/parse/file")
async def parse_file(
    file: UploadFile = File(...),
    content_type: str = None
) -> Dict:
    """
    Parse a file and return structured mod-dlm data
    
    Args:
        file: Uploaded file
        content_type: Type of content (optional, will be auto-detected if not provided)
    Returns:
        Structured data in mod-dlm format
    """
    try:
        # Auto-detect content type if not provided
        if not content_type:
            content_type = _detect_content_type(file.filename)
        
        coordinator = PipelineCoordinator()
        result = await coordinator.process_document(file, content_type)
        
        return result
        
    except Exception as e:
        logger.error(f"Error processing file: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/parse/url")
async def parse_url(url: str) -> Dict:
    """
    Parse a URL and return structured mod-dlm data
    
    Args:
        url: URL to parse
    Returns:
        Structured data in mod-dlm format
    """
    try:
        coordinator = PipelineCoordinator()
        result = await coordinator.process_document(url, 'web')
        
        return result
        
    except Exception as e:
        logger.error(f"Error processing URL: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

def _detect_content_type(filename: str) -> str:
    """Detect content type from filename"""
    extension = filename.lower().split('.')[-1]
    content_types = {
        'pdf': 'pdf',
        'jpg': 'image',
        'jpeg': 'image',
        'png': 'image',
        'html': 'web',
        'htm': 'web'
    }
    return content_types.get(extension, 'unknown') 