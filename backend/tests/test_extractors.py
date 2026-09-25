import os
import pytest
from app.services.extractors.pipeline import ExtractionPipeline
from app.services.extractors.tabular import TabularExtractor
from app.services.extractors.pdf_extractor import PDFExtractor
from app.services.extractors.docx_extractor import DOCXExtractor

SAMPLE_DIR = os.path.join(os.path.dirname(__file__), "..", "..", "sample_data")

@pytest.mark.asyncio
async def test_csv_extraction():
    file_path = os.path.join(SAMPLE_DIR, "sales_dirty.csv")
    assert os.path.exists(file_path)
    
    result = await ExtractionPipeline.extract_file(file_path, "sales_dirty.csv")
    assert result.dataframe is not None
    assert len(result.dataframe) > 0
    assert result.doc_stats["rows"] > 0
    assert "Sales" in result.topics or "Revenue" in result.topics or len(result.topics) > 0

@pytest.mark.asyncio
async def test_excel_extraction():
    file_path = os.path.join(SAMPLE_DIR, "financial_report.xlsx")
    assert os.path.exists(file_path)

    result = await ExtractionPipeline.extract_file(file_path, "financial_report.xlsx")
    assert result.dataframe is not None
    assert result.doc_stats["pages"] == 2 # 2 sheets
    assert "Revenue" in result.dataframe.columns

@pytest.mark.asyncio
async def test_docx_extraction():
    file_path = os.path.join(SAMPLE_DIR, "project_summary.docx")
    assert os.path.exists(file_path)

    result = await ExtractionPipeline.extract_file(file_path, "project_summary.docx")
    assert result.dataframe is not None
    assert len(result.tables) >= 1

@pytest.mark.asyncio
async def test_pdf_extraction():
    file_path = os.path.join(SAMPLE_DIR, "quarterly_report.pdf")
    assert os.path.exists(file_path)

    result = await ExtractionPipeline.extract_file(file_path, "quarterly_report.pdf")
    assert result.dataframe is not None
    assert len(result.tables) >= 1
