from typing import List, Dict, Any
from app.services.report.templates import TEMPLATES_CONFIG

class HTMLExporter:
    """Generates standalone styled HTML reports."""

    @classmethod
    def export_to_html(
        cls,
        output_path: str,
        report_title: str,
        sections: List[Dict[str, Any]],
        template_type: str = "professional",
        selected_charts: List[Dict[str, Any]] = None
    ) -> str:
        html_str = cls.generate_html_report(
            report_title=report_title,
            template_type=template_type,
            sections=sections,
            selected_charts=selected_charts or []
        )
        with open(output_path, "w", encoding="utf-8") as f:
            f.write(html_str)
        return output_path

    @classmethod
    def generate_html_report(
        cls,
        report_title: str,
        template_type: str,
        sections: List[Dict[str, Any]],
        selected_charts: List[Dict[str, Any]]
    ) -> str:
        tpl = TEMPLATES_CONFIG.get(template_type, TEMPLATES_CONFIG["professional"])
        primary = tpl.get("primary_color", "#1E3A8A")
        accent = tpl.get("accent_color", "#3B82F6")
        font_family = tpl.get("font_family", "Inter, sans-serif")

        sections_html = []
        for s in sections:
            if not s.get("is_visible", True):
                continue

            sec_title = s.get("title", "")
            raw_content = s.get("content", "")
            # Convert markdown linebreaks and bold
            formatted_content = raw_content.replace("\n", "<br/>")
            import re
            formatted_content = re.sub(r"\*\*(.*?)\*\*", r"<strong>\1</strong>", formatted_content)

            sec_html = f"""
            <div class="report-section">
                <h2 class="section-title">{sec_title}</h2>
                <div class="section-body">{formatted_content}</div>
            </div>
            """
            sections_html.append(sec_html)

        html_template = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{report_title} - DataMorph AI</title>
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&family=Outfit:wght@400;600;700&display=swap');
        
        * {{
            box-sizing: border-box;
            margin: 0;
            padding: 0;
        }}
        body {{
            font-family: {font_family};
            background-color: #F8FAFC;
            color: #1E293B;
            line-height: 1.6;
            padding: 40px 20px;
        }}
        .report-container {{
            max-width: 900px;
            margin: 0 auto;
            background: #FFFFFF;
            border-radius: 16px;
            box-shadow: 0 10px 25px -5px rgba(0, 0, 0, 0.05);
            border: 1px solid #E2E8F0;
            overflow: hidden;
        }}
        .report-header {{
            background: {primary};
            color: #FFFFFF;
            padding: 40px;
            border-bottom: 4px solid {accent};
        }}
        .report-header h1 {{
            font-size: 28px;
            font-weight: 700;
            margin-bottom: 8px;
        }}
        .report-header .meta {{
            font-size: 14px;
            opacity: 0.85;
        }}
        .report-content {{
            padding: 40px;
        }}
        .report-section {{
            margin-bottom: 35px;
            padding-bottom: 25px;
            border-bottom: 1px solid #F1F5F9;
        }}
        .report-section:last-child {{
            border-bottom: none;
        }}
        .section-title {{
            font-size: 20px;
            color: {primary};
            font-weight: 600;
            margin-bottom: 15px;
            display: flex;
            align-items: center;
            gap: 10px;
        }}
        .section-body {{
            font-size: 15px;
            color: #334155;
            line-height: 1.7;
        }}
        .report-footer {{
            background: #F8FAFC;
            border-top: 1px solid #E2E8F0;
            padding: 20px 40px;
            font-size: 13px;
            color: #64748B;
            display: flex;
            justify-content: space-between;
            align-items: center;
        }}
        .badge {{
            display: inline-block;
            padding: 4px 10px;
            background: {accent}22;
            color: {accent};
            border-radius: 999px;
            font-size: 12px;
            font-weight: 600;
        }}
        @media print {{
            body {{ background: #FFF; padding: 0; }}
            .report-container {{ box-shadow: none; border: none; }}
        }}
    </style>
</head>
<body>
    <div class="report-container">
        <header class="report-header">
            <span class="badge">DataMorph AI Report</span>
            <h1 style="margin-top: 10px;">{report_title}</h1>
            <div class="meta">Automated Intelligence & Data Structuring Workspace</div>
        </header>
        <main class="report-content">
            {"".join(sections_html)}
        </main>
        <footer class="report-footer">
            <span>Generated by DataMorph AI</span>
            <span>Confidential & Proprietary</span>
        </footer>
    </div>
</body>
</html>
"""
        return html_template
