import logging
logger = logging.getLogger(__name__)
from pypdf import PdfReader


def parse_pdf(file_path: str) -> str:
    """
    Extract text from a PDF locally using pypdf.
    Falls back to pdfplumber for pages that yield no text (e.g. image-heavy pages).
    """
    if True:  # observability stripped
        try:
            reader = PdfReader(file_path)
            total_pages = len(reader.pages)
            logger.info(f"PDF has {total_pages} pages.")

            text_parts: list[str] = []
            blank_pages: list[int] = []

            for i, page in enumerate(reader.pages):
                text = page.extract_text() or ""
                if text.strip():
                    text_parts.append(text)
                else:
                    blank_pages.append(i + 1)

            # Fallback: use pdfplumber for any pages pypdf returned blank
            if blank_pages:
                logger.info(f"pypdf returned blank on pages {blank_pages} — retrying with pdfplumber.")
                try:
                    import pdfplumber
                    with pdfplumber.open(file_path) as pdf:
                        for page_num in blank_pages:
                            page = pdf.pages[page_num - 1]
                            fallback_text = page.extract_text() or ""
                            if fallback_text.strip():
                                text_parts.append(fallback_text)
                except Exception as plumber_err:
                    logger.warning(f"pdfplumber fallback failed: {plumber_err}")

            full_text = "\n".join(text_parts)

            if not full_text.strip():
                logger.warning(f"No text extracted from {file_path}. File may be fully image-based.")
            else:
                logger.info(f"Extracted {len(full_text)} characters from {file_path}.")

            return full_text

        except Exception as e:
            logger.error(f"PDF Parse Failed for {file_path}: {e}")
            raise
