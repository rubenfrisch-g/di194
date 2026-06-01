from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import cm
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, HRFlowable
from reportlab.lib.enums import TA_CENTER, TA_LEFT
import io
from datetime import datetime


def generate_pdf(
    grade: float,
    scale: int,
    level: str,
    subject: str,
    languages: list,
    continents: list,
    recommendations: list,
) -> bytes:
    """
    Generate a PDF report of university recommendations.
    Returns the PDF as bytes for Streamlit download.
    """
    buffer = io.BytesIO()
    doc = SimpleDocTemplate(
        buffer,
        pagesize=A4,
        rightMargin=2*cm,
        leftMargin=2*cm,
        topMargin=2*cm,
        bottomMargin=2*cm,
    )

    styles = getSampleStyleSheet()

    # Custom styles
    title_style = ParagraphStyle(
        'Title',
        parent=styles['Heading1'],
        fontSize=22,
        textColor=colors.HexColor('#1a1a2e'),
        spaceAfter=6,
        alignment=TA_CENTER,
    )
    subtitle_style = ParagraphStyle(
        'Subtitle',
        parent=styles['Normal'],
        fontSize=11,
        textColor=colors.HexColor('#666666'),
        spaceAfter=4,
        alignment=TA_CENTER,
    )
    section_style = ParagraphStyle(
        'Section',
        parent=styles['Heading2'],
        fontSize=14,
        textColor=colors.HexColor('#1a1a2e'),
        spaceBefore=12,
        spaceAfter=6,
    )
    body_style = ParagraphStyle(
        'Body',
        parent=styles['Normal'],
        fontSize=10,
        textColor=colors.HexColor('#333333'),
        spaceAfter=4,
    )

    # Level colors
    level_colors = {
        'Elite': colors.HexColor('#e74c3c'),
        'Mid': colors.HexColor('#3498db'),
        'Accessible': colors.HexColor('#2ecc71'),
    }
    level_color = level_colors.get(level, colors.black)

    story = []

    # ── Header ────────────────────────────────────────────────────
    story.append(Paragraph("🎓 University Recommendations", title_style))
    story.append(Paragraph(
        f"Generated on {datetime.now().strftime('%B %d, %Y')}",
        subtitle_style
    ))
    story.append(Spacer(1, 0.3*cm))
    story.append(HRFlowable(width="100%", thickness=1, color=colors.HexColor('#1a1a2e')))
    story.append(Spacer(1, 0.5*cm))

    # ── Student Profile ───────────────────────────────────────────
    story.append(Paragraph("Student Profile", section_style))

    profile_data = [
        ["Grade", f"{grade}/{scale} ({grade/scale*100:.0f}%)"],
        ["Level", level],
        ["Field of Study", subject],
        ["Languages", ", ".join(languages) if languages else "All"],
        ["Continents", ", ".join(continents) if "All continents" not in continents else "Worldwide"],
    ]

    profile_table = Table(profile_data, colWidths=[5*cm, 12*cm])
    profile_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (0, -1), colors.HexColor('#f0f0f0')),
        ('TEXTCOLOR', (0, 0), (0, -1), colors.HexColor('#1a1a2e')),
        ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, -1), 10),
        ('PADDING', (0, 0), (-1, -1), 8),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#dddddd')),
        ('ROWBACKGROUNDS', (0, 0), (-1, -1), [colors.white, colors.HexColor('#f9f9f9')]),
    ]))
    story.append(profile_table)
    story.append(Spacer(1, 0.5*cm))

    # ── Recommendations ───────────────────────────────────────────
    story.append(Paragraph(f"Recommended Universities — {level} Level", section_style))
    story.append(Paragraph(
        f"Based on your profile, here are the {len(recommendations)} most suitable universities:",
        body_style
    ))
    story.append(Spacer(1, 0.3*cm))

    # Table header
    table_data = [["#", "University", "Country", "QS Score", "QS Rank", "Languages"]]

    for i, uni in enumerate(recommendations, start=1):
        table_data.append([
            str(i),
            uni.get("Institution Name", ""),
            uni.get("Location", ""),
            f"{uni.get('score_numeric', 0):.1f}",
            str(int(uni.get('rank_numeric', 0))),
            uni.get("Languages", "N/A") or "N/A",
        ])

    uni_table = Table(
        table_data,
        colWidths=[0.8*cm, 7*cm, 2*cm, 2.2*cm, 2*cm, 3.5*cm]
    )
    uni_table.setStyle(TableStyle([
        # Header
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#1a1a2e')),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 10),
        ('ALIGN', (0, 0), (-1, 0), 'CENTER'),
        # Body
        ('FONTSIZE', (0, 1), (-1, -1), 9),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor('#f5f5f5')]),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#dddddd')),
        ('PADDING', (0, 0), (-1, -1), 6),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        # Level color on rank column
        ('TEXTCOLOR', (3, 1), (3, -1), level_color),
        ('FONTNAME', (3, 1), (3, -1), 'Helvetica-Bold'),
    ]))
    story.append(uni_table)
    story.append(Spacer(1, 0.5*cm))

    # ── Websites ──────────────────────────────────────────────────
    story.append(Paragraph("University Websites", section_style))
    for i, uni in enumerate(recommendations, start=1):
        name = uni.get("Institution Name", "")
        website = uni.get("Website", "")
        if website and "google.com" not in str(website):
            story.append(Paragraph(f"{i}. <b>{name}</b> — {website}", body_style))
        else:
            story.append(Paragraph(f"{i}. <b>{name}</b> — Visit official website for more info", body_style))

    story.append(Spacer(1, 0.5*cm))
    story.append(HRFlowable(width="100%", thickness=0.5, color=colors.HexColor('#cccccc')))
    story.append(Spacer(1, 0.3*cm))
    story.append(Paragraph(
        "Generated by University Recommender — Powered by KNN & K-Means Machine Learning",
        subtitle_style
    ))

    doc.build(story)
    buffer.seek(0)
    return buffer.getvalue()
