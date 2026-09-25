import logging
from pptx import Presentation
import pandas as pd
from app.services.extractors.base import ExtractionResult
from app.services.extractors.unstructured_structurer import UnstructuredDataStructurer

logger = logging.getLogger(__name__)

class PPTXExtractor:
    """Extracts slide text, tables, shape notes, and structures slide contents from PowerPoint files."""

    @staticmethod
    def extract_pptx(file_path: str) -> ExtractionResult:
        prs = Presentation(file_path)
        slide_count = len(prs.slides)
        
        slide_texts = []
        extracted_tables = []
        chart_count = 0

        for slide_num, slide in enumerate(prs.slides, 1):
            slide_content = []
            for shape in slide.shapes:
                if shape.has_text_frame:
                    for paragraph in shape.text_frame.paragraphs:
                        text = paragraph.text.strip()
                        if text:
                            slide_content.append(text)
                
                if shape.has_table:
                    table = shape.table
                    rows_data = []
                    for row in table.rows:
                        row_cells = [cell.text.strip() for cell in row.cells]
                        rows_data.append(row_cells)
                    
                    if rows_data and len(rows_data) > 1:
                        header = [f"Col_{i+1}" if not c else c for i, c in enumerate(rows_data[0])]
                        df_table = pd.DataFrame(rows_data[1:], columns=header)
                        extracted_tables.append(df_table)

                if shape.has_chart:
                    chart_count += 1

            if slide_content:
                slide_texts.append(f"--- Slide {slide_num} ---\n" + "\n".join(slide_content))

        raw_text = "\n\n".join(slide_texts)

        if extracted_tables:
            primary_df = extracted_tables[0]
            data_type = "semi-structured"
        else:
            primary_df, meta, sections = UnstructuredDataStructurer.structure_unstructured_text(raw_text)
            data_type = "unstructured_presentation"

        return ExtractionResult(
            dataframe=primary_df,
            raw_text=raw_text[:8000],
            tables=extracted_tables if extracted_tables else [primary_df],
            doc_stats={
                "pages": slide_count,
                "tables": max(len(extracted_tables), 1),
                "charts": chart_count,
                "sections": slide_count,
                "rows": int(len(primary_df)),
                "columns": int(len(primary_df.columns))
            },
            data_type=data_type,
            metadata={"slides": slide_count, "charts_detected": chart_count}
        )
