import os
import pytest
from httpx import AsyncClient, ASGITransport
from app.main import app
from app.database import init_db

SAMPLE_DIR = os.path.join(os.path.dirname(__file__), "..", "..", "sample_data")

@pytest.fixture(scope="session", autouse=True)
async def setup_db():
    await init_db()

@pytest.mark.asyncio
async def test_health_and_root():
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        res_health = await ac.get("/health")
        assert res_health.status_code == 200
        assert res_health.json()["status"] == "healthy"

        res_root = await ac.get("/")
        assert res_root.status_code == 200

@pytest.mark.asyncio
async def test_upload_and_pipeline_flow():
    csv_file = os.path.join(SAMPLE_DIR, "sales_dirty.csv")
    assert os.path.exists(csv_file)

    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        # 1. Upload
        with open(csv_file, "rb") as f:
            upload_res = await ac.post(
                "/api/v1/upload",
                files={"file": ("sales_dirty.csv", f, "text/csv")}
            )
        assert upload_res.status_code == 200
        data = upload_res.json()
        file_id = data["file_id"]
        assert file_id is not None

        # 2. Check Status
        status_res = await ac.get(f"/api/v1/upload/{file_id}/status")
        assert status_res.status_code == 200
        assert len(status_res.json()["timeline"]) == 6

        # Process pipeline synchronously for test assertion
        from app.api.v1.upload import process_file_pipeline
        file_path = os.path.join(SAMPLE_DIR, "sales_dirty.csv")
        await process_file_pipeline(file_id, file_path, "sales_dirty.csv")

        # 3. Check Analysis
        analysis_res = await ac.get(f"/api/v1/analysis/{file_id}")
        assert analysis_res.status_code == 200
        analysis_data = analysis_res.json()
        assert analysis_data["filename"] == "sales_dirty.csv"
        assert analysis_data["doc_stats"]["rows"] > 0

        # 4. Check Structuring (Raw vs Cleaned)
        struct_res = await ac.get(f"/api/v1/structuring/{file_id}")
        assert struct_res.status_code == 200
        struct_data = struct_res.json()
        assert len(struct_data["recommendations"]) > 0

        # Accept first recommendation
        rec_id = struct_data["recommendations"][0]["id"]
        action_res = await ac.post(
            f"/api/v1/structuring/{file_id}/rules/action",
            json={"recommendation_id": rec_id, "action": "accept"}
        )
        assert action_res.status_code == 200

        # 5. Check Visualizations
        viz_res = await ac.get(f"/api/v1/visualizations/{file_id}")
        assert viz_res.status_code == 200
        viz_data = viz_res.json()
        assert len(viz_data["recommended_charts"]) > 0

        # 6. Ask Your Data
        ask_res = await ac.post(
            f"/api/v1/ask-data/{file_id}",
            json={"question": "Which product generated the highest revenue?"}
        )
        assert ask_res.status_code == 200
        assert ask_res.json()["answer"] != ""

        # 7. ML Anomalies
        anomaly_res = await ac.get(f"/api/v1/ml/{file_id}/anomalies")
        assert anomaly_res.status_code == 200
        assert "anomalies" in anomaly_res.json()

        # 8. Report Generation
        rep_res = await ac.post(
            "/api/v1/reports/generate",
            json={"file_id": file_id, "title": "Quarterly Sales Report", "template_type": "professional"}
        )
        assert rep_res.status_code == 200
        report_data = rep_res.json()
        report_id = report_data["id"]
        assert len(report_data["sections"]) >= 6

        # 9. Multi-Format Export
        for fmt in ["pdf", "docx", "pptx", "xlsx", "html"]:
            export_res = await ac.post(
                "/api/v1/export",
                json={"report_id": report_id, "format": fmt}
            )
            assert export_res.status_code == 200
            assert export_res.json()["download_url"] != ""
