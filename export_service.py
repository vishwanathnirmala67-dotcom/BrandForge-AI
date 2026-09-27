from io import BytesIO
from typing import Any, Dict

from reportlab.lib import colors
from reportlab.lib.enums import TA_LEFT
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import mm
from reportlab.platypus import (
    KeepTogether,
    Paragraph,
    SimpleDocTemplate,
    Spacer,
    Table,
    TableStyle,
)


def _safe(value: Any) -> str:
    if value is None:
        return ""
    return str(value)


def build_brand_pdf(project: Dict[str, Any]) -> bytes:
    buffer = BytesIO()

    doc = SimpleDocTemplate(
        buffer,
        pagesize=A4,
        rightMargin=16 * mm,
        leftMargin=16 * mm,
        topMargin=14 * mm,
        bottomMargin=14 * mm,
        title="BrandForge Personal Branding Kit",
        author="BrandForge AI",
    )

    styles = getSampleStyleSheet()
    title = ParagraphStyle(
        "BrandTitle",
        parent=styles["Title"],
        fontName="Helvetica-Bold",
        fontSize=24,
        leading=28,
        textColor=colors.HexColor("#0F172A"),
        alignment=TA_LEFT,
        spaceAfter=8,
    )
    section = ParagraphStyle(
        "Section",
        parent=styles["Heading2"],
        fontName="Helvetica-Bold",
        fontSize=15,
        leading=18,
        textColor=colors.HexColor("#2563EB"),
        spaceBefore=12,
        spaceAfter=7,
    )
    body = ParagraphStyle(
        "Body",
        parent=styles["BodyText"],
        fontName="Helvetica",
        fontSize=9.3,
        leading=13,
        textColor=colors.HexColor("#334155"),
        spaceAfter=5,
    )
    small = ParagraphStyle(
        "Small",
        parent=body,
        fontSize=8,
        leading=11,
        textColor=colors.HexColor("#64748B"),
    )

    pos = project.get("positioning", {}) or {}
    dna = project.get("brand_dna", {}) or {}
    visual = project.get("visual_identity", {}) or {}
    content = project.get("content_strategy", {}) or {}
    launch = project.get("launch_strategy", {}) or {}
    critic = project.get("brand_critic", {}) or {}

    story = []
    story.append(Paragraph("BRANDFORGE AI", small))
    story.append(Paragraph(_safe(pos.get("brand_name") or pos.get("niche") or "Personal Brand"), title))
    story.append(Paragraph(_safe(pos.get("positioning_statement")), body))
    story.append(Spacer(1, 6))

    story.append(Paragraph("01 · POSITIONING", section))
    position_rows = [
        [Paragraph("Audience", body), Paragraph(_safe(pos.get("target_audience")), body)],
        [Paragraph("Problem", body), Paragraph(_safe(pos.get("audience_problem")), body)],
        [Paragraph("Value Proposition", body), Paragraph(_safe(pos.get("value_proposition")), body)],
        [Paragraph("Unique Angle", body), Paragraph(_safe(pos.get("unique_angle")), body)],
        [Paragraph("Point of View", body), Paragraph(_safe(pos.get("point_of_view")), body)],
    ]
    table = Table(position_rows, colWidths=[38 * mm, 132 * mm], hAlign="LEFT")
    table.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (0, -1), colors.HexColor("#EFF6FF")),
        ("BOX", (0, 0), (-1, -1), 0.4, colors.HexColor("#CBD5E1")),
        ("INNERGRID", (0, 0), (-1, -1), 0.25, colors.HexColor("#E2E8F0")),
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("LEFTPADDING", (0, 0), (-1, -1), 7),
        ("RIGHTPADDING", (0, 0), (-1, -1), 7),
        ("TOPPADDING", (0, 0), (-1, -1), 6),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 6),
    ]))
    story.append(table)

    story.append(Paragraph("02 · BRAND DNA", section))
    personality = dna.get("personality", []) or []
    personality_text = ", ".join(
        item.get("trait", "") if isinstance(item, dict) else str(item)
        for item in personality
    )
    story.append(Paragraph(f"<b>Personality:</b> {personality_text}", body))
    story.append(Paragraph(f"<b>Tagline:</b> {dna.get('recommended_tagline', '')}", body))
    voice = dna.get("voice", {}) or {}
    story.append(Paragraph(f"<b>Voice:</b> {_safe(voice.get('should_sound_like'))}", body))

    story.append(Paragraph("03 · VISUAL IDENTITY", section))
    logo = visual.get("logo_direction", {}) or {}
    story.append(Paragraph(f"<b>Logo:</b> {_safe(logo.get('concept'))}", body))
    palette = visual.get("palette", []) or []
    palette_data = [[Paragraph("Name", small), Paragraph("HEX", small), Paragraph("Role", small)]]
    for item in palette:
        if isinstance(item, dict):
            palette_data.append([
                Paragraph(_safe(item.get("name")), body),
                Paragraph(_safe(item.get("hex")), body),
                Paragraph(_safe(item.get("role")), body),
            ])
    pt = Table(palette_data, colWidths=[38 * mm, 30 * mm, 102 * mm])
    pt.setStyle(TableStyle([
        ("BOX", (0, 0), (-1, -1), 0.4, colors.HexColor("#CBD5E1")),
        ("INNERGRID", (0, 0), (-1, -1), 0.25, colors.HexColor("#E2E8F0")),
        ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#F8FAFC")),
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("LEFTPADDING", (0, 0), (-1, -1), 6),
        ("RIGHTPADDING", (0, 0), (-1, -1), 6),
    ]))
    story.append(pt)

    story.append(Paragraph("04 · CONTENT SYSTEM", section))
    for pillar in content.get("content_pillars", []) or []:
        if isinstance(pillar, dict):
            examples = ", ".join(pillar.get("example_topics", [])[:3])
            story.append(KeepTogether([
                Paragraph(f"<b>{_safe(pillar.get('name'))}</b>", body),
                Paragraph(f"{_safe(pillar.get('promise'))} · Examples: {examples}", small),
            ]))

    story.append(Paragraph("05 · FIRST 10 POSTS", section))
    for post in content.get("first_10_posts", []) or []:
        if isinstance(post, dict):
            story.append(Paragraph(
                f"<b>{_safe(post.get('number'))}. {_safe(post.get('hook'))}</b><br/>{_safe(post.get('idea'))}",
                body,
            ))

    story.append(Paragraph("06 · LAUNCH", section))
    story.append(Paragraph(f"<b>Bio:</b> {_safe(launch.get('profile_bio'))}", body))
    story.append(Paragraph(f"<b>Intro:</b> {_safe(launch.get('intro_post'))}", body))
    story.append(Paragraph(f"<b>CTA:</b> {_safe(launch.get('launch_cta'))}", body))

    story.append(Paragraph("07 · AI CRITIC", section))
    story.append(Paragraph(f"<b>Status:</b> {_safe(critic.get('status'))}", body))
    for finding in critic.get("findings", [])[:8]:
        if isinstance(finding, dict):
            story.append(Paragraph(
                f"<b>{_safe(finding.get('severity')).upper()} · {_safe(finding.get('area'))}</b>: {_safe(finding.get('issue'))} — Fix: {_safe(finding.get('fix'))}",
                body,
            ))

    story.append(Spacer(1, 10))
    story.append(Paragraph(
        "Generated by BrandForge AI. Research mode and source links should be reviewed before public claims are published.",
        small,
    ))

    doc.build(story)
    return buffer.getvalue()
