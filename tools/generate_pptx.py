import json
import argparse
import logging
from pathlib import Path
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.enum.text import PP_ALIGN
from pptx.enum.shapes import MSO_SHAPE
from pptx.dml.color import RGBColor

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(message)s')
logger = logging.getLogger(__name__)

def create_presentation(json_data, output_path):
    """
    Creates a PowerPoint presentation from the provided JSON data.
    """
    prs = Presentation()

    # Layout mappings (Standard Default Template)
    # 0: Title Slide
    # 1: Title and Content
    # 2: Section Header
    # 3: Two Content
    # 4: Comparison
    # 5: Title Only
    # 6: Blank

    LAYOUT_MAP = {
        "title": 0,
        "section": 2,
        "bulleted": 1,
        "2_col": 5, # Using Title Only and manually adding columns
        "3_col": 5,
        "4_col": 5
    }

    for slide_data in json_data:
        layout_name = slide_data.get("layout", "bulleted")
        layout_idx = LAYOUT_MAP.get(layout_name, 1)

        slide_layout = prs.slide_layouts[layout_idx]
        slide = prs.slides.add_slide(slide_layout)

        # 1. Handle Title and Subtitle
        if slide.shapes.title:
            slide.shapes.title.text = slide_data.get("title", "")

        # Handle Subtitle for Title Slides
        if layout_name == "title":
            # In Layout 0, the second placeholder is usually the subtitle
            if len(slide.placeholders) > 1:
                slide.placeholders[1].text = slide_data.get("subtitle", "")

        # 2. Handle Content (Bulleted vs Columns)
        content = slide_data.get("content", [])

        if layout_name == "bulleted":
            # Standard single column layout
            if len(slide.placeholders) > 1 and content:
                # Use the main content placeholder
                tf = slide.placeholders[1].text_frame
                tf.clear() # Clear existing empty bullets if any

                # Assume single content block for bulleted layout
                if len(content) > 0:
                    item = content[0]
                    # Optional header if provided, though usually redundant with slide title
                    # if item.get("header"):
                    #     p = tf.add_paragraph()
                    #     p.text = item.get("header")
                    #     p.font.bold = True

                    for bullet in item.get("bullets", []):
                        p = tf.add_paragraph()
                        p.text = bullet
                        p.level = 0

        elif layout_name in ["2_col", "3_col", "4_col"]:
            # Custom Column Logic
            num_cols = int(layout_name.split("_")[0])
            _create_columns(slide, content, num_cols, prs.slide_width, prs.slide_height)

        # 3. Handle Visual Data Description (Placeholder)
        visual_desc = slide_data.get("visual_data_description")
        if visual_desc:
            _add_visual_placeholder(slide, visual_desc, prs.slide_width, prs.slide_height)

        # 4. Handle Speaker Notes & Metadata
        _add_notes_and_metadata(slide, slide_data)

    # Save
    prs.save(output_path)
    logger.info(f"Presentation saved to: {output_path}")

def _create_columns(slide, content, num_cols, slide_width, slide_height):
    """
    Manually creates text boxes for multi-column layouts.
    """
    # Dimensions
    margin_left = Inches(0.5)
    margin_right = Inches(0.5)
    margin_top = Inches(2.0) # Leave room for Title

    available_width = slide_width - margin_left - margin_right
    col_width = available_width / num_cols
    col_spacing = Inches(0.2)

    # Adjust width for spacing
    final_col_width = col_width - (col_spacing * (num_cols - 1) / num_cols)

    for i in range(num_cols):
        if i >= len(content):
            break

        col_data = content[i]

        # Calculate Position
        left = margin_left + (i * (final_col_width + col_spacing))
        top = margin_top
        height = slide_height - margin_top - Inches(1.0) # Leave bottom margin

        # Create Text Box
        txBox = slide.shapes.add_textbox(left, top, final_col_width, height)
        tf = txBox.text_frame
        tf.word_wrap = True

        # Header (Bold)
        header_text = col_data.get("header", "")
        if header_text:
            p = tf.add_paragraph()
            p.text = header_text
            p.font.bold = True
            p.font.size = Pt(18)
            # Add some space after header
            p.space_after = Pt(10)

        # Bullets
        for bullet in col_data.get("bullets", []):
            p = tf.add_paragraph()
            p.text = f"• {bullet}"
            p.level = 0
            p.font.size = Pt(14)

def _add_visual_placeholder(slide, description, slide_width, slide_height):
    """
    Adds a placeholder shape for visual data.
    """
    # Place it at the bottom or right depending on space,
    # but for simplicity, let's put it in the center-bottom or overlay if empty.
    # A standard "sticker" approach:

    width = Inches(4)
    height = Inches(1.5)
    left = slide_width - width - Inches(0.5)
    top = slide_height - height - Inches(0.5)

    shape = slide.shapes.add_shape(
        MSO_SHAPE.ROUNDED_RECTANGLE,
        left, top, width, height
    )

    # Style
    shape.fill.solid()
    shape.fill.fore_color.rgb = RGBColor(200, 200, 200) # Gray
    shape.line.color.rgb = RGBColor(100, 100, 100)

    tf = shape.text_frame
    p = tf.paragraphs[0]
    p.text = f"[VISUAL DATA REQUEST]\n{description}"
    p.alignment = PP_ALIGN.CENTER
    p.font.size = Pt(12)
    p.font.bold = True

def _add_notes_and_metadata(slide, data):
    """
    Adds speaker notes and governance metadata.
    """
    notes_slide = slide.notes_slide
    text_frame = notes_slide.notes_text_frame

    # Speaker Notes
    notes = data.get("speaker_notes", "")
    if notes:
        text_frame.text = f"{notes}\n"

    # Governance Metadata
    classification = data.get("classification", "Internal Use Only")
    confidence = data.get("data_confidence", "Unknown")
    sources = ", ".join(data.get("source_references", []))

    metadata = (
        f"\n--- GOVERNANCE METADATA ---\n"
        f"Classification: {classification}\n"
        f"Confidence: {confidence}\n"
        f"Sources: {sources}"
    )

    # Append metadata
    # If text_frame already has text, append.
    if text_frame.text:
        text_frame.text += metadata
    else:
        text_frame.text = metadata

def main():
    parser = argparse.ArgumentParser(description="Generate PowerPoint from JSON source.")
    parser.add_argument("input_json", type=Path, help="Path to input JSON file.")
    parser.add_argument("--output", "-o", type=Path, help="Output path (default: input_filename.pptx)")

    args = parser.parse_args()

    if not args.input_json.exists():
        logger.error(f"File not found: {args.input_json}")
        exit(1)

    # Determine output path
    if args.output:
        output_path = args.output
    else:
        output_path = args.input_json.with_suffix(".pptx")

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
