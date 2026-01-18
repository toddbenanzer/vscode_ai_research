import json
import argparse
import logging
from pathlib import Path
from docx import Document
from docx.shared import Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(message)s')
logger = logging.getLogger(__name__)

def create_document(json_data, output_path):
    """
    Creates a Word document from the provided JSON data.
    Follows 'Report Style': Speaker Notes are body text, Slides are highlights.
    """
    doc = Document()

    # Set up some styles (optional, relying on default styles is usually safer/easier)
    # We will use standard 'Heading 1', 'Normal', 'List Bullet', etc.

    for slide_index, slide_data in enumerate(json_data):
        _add_slide_section(doc, slide_data, slide_index)

        # Add a page break between slides to keep them distinct sections?
        # Or just a spacer? Use page break for clean separation of "Chapters".
        if slide_index < len(json_data) - 1:
            doc.add_page_break()

    doc.save(output_path)
    logger.info(f"Document saved to: {output_path}")

def _add_slide_section(doc, slide_data, index):
    """
    Adds a single slide's content to the document.
    """
    title = slide_data.get("title", f"Slide {index + 1}")
    layout = slide_data.get("layout", "")

    # 1. Title (Heading 1)
    doc.add_heading(title, level=1)

    # Subtitle (if Title slide)
    if layout == "title":
        subtitle = slide_data.get("subtitle")
        if subtitle:
            p = doc.add_paragraph(subtitle)
            p.style = "Subtitle"

    # 2. Body Text (Speaker Notes)
    notes = slide_data.get("speaker_notes", "")
    if notes:
        # Split by newlines to handle multiple paragraphs in notes
        for paragraph in notes.split("\n"):
            if paragraph.strip():
                doc.add_paragraph(paragraph.strip())
    else:
        # If no notes, maybe add a placeholder or just skip
        pass

    # 3. Slide Content (Highlights / Key Points)
    content = slide_data.get("content", [])
    if content:
        # Add a subhead for the visual content
        h2 = doc.add_heading("Key Points", level=2)

        for item in content:
            # Header for the block (e.g. column header)
            header = item.get("header")
            if header:
                p = doc.add_paragraph(header)
                p.runs[0].bold = True

            # Bullets
            for bullet in item.get("bullets", []):
                doc.add_paragraph(bullet, style='List Bullet')

    # 4. Visual Data Description
    visual_desc = slide_data.get("visual_data_description")
    if visual_desc:
        p = doc.add_paragraph()
        runner = p.add_run(f"[VISUAL DATA REQUEST: {visual_desc}]")
        runner.italic = True
        runner.font.color.rgb = RGBColor(100, 100, 100) # Gray

    # 5. Governance Metadata
    classification = slide_data.get("classification", "Internal Use Only")
    confidence = slide_data.get("data_confidence", "Unknown")
    sources = slide_data.get("source_references", [])
    source_text = ", ".join(sources) if sources else "None"

    # Add a separator and metadata
    doc.add_paragraph("_" * 20) # Divider
    meta_p = doc.add_paragraph()
    meta_p.add_run(f"Classification: {classification} | Confidence: {confidence} | Sources: {source_text}").font.size = Pt(9)


def main():
    parser = argparse.ArgumentParser(description="Generate Word Document from JSON source.")
    parser.add_argument("input_json", type=Path, help="Path to input JSON file.")
    parser.add_argument("--output", "-o", type=Path, help="Output path (default: input_filename.docx)")

    args = parser.parse_args()

    if not args.input_json.exists():
        logger.error(f"File not found: {args.input_json}")
        exit(1)

    # Determine output path
    if args.output:
        output_path = args.output
    else:
        output_path = args.input_json.with_suffix(".docx")

    try:
        with open(args.input_json, 'r', encoding='utf-8') as f:
            data = json.load(f)

        create_document(data, output_path)

    except json.JSONDecodeError as e:
        logger.error(f"Invalid JSON format: {e}")
        exit(1)
    except Exception as e:
        logger.error(f"An error occurred: {e}")
        exit(1)

if __name__ == "__main__":
    main()
