import os
import pytest
import pandas as pd
from app.config import settings
from app.services.export.pdf_exporter import PDFExporter
from app.services.export.docx_exporter import DOCXExporter
from app.services.export.pptx_exporter import PPTXExporter
from app.services.export.xlsx_exporter import XLSXExporter
from app.services.export.html_exporter import HTMLExporter

def test_multi_format_exports():
    test_sections = [
        {
            "id": "s1",
            "section_type": "title_page",
            "title": "DataMorph AI Executive Intelligence Report",
            "content": "Automated dataset analysis and insights.",
            "is_visible": True
        },
        {
            "id": "s2",
            "section_type": "executive_summary",
            "title": "Executive Summary",
            "content": "The dataset shows **strong growth** across top categories.",
            "is_visible": True
        }
    ]

    export_dir = settings.EXPORT_DIR
    os.makedirs(export_dir, exist_ok=True)

    # 1. HTML
    html_path = os.path.join(export_dir, "test_report.html")
    html_content = HTMLExporter.generate_html_report(
        report_title="Test Intelligence Report",
        template_type="professional",
        sections=test_sections,
        selected_charts=[]
    )
    with open(html_path, "w", encoding="utf-8") as f:
        f.write(html_content)
    assert os.path.exists(html_path)
    assert os.path.getsize(html_path) > 100

    # 2. DOCX
    docx_path = os.path.join(export_dir, "test_report.docx")
    DOCXExporter.export_to_docx(
        output_path=docx_path,
        report_title="Test Report",
        template_type="professional",
        sections=test_sections
    )
    assert os.path.exists(docx_path)
    assert os.path.getsize(docx_path) > 500

    # 3. PPTX
    pptx_path = os.path.join(export_dir, "test_report.pptx")
    PPTXExporter.export_to_pptx(
        output_path=pptx_path,
        report_title="Test Presentation",
        template_type="professional",
        sections=test_sections
    )
    assert os.path.exists(pptx_path)
    assert os.path.getsize(pptx_path) > 500

    # 4. XLSX
    xlsx_path = os.path.join(export_dir, "test_report.xlsx")
    df = pd.DataFrame({"Category": ["A", "B"], "Revenue": [1000, 2000]})
    XLSXExporter.export_to_xlsx(
        output_path=xlsx_path,
        df=df,
        quality_score=92.5,
        recommendations=[],
        anomalies=[]
    )
    assert os.path.exists(xlsx_path)
    assert os.path.getsize(xlsx_path) > 500

    # 5. PDF
    pdf_path = os.path.join(export_dir, "test_report.pdf")
    PDFExporter.export_to_pdf(
        output_path=pdf_path,
        report_title="Test PDF Report",
        template_type="professional",
        sections=test_sections
    )
    assert os.path.exists(pdf_path)
    assert os.path.getsize(pdf_path) > 500
