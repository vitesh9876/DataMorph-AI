import io
import json
import logging
from typing import Optional, Dict, Any, List
import pandas as pd
import xmltodict
from app.services.extractors.base import ExtractionResult

logger = logging.getLogger(__name__)

class TabularExtractor:
    """Extracts data from CSV, TSV, XLSX, XLS, JSON, and XML files."""

    @staticmethod
    def extract_csv(file_path: str) -> ExtractionResult:
        encodings = ["utf-8", "latin-1", "cp1252", "iso-8859-1"]
        df = None
        used_encoding = "utf-8"
        for enc in encodings:
            try:
                # Try comma, then sniff delimiter
                df = pd.read_csv(file_path, encoding=enc, on_bad_lines="skip")
                if len(df.columns) <= 1:
                    # Retry with semicolon or tab
                    for sep in [";", "\t", "|"]:
                        temp_df = pd.read_csv(file_path, sep=sep, encoding=enc, on_bad_lines="skip")
                        if len(temp_df.columns) > 1:
                            df = temp_df
                            break
                used_encoding = enc
                break
            except Exception:
                continue

        if df is None:
            raise ValueError("Unable to parse CSV file with standard encodings.")

        # Clean column names
        df.columns = [str(c).strip() for c in df.columns]
        
        return ExtractionResult(
            dataframe=df,
            raw_text=f"CSV dataset containing {len(df)} rows and {len(df.columns)} columns.",
            tables=[df],
            doc_stats={
                "pages": 1,
                "tables": 1,
                "charts": 0,
                "sections": 1,
                "rows": int(len(df)),
                "columns": int(len(df.columns))
            },
            data_type="tabular",
            metadata={"encoding": used_encoding, "format": "csv"}
        )

    @staticmethod
    def extract_excel(file_path: str) -> ExtractionResult:
        excel_file = pd.ExcelFile(file_path)
        sheet_names = excel_file.sheet_names
        
        tables: List[pd.DataFrame] = []
        for sheet in sheet_names:
            try:
                sheet_df = pd.read_excel(file_path, sheet_name=sheet)
                if not sheet_df.empty:
                    sheet_df.columns = [str(c).strip() for c in sheet_df.columns]
                    tables.append(sheet_df)
            except Exception as e:
                logger.warning(f"Error reading sheet {sheet}: {e}")

        primary_df = tables[0] if tables else pd.DataFrame()
        total_rows = sum(len(t) for t in tables)
        total_cols = len(primary_df.columns) if not primary_df.empty else 0

        return ExtractionResult(
            dataframe=primary_df,
            raw_text=f"Excel workbook with sheets: {', '.join(sheet_names)}",
            tables=tables,
            doc_stats={
                "pages": len(sheet_names),
                "tables": len(tables),
                "charts": 0,
                "sections": len(sheet_names),
                "rows": total_rows,
                "columns": total_cols
            },
            data_type="tabular",
            metadata={"sheet_names": sheet_names, "format": "excel"}
        )

    @staticmethod
    def extract_json(file_path: str) -> ExtractionResult:
        with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
            data = json.load(f)

        df = None
        if isinstance(data, list):
            # List of records
            df = pd.json_normalize(data)
        elif isinstance(data, dict):
            # Check if there's a key containing a list of records
            records_key = None
            for k, v in data.items():
                if isinstance(v, list) and len(v) > 0 and isinstance(v[0], dict):
                    records_key = k
                    break
            if records_key:
                df = pd.json_normalize(data[records_key])
            else:
                # Flat single record or key-value dict
                df = pd.json_normalize([data])

        if df is None or df.empty:
            df = pd.DataFrame([{"key": k, "value": str(v)} for k, v in (data.items() if isinstance(data, dict) else enumerate(data))])

        df.columns = [str(c).strip() for c in df.columns]

        return ExtractionResult(
            dataframe=df,
            raw_text=json.dumps(data, indent=2)[:3000],
            tables=[df],
            doc_stats={
                "pages": 1,
                "tables": 1,
                "charts": 0,
                "sections": 1,
                "rows": int(len(df)),
                "columns": int(len(df.columns))
            },
            data_type="semi-structured",
            metadata={"format": "json"}
        )

    @staticmethod
    def extract_xml(file_path: str) -> ExtractionResult:
        with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
            xml_str = f.read()

        parsed_dict = xmltodict.parse(xml_str)
        
        # Flatten dictionary to tabular rows if repeated tags exist
        def find_list_of_dicts(obj: Any) -> Optional[List[Dict]]:
            if isinstance(obj, list) and len(obj) > 0 and isinstance(obj[0], dict):
                return obj
            if isinstance(obj, dict):
                for val in obj.values():
                    res = find_list_of_dicts(val)
                    if res:
                        return res
            return None

        records = find_list_of_dicts(parsed_dict)
        if records:
            df = pd.json_normalize(records)
        else:
            df = pd.json_normalize(parsed_dict)

        df.columns = [str(c).strip() for c in df.columns]

        return ExtractionResult(
            dataframe=df,
            raw_text=xml_str[:3000],
            tables=[df],
            doc_stats={
                "pages": 1,
                "tables": 1,
                "charts": 0,
                "sections": 1,
                "rows": int(len(df)),
                "columns": int(len(df.columns))
            },
            data_type="semi-structured",
            metadata={"format": "xml"}
        )
