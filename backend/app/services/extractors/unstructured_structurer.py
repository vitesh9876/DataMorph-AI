import re
from typing import List, Dict, Any, Tuple
import pandas as pd

class UnstructuredDataStructurer:
    """
    Intelligent engine that detects, parses, and transforms unstructured text,
    raw test results, diagnostic reports, scientific logs, and scattered numbers
    into clean, queryable structured tables and visual insights.
    """

    @classmethod
    def structure_unstructured_text(cls, text: str) -> Tuple[pd.DataFrame, Dict[str, Any], List[Dict[str, Any]]]:
        lines = [line.strip() for line in text.splitlines() if line.strip()]
        
        extracted_records = []
        structured_sections = []
        
        current_section_title = "Executive Summary & Overview"
        current_section_lines = []

        # Comprehensive regular expression patterns for test results & metrics
        test_patterns = [
            # 1. Test Name: Value [Unit] (e.g. "Hemoglobin: 14.2 g/dL", "Latency p99: 18.5 ms", "Throughput: 1450 req/s")
            r"(?P<test>[A-Za-z0-9\s\-_/#&()]+?)\s*[:=]\s*(?P<val>[$₹€£]?\s*[-+]?[0-9,]+(?:\.[0-9]+)?)\s*(?P<unit>[a-zA-Z/%°µu]+(?:\s*[a-zA-Z/%°µu]+)*)?\s*(?:\((?P<status>[A-Za-z\s]+)\))?",
            
            # 2. Score / Ratio format (e.g. "Math: 92/100", "Accuracy: 48/50")
            r"(?P<test>[A-Za-z0-9\s\-_]+?)\s*[:=]\s*(?P<score>[0-9]+(?:\.[0-9]+)?)\s*/\s*(?P<total>[0-9]+(?:\.[0-9]+)?)",
            
            # 3. Verbal Metric sentences (e.g. "Trial 1 recorded 450 RPM", "Glucose measured 98 mg/dL", "Yield was 94.5%")
            r"(?P<test>[A-Za-z0-9\s]{3,35}?)\s+(?:measured|recorded|yielded|scored|reached|generated|totaled|tested at|showed)\s+(?P<val>[$₹€£]?\s*[-+]?[0-9,]+(?:\.[0-9]+)?)\s*(?P<unit>[a-zA-Z/%°µu]+)?",
            
            # 4. Tabular text delimited by dashes or tabs (e.g. "Cholesterol - 195 mg/dL - Normal", "CPU Load | 45% | Optimal")
            r"(?P<test>[A-Za-z0-9\s\-_/]+?)\s*[-|]\s*(?P<val>[$₹€£]?\s*[-+]?[0-9,]+(?:\.[0-9]+)?)\s*(?P<unit>[a-zA-Z/%°µu]+)?\s*(?:[-|]\s*(?P<status>[A-Za-z\s]+))?"
        ]

        for line in lines:
            # Check for header/section markers
            if (line.startswith("#") or (line.isupper() and len(line) < 45)) and not re.search(r"[$₹€0-9]", line):
                if current_section_lines:
                    structured_sections.append({
                        "title": current_section_title.lstrip("#").strip(": ").strip(),
                        "content": "\n".join(current_section_lines)
                    })
                    current_section_lines = []
                current_section_title = line
                continue
            
            current_section_lines.append(line)

            # Match test result patterns
            matched = False
            for pat in test_patterns:
                matches = re.finditer(pat, line, re.IGNORECASE)
                for m in matches:
                    groups = m.groupdict()
                    test_name = groups.get("test", "").strip(" -_:\t|#")
                    
                    # Skip invalid strings or URLs
                    if not test_name or len(test_name) < 2 or len(test_name) > 40 or test_name.lower().startswith("http"):
                        continue

                    # Parse score/ratio or single value
                    if "score" in groups and groups.get("score"):
                        try:
                            score = float(groups["score"])
                            total = float(groups.get("total", 100))
                            pct = round((score / total) * 100.0, 2) if total > 0 else score
                            extracted_records.append({
                                "Test_Name": test_name.title(),
                                "Measured_Value": pct,
                                "Raw_Result": f"{score}/{total} ({pct}%)",
                                "Unit": "%",
                                "Test_Category": cls._classify_test_category(test_name),
                                "Assessment": "Optimal" if pct >= 80 else ("Moderate" if pct >= 50 else "Attention")
                            })
                            matched = True
                        except Exception:
                            pass
                    elif "val" in groups and groups.get("val"):
                        v_raw = groups["val"].strip()
                        num_val = cls._parse_numeric_value(v_raw)
                        unit = groups.get("unit") or ""
                        unit_clean = unit.strip(" ()[]") if unit else cls._infer_unit(v_raw, test_name)
                        status = groups.get("status") or ""

                        if num_val is not None:
                            extracted_records.append({
                                "Test_Name": test_name.title(),
                                "Measured_Value": round(num_val, 2),
                                "Raw_Result": f"{v_raw} {unit_clean}".strip(),
                                "Unit": unit_clean or "Metric",
                                "Test_Category": cls._classify_test_category(test_name),
                                "Assessment": status.title().strip() if status else cls._infer_assessment(num_val, test_name)
                            })
                            matched = True

                if matched:
                    break

        if current_section_lines:
            structured_sections.append({
                "title": current_section_title.lstrip("#").strip(": ").strip(),
                "content": "\n".join(current_section_lines)
            })

        # Fallback: Extract isolated numbers with surrounding key labels
        if not extracted_records:
            for i, line in enumerate(lines[:50]):
                nums = re.findall(r"([-+]?[0-9,]+(?:\.[0-9]+)?)", line)
                if nums:
                    words = [w for w in re.sub(r"[^a-zA-Z\s]", "", line).split() if len(w) > 3][:3]
                    label = " ".join(words).title() if words else f"Trial Item {i+1}"
                    num_val = cls._parse_numeric_value(nums[0])
                    if num_val is not None and num_val != 0:
                        extracted_records.append({
                            "Test_Name": label,
                            "Measured_Value": round(num_val, 2),
                            "Raw_Result": str(nums[0]),
                            "Unit": "Units",
                            "Test_Category": "Extracted Observation",
                            "Assessment": "Recorded"
                        })

        # Ultimate fallback
        if not extracted_records:
            for i, line in enumerate(lines[:15]):
                extracted_records.append({
                    "Test_Name": f"Sample Segment {i+1}",
                    "Measured_Value": float(len(line.split())),
                    "Raw_Result": f"{len(line.split())} words",
                    "Unit": "Words",
                    "Test_Category": "Text Density",
                    "Assessment": "Analyzed"
                })

        df = pd.DataFrame(extracted_records)
        df = df.drop_duplicates(subset=["Test_Name"]).head(60)

        meta = {
            "total_extracted_tests": len(df),
            "sections_count": len(structured_sections),
            "data_mode": "structured_test_results"
        }

        return df, meta, structured_sections

    @staticmethod
    def _parse_numeric_value(val_str: str) -> float | None:
        clean = val_str.replace("$", "").replace("₹", "").replace("€", "").replace("£", "").replace(",", "").strip()
        if clean.endswith("%"):
            clean = clean[:-1].strip()
        elif clean.lower().endswith("k"):
            clean = f"{float(clean[:-1].strip()) * 1000}"
        elif clean.lower().endswith("m"):
            clean = f"{float(clean[:-1].strip()) * 1000000}"

        try:
            return float(clean)
        except Exception:
            return None

    @staticmethod
    def _infer_unit(val_str: str, name: str) -> str:
        if "%" in val_str:
            return "%"
        if "$" in val_str or "usd" in val_str.lower():
            return "USD"
        if "₹" in val_str or "inr" in val_str.lower():
            return "INR"
        if "€" in val_str or "eur" in val_str.lower():
            return "EUR"
        
        name_l = name.lower()
        if any(k in name_l for k in ["latency", "duration", "delay", "time", "speed"]):
            return "ms"
        if any(k in name_l for k in ["rate", "percentage", "accuracy", "yield", "uptime"]):
            return "%"
        if any(k in name_l for k in ["temp", "temperature", "heat"]):
            return "°C"
        if any(k in name_l for k in ["memory", "ram", "storage"]):
            return "MB"
        if any(k in name_l for k in ["pressure"]):
            return "mmHg"
        if any(k in name_l for k in ["glucose", "sugar", "cholesterol"]):
            return "mg/dL"
        return ""

    @staticmethod
    def _classify_test_category(name: str) -> str:
        n = name.lower()
        if any(k in n for k in ["glucose", "hemoglobin", "wbc", "rbc", "platelet", "cholesterol", "pressure", "cardio", "biomarker", "creatinine", "alt", "ast"]):
            return "Diagnostic & Clinical"
        elif any(k in n for k in ["latency", "throughput", "cpu", "memory", "load", "fps", "response", "bandwidth", "ping", "uptime"]):
            return "System Performance"
        elif any(k in n for k in ["math", "physics", "chemistry", "biology", "exam", "score", "grade", "gpa", "quiz", "test score"]):
            return "Academic & Evaluation"
        elif any(k in n for k in ["stress", "tensile", "torque", "rpm", "voltage", "current", "vibration", "temperature", "pressure", "yield"]):
            return "Engineering & Sensor"
        elif any(k in n for k in ["revenue", "cost", "expense", "profit", "sales", "budget", "ebitda"]):
            return "Financial & Business"
        else:
            return "Experimental Metric"

    @staticmethod
    def _infer_assessment(val: float, name: str) -> str:
        n = name.lower()
        if "%" in n or "rate" in n or "score" in n or "accuracy" in n:
            if val >= 90:
                return "Optimal"
            elif val >= 75:
                return "Normal"
            elif val >= 50:
                return "Acceptable"
            else:
                return "Low / Review"
        return "Recorded"
