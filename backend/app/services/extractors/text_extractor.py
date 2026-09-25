import os
import re
import pandas as pd
from app.services.extractors.base import ExtractionResult
from app.services.extractors.unstructured_structurer import UnstructuredDataStructurer

class TextExtractor:
    """Extracts unstructured text, notes, logs, and transforms raw narrative & scattered data into structured tables while preserving full text."""

    @staticmethod
    def extract_text(file_path: str) -> ExtractionResult:
        with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
            content = f.read()

        lines = [line.strip() for line in content.splitlines() if line.strip()]

        # Try to detect if the text is CSV-like or tab-delimited
        sample_lines = lines[:20]
        detected_delimiter = None
        for delim in ["\t", "|", ","]:
            counts = [l.count(delim) for l in sample_lines]
            if len(counts) > 2 and all(c > 0 for c in counts) and len(set(counts)) <= 2:
                detected_delimiter = delim
                break

        if detected_delimiter:
            try:
                import io
                df = pd.read_csv(io.StringIO(content), sep=detected_delimiter, on_bad_lines="skip")
                data_type = "tabular"
                sections_count = 1
            except Exception:
                df, meta, sections = UnstructuredDataStructurer.structure_unstructured_text(content)
                data_type = "unstructured_text"
                sections_count = meta.get("sections_count", 1)
        else:
            # Unstructured text or notes with numbers/facts
            df, meta, sections = UnstructuredDataStructurer.structure_unstructured_text(content)
            data_type = "unstructured_text"
            sections_count = meta.get("sections_count", 1)

        return ExtractionResult(
            dataframe=df,
            raw_text=content[:8000],
            tables=[df],
            doc_stats={
                "pages": max(len(lines) // 40, 1),
                "tables": 1,
                "charts": 0,
                "sections": max(sections_count, 1),
                "rows": int(len(df)),
                "columns": int(len(df.columns))
            },
            data_type=data_type,
            metadata={"total_lines": len(lines)}
        )
