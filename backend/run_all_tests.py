import asyncio
import os
import sys

# Ensure sys.path includes backend
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

from app.database import init_db
from app.services.extractors.pipeline import ExtractionPipeline
from app.services.structuring.normalizer import DataNormalizer
from app.services.structuring.quality import QualityAnalyzer
from app.services.structuring.cleaner import DataCleaner
from app.services.ml.anomaly import AnomalyDetector
from app.services.ml.forecasting import TimeSeriesForecaster
from app.services.ml.clustering import CorrelationEngine
from app.services.visualization.recommender import VisualizationRecommender
from app.services.visualization.aggregator import ChartAggregator
from app.services.ask_data.engine import AskDataEngine
from app.services.export.pdf_exporter import PDFExporter
from app.services.export.docx_exporter import DOCXExporter
from app.services.export.pptx_exporter import PPTXExporter
from app.services.export.xlsx_exporter import XLSXExporter
from app.services.export.html_exporter import HTMLExporter
from app.config import settings
import pandas as pd

SAMPLE_DIR = os.path.join(os.path.dirname(__file__), "..", "sample_data")

async def test_suite():
    print("========================================")
    print("STARTING DATAMORPH AI BACKEND TEST SUITE")
    print("========================================")
    
    # 0. Database Init
    await init_db()
    print(" [OK] Database initialized successfully.")

    # 1. Extractors Test
    print("\n--- Testing File Extractors ---")
    res_csv = await ExtractionPipeline.extract_file(os.path.join(SAMPLE_DIR, "sales_dirty.csv"), "sales_dirty.csv")
    assert res_csv.dataframe is not None and len(res_csv.dataframe) > 0
    print(f" [OK] CSV Extractor: {len(res_csv.dataframe)} rows, topics: {res_csv.topics}")

    res_xlsx = await ExtractionPipeline.extract_file(os.path.join(SAMPLE_DIR, "financial_report.xlsx"), "financial_report.xlsx")
    assert res_xlsx.dataframe is not None and res_xlsx.doc_stats["pages"] == 2
    print(f" [OK] XLSX Extractor: {res_xlsx.doc_stats['pages']} sheets parsed.")

    res_docx = await ExtractionPipeline.extract_file(os.path.join(SAMPLE_DIR, "project_summary.docx"), "project_summary.docx")
    assert res_docx.dataframe is not None
    print(f" [OK] DOCX Extractor: {len(res_docx.tables)} tables parsed.")

    res_pdf = await ExtractionPipeline.extract_file(os.path.join(SAMPLE_DIR, "quarterly_report.pdf"), "quarterly_report.pdf")
    assert res_pdf.dataframe is not None
    print(f" [OK] PDF Extractor: {len(res_pdf.tables)} tables parsed.")

    # 2. Structuring & Normalization
    print("\n--- Testing Data Structuring & Quality ---")
    val, ok = DataNormalizer.clean_currency_or_number("₹1,00,000")
    assert ok and val == 100000.0
    val_neg, ok_neg = DataNormalizer.clean_currency_or_number("(500.50)")
    assert ok_neg and val_neg == -500.50

    d, d_ok = DataNormalizer.standardize_date("01/16/2024")
    assert d_ok and d == "2024-01-16"

    dirty_df = pd.read_csv(os.path.join(SAMPLE_DIR, "sales_dirty.csv"))
    quality_before = QualityAnalyzer.evaluate_quality(dirty_df)
    print(f" [OK] Initial Data Quality Score: {quality_before['overall_score']:.1f}%")

    recs = DataCleaner.generate_recommendations(dirty_df)
    print(f" [OK] Generated {len(recs)} cleaning recommendations.")
    assert len(recs) > 0

    cleaned_df = dirty_df.copy()
    for r in recs:
        cleaned_df = DataCleaner.apply_rule(
            df=cleaned_df,
            rule_type=r["rule_type"],
            target_column=r["target_column"],
            suggested_action=r["suggested_action"],
            parameters=r.get("parameters", {})
        )
    quality_after = QualityAnalyzer.evaluate_quality(cleaned_df)
    print(f" [OK] Post-Cleaning Data Quality Score: {quality_after['overall_score']:.1f}% (Gained +{quality_after['overall_score'] - quality_before['overall_score']:.1f}%)")

    # 3. Machine Learning Analytics
    print("\n--- Testing Machine Learning Modules ---")
    # Isolation Forest Anomaly Detection
    anomaly_res = AnomalyDetector.detect_anomalies(dirty_df, contamination=0.1)
    print(f" [OK] Isolation Forest: Detected {anomaly_res['total_anomalies']} anomalies ({anomaly_res['anomaly_percentage']}%).")
    assert anomaly_res["total_anomalies"] > 0

    # Forecasting
    dates = pd.date_range(start="2023-01-01", periods=12, freq="ME")
    revenue_series = [1000, 1150, 1280, 1400, 1550, 1680, 1800, 1950, 2100, 2250, 2400, 2600]
    forecast_df = pd.DataFrame({"Date": dates, "Revenue": revenue_series})
    forecast_res = TimeSeriesForecaster.generate_forecast(forecast_df, "Date", "Revenue", periods=6, frequency="M")
    print(f" [OK] Time-Series Forecast: {len(forecast_res['forecast_data'])} data points generated with 95% confidence intervals.")
    assert len(forecast_res["forecast_data"]) == 18

    # Correlations
    corr_res = CorrelationEngine.analyze_correlations(dirty_df)
    print(f" [OK] Correlation Engine: {len(corr_res['columns'])} numeric columns analyzed.")

    # 4. Visualization Recommender
    print("\n--- Testing Visualization Recommendation Engine ---")
    recommended_charts = VisualizationRecommender.recommend_charts(dirty_df)
    print(f" [OK] Recommended {len(recommended_charts)} charts:")
    for ch in recommended_charts:
        print(f"      • {ch['title']} ({ch['chart_type'].upper()}) - Confidence: {ch['confidence_score']}%")
    assert len(recommended_charts) >= 2

    # 5. Ask Your Data AI Engine
    print("\n--- Testing 'Ask Your Data' Engine ---")
    q1 = "Which product generated the highest revenue?"
    ans1 = await AskDataEngine.query_dataset(dirty_df, q1)
    print(f" [OK] Q: '{q1}'")
    print(f"      A: {ans1['answer']}")
    assert ans1["answer"] != ""

    # 6. Multi-Format Exporters
    print("\n--- Testing Multi-Format Exporters ---")
    export_dir = settings.EXPORT_DIR
    os.makedirs(export_dir, exist_ok=True)
    test_sections = [
        {"id": "1", "section_type": "title_page", "title": "Quarterly Intelligence Report", "content": "Executive overview.", "is_visible": True},
        {"id": "2", "section_type": "executive_summary", "title": "Executive Summary", "content": "Performance is **strong**.", "is_visible": True}
    ]

    html_file = os.path.join(export_dir, "test_report.html")
    with open(html_file, "w", encoding="utf-8") as f:
        f.write(HTMLExporter.generate_html_report("Test Report", "professional", test_sections, []))
    print(f" [OK] HTML Exported: {html_file} ({os.path.getsize(html_file):,} bytes)")

    docx_file = os.path.join(export_dir, "test_report.docx")
    DOCXExporter.export_to_docx(docx_file, "Test Report", "professional", test_sections)
    print(f" [OK] DOCX Exported: {docx_file} ({os.path.getsize(docx_file):,} bytes)")

    pptx_file = os.path.join(export_dir, "test_report.pptx")
    PPTXExporter.export_to_pptx(pptx_file, "Test Report", "professional", test_sections)
    print(f" [OK] PPTX Exported: {pptx_file} ({os.path.getsize(pptx_file):,} bytes)")

    xlsx_file = os.path.join(export_dir, "test_report.xlsx")
    XLSXExporter.export_to_xlsx(xlsx_file, cleaned_df, quality_after["overall_score"], recs, [])
    print(f" [OK] XLSX Exported: {xlsx_file} ({os.path.getsize(xlsx_file):,} bytes)")

    pdf_file = os.path.join(export_dir, "test_report.pdf")
    PDFExporter.export_to_pdf(pdf_file, "Test Report", "professional", test_sections)
    print(f" [OK] PDF Exported: {pdf_file} ({os.path.getsize(pdf_file):,} bytes)")

    print("\n========================================")
    print("ALL TESTS PASSED SUCCESSFULLY! (100%)")
    print("========================================")

if __name__ == "__main__":
    asyncio.run(test_suite())
