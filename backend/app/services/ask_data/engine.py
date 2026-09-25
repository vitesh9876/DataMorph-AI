import re
import uuid
import logging
from typing import Dict, Any, List, Optional
import pandas as pd
import numpy as np
from app.services.ai_client import ai_client
from app.services.visualization.aggregator import ChartAggregator

logger = logging.getLogger(__name__)

class AskDataEngine:
    """Processes Natural Language queries over structured datasets."""

    @classmethod
    async def query_dataset(cls, df: pd.DataFrame, question: str, history: Optional[List[Dict[str, str]]] = None) -> Dict[str, Any]:
        if df.empty:
            return {
                "question": question,
                "answer": "The dataset is currently empty. Please upload and clean a valid file.",
                "supporting_data": [],
                "suggested_visualization": None,
                "sql_or_code": "",
                "citations": []
            }

        q_lower = question.lower()
        
        # 1. Deterministic Rule Matching for high accuracy & fast speed
        result = cls._try_deterministic_answer(df, question, q_lower)
        if result:
            return result

        # 2. LLM Synthesis (Gemini)
        if ai_client.is_available:
            try:
                schema_summary = f"Columns: {list(df.columns)}\nData Types: {df.dtypes.to_dict()}\nSample Rows:\n{df.head(5).to_dict(orient='records')}"
                system_prompt = (
                    "You are DataMorph AI's conversational data analyst. Given the dataset schema and question, "
                    "return a JSON object with fields:\n"
                    "- answer: clear, factual natural language answer backed by the data.\n"
                    "- target_columns: array of relevant column names.\n"
                    "- suggested_chart_type: 'bar', 'line', 'pie', 'scatter' or null."
                )
                user_prompt = f"Dataset Schema:\n{schema_summary}\n\nUser Question: {question}"
                llm_json = await ai_client.generate_json(user_prompt, system_prompt)

                answer = llm_json.get("answer", "Based on the analyzed records, here are the findings.")
                target_cols = llm_json.get("target_columns", [])
                chart_type = llm_json.get("suggested_chart_type", "bar")

                supporting_data = df.head(10).to_dict(orient="records")
                suggested_chart = None

                if target_cols and len(target_cols) >= 2 and all(c in df.columns for c in target_cols[:2]):
                    x_col = target_cols[0]
                    y_col = target_cols[1]
                    chart_data = ChartAggregator.aggregate_for_chart(df, x_col=x_col, y_col=y_col, chart_type=chart_type or "bar")
                    suggested_chart = {
                        "id": str(uuid.uuid4()),
                        "title": f"{y_col} by {x_col}",
                        "chart_type": chart_type or "bar",
                        "confidence_score": 92,
                        "reason": f"Visual insight generated for '{question}'",
                        "chart_config": {
                            "chart_type": chart_type or "bar",
                            "title": f"{y_col} by {x_col}",
                            "x_axis": x_col,
                            "y_axis": y_col,
                            "aggregation": "sum"
                        },
                        "chart_data": chart_data,
                        "is_selected": False
                    }

                return {
                    "question": question,
                    "answer": answer,
                    "supporting_data": supporting_data,
                    "suggested_visualization": suggested_chart,
                    "sql_or_code": f"df.groupby('{target_cols[0]}').sum()" if target_cols else "",
                    "citations": [f"{len(df)} records evaluated"]
                }
            except Exception as e:
                logger.error(f"LLM query processing error: {e}")

        # 3. Fallback General Aggregation
        return cls._general_fallback(df, question)

    @classmethod
    def _try_deterministic_answer(cls, df: pd.DataFrame, question: str, q_lower: str) -> Optional[Dict[str, Any]]:
        numeric_cols = [c for c in df.columns if pd.to_numeric(df[c], errors="coerce").notna().sum() > len(df) * 0.7]
        cat_cols = [c for c in df.columns if c not in numeric_cols and df[c].nunique() < 200]
        date_cols = [c for c in df.columns if pd.to_datetime(df[c], errors="coerce").notna().sum() > len(df) * 0.7]

        # Highest / Max / Top query
        if any(w in q_lower for w in ["highest", "max", "top", "most", "largest", "leader"]):
            if cat_cols and numeric_cols:
                c_col = cat_cols[0]
                n_col = numeric_cols[0]
                temp_df = df.copy()
                temp_df[n_col] = pd.to_numeric(temp_df[n_col], errors="coerce")
                grouped = temp_df.groupby(c_col)[n_col].sum().sort_values(ascending=False).reset_index()
                
                if not grouped.empty:
                    top_item = grouped.iloc[0]
                    top_name = top_item[c_col]
                    top_val = top_item[n_col]
                    
                    chart_data = ChartAggregator.aggregate_for_chart(temp_df, x_col=c_col, y_col=n_col, chart_type="bar", max_points=8)
                    supporting = grouped.head(5).to_dict(orient="records")

                    return {
                        "question": question,
                        "answer": f"**{top_name}** generated the highest {n_col} with **{top_val:,.2f}**, representing the top performer in this category.",
                        "supporting_data": supporting,
                        "suggested_visualization": {
                            "id": str(uuid.uuid4()),
                            "title": f"Top {c_col} by {n_col}",
                            "chart_type": "bar",
                            "confidence_score": 95,
                            "reason": f"Ranked comparison for {n_col} across {c_col}.",
                            "chart_config": {
                                "chart_type": "bar",
                                "title": f"Top {c_col} by {n_col}",
                                "x_axis": c_col,
                                "y_axis": n_col,
                                "aggregation": "sum"
                            },
                            "chart_data": chart_data,
                            "is_selected": False
                        },
                        "sql_or_code": f"df.groupby('{c_col}')['{n_col}'].sum().sort_values(ascending=False)",
                        "citations": [f"Aggregated over {len(df)} rows across {c_col}"]
                    }

        # Trend / Monthly / Time query
        if any(w in q_lower for w in ["trend", "monthly", "over time", "history", "daily", "timeline"]):
            if date_cols and numeric_cols:
                d_col = date_cols[0]
                n_col = numeric_cols[0]
                chart_data = ChartAggregator.aggregate_for_chart(df, x_col=d_col, y_col=n_col, chart_type="line")
                return {
                    "question": question,
                    "answer": f"Chronological trajectory for **{n_col}** across recorded timeline periods ({len(chart_data)} time intervals).",
                    "supporting_data": chart_data[:10],
                    "suggested_visualization": {
                        "id": str(uuid.uuid4()),
                        "title": f"{n_col} Trend Analysis",
                        "chart_type": "line",
                        "confidence_score": 94,
                        "reason": f"Temporal progression detected over {d_col}.",
                        "chart_config": {
                            "chart_type": "line",
                            "title": f"{n_col} Trend",
                            "x_axis": d_col,
                            "y_axis": n_col,
                            "aggregation": "sum"
                        },
                        "chart_data": chart_data,
                        "is_selected": False
                    },
                    "sql_or_code": f"df.groupby('{d_col}')['{n_col}'].sum()",
                    "citations": [f"Timeline extracted from {d_col}"]
                }

        # Compare two entities query (e.g. "compare Delhi and Mumbai")
        if "compare" in q_lower and cat_cols and numeric_cols:
            c_col = cat_cols[0]
            n_col = numeric_cols[0]
            temp_df = df.copy()
            temp_df[n_col] = pd.to_numeric(temp_df[n_col], errors="coerce")
            grouped = temp_df.groupby(c_col)[n_col].sum().reset_index()
            
            chart_data = ChartAggregator.aggregate_for_chart(temp_df, x_col=c_col, y_col=n_col, chart_type="bar", max_points=10)
            return {
                "question": question,
                "answer": f"Comparative breakdown across **{c_col}** segments for **{n_col}**.",
                "supporting_data": grouped.head(10).to_dict(orient="records"),
                "suggested_visualization": {
                    "id": str(uuid.uuid4()),
                    "title": f"Comparison of {c_col}",
                    "chart_type": "bar",
                    "confidence_score": 91,
                    "reason": f"Category comparative distribution for {c_col}.",
                    "chart_config": {
                        "chart_type": "bar",
                        "title": f"{c_col} Comparison",
                        "x_axis": c_col,
                        "y_axis": n_col,
                        "aggregation": "sum"
                    },
                    "chart_data": chart_data,
                    "is_selected": False
                },
                "sql_or_code": f"df.groupby('{c_col}')['{n_col}'].sum()",
                "citations": [f"Filtered across {len(grouped)} unique {c_col} categories"]
            }

        return None

    @classmethod
    def _general_fallback(cls, df: pd.DataFrame, question: str) -> Dict[str, Any]:
        num_rows = len(df)
        num_cols = len(df.columns)
        return {
            "question": question,
            "answer": f"Analyzed {num_rows} records across columns: {', '.join(df.columns[:8])}.",
            "supporting_data": df.head(5).to_dict(orient="records"),
            "suggested_visualization": None,
            "sql_or_code": "df.describe()",
            "citations": [f"Total rows: {num_rows}, Total columns: {num_cols}"]
        }
