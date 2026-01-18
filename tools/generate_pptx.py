import json
import argparse
import logging
from pathlib import Path
from typing import Any

from pptx import Presentation
from pptx.presentation import Presentation as PresentationType
from pptx.slide import Slide
from pptx.text.text import TextFrame
from pptx.util import Inches, Pt
from pptx.enum.text import PP_ALIGN
from pptx.enum.shapes import MSO_SHAPE
from pptx.dml.color import RGBColor

# Configure logging
logger = logging.getLogger(__name__)

# --- TYPES ---
SlideData = dict[str, Any]

# --- CONSTANTS ---
# JSON Keys
KEY_TITLE = "title"
KEY_SUBTITLE = "subtitle"
KEY_LAYOUT = "layout"
KEY_CONTENT = "content"
KEY_SPEAKER_NOTES = "speaker_notes"
KEY_VISUAL_DESC = "visual_data_description"
KEY_HEADER = "header"
KEY_BULLETS = "bullets"
KEY_CLASSIFICATION = "classification"
KEY_CONFIDENCE = "data_confidence"
KEY_SOURCES = "source_references"

# Layout Names
LAYOUT_TITLE = "title"
LAYOUT_SECTION = "section"
LAYOUT_BULLETED = "bulleted"
LAYOUT_2_COL = "2_col"
LAYOUT_3_COL = "3_col"
LAYOUT_4_COL = "4_col"

DEFAULT_LAYOUT = LAYOUT_BULLETED
COLUMN_LAYOUTS = {LAYOUT_2_COL, LAYOUT_3_COL, LAYOUT_4_COL}

# Standard Layout Indices (Default Template)
LAYOUT_MAP = {
    LAYOUT_TITLE: 0,      # Title Slide
    LAYOUT_SECTION: 2,    # Section Header
    LAYOUT_BULLETED: 1,   # Title and Content
    LAYOUT_2_COL: 5,      # Title Only
    LAYOUT_3_COL: 5,
    LAYOUT_4_COL: 5
}

# Dimensions & Fonts
MARGIN_HORIZONTAL = Inches(0.5)
MARGIN_TOP = Inches(2.0)  # Room for Title
MARGIN_BOTTOM = Inches(1.0)
GAP_WIDTH = Inches(0.2)

VISUAL_WIDTH = Inches(4)
VISUAL_HEIGHT = Inches(1.5)
VISUAL_OFFSET = Inches(0.5)

FONT_SIZE_HEADER = Pt(18)
FONT_SIZE_BODY = Pt(14)
FONT_SIZE_VISUAL = Pt(12)
BULLET_CHAR = "• "

# Visual Placeholder Colors
COLOR_GRAY_FILL = RGBColor(200, 200, 200)
COLOR_GRAY_LINE = RGBColor(100, 100, 100)

# Defaults
DEFAULT_CLASSIFICATION = "Internal Use Only"
DEFAULT_CONFIDENCE = "Unknown"


def build_presentation(json_data: list[SlideData]) -> PresentationType:
    """
    Builds a PowerPoint presentation object from the provided JSON data.
    Does not save the file to disk.
    """
    prs = Presentation()

    for slide_data in json_data:
        layout_name = slide_data.get(KEY_LAYOUT, DEFAULT_LAYOUT)
        layout_idx = LAYOUT_MAP.get(layout_name, LAYOUT_MAP[DEFAULT_LAYOUT])

        slide_layout = prs.slide_layouts[layout_idx]
        slide = prs.slides.add_slide(slide_layout)

        _add_title(slide, slide_data)
        _add_slide_content(slide, slide_data, prs, layout_name)
        _add_notes_and_metadata(slide, slide_data)

    return prs


def _add_title(slide: Slide, slide_data: SlideData) -> None:
    """Sets the slide title and subtitle if applicable."""
    title = slide_data.get(KEY_TITLE)
    if title and slide.shapes.title:
        slide.shapes.title.text = title

    layout = slide_data.get(KEY_LAYOUT)
    if layout == LAYOUT_TITLE and len(slide.placeholders) > 1:
        subtitle = slide_data.get(KEY_SUBTITLE)
        if subtitle:
            slide.placeholders[1].text = subtitle


def _add_slide_content(slide: Slide, slide_data: SlideData, prs: PresentationType, layout_name: str) -> None:
    """Orchestrates adding content (bullets, columns, visual requests) to the slide."""
    content = slide_data.get(KEY_CONTENT, [])

    # Text Content
    if layout_name in COLUMN_LAYOUTS:
        num_cols = int(layout_name.split("_")[0])
        _add_columns(slide, content, num_cols, prs)
    elif layout_name == DEFAULT_LAYOUT:
        _add_standard_bullets(slide, content)

    # Visual Request
    visual_desc = slide_data.get(KEY_VISUAL_DESC)
    if visual_desc:
        _add_visual_placeholder(slide, visual_desc, prs.slide_width, prs.slide_height)


