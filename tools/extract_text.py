import os
import sys
from pptx import Presentation
from docx import Document
from pypdf import PdfReader
from bs4 import BeautifulSoup

def extract_from_pptx(filepath):
    """Extracts text from slides and speaker notes in a PowerPoint file."""
    text_content = []
    try:
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
                text_content.append("\n[Speaker Notes]:")
                text_frame = notes_slide.notes_text_frame
                if text_frame:
                    text_content.append(text_frame.text)

            text_content.append("\n")

    except Exception as e:
        print(f"Error reading {filepath}: {e}")
        return None

    return "\n".join(text_content)

def extract_from_docx(filepath):
    """Extracts text from a Word document."""
    text_content = []
    try:
        doc = Document(filepath)
        for para in doc.paragraphs:
            text_content.append(para.text)
    except Exception as e:
        print(f"Error reading {filepath}: {e}")
        return None

    return "\n".join(text_content)

def extract_from_pdf(filepath):
    """Extracts text from a PDF file."""
    text_content = []
    try:
        reader = PdfReader(filepath)
        for i, page in enumerate(reader.pages):
            text_content.append(f"--- Page {i+1} ---")
            text_content.append(page.extract_text())
            text_content.append("\n")
    except Exception as e:
        print(f"Error reading {filepath}: {e}")
        return None

    return "\n".join(text_content)

def extract_from_html(filepath):
    """Extracts text from an HTML file."""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            soup = BeautifulSoup(f, 'html.parser')
            # remove scripts and styles
            for script in soup(["script", "style"]):
                script.decompose()
            text = soup.get_text(separator='\n')
            # break into lines and remove leading and trailing space on each
            lines = (line.strip() for line in text.splitlines())
            # break multi-headlines into a line each
            chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
            # drop blank lines
            text = '\n'.join(chunk for chunk in chunks if chunk)
            return text
    except Exception as e:
        print(f"Error reading {filepath}: {e}")
        return None

def process_directory(directory):
    """Scans the directory for supported files and extracts text."""
    supported_extensions = {
        '.pptx': extract_from_pptx,
        '.docx': extract_from_docx,
        '.pdf': extract_from_pdf,
        '.html': extract_from_html
    }

    print(f"Scanning {directory}...")

    count = 0
    for root, dirs, files in os.walk(directory):
        for file in files:
            ext = os.path.splitext(file)[1].lower()
            if ext in supported_extensions:
                filepath = os.path.join(root, file)
                print(f"Processing: {filepath}")

                extractor = supported_extensions[ext]
                extracted_text = extractor(filepath)

                if extracted_text is not None:
                    output_filename = os.path.splitext(file)[0] + ".txt"
                    output_path = os.path.join(root, output_filename)

                    with open(output_path, "w", encoding="utf-8") as f:
                        f.write(extracted_text)

                    print(f"Saved to: {output_path}")
                    count += 1

    print(f"Finished processing. Extracted text from {count} files.")

if __name__ == "__main__":
    # Default to workspace/sources if no argument provided
    target_dir = "workspace/sources"
    if len(sys.argv) > 1:
        target_dir = sys.argv[1]

    if not os.path.exists(target_dir):
        print(f"Directory not found: {target_dir}")
        sys.exit(1)

    process_directory(target_dir)
