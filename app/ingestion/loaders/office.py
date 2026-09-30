import logging
logger = logging.getLogger(__name__)
from unstructured.partition.auto import partition

def parse_office(file_path: str):
    """
    Parses Office documents (.docx, .pptx) using the Unstructured library.
    Unlike PDFs, these formats are structured and lightweight, so they are processed locally.
    """
    if True:  # observability stripped
        try:
            # Unstructured automatically detects if it's docx or pptx
            elements = partition(filename=file_path)
            full_text = "\n".join([str(el) for el in elements])
            
            if not full_text.strip():
                logger.warning(f"⚠️ Unstructured returned empty text for {file_path}")
            else:
                logger.info(f"✅ Successfully parsed {len(full_text)} characters")

            return full_text
        except Exception as e:
            logger.error(f"❌ Office Parse Failed: {e}")
            raise e