def _add_standard_bullets(slide: Slide, content: list[SlideData]) -> None:
    """Handles standard bulleted content using the template's placeholder."""
    if not content or len(slide.placeholders) < 2:
        return

    tf = slide.placeholders[1].text_frame
    tf.clear()

    item = content[0]
    for bullet in item.get(KEY_BULLETS, []):
        _add_paragraph(tf, bullet, level=0)


def _add_columns(slide: Slide, content: list[SlideData], num_cols: int, prs: PresentationType) -> None:
    """Programmatically creates text boxes for multi-column layouts."""
    slide_width = prs.slide_width
    slide_height = prs.slide_height

    available_width = slide_width - (2 * MARGIN_HORIZONTAL)
    total_gap_width = GAP_WIDTH * (num_cols - 1)
    col_width = (available_width - total_gap_width) / num_cols

    for i in range(num_cols):
        if i >= len(content):
            break

        col_data = content[i]

        left = MARGIN_HORIZONTAL + (i * (col_width + GAP_WIDTH))
        top = MARGIN_TOP
        height = slide_height - MARGIN_TOP - MARGIN_BOTTOM

        txBox = slide.shapes.add_textbox(left, top, col_width, height)
        tf = txBox.text_frame
        tf.word_wrap = True

        header_text = col_data.get(KEY_HEADER, "")
        if header_text:
            _add_paragraph(tf, header_text, bold=True, size=FONT_SIZE_HEADER, space_after=Pt(10))

        for bullet in col_data.get(KEY_BULLETS, []):
            _add_paragraph(tf, f"{BULLET_CHAR}{bullet}", size=FONT_SIZE_BODY)


def _add_paragraph(text_frame: TextFrame, text: str, level: int = 0, bold: bool = False, size: Pt = None, space_after: Pt = None) -> None:
    """
    Adds a paragraph to the text frame.
    Uses the first paragraph if it exists and is empty to avoid leading whitespace.
    """
    if len(text_frame.paragraphs) == 1 and not text_frame.paragraphs[0].text:
        p = text_frame.paragraphs[0]
    else:
        p = text_frame.add_paragraph()

    p.text = text
    p.level = level

    if bold:
        p.font.bold = True
    if size:
        p.font.size = size
    if space_after:
        p.space_after = space_after


def _add_visual_placeholder(slide: Slide, description: str, slide_width: int, slide_height: int) -> None:
    """Adds a placeholder shape for visual data requests."""
    left = slide_width - VISUAL_WIDTH - VISUAL_OFFSET
    top = slide_height - VISUAL_HEIGHT - VISUAL_OFFSET

    shape = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, left, top, VISUAL_WIDTH, VISUAL_HEIGHT)

    shape.fill.solid()
    shape.fill.fore_color.rgb = COLOR_GRAY_FILL
    shape.line.color.rgb = COLOR_GRAY_LINE

    tf = shape.text_frame
    p = tf.paragraphs[0]
    p.text = f"[VISUAL DATA REQUEST]\n{description}"
    p.alignment = PP_ALIGN.CENTER
    p.font.size = FONT_SIZE_VISUAL
    p.font.bold = True


def _add_notes_and_metadata(slide: Slide, data: SlideData) -> None:
    """Appends speaker notes and governance metadata to the Notes slide."""
    text_frame = slide.notes_slide.notes_text_frame

    parts = []

    if text_frame.text.strip():
        parts.append(text_frame.text)

    notes = data.get(KEY_SPEAKER_NOTES, "")
    if notes:
        parts.append(notes)

    classification = data.get(KEY_CLASSIFICATION, DEFAULT_CLASSIFICATION)
    confidence = data.get(KEY_CONFIDENCE, DEFAULT_CONFIDENCE)
    sources = ", ".join(data.get(KEY_SOURCES, []))

    metadata = (
        f"--- GOVERNANCE METADATA ---\n"
        f"Classification: {classification}\n"
        f"Confidence: {confidence}\n"
        f"Sources: {sources}"
    )
    parts.append(metadata)

    text_frame.text = "\n\n".join(parts)


def main() -> None:
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

        prs = build_presentation(data)
        prs.save(output_path)
        logger.info(f"Presentation saved to: {output_path}")

    except json.JSONDecodeError as e:
        logger.error(f"Invalid JSON format: {e}")
        exit(1)
    except Exception as e:
        logger.error(f"An error occurred: {e}")
        exit(1)

if __name__ == "__main__":
    main()
