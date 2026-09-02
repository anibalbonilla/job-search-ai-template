#!/usr/bin/env python3
"""Convert a CV/cover-letter Markdown file (our fixed subset) to an ATS-friendly PDF.

Supported subset: # H1, ## H2, ### H3, **bold**, *italic*, "- " bullets, blank-line
paragraphs. Single column, standard font (Helvetica), no images/tables — by design,
so ATS parsers read it cleanly.

Usage: python3 md_to_pdf.py input.md output.pdf
"""
import re
import sys

from fpdf import FPDF

MARGIN = 16
FONT = "Helvetica"
BODY_SIZE = 10
LINE_H = 4.8

# Core PDF fonts only support latin-1; normalize common Unicode punctuation
# (also safer for ATS parsers, which sometimes choke on smart quotes/dashes).
CHAR_MAP = {
    "—": "-",  # em dash
    "–": "-",  # en dash
    "‘": "'", "’": "'",  # curly single quotes
    "“": '"', "”": '"',  # curly double quotes
    "…": "...",  # ellipsis
    "•": "-",  # bullet
}


def normalize(text: str) -> str:
    for src, dst in CHAR_MAP.items():
        text = text.replace(src, dst)
    return text


def write_inline(pdf: FPDF, text: str, line_height: float, size: float = BODY_SIZE):
    """Write a line with **bold** / *italic* spans; wraps automatically."""
    for token in re.split(r"(\*\*.*?\*\*|\*.*?\*)", text):
        if not token:
            continue
        if token.startswith("**") and token.endswith("**"):
            pdf.set_font(FONT, style="B", size=size)
            token = token[2:-2]
        elif token.startswith("*") and token.endswith("*"):
            pdf.set_font(FONT, style="I", size=size)
            token = token[1:-1]
        else:
            pdf.set_font(FONT, style="", size=size)
        pdf.write(line_height, token)
    pdf.ln(line_height)


def convert(input_path: str, output_path: str):
    with open(input_path, encoding="utf-8") as f:
        lines = f.read().splitlines()

    pdf = FPDF(format="Letter")
    pdf.set_margins(MARGIN, MARGIN, MARGIN)
    pdf.set_auto_page_break(auto=True, margin=MARGIN)
    pdf.add_page()
    pdf.set_font(FONT, size=BODY_SIZE)

    for raw in lines:
        line = normalize(raw.rstrip())

        if not line:
            pdf.ln(1.8)
            continue

        if line.startswith("# "):
            pdf.set_font(FONT, style="B", size=17)
            pdf.cell(0, 8, line[2:], new_x="LMARGIN", new_y="NEXT")
            continue

        if line.startswith("## "):
            pdf.ln(1.5)
            pdf.set_font(FONT, style="B", size=12)
            pdf.cell(0, 6, line[3:].upper(), new_x="LMARGIN", new_y="NEXT")
            y = pdf.get_y()
            pdf.set_draw_color(90, 90, 90)
            pdf.line(MARGIN, y, pdf.w - MARGIN, y)
            pdf.ln(1.5)
            continue

        if line.startswith("### "):
            pdf.ln(0.5)
            write_inline(pdf, line[4:], LINE_H, size=11)
            continue

        if line.startswith("- "):
            pdf.set_font(FONT, size=BODY_SIZE)
            pdf.write(LINE_H, "-  ")
            write_inline(pdf, line[2:], LINE_H)
            continue

        write_inline(pdf, line, LINE_H)

    pdf.output(output_path)


if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python3 md_to_pdf.py input.md output.pdf")
        sys.exit(1)
    convert(sys.argv[1], sys.argv[2])
    print(f"Wrote {sys.argv[2]}")
