import argparse
import logging
from pathlib import Path
from typing import Optional

from pptx import Presentation
from docx import Document
from pypdf import PdfReader
from bs4 import BeautifulSoup

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(message)s')
logger = logging.getLogger(__name__)

def extract_from_pptx(filepath: Path) -> str:
    """Extracts text from slides and speaker notes in a PowerPoint file."""
    text_content = []
    prs = Presentation(filepath)
    for i, slide in enumerate(prs.slides):
        text_content.append(f"--- Slide {i+1} ---")

        # Extract text from shapes
        for shape in slide.shapes:
            if shape.has_text_frame:
                text_content.append(shape.text_frame.text)

        # Extract text from notes
        if slide.has_notes_slide:
            notes_slide = slide.notes_slide
            text_frame = notes_slide.notes_text_frame
            if text_frame:
                text_content.append("\n[Speaker Notes]:")
                text_content.append(text_frame.text)

        text_content.append("\n")

    return "\n".join(text_content)

def extract_from_docx(filepath: Path) -> str:
    """Extracts text from a Word document."""
    doc = Document(filepath)
    return "\n".join(para.text for para in doc.paragraphs)

def extract_from_pdf(filepath: Path) -> str:
    """Extracts text from a PDF file."""
    text_content = []
    reader = PdfReader(filepath)
    for i, page in enumerate(reader.pages):
        text_content.append(f"--- Page {i+1} ---")
        text_content.append(page.extract_text())
        text_content.append("\n")
    return "\n".join(text_content)

def extract_from_html(filepath: Path) -> str:
    """Extracts text from an HTML file."""
    with filepath.open('r', encoding='utf-8') as f:
        soup = BeautifulSoup(f, 'html.parser')
        # remove scripts and styles
        for script in soup(["script", "style"]):
            script.decompose()
        return soup.get_text(separator='\n', strip=True)

# Map extensions to extractor functions
SUPPORTED_EXTENSIONS = {
    '.pptx': extract_from_pptx,
    '.docx': extract_from_docx,
    '.pdf': extract_from_pdf,
    '.html': extract_from_html
}

def process_directory(directory: Path):
    """Scans the directory for supported files and extracts text."""
    logger.info(f"Scanning {directory}...")

    count = 0
    # Recursive scan
    for filepath in directory.rglob('*'):
        if filepath.suffix.lower() in SUPPORTED_EXTENSIONS:
            logger.info(f"Processing: {filepath}")

            extractor = SUPPORTED_EXTENSIONS[filepath.suffix.lower()]

            try:
                extracted_text = extractor(filepath)

                output_path = filepath.with_suffix('.txt')
                output_path.write_text(extracted_text, encoding='utf-8')

                logger.info(f"Saved to: {output_path}")
                count += 1

            except Exception as e:
                logger.error(f"Error reading {filepath}: {e}")

    logger.info(f"Finished processing. Extracted text from {count} files.")

def main():
    parser = argparse.ArgumentParser(description="Extract raw text from documents (PPTX, DOCX, PDF, HTML).")
    parser.add_argument("directory", nargs="?", default="workspace/sources", help="Directory to scan (default: workspace/sources)")
    args = parser.parse_args()

    target_dir = Path(args.directory)

    if not target_dir.exists():
        logger.error(f"Directory not found: {target_dir}")
        exit(1)

    process_directory(target_dir)

if __name__ == "__main__":
    main()
