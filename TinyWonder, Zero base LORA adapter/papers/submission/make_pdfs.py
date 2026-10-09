#!/usr/bin/env python3
"""Build the isolated publication revision with controlled typography and vector figures."""
from __future__ import annotations

import argparse
import html
from pathlib import Path
from xml.sax.saxutils import escape

import markdown
from lxml import html as lhtml
from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_LEFT
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import inch
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import Image, KeepTogether, ListFlowable, ListItem, Paragraph, Preformatted, SimpleDocTemplate, Spacer, Table, TableStyle

HERE = Path(__file__).resolve().parent
PAPERS = HERE.parent


def register_fonts():
    serif = Path("/usr/share/fonts/truetype/dejavu/DejaVuSerif.ttf")
    serif_bold = Path("/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf")
    sans = Path("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf")
    sans_bold = Path("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf")
    mono = Path("/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf")
    if all(p.exists() for p in (serif, serif_bold, sans, sans_bold, mono)):
        pdfmetrics.registerFont(TTFont("TWSerif", str(serif)))
        pdfmetrics.registerFont(TTFont("TWSerif-Bold", str(serif_bold)))
        pdfmetrics.registerFont(TTFont("TWSans", str(sans)))
        pdfmetrics.registerFont(TTFont("TWSans-Bold", str(sans_bold)))
        pdfmetrics.registerFont(TTFont("TWMono", str(mono)))
        return "TWSerif", "TWSerif-Bold", "TWSans", "TWSans-Bold", "TWMono"
    return "Times-Roman", "Times-Bold", "Helvetica", "Helvetica-Bold", "Courier"


def make_styles():
    serif, serif_bold, sans, sans_bold, mono = register_fonts()
    base = getSampleStyleSheet()
    return {
        "title": ParagraphStyle("TWTitle", parent=base["Title"], fontName=serif_bold, fontSize=19, leading=23, alignment=TA_CENTER, textColor=colors.HexColor("#17324D"), spaceAfter=7),
        "subtitle": ParagraphStyle("TWSubtitle", parent=base["Normal"], fontName=serif, fontSize=11.2, leading=14, alignment=TA_CENTER, textColor=colors.HexColor("#52606D"), spaceAfter=9),
        "front": ParagraphStyle("TWFront", parent=base["Normal"], fontName=sans, fontSize=8.7, leading=11, alignment=TA_CENTER, textColor=colors.HexColor("#52606D"), spaceAfter=4),
        "abstract_head": ParagraphStyle("TWAbstractHead", parent=base["Heading2"], fontName=sans_bold, fontSize=11, leading=13, alignment=TA_LEFT, textColor=colors.HexColor("#17324D"), spaceBefore=8, spaceAfter=4),
        "body": ParagraphStyle("TWBody", parent=base["BodyText"], fontName=serif, fontSize=9.8, leading=13.6, alignment=TA_LEFT, textColor=colors.HexColor("#1F2933"), spaceAfter=6, splitLongWords=True),
        "major": ParagraphStyle("TWMajor", parent=base["Heading1"], fontName=sans_bold, fontSize=13, leading=16, textColor=colors.HexColor("#17324D"), spaceBefore=12, spaceAfter=6, keepWithNext=True),
        "minor": ParagraphStyle("TWMinor", parent=base["Heading2"], fontName=sans_bold, fontSize=10.8, leading=13, textColor=colors.HexColor("#234E70"), spaceBefore=9, spaceAfter=4, keepWithNext=True),
        "subminor": ParagraphStyle("TWSubminor", parent=base["Heading3"], fontName=sans_bold, fontSize=9.8, leading=12, textColor=colors.HexColor("#52606D"), spaceBefore=7, spaceAfter=3, keepWithNext=True),
        "caption": ParagraphStyle("TWCaption", parent=base["Normal"], fontName=serif, fontSize=8.3, leading=10.3, alignment=TA_LEFT, textColor=colors.HexColor("#52606D"), spaceBefore=3, spaceAfter=8),
        "table_head": ParagraphStyle("TWTableHead", parent=base["Normal"], fontName=sans_bold, fontSize=7.4, leading=9, textColor=colors.HexColor("#102A43")),
        "table_cell": ParagraphStyle("TWTableCell", parent=base["Normal"], fontName=serif, fontSize=7.4, leading=9, textColor=colors.HexColor("#1F2933")),
        "code": ParagraphStyle("TWCode", parent=base["Code"], fontName=mono, fontSize=7.4, leading=9, leftIndent=12, rightIndent=12, backColor=colors.HexColor("#F0F4F8"), spaceAfter=7),
    }


