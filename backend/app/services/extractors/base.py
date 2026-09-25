from dataclasses import dataclass, field
from typing import List, Dict, Any, Optional
import pandas as pd

@dataclass
class ExtractionResult:
    dataframe: Optional[pd.DataFrame] = None
    raw_text: str = ""
    tables: List[pd.DataFrame] = field(default_factory=list)
    doc_stats: Dict[str, Any] = field(default_factory=lambda: {
        "pages": 1,
        "tables": 0,
        "charts": 0,
        "sections": 1,
        "rows": 0,
        "columns": 0
    })
    topics: List[str] = field(default_factory=list)
    entities: List[Dict[str, Any]] = field(default_factory=list)
    summary: str = ""
    data_type: str = "tabular" # tabular, unstructured, semi-structured
    metadata: Dict[str, Any] = field(default_factory=dict)
