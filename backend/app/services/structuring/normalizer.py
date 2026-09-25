import re
from typing import Any, Tuple, Optional, Dict, List
from collections import Counter
import pandas as pd
import numpy as np

class DataNormalizer:
    """Methods for normalizing messy raw data values."""

    CURRENCY_SYMBOLS = ["$", "€", "£", "₹", "¥", "Rs.", "USD", "INR", "EUR", "GBP", "CAD", "AUD"]

    @classmethod
    def clean_currency_or_number(cls, val: Any) -> Tuple[Optional[float], bool]:
        """Strips currency symbols, commas, parentheses (negatives) and parses float."""
        if pd.isna(val) or val is None:
            return None, False
        
        s = str(val).strip()
        if not s:
            return None, False

        # Detect negative in parentheses e.g. (100.50)
        is_negative = False
        if s.startswith("(") and s.endswith(")"):
            is_negative = True
            s = s[1:-1].strip()

        # Remove currency symbols
        for sym in cls.CURRENCY_SYMBOLS:
            s = s.replace(sym, "")

        # Clean commas and extra spaces
        s = s.replace(",", "").replace(" ", "")

        try:
            num = float(s)
            return -num if is_negative else num, True
        except ValueError:
            return None, False

    @classmethod
    def standardize_date(cls, val: Any) -> Tuple[Optional[str], bool]:
        """Parses various date formats and outputs standard YYYY-MM-DD."""
        if pd.isna(val) or val is None:
            return None, False
        
        s = str(val).strip()
        if not s:
            return None, False

        try:
            dt = pd.to_datetime(s, errors="coerce")
            if pd.notna(dt):
                return dt.strftime("%Y-%m-%d"), True
        except Exception:
            pass

        return s, False

    @classmethod
    def unify_category_names(cls, series: pd.Series) -> Tuple[pd.Series, Dict[str, str], int]:
        """
        Detects casing and punctuation variations (e.g. 'iphone', 'iPhone', 'IPHONE')
        and maps them to the most common canonical form.
        """
        cleaned_series = series.copy()
        non_nulls = series.dropna().astype(str).tolist()
        
        if not non_nulls:
            return cleaned_series, {}, 0

        # Group by lowercase / stripped
        groups: Dict[str, List[str]] = {}
        for original in non_nulls:
            key = re.sub(r"[_\-\s]+", "", original.lower().strip())
            groups.setdefault(key, []).append(original)

        mapping: Dict[str, str] = {}
        variations_found = 0

        for key, originals in groups.items():
            unique_variations = set(originals)
            if len(unique_variations) > 1:
                # Find most frequent original capitalization or title case
                counts = Counter(originals)
                canonical = counts.most_common(1)[0][0]
                # If all are lowercase/uppercase, prefer Title Case
                if canonical.islower() or canonical.isupper():
                    canonical = canonical.title()

                for var in unique_variations:
                    if var != canonical:
                        mapping[var] = canonical
                        variations_found += 1

        if mapping:
            cleaned_series = cleaned_series.replace(mapping)

        return cleaned_series, mapping, variations_found
