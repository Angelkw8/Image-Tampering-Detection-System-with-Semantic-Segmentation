from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer,
    Image, Table, TableStyle, PageBreak
)
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from io import BytesIO
from datetime import datetime
import numpy as np

# -----------------------------
# Helper: tampered area
# -----------------------------
def calculate_tamper_ratio(mask):
    total_pixels = mask.size
    tampered_pixels = (mask > 0).sum()
    return round((tampered_pixels / total_pixels) * 100, 2)

# -----------------------------
# PDF generator
# -----------------------------
def generate_report_bytes(
    original_image,
    overlay_image,
    tampered,
    mask,
    confidence  
):
    buffer = BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=A4)
    styles = getSampleStyleSheet()
    elements = []

    # =============================
    # PAGE 1 — RESULTS
    # =============================
    elements.append(Paragraph(
        "Image Tampering Detection Report",
        styles["Title"]
    ))
    elements.append(Spacer(1, 12))

    elements.append(Paragraph(
        f"<b>Date:</b> {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
        styles["Normal"]
    ))
    elements.append(Spacer(1, 10))

    status = "TAMPERED" if tampered else "AUTHENTIC"
    status_color = colors.red if tampered else colors.green

    elements.append(Paragraph(
        f"<b>Detection Result:</b> "
        f"<font color='{status_color.hexval()}'>{status}</font>",
        styles["Normal"]
    ))
    elements.append(Spacer(1, 12))

    # ---- Metrics ----
    tamper_ratio = calculate_tamper_ratio(mask)

    elements.append(Paragraph(
        f"<b>Tampered Area:</b> {tamper_ratio}%",
        styles["Normal"]
    ))
    elements.append(Spacer(1, 10))

    elements.append(Paragraph(
        f"<b>Detection Confidence:</b> {confidence}%",
        styles["Normal"]
    ))
    elements.append(Spacer(1, 14))

    # ---- Images ----
    image_table = Table([
        [
            Image(original_image, 230, 160),
            Image(overlay_image, 230, 160)
        ],
        ["Original Image", "Detected Tampered Regions"]
    ])

    image_table.setStyle(TableStyle([
        ("GRID", (0, 0), (-1, -2), 0.5, colors.grey),
        ("ALIGN", (0, 0), (-1, -1), "CENTER"),
        ("BACKGROUND", (0, -1), (-1, -1), colors.whitesmoke),
        ("FONT", (0, -1), (-1, -1), "Helvetica-Bold")
    ]))

    elements.append(image_table)
    elements.append(Spacer(1, 18))

    # ---- Non-expert explanation ----
    elements.append(Paragraph(
        "Highlighted regions indicate areas identified by the system as "
        "potentially manipulated. Tampered area represents the proportion "
        "of the image affected, while detection confidence reflects how "
        "certain the system is based on learned manipulation patterns.",
        styles["Normal"]
    ))

    # =============================
    # PAGE 2 — TECHNICAL DETAILS
    # =============================
    elements.append(PageBreak())

    elements.append(Paragraph(
        "Technical Analysis Details",
        styles["Heading2"]
    ))
    elements.append(Spacer(1, 12))

    tech_table = Table([
        ["Component", "Description"],
        ["Model Type", "SegFormer B2"],
        ["Task", "Pixel-level tampering segmentation"],
        ["Input", "RGB Image"],
        ["Output", "Binary tampering mask"],
        ["Confidence Metric",
         "Mean probability of detected tampered pixels"],
        ["Area Metric",
         "Ratio of tampered pixels to total image pixels"]
    ])

    tech_table.setStyle(TableStyle([
        ("GRID", (0, 0), (-1, -1), 0.5, colors.grey),
        ("BACKGROUND", (0, 0), (-1, 0), colors.lightgrey),
        ("FONT", (0, 0), (-1, 0), "Helvetica-Bold"),
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE")
    ]))

    elements.append(tech_table)
    elements.append(Spacer(1, 14))

    elements.append(Paragraph(
        "This section is intended for advanced users who wish to understand "
        "the internal decision logic of the tampering detection model.",
        styles["Italic"]
    ))

    doc.build(elements)
    buffer.seek(0)
    return buffer
