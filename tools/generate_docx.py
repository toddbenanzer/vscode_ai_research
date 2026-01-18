import json
import argparse
import logging
from pathlib import Path
from typing import Dict, Any, List
from docx import Document
from docx.shared import Pt, RGBColor

# Constants
STYLE_TITLE = 'Heading 1'
STYLE_SUBTITLE = 'Subtitle'
STYLE_HEADING_2 = 'Heading 2'
STYLE_BULLET = 'List Bullet'
STYLE_NORMAL = 'Normal'

DEFAULT_CLASSIFICATION = "Internal Use Only"
DEFAULT_CONFIDENCE = "Unknown"
DIVIDER_LINE = "_" * 20

TEXT_KEY_POINTS = "Key Points"
TEXT_VISUAL_PREFIX = "[VISUAL DATA REQUEST: {}]"

logger = logging.getLogger(__name__)

def create_document(json_data: List[Dict[str, Any]], output_path: Path) -> None:
    """
    Creates a Word document from the provided JSON data.
    Follows 'Report Style': Speaker Notes are body text, Slides are highlights.
    """
    doc = Document()

    for slide_index, slide_data in enumerate(json_data):
        _add_slide_section(doc, slide_data, slide_index)

        # Add page break between sections
        if slide_index < len(json_data) - 1:
            doc.add_page_break()

    doc.save(output_path)
    logger.info(f"Document saved to: {output_path}")

def _add_slide_section(doc: Document, slide_data: Dict[str, Any], index: int) -> None:
    """
    Orchestrates adding a single slide's content to the document.
    """
    _add_title(doc, slide_data, index)
    _add_speaker_notes(doc, slide_data)
    _add_key_points(doc, slide_data)
    _add_visual_placeholder(doc, slide_data)
    _add_metadata(doc, slide_data)

def _add_title(doc: Document, slide_data: Dict[str, Any], index: int) -> None:
    """Adds the slide title and optional subtitle."""
    title = slide_data.get("title", f"Slide {index + 1}")
    layout = slide_data.get("layout", "")

    doc.add_heading(title, level=1)

    if layout == "title":
        subtitle = slide_data.get("subtitle")
        if subtitle:
            doc.add_paragraph(subtitle, style=STYLE_SUBTITLE)

def _add_speaker_notes(doc: Document, slide_data: Dict[str, Any]) -> None:
    """Adds speaker notes as the main body text."""
    notes = slide_data.get("speaker_notes", "")
    if notes:
        for paragraph in notes.split("\n"):
            if paragraph.strip():
                doc.add_paragraph(paragraph.strip())

def _add_key_points(doc: Document, slide_data: Dict[str, Any]) -> None:
    """Adds slide content (bullets/columns) as a highlighted list section."""
    content = slide_data.get("content", [])
    if not content:
        return

    doc.add_heading(TEXT_KEY_POINTS, level=2)

    for item in content:
        header = item.get("header")
        if header:
            p = doc.add_paragraph(header)
            p.runs[0].bold = True

        for bullet in item.get("bullets", []):
            doc.add_paragraph(bullet, style=STYLE_BULLET)

def _add_visual_placeholder(doc: Document, slide_data: Dict[str, Any]) -> None:
    """Adds a styled placeholder for requested visual data."""
    visual_desc = slide_data.get("visual_data_description")
    if visual_desc:
        p = doc.add_paragraph()
        runner = p.add_run(TEXT_VISUAL_PREFIX.format(visual_desc))
        runner.italic = True
        runner.font.color.rgb = RGBColor(100, 100, 100) # Gray

def _add_metadata(doc: Document, slide_data: Dict[str, Any]) -> None:
    """Adds governance metadata at the bottom of the section."""
    classification = slide_data.get("classification", DEFAULT_CLASSIFICATION)
    confidence = slide_data.get("data_confidence", DEFAULT_CONFIDENCE)
    sources = slide_data.get("source_references", [])
    source_text = ", ".join(sources) if sources else "None"

    doc.add_paragraph(DIVIDER_LINE)

    meta_text = f"Classification: {classification} | Confidence: {confidence} | Sources: {source_text}"
    meta_p = doc.add_paragraph()
    meta_p.add_run(meta_text).font.size = Pt(9)

def main() -> None:
    # Configure logging here to avoid import side effects
    logging.basicConfig(level=logging.INFO, format='%(message)s')

    parser = argparse.ArgumentParser(description="Generate Word Document from JSON source.")
    parser.add_argument("input_json", type=Path, help="Path to input JSON file.")
    parser.add_argument("--output", "-o", type=Path, help="Output path (default: input_filename.docx)")

    args = parser.parse_args()

    if not args.input_json.exists():
        logger.error(f"File not found: {args.input_json}")
        exit(1)

    # Determine output path
    output_path = args.output if args.output else args.input_json.with_suffix(".docx")

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
