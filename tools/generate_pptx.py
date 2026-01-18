import json
import argparse
import logging
from pathlib import Path
from typing import Any

from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.enum.text import PP_ALIGN
from pptx.enum.shapes import MSO_SHAPE
from pptx.dml.color import RGBColor

# Configure logging
logger = logging.getLogger(__name__)

# --- CONSTANTS ---
# Standard Layout Indices (Default Template)
LAYOUT_TITLE = 0
LAYOUT_TITLE_CONTENT = 1
LAYOUT_SECTION = 2
LAYOUT_TITLE_ONLY = 5

LAYOUT_MAP = {
    "title": LAYOUT_TITLE,
    "section": LAYOUT_SECTION,
    "bulleted": LAYOUT_TITLE_CONTENT,
    "2_col": LAYOUT_TITLE_ONLY,
    "3_col": LAYOUT_TITLE_ONLY,
    "4_col": LAYOUT_TITLE_ONLY
}

# Dimensions & Fonts
MARGIN_HORIZONTAL = Inches(0.5)
MARGIN_TOP = Inches(2.0)  # Room for Title
MARGIN_BOTTOM = Inches(1.0)
GAP_WIDTH = Inches(0.2)
FONT_SIZE_HEADER = Pt(18)
FONT_SIZE_BODY = Pt(14)
FONT_SIZE_VISUAL = Pt(12)
BULLET_CHAR = "• "

# Visual Placeholder Colors
COLOR_GRAY_FILL = RGBColor(200, 200, 200)
COLOR_GRAY_LINE = RGBColor(100, 100, 100)


def create_presentation(json_data: list[dict[str, Any]], output_path: Path):
    """
    Creates a PowerPoint presentation from the provided JSON data.
    """
    prs = Presentation()

    for slide_data in json_data:
        layout_name = slide_data.get("layout", "bulleted")
        layout_idx = LAYOUT_MAP.get(layout_name, LAYOUT_TITLE_CONTENT)

        slide_layout = prs.slide_layouts[layout_idx]
        slide = prs.slides.add_slide(slide_layout)

        # 1. Handle Title and Subtitle
        if slide.shapes.title:
            slide.shapes.title.text = slide_data.get("title", "")

        if layout_name == "title" and len(slide.placeholders) > 1:
            slide.placeholders[1].text = slide_data.get("subtitle", "")

        # 2. Handle Content
        content = slide_data.get("content", [])

        if layout_name in ["2_col", "3_col", "4_col"]:
            num_cols = int(layout_name.split("_")[0])
            _handle_column_layout(slide, content, num_cols, prs.slide_width, prs.slide_height)
        elif layout_name == "bulleted":
            _handle_standard_layout(slide, content)

        # 3. Handle Visual Data Description
        visual_desc = slide_data.get("visual_data_description")
        if visual_desc:
            _add_visual_placeholder(slide, visual_desc, prs.slide_width, prs.slide_height)

        # 4. Handle Speaker Notes & Metadata
        _add_notes_and_metadata(slide, slide_data)

    prs.save(output_path)
    logger.info(f"Presentation saved to: {output_path}")


def _handle_standard_layout(slide, content: list[dict[str, Any]]):
    """Handles standard bulleted content using the template's placeholder."""
    if not content or len(slide.placeholders) < 2:
        return

    tf = slide.placeholders[1].text_frame
    tf.clear()

    item = content[0]
    for bullet in item.get("bullets", []):
        p = tf.add_paragraph()
        p.text = bullet
        p.level = 0


def _handle_column_layout(slide, content: list[dict[str, Any]], num_cols: int, slide_width: int, slide_height: int):
    """Programmatically creates text boxes for multi-column layouts."""
    available_width = slide_width - (2 * MARGIN_HORIZONTAL)
    total_gap_width = GAP_WIDTH * (num_cols - 1)

    # Calculate single column width
    col_width = (available_width - total_gap_width) / num_cols

    for i in range(num_cols):
        if i >= len(content):
            break

        col_data = content[i]

        # Calculate Position
        left = MARGIN_HORIZONTAL + (i * (col_width + GAP_WIDTH))
        top = MARGIN_TOP
        height = slide_height - MARGIN_TOP - MARGIN_BOTTOM

        # Create Text Box
        txBox = slide.shapes.add_textbox(left, top, col_width, height)
        tf = txBox.text_frame
        tf.word_wrap = True

        # Header (Bold)
        header_text = col_data.get("header", "")
        if header_text:
            p = tf.add_paragraph()
            p.text = header_text
            p.font.bold = True
            p.font.size = FONT_SIZE_HEADER
            p.space_after = Pt(10)

        # Bullets
        for bullet in col_data.get("bullets", []):
            p = tf.add_paragraph()
            p.text = f"{BULLET_CHAR}{bullet}"
            p.level = 0
            p.font.size = FONT_SIZE_BODY


def _add_visual_placeholder(slide, description: str, slide_width: int, slide_height: int):
    """Adds a placeholder shape for visual data requests."""
    width = Inches(4)
    height = Inches(1.5)
    left = slide_width - width - Inches(0.5)
    top = slide_height - height - Inches(0.5)

    shape = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, left, top, width, height)

    shape.fill.solid()
    shape.fill.fore_color.rgb = COLOR_GRAY_FILL
    shape.line.color.rgb = COLOR_GRAY_LINE

    tf = shape.text_frame
    p = tf.paragraphs[0]
    p.text = f"[VISUAL DATA REQUEST]\n{description}"
    p.alignment = PP_ALIGN.CENTER
    p.font.size = FONT_SIZE_VISUAL
    p.font.bold = True


def _add_notes_and_metadata(slide, data: dict[str, Any]):
    """Appends speaker notes and governance metadata to the Notes slide."""
    text_frame = slide.notes_slide.notes_text_frame

    parts = []

    # Preserve existing notes if any (unlikely in new slide, but safe)
    if text_frame.text.strip():
        parts.append(text_frame.text)

    # User Notes
    notes = data.get("speaker_notes", "")
    if notes:
        parts.append(notes)

    # Governance Metadata
    classification = data.get("classification", "Internal Use Only")
    confidence = data.get("data_confidence", "Unknown")
    sources = ", ".join(data.get("source_references", []))

    metadata = (
        f"--- GOVERNANCE METADATA ---\n"
        f"Classification: {classification}\n"
        f"Confidence: {confidence}\n"
        f"Sources: {sources}"
    )
    parts.append(metadata)

    text_frame.text = "\n\n".join(parts)


def main():
    # Configure logging only when running as a script
    logging.basicConfig(level=logging.INFO, format='%(message)s')

    parser = argparse.ArgumentParser(description="Generate PowerPoint from JSON source.")
    parser.add_argument("input_json", type=Path, help="Path to input JSON file.")
    parser.add_argument("--output", "-o", type=Path, help="Output path (default: input_filename.pptx)")

    args = parser.parse_args()

    if not args.input_json.exists():
        logger.error(f"File not found: {args.input_json}")
        exit(1)

    output_path = args.output if args.output else args.input_json.with_suffix(".pptx")

    try:
        with open(args.input_json, 'r', encoding='utf-8') as f:
            data = json.load(f)

        create_presentation(data, output_path)

    except json.JSONDecodeError as e:
        logger.error(f"Invalid JSON format: {e}")
        exit(1)
    except Exception as e:
        logger.error(f"An error occurred: {e}")
        exit(1)

if __name__ == "__main__":
    main()
