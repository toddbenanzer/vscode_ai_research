import argparse
import logging
from pathlib import Path

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

def extract_text(filepath: Path) -> str:
    """
    Extracts text from the given file based on its extension.
    Raises ValueError if the file extension is not supported.
    """
    ext = filepath.suffix.lower()
    if ext not in SUPPORTED_EXTENSIONS:
        raise ValueError(f"Unsupported file type: {ext}")

    return SUPPORTED_EXTENSIONS[ext](filepath)

def save_text_file(filepath: Path, text: str):
    """Saves the extracted text to a .txt file in the same directory."""
    output_path = filepath.with_suffix('.txt')
    output_path.write_text(text, encoding='utf-8')
    logger.info(f"Saved to: {output_path}")

def process_file(filepath: Path):
    """Process a single file."""
    if filepath.suffix.lower() not in SUPPORTED_EXTENSIONS:
        return

    logger.info(f"Processing: {filepath}")
    try:
        extracted_text = extract_text(filepath)
        save_text_file(filepath, extracted_text)
    except Exception as e:
        logger.error(f"Error reading {filepath}: {e}")

def process_directory(directory: Path):
    """Scans the directory for supported files and extracts text."""
    logger.info(f"Scanning {directory}...")

    count = 0
    # Recursive scan
    for filepath in directory.rglob('*'):
        if filepath.is_file() and filepath.suffix.lower() in SUPPORTED_EXTENSIONS:
            process_file(filepath)
            count += 1

    logger.info(f"Finished processing. Extracted text from {count} files.")

def main():
    parser = argparse.ArgumentParser(description="Extract raw text from documents (PPTX, DOCX, PDF, HTML).")
    parser.add_argument("path", nargs="?", default="workspace/sources", help="File or Directory to scan (default: workspace/sources)")
    args = parser.parse_args()

    target_path = Path(args.path)

    if not target_path.exists():
        logger.error(f"Path not found: {target_path}")
        exit(1)

    if target_path.is_file():
        process_file(target_path)
    elif target_path.is_dir():
        process_directory(target_path)
    else:
        logger.error(f"Invalid path type: {target_path}")
        exit(1)

if __name__ == "__main__":
    main()
