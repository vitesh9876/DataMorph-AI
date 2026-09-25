import os
import logging
from typing import Dict, Any, List, Optional
import pandas as pd
from app.services.extractors.base import ExtractionResult
from app.services.extractors.tabular import TabularExtractor
from app.services.extractors.pdf_extractor import PDFExtractor
from app.services.extractors.docx_extractor import DOCXExtractor
from app.services.extractors.pptx_extractor import PPTXExtractor
from app.services.extractors.text_extractor import TextExtractor
from app.services.ai_client import ai_client

logger = logging.getLogger(__name__)

class ExtractionPipeline:
    """Master orchestrator for multi-format extraction and intelligent metadata discovery."""

    @classmethod
    async def extract_file(cls, file_path: str, original_filename: str) -> ExtractionResult:
        ext = os.path.splitext(original_filename)[1].lower().replace(".", "")
        
        # 1. Format-specific extraction
        if ext in ["csv", "tsv"]:
            result = TabularExtractor.extract_csv(file_path)
        elif ext in ["xlsx", "xls"]:
            result = TabularExtractor.extract_excel(file_path)
        elif ext in ["json"]:
            result = TabularExtractor.extract_json(file_path)
        elif ext in ["xml"]:
            result = TabularExtractor.extract_xml(file_path)
        elif ext in ["pdf"]:
            result = PDFExtractor.extract_pdf(file_path)
        elif ext in ["docx", "doc"]:
            result = DOCXExtractor.extract_docx(file_path)
        elif ext in ["pptx", "ppt"]:
            result = PPTXExtractor.extract_pptx(file_path)
        elif ext in ["txt", "log", "md"]:
            result = TextExtractor.extract_text(file_path)
        else:
            # Fallback to text parsing
            result = TextExtractor.extract_text(file_path)

        # 2. Enrich with column metadata & statistical analysis
        df = result.dataframe
        if df is not None and not df.empty:
            result.doc_stats["rows"] = int(len(df))
            result.doc_stats["columns"] = int(len(df.columns))

            # Detect topics & entities from columns and text
            detected_topics = cls._infer_topics(df, original_filename, result.raw_text)
            result.topics = detected_topics
            result.entities = cls._infer_entities(df)
            
            # Generate AI understanding
            result.summary = await cls._generate_ai_understanding(df, original_filename, detected_topics, result.data_type)
        else:
            result.topics = ["General Content"]
            result.summary = "Extracted document content successfully."

        return result

    @staticmethod
    def _infer_topics(df: pd.DataFrame, filename: str, raw_text: str) -> List[str]:
        topics = set()
        text_lower = (filename + " " + " ".join(df.columns.astype(str)) + " " + raw_text[:1000]).lower()

        keywords_map = {
            "Sales": ["sales", "revenue", "order", "invoice", "deal", "discount", "margin"],
            "Finance": ["revenue", "profit", "ebitda", "expense", "budget", "cost", "tax", "cash", "amount", "price"],
            "Customers": ["customer", "client", "buyer", "user", "account", "lead", "contact"],
            "Products": ["product", "item", "sku", "category", "inventory", "stock", "goods"],
            "Operations": ["shipping", "status", "delivery", "supplier", "warehouse", "logistics"],
            "Locations": ["city", "country", "state", "region", "zip", "location", "address", "zone"],
            "Marketing": ["campaign", "clicks", "impressions", "conversion", "channel", "ad"],
            "HR": ["employee", "salary", "department", "tenure", "hiring", "headcount"]
        }

        for topic, kws in keywords_map.items():
            if any(kw in text_lower for kw in kws):
                topics.add(topic)

        if not topics:
            topics.add("Operational Data")
            topics.add("Metrics")

        return list(topics)[:6]

    @staticmethod
    def _infer_entities(df: pd.DataFrame) -> List[Dict[str, Any]]:
        entities = []
        for col in df.columns:
            col_lower = str(col).lower()
            entity_type = "attribute"
            if any(k in col_lower for k in ["id", "code", "sku", "key", "number"]):
                entity_type = "identifier"
            elif any(k in col_lower for k in ["date", "time", "year", "month", "day"]):
                entity_type = "temporal"
            elif any(k in col_lower for k in ["price", "cost", "revenue", "amount", "salary", "profit", "sales", "qty", "quantity", "count"]):
                entity_type = "metric"
            elif any(k in col_lower for k in ["name", "category", "type", "city", "country", "status", "department"]):
                entity_type = "dimension"
            
            entities.append({
                "column": str(col),
                "type": entity_type,
                "unique_values_count": int(df[col].nunique()) if col in df else 0
            })
        return entities

    @classmethod
    async def _generate_ai_understanding(cls, df: pd.DataFrame, filename: str, topics: List[str], data_type: str) -> str:
        columns_str = ", ".join(df.columns.astype(str)[:15])
        prompt = (
            f"Generate a concise 2-3 sentence AI understanding explanation of this dataset/document for an executive summary.\n"
            f"File: {filename}\n"
            f"Data Type: {data_type}\n"
            f"Detected Topics: {', '.join(topics)}\n"
            f"Columns: {columns_str}\n"
            f"Rows: {len(df)}\n"
            f"Explain in simple language what information it contains and what analyses it is suitable for (e.g. trend analysis, category comparison, anomaly detection)."
        )
        return await ai_client.generate_text(prompt)
