import uuid
from datetime import datetime
from typing import List, Dict, Any, Optional
import pandas as pd
from app.services.ai_client import ai_client

class ReportSynthesizer:
    """Generates structured intelligence reports containing user-selected visualizations, structured tables, and branding."""

    @classmethod
    async def generate_full_report(
        cls,
        df: pd.DataFrame,
        filename: str,
        topics: List[str],
        quality_score_before: float,
        quality_score_after: float,
        quality_breakdown: Dict[str, float],
        selected_charts: List[Dict[str, Any]],
        anomalies: List[Dict[str, Any]],
        template_type: str = "professional",
        include_summary: bool = True
    ) -> List[Dict[str, Any]]:
        sections = []
        
        # 1. Header & Title Section (DataMorph AI Branding)
        sections.append({
            "id": str(uuid.uuid4()),
            "section_type": "title_page",
            "title": f"{filename} — Visual Intelligence Report",
            "content": f"Automated Intelligence Analysis by DataMorph AI\nGenerated: {datetime.utcnow().strftime('%B %d, %Y')}",
            "charts": [],
            "order": 0,
            "is_visible": True
        })

        # 2. Optional Summarized Data Text
        if include_summary:
            exec_summary_text = await cls._synthesize_executive_summary(df, filename, topics)
            sections.append({
                "id": str(uuid.uuid4()),
                "section_type": "executive_summary",
                "title": "Data Summary & Key Insights",
                "content": exec_summary_text,
                "charts": [],
                "order": 1,
                "is_visible": True
            })

        # 3. Selected Visualizations ONLY
        for idx, chart in enumerate(selected_charts):
            chart_type = chart.get("chart_type", "bar").upper().replace("_", " ")
            title = chart.get("title", f"Visualization {idx + 1}")
            reason = chart.get("reason", "")
            chart_data = chart.get("chart_data", [])

            content_text = f"**Chart Archetype:** {chart_type} | **Confidence:** {chart.get('confidence_score', 90)}%\n\n"
            if reason:
                content_text += f"**Analysis:** {reason}\n\n"

            sections.append({
                "id": str(uuid.uuid4()),
                "section_type": "visualizations",
                "title": title,
                "content": content_text,
                "charts": [chart.get("chart_config", {})],
                "chart_data": chart_data,
                "chart_type": chart.get("chart_type", "bar"),
                "order": 2 + idx,
                "is_visible": True
            })

        # 4. Structured Dataset Record Table Section
        table_rows = df.head(30).to_dict(orient="records")
        columns = list(df.columns)
        sections.append({
            "id": str(uuid.uuid4()),
            "section_type": "structured_table",
            "title": "Structured Dataset Record Table",
            "content": f"Verified structured tabular representation ({len(df)} total records, {len(columns)} dimensions).",
            "charts": [],
            "table_data": table_rows,
            "table_columns": columns,
            "order": 50,
            "is_visible": True # Enabled by default for full visibility
        })

        return sections

    @classmethod
    async def _synthesize_executive_summary(cls, df: pd.DataFrame, filename: str, topics: List[str]) -> str:
        prompt = (
            f"Write a concise executive data summary for '{filename}'. "
            f"Columns: {list(df.columns)}. Rows: {len(df)}. "
            f"Topics: {topics}. Keep it direct, focused, and data-driven without unnecessary fluff."
        )
        return await ai_client.generate_text(prompt)