def inline(node, mono_font):
    parts = []
    if node.text:
        parts.append(escape(node.text))
    for child in node:
        content = inline(child, mono_font)
        tag = child.tag.lower() if isinstance(child.tag, str) else ""
        if tag in {"strong", "b"}:
            content = f"<b>{content}</b>"
        elif tag in {"em", "i"}:
            content = f"<i>{content}</i>"
        elif tag in {"code", "tt"}:
            content = f'<font name="{mono_font}">{content}</font>'
        elif tag == "a":
            content = f"<u>{content}</u>"
        parts.append(content)
        if child.tail:
            parts.append(escape(child.tail))
    return "".join(parts)


def text_of(node):
    return " ".join("".join(node.itertext()).split())


def table_flow(node, styles):
    rows = []
    for tr in node.xpath(".//tr"):
        cells = tr.xpath("./th|./td")
        is_header = bool(tr.xpath("./th")) or not rows
        style = styles["table_head"] if is_header else styles["table_cell"]
        rows.append([Paragraph(escape(text_of(c)), style) for c in cells])
    if not rows:
        return Spacer(1, 1)
    table = Table(rows, repeatRows=1, hAlign="LEFT")
    table.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#D9EAF7")),
        ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.white, colors.HexColor("#F7FAFC")]),
        ("GRID", (0, 0), (-1, -1), 0.35, colors.HexColor("#9FB3C8")),
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("LEFTPADDING", (0, 0), (-1, -1), 4),
        ("RIGHTPADDING", (0, 0), (-1, -1), 4),
        ("TOPPADDING", (0, 0), (-1, -1), 3),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 3),
    ]))
    return KeepTogether([table, Spacer(1, 8)])


def figure_flow(node, paper_path, styles):
    src = (paper_path.parent / node.get("src", "")).resolve()
    if src.suffix.lower() == ".svg":
        png = src.parent / "rendered" / f"{src.stem}.png"
        pdf = src.with_suffix(".pdf")
        if png.exists():
            src = png
        elif pdf.exists():
            src = pdf
    if not src.exists():
        return Paragraph(f"[Figure unavailable: {escape(str(node.get('src')))}]", styles["caption"])
    img = Image(str(src))
    img._restrictSize(6.7 * inch, 4.8 * inch)
    return KeepTogether([img, Spacer(1, 3)])


def walk_block(node, paper_path, styles, mono_font):
    tag = node.tag.lower() if isinstance(node.tag, str) else ""
    if tag == "h2":
        return Paragraph(inline(node, mono_font), styles["major"])
    if tag == "h3":
        return Paragraph(inline(node, mono_font), styles["minor"])
    if tag == "h4":
        return Paragraph(inline(node, mono_font), styles["subminor"])
    if tag == "p":
        embedded = node.xpath(".//img")
        if embedded:
            return figure_flow(embedded[0], paper_path, styles)
        text = inline(node, mono_font)
        if text.startswith("Keywords:"):
            text = f"<b>{text}</b>"
        style = styles["caption"] if node.xpath(".//em") and len(text) < 420 else styles["body"]
        return Paragraph(text, style)
    if tag == "pre":
        return Preformatted(html.unescape(text_of(node)), styles["code"])
    if tag == "table":
        return table_flow(node, styles)
    if tag == "img":
        return figure_flow(node, paper_path, styles)
    if tag in {"ul", "ol"}:
        items = [ListItem(Paragraph(inline(li, mono_font), styles["body"]), leftIndent=13) for li in node.xpath("./li")]
        return ListFlowable(items, bulletType="1" if tag == "ol" else "bullet", leftIndent=19, bulletFontName=styles["body"].fontName)
    if tag == "hr":
        return Spacer(1, 6)
    return None


