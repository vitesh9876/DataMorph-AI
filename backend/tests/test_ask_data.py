import pytest
import pandas as pd
from app.services.ask_data.engine import AskDataEngine

@pytest.mark.asyncio
async def test_ask_highest_product():
    df = pd.DataFrame({
        "Product": ["Product A", "Product B", "Product C"],
        "Revenue": [850000, 420000, 190000]
    })
    
    res = await AskDataEngine.query_dataset(df, "Which product generated the highest revenue?")
    assert "Product A" in res["answer"]
    assert res["supporting_data"] is not None
    assert res["suggested_visualization"] is not None

@pytest.mark.asyncio
async def test_ask_trend():
    df = pd.DataFrame({
        "Date": ["2024-01-01", "2024-02-01", "2024-03-01"],
        "Sales": [1000, 2000, 3000]
    })
    res = await AskDataEngine.query_dataset(df, "Show monthly sales trends.")
    assert "Sales" in res["answer"] or "trajectory" in res["answer"]
    assert res["suggested_visualization"] is not None
