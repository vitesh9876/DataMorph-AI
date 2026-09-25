import os
import io
import re
from typing import List, Dict, Any

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors
from reportlab.platypus import (
    SimpleDocTemplate, 
    Paragraph, 
    Spacer, 
    Table, 
    TableStyle, 
    HRFlowable,
    Image,
    KeepTogether
)
from reportlab.lib.units import inch

class PDFExporter:
    """Exports visual intelligence reports to PDF with DataMorph AI header branding, real charts, and structured dataset tables."""

    @classmethod
    def _create_chart_image(cls, chart_type: str, chart_data: List[Dict[str, Any]], title: str) -> io.BytesIO:
        """Generates a high-resolution Matplotlib chart image and returns bytes buffer."""
        fig, ax = plt.subplots(figsize=(6.2, 2.7), dpi=180)
        fig.patch.set_facecolor("#FFFFFF")
        ax.set_facecolor("#FAFAFC")

        palette = ["#2E5BFF", "#943FE2", "#10B981", "#F59E0B", "#EF4444", "#38BDF8", "#EC4899", "#8B5CF6"]

        clean_pts = []
        for d in chart_data[:10]:
            name = str(d.get("name", d.get("label", "Item")))[:18]
            val = d.get("value", 0)
            try:
                num = float(val) if val is not None else 0.0
            except Exception:
                num = 0.0
            clean_pts.append((name, num))

        if not clean_pts:
            clean_pts = [("No Data", 0)]

        names = [p[0] for p in clean_pts]
        vals = [p[1] for p in clean_pts]
        c_type = (chart_type or "bar").lower()

        if c_type in ["pie", "donut"]:
            valid_idx = [i for i, v in enumerate(vals) if v > 0]
            if not valid_idx:
                valid_idx = list(range(len(vals)))
            p_vals = [vals[i] for i in valid_idx]
            p_names = [names[i] for i in valid_idx]
            p_cols = [palette[i % len(palette)] for i in range(len(p_vals))]

            wedges, texts, autotexts = ax.pie(
                p_vals,
                labels=p_names,
                autopct="%1.1f%%",
                startangle=140,
                colors=p_cols,
                textprops=dict(color="#1E293B", fontsize=7.5),
                pctdistance=0.75 if c_type == "donut" else 0.6
            )
            for autotext in autotexts:
                autotext.set_color("white")
                autotext.set_fontsize(7.5)
                autotext.set_weight("bold")

            if c_type == "donut":
                centre_circle = plt.Circle((0, 0), 0.50, fc="white")
                fig.gca().add_artist(centre_circle)

            ax.axis("equal")

        elif c_type == "line":
            ax.plot(names, vals, marker="o", markersize=5, linewidth=2.2, color="#2E5BFF", label="Value")
            ax.fill_between(range(len(names)), vals, alpha=0.15, color="#2E5BFF")
            ax.set_xticks(range(len(names)))
            ax.set_xticklabels(names, rotation=25, ha="right", fontsize=7.5, color="#475569")
            ax.tick_params(axis="y", labelsize=7.5, colors="#475569")
            for i, txt in enumerate(vals):
                ax.annotate(f"{txt:,.1f}" if isinstance(txt, float) else str(txt), 
                            (i, txt), textcoords="offset points", xytext=(0, 6), ha="center", fontsize=7, color="#1E293B", weight="bold")

        elif c_type == "area":
            ax.fill_between(range(len(names)), vals, alpha=0.4, color="#943FE2")
            ax.plot(names, vals, color="#943FE2", linewidth=2)
            ax.set_xticks(range(len(names)))
            ax.set_xticklabels(names, rotation=25, ha="right", fontsize=7.5, color="#475569")
            ax.tick_params(axis="y", labelsize=7.5, colors="#475569")

        elif c_type in ["horizontal_bar", "leaderboard"]:
            y_pos = np.arange(len(names))
            bars = ax.barh(y_pos, vals, color=[palette[i % len(palette)] for i in range(len(names))], height=0.6, edgecolor="none")
            ax.set_yticks(y_pos)
            ax.set_yticklabels(names, fontsize=7.5, color="#1E293B")
            ax.invert_yaxis()
            ax.tick_params(axis="x", labelsize=7.5, colors="#475569")
            max_v = max(vals) if vals and max(vals) > 0 else 1
            for bar in bars:
                w = bar.get_width()
                ax.text(w + max_v * 0.02, bar.get_y() + bar.get_height() / 2, f"{w:,.1f}", ha="left", va="center", fontsize=7, color="#1E293B", weight="bold")

        else: # Standard vertical bar chart
            x_pos = np.arange(len(names))
            bars = ax.bar(x_pos, vals, color=[palette[i % len(palette)] for i in range(len(names))], width=0.55, edgecolor="none")
            ax.set_xticks(x_pos)
            ax.set_xticklabels(names, rotation=25, ha="right", fontsize=7.5, color="#475569")
            ax.tick_params(axis="y", labelsize=7.5, colors="#475569")
            max_v = max(vals) if vals and max(vals) > 0 else 1
            for bar in bars:
                h = bar.get_height()
                ax.text(bar.get_x() + bar.get_width() / 2.0, h + max_v * 0.02, f"{h:,.1f}", ha="center", va="bottom", fontsize=7, color="#1E293B", weight="bold")

        # Clean gridlines
        ax.spines["top"].set_visible(False)
        ax.spines["right"].set_visible(False)
        ax.spines["left"].set_color("#E2E8F0")
        ax.spines["bottom"].set_color("#E2E8F0")
        if c_type not in ["pie", "donut"]:
            ax.yaxis.grid(True, linestyle="--", alpha=0.5, color="#E2E8F0")

        plt.tight_layout()
        buf = io.BytesIO()
        plt.savefig(buf, format="png", dpi=200, bbox_inches="tight")
        buf.seek(0)
        plt.close(fig)
        return buf

    @classmethod
    def export_to_pdf(
        cls,
        output_path: str,
        report_title: str,
        template_type: str,
        sections: List[Dict[str, Any]]
    ) -> str:
        doc = SimpleDocTemplate(
            output_path,
            pagesize=letter,
            rightMargin=0.6 * inch,
            leftMargin=0.6 * inch,
            topMargin=0.6 * inch,
            bottomMargin=0.6 * inch
        )

        styles = getSampleStyleSheet()

        brand_style = ParagraphStyle(
            "BrandHeader",
            parent=styles["Normal"],
            fontName="Helvetica-Bold",
            fontSize=10,
            leading=12,
            textColor=colors.HexColor("#6366F1"),
            spaceAfter=2
        )

        title_style = ParagraphStyle(
            "DocTitle",
            parent=styles["Heading1"],
            fontName="Helvetica-Bold",
            fontSize=20,
            leading=24,
            textColor=colors.HexColor("#0F172A"),
            spaceAfter=3
        )

        subtitle_style = ParagraphStyle(
            "DocSubTitle",
            parent=styles["Normal"],
            fontName="Helvetica",
            fontSize=9,
            leading=13,
            textColor=colors.HexColor("#64748B"),
            spaceAfter=8
        )

        heading_style = ParagraphStyle(
            "SectionHeading",
            parent=styles["Heading2"],
            fontName="Helvetica-Bold",
            fontSize=12,
            leading=16,
            textColor=colors.HexColor("#1E293B"),
            spaceBefore=8,
            spaceAfter=4
        )

        badge_style = ParagraphStyle(
            "BadgeStyle",
            parent=styles["Normal"],
            fontName="Helvetica-Bold",
            fontSize=8,
            leading=10,
            textColor=colors.HexColor("#6366F1"),
            spaceAfter=4
        )

        body_style = ParagraphStyle(
            "SectionBody",
            parent=styles["Normal"],
            fontName="Helvetica",
            fontSize=8.5,
            leading=12,
            textColor=colors.HexColor("#334155"),
            spaceAfter=4
        )

        table_header_style = ParagraphStyle(
            "TableHeader",
            parent=styles["Normal"],
            fontName="Helvetica-Bold",
            fontSize=8,
            leading=10,
            textColor=colors.white
        )

        table_cell_style = ParagraphStyle(
            "TableCell",
            parent=styles["Normal"],
            fontName="Helvetica",
            fontSize=8,
            leading=10,
            textColor=colors.HexColor("#1E293B")
        )

        story = []

        # 🌟 Header Branding Only
        story.append(Paragraph("DATAMORPH AI • VISUAL INTELLIGENCE WORKSPACE", brand_style))
        story.append(Paragraph(report_title, title_style))
        story.append(Paragraph("Automated Data Structuring & Verified Visual Analytics", subtitle_style))
        story.append(HRFlowable(width="100%", thickness=2, color=colors.HexColor("#6366F1"), spaceAfter=10))

        for s in sections:
            if not s.get("is_visible", True):
                continue

            sec_type = s.get("section_type", "")
            if sec_type == "title_page":
                continue

            sec_title = s.get("title", "")
            raw_content = s.get("content", "")
            chart_data = s.get("chart_data") or []
            chart_type = s.get("chart_type") or "bar"

            section_elements = []

            # 1. Executive Summary Section
            if sec_type == "executive_summary":
                section_elements.append(Paragraph(sec_title, heading_style))
                formatted = re.sub(r"\*\*(.*?)\*\*", r"<b>\1</b>", raw_content)
                summary_table = Table(
                    [[Paragraph(formatted, body_style)]],
                    colWidths=[480]
                )
                summary_table.setStyle(TableStyle([
                    ("BACKGROUND", (0, 0), (-1, -1), colors.HexColor("#F8FAFC")),
                    ("BOX", (0, 0), (-1, -1), 1, colors.HexColor("#E2E8F0")),
                    ("TOPPADDING", (0, 0), (-1, -1), 8),
                    ("BOTTOMPADDING", (0, 0), (-1, -1), 8),
                    ("LEFTPADDING", (0, 0), (-1, -1), 10),
                    ("RIGHTPADDING", (0, 0), (-1, -1), 10),
                ]))
                section_elements.append(summary_table)
                section_elements.append(Spacer(1, 10))
                story.append(KeepTogether(section_elements))
                continue

            # 2. Structured Dataset Table Section
            if sec_type == "structured_table":
                section_elements.append(Paragraph(sec_title, heading_style))
                section_elements.append(Paragraph(raw_content, body_style))
                section_elements.append(Spacer(1, 4))

                table_data = s.get("table_data") or []
                table_columns = s.get("table_columns") or []
                if not table_columns and table_data:
                    table_columns = list(table_data[0].keys())

                if table_data and table_columns:
                    disp_cols = table_columns[:6]
                    col_w = int(480 / len(disp_cols))

                    t_rows = [[Paragraph(c, table_header_style) for c in disp_cols]]
                    for row in table_data[:25]:
                        t_rows.append([Paragraph(str(row.get(c, "—")), table_cell_style) for c in disp_cols])

                    t = Table(t_rows, colWidths=[col_w] * len(disp_cols))
                    t.setStyle(TableStyle([
                        ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#6366F1")),
                        ("ALIGN", (0, 0), (-1, -1), "LEFT"),
                        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
                        ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.HexColor("#F8FAFC"), colors.white]),
                        ("GRID", (0, 0), (-1, -1), 0.5, colors.HexColor("#CBD5E1")),
                        ("TOPPADDING", (0, 0), (-1, -1), 3),
                        ("BOTTOMPADDING", (0, 0), (-1, -1), 3),
                        ("LEFTPADDING", (0, 0), (-1, -1), 4),
                        ("RIGHTPADDING", (0, 0), (-1, -1), 4),
                    ]))
                    section_elements.append(t)

                section_elements.append(Spacer(1, 12))
                story.extend(section_elements)
                continue

            # 3. Visual Chart Section
            section_elements.append(Paragraph(sec_title, heading_style))
            section_elements.append(Paragraph(f"ARCHETYPE: {chart_type.upper().replace('_', ' ')}", badge_style))

            # Extract Analytical finding narrative
            analysis_match = re.search(r"\*\*Analysis:\*\*\s*(.*?)(?=\*\*Data Breakdown|\Z)", raw_content, re.DOTALL)
            if analysis_match:
                finding_text = analysis_match.group(1).strip()
                if finding_text:
                    section_elements.append(Paragraph(f"<b>Key Insight:</b> {finding_text}", body_style))

            # 🌟 REAL VISUAL CHART GRAPHIC IMAGE
            if chart_data and len(chart_data) > 0:
                try:
                    img_buf = cls._create_chart_image(chart_type, chart_data, sec_title)
                    chart_img = Image(img_buf, width=480, height=205)
                    section_elements.append(Spacer(1, 4))
                    section_elements.append(chart_img)
                    section_elements.append(Spacer(1, 4))
                except Exception as img_err:
                    pass

                # Compact Data Breakdown Table below chart
                clean_pts = []
                for d in chart_data[:8]:
                    name = str(d.get("name", d.get("label", "Item")))[:24]
                    val = d.get("value", 0)
                    clean_pts.append((name, val))

                table_rows = [
                    [
                        Paragraph("Dimension / Test Metric", table_header_style),
                        Paragraph("Measured Value", table_header_style)
                    ]
                ]
                for name, val in clean_pts:
                    v_str = f"{val:,.2f}" if isinstance(val, float) else str(val)
                    table_rows.append([
                        Paragraph(name, table_cell_style),
                        Paragraph(v_str, table_cell_style)
                    ])

                t = Table(table_rows, colWidths=[280, 200])
                t.setStyle(TableStyle([
                    ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#6366F1")),
                    ("ALIGN", (0, 0), (-1, -1), "LEFT"),
                    ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
                    ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.HexColor("#F8FAFC"), colors.white]),
                    ("GRID", (0, 0), (-1, -1), 0.5, colors.HexColor("#E2E8F0")),
                    ("TOPPADDING", (0, 0), (-1, -1), 3),
                    ("BOTTOMPADDING", (0, 0), (-1, -1), 3),
                    ("LEFTPADDING", (0, 0), (-1, -1), 6),
                    ("RIGHTPADDING", (0, 0), (-1, -1), 6),
                ]))
                section_elements.append(t)

            section_elements.append(Spacer(1, 12))
            story.append(KeepTogether(section_elements))

        # Footer
        story.append(Spacer(1, 8))
        story.append(HRFlowable(width="100%", thickness=0.75, color=colors.HexColor("#E2E8F0"), spaceAfter=4))
        story.append(Paragraph("<font size=7.5 color='#94A3B8'>DataMorph AI • Confidential Intelligence Analysis</font>", body_style))

        doc.build(story)
        return output_path
