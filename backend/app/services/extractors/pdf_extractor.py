import fitz  # PyMuPDF
import pdfplumber
import logging
from typing import List, Dict, Any
import pandas as pd
from app.services.extractors.base import ExtractionResult
from app.services.extractors.unstructured_structurer import UnstructuredDataStructurer

logger = logging.getLogger(__name__)

class PDFExtractor:
    """Extracts tables, text, page count, and structure from PDF documents."""

    @staticmethod
    def extract_pdf(file_path: str) -> ExtractionResult:
        doc = fitz.open(file_path)
        page_count = len(doc)
        
        full_text_list = []
        image_count = 0
        
        # 1. PyMuPDF pass for metadata, text, and visual image count
        for i, page in enumerate(doc):
            full_text_list.append(page.get_text())
            image_list = page.get_images()
            image_count += len(image_list)

        raw_text = "\n\n".join(full_text_list)

        # 2. pdfplumber pass for precise table extraction
        extracted_tables: List[pd.DataFrame] = []
        try:
            with pdfplumber.open(file_path) as pdf:
                for page in pdf.pages:
                    tables = page.extract_tables()
                    for table in tables:
                        if table and len(table) > 1:
                            raw_header = table[0]
                            header = [str(col).strip() if col is not None else f"Column_{j+1}" for j, col in enumerate(raw_header)]
                            
                            rows = []
                            for r in table[1:]:
                                if any(cell is not None and str(cell).strip() != "" for cell in r):
                                    clean_row = [str(c).strip() if c is not None else "" for c in r]
                                    if len(clean_row) < len(header):
                                        clean_row += [""] * (len(header) - len(clean_row))
                                    else:
                                        clean_row = clean_row[:len(header)]
                                    rows.append(clean_row)

                            if rows:
                                df_table = pd.DataFrame(rows, columns=header)
                                extracted_tables.append(df_table)
        except Exception as e:
            logger.warning(f"pdfplumber table extraction warning: {e}")

        # Build primary dataframe
        if extracted_tables:
            primary_df = extracted_tables[0]
            if len(extracted_tables) > 1:
                matching_tables = [t for t in extracted_tables if list(t.columns) == list(primary_df.columns)]
                if len(matching_tables) == len(extracted_tables):
                    primary_df = pd.concat(extracted_tables, ignore_index=True)
            data_type = "semi-structured"
            section_count = max(len([l for l in raw_text.splitlines() if l.strip().isupper() and len(l) < 50]), page_count)
        else:
            # Extract structured data points and metrics from the unstructured PDF text
            primary_df, meta, sections = UnstructuredDataStructurer.structure_unstructured_text(raw_text)
            data_type = "unstructured_document"
            section_count = meta.get("sections_count", page_count)

        return ExtractionResult(
            dataframe=primary_df,
            raw_text=raw_text[:8000],
            tables=extracted_tables if extracted_tables else [primary_df],
            doc_stats={
                "pages": page_count,
                "tables": max(len(extracted_tables), 1),
                "charts": max(image_count // 2, 1) if image_count > 0 else 0,
                "sections": max(section_count, 1),
                "rows": int(len(primary_df)),
                "columns": int(len(primary_df.columns))
            },
            data_type=data_type,
            metadata={"total_pages": page_count, "images_found": image_count}
        )