def build(paper_path: Path, output: Path):
    styles = make_styles()
    source = paper_path.read_text(encoding="utf-8")
    rendered = markdown.markdown(source, extensions=["tables", "fenced_code"])
    root = lhtml.fromstring(f"<div>{rendered}</div>")
    blocks = list(root)
    title_node = next((n for n in blocks if n.tag == "h1"), None)
    title = text_of(title_node) if title_node is not None else paper_path.stem
    h2s = [n for n in blocks if n.tag == "h2"]
    subtitle_node = h2s[0] if h2s and text_of(h2s[0]).strip().lower() != "abstract" else None
    abstract_node = next((n for n in blocks if n.tag in {"h2", "h3"} and text_of(n).strip().lower() == "abstract"), None)
    story = [Paragraph(escape(title), styles["title"])]
    if subtitle_node is not None:
        story.append(Paragraph(escape(text_of(subtitle_node)), styles["subtitle"]))
    story.append(Paragraph("Ali Imran Malik", styles["front"]))
    story.append(Paragraph("Independent Researcher, Islamabad, Pakistan", styles["front"]))
    story.append(Paragraph("CEO, Hydrabotics Group", styles["front"]))
    story.append(Paragraph("GitHub: github.com/am-llm · LinkedIn: linkedin.com/in/aliimranmalik", styles["front"]))
    if abstract_node is not None:
        story.append(Paragraph("Abstract", styles["abstract_head"]))
    skipped_title = False
    skipped_subtitle = False
    skipped_abstract = False
    mono = "TWMono" if "TWMono" in pdfmetrics.getRegisteredFontNames() else "Courier"
    for node in blocks:
        tag = node.tag.lower() if isinstance(node.tag, str) else ""
        if tag == "h1" and not skipped_title:
            skipped_title = True; continue
        if subtitle_node is not None and node is subtitle_node and not skipped_subtitle:
            skipped_subtitle = True; continue
        if abstract_node is not None and node is abstract_node and not skipped_abstract:
            skipped_abstract = True; continue
        flow = walk_block(node, paper_path, styles, mono)
        if flow is not None:
            story.append(flow)
    doc = SimpleDocTemplate(str(output), pagesize=letter, rightMargin=.72*inch, leftMargin=.72*inch, topMargin=.68*inch, bottomMargin=.60*inch, title=title, author="Ali Imran Malik")
    short_title = title[:80]
    def footer(canvas, document):
        canvas.saveState()
        canvas.setStrokeColor(colors.HexColor("#D9E2EC")); canvas.setLineWidth(.4)
        canvas.line(.72*inch, .43*inch, letter[0]-.72*inch, .43*inch)
        canvas.setFont("TWSans" if "TWSans" in pdfmetrics.getRegisteredFontNames() else "Helvetica", 7.5)
        canvas.setFillColor(colors.HexColor("#7B8794"))
        canvas.drawString(.72*inch, .27*inch, short_title)
        canvas.drawRightString(letter[0]-.72*inch, .27*inch, f"{document.page}")
        canvas.restoreState()
    doc.build(story, onFirstPage=footer, onLaterPages=footer)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--output-dir", type=Path, default=HERE)
    args = parser.parse_args()
    build(PAPERS / "paper1_zero_base_host_draft.md", args.output_dir / "paper1_zero_base_host.pdf")
    build(PAPERS / "paper2_stacking_attenuation_draft.md", args.output_dir / "paper2_stacking_attenuation.pdf")
    print("built isolated publication PDFs")


if __name__ == "__main__":
    main()
