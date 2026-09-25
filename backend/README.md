# DataMorph AI - Backend API

> **"Transform Any Raw File into Structured Data, Visual Insights & Professional Reports."**

DataMorph AI is a next-generation full-stack AI workspace backend that scans multi-format files (PDF, PPT/PPTX, CSV, XLSX, XLS, TXT, XML, JSON, DOCX), extracts structured data, runs Machine Learning analytics & anomaly detection, recommends high-confidence visualizations, provides a conversational "Ask Your Data" interface, synthesizes editable executive reports, and exports them to PDF, DOCX, PPTX, XLSX, and HTML.

---

## Key Modules & Capabilities

1. **Multi-Format Extraction Pipeline**
   - Ingests CSV, XLSX/XLS (multi-sheet), PDF (tables & visual structure), DOCX, PPTX, JSON, XML, TXT/logs.
   - Extracts page counts, table matrices, entity topologies, and semantic topic tags.

2. **Data Structuring & Cleaning Engine**
   - Deduplication, missing value imputation (median/mode), currency normalization (handles `$`, `₹`, `€`, `(100)`), date normalization (ISO 8601), and category name unification (`iphone`, `iPhone`, `IPHONE` → `iPhone`).
   - Interactive rule review with live Before vs. After previews and dynamic Quality Score recomputation (e.g. 68% → 92%).

3. **Machine Learning Analytics**
   - **Anomaly Detection**: Scikit-Learn `IsolationForest` multivariate outlier detection with severity tiers and explanation drivers.
   - **Time-Series Forecasting**: Polynomial & Ridge trend estimators with 95% confidence bounds (upper/lower margin).
   - **Correlation Matrix**: Variable relationship scoring and high-correlation discovery.

4. **Visualization Recommendation Engine**
   - Recommends best-fit charts (Line, Bar, Pie/Donut, Scatter, Area, Radar) with confidence scores (e.g. 96%, 94%, 89%) and reasoning.
   - Dynamic aggregation and on-the-fly custom chart generation.

5. **"Ask Your Data" Conversational Query Engine**
   - Natural language question answering backed by pandas computation and hybrid Gemini LLM synthesis.
   - Returns factual answer, tabular supporting slice, and auto-suggested visual chart.

6. **AI Report Builder & Synthesis**
   - Automatically generates Title Page, Executive Summary, Dataset Overview, Data Quality Assessment, Key Findings, Visualizations, Anomaly Highlights, and Strategic Recommendations.
   - Supports 5 styling templates: `Professional`, `Minimal`, `Modern`, `Corporate`, and `Research`.
   - Full section reordering, editing, adding, and deletion.

7. **Multi-Format Exporter**
   - Export reports and data to **PDF** (ReportLab), **Word (.docx)** (`python-docx`), **PowerPoint (.pptx)** (`python-pptx`), **Excel (.xlsx)** (`openpyxl`), and standalone responsive **HTML**.

---

## API Endpoints Reference

### Upload & Progress Timeline
- `POST /api/v1/upload` - Upload file and trigger background processing pipeline.
- `GET /api/v1/upload/{file_id}/status` - Live 6-stage AI processing timeline progress.

### AI File Analysis
- `GET /api/v1/analysis/{file_id}` - Summary statistics, document stats (pages, tables, charts), topics, AI understanding card, and quality score.

### Structuring & Cleaning
- `GET /api/v1/structuring/{file_id}` - Side-by-side Raw vs AI-Structured data and cleaning recommendations.
- `POST /api/v1/structuring/{file_id}/rules/action` - Accept/reject cleaning recommendation with live score update.
- `POST /api/v1/structuring/{file_id}/rules/batch` - Batch accept/reject.

### Visualizations
- `GET /api/v1/visualizations/{file_id}` - High-confidence recommended charts.
- `POST /api/v1/visualizations/{file_id}/custom` - Build custom chart by X/Y axes and chart type.

### Ask Your Data
- `POST /api/v1/ask-data/{file_id}` - Conversational question query endpoint.
- `GET /api/v1/ask-data/{file_id}/history` - Chat conversation history.

### Machine Learning
- `GET /api/v1/ml/{file_id}/anomalies` - Isolation Forest anomaly list with scores and reasons.
- `POST /api/v1/ml/{file_id}/forecast` - Time-series future forecast.
- `GET /api/v1/ml/{file_id}/correlations` - Numeric correlation matrix.

### Reports
- `POST /api/v1/reports/generate` - Generate AI executive report.
- `GET /api/v1/reports/{report_id}` - Retrieve editable report sections.
- `PUT /api/v1/reports/{report_id}` - Update report title, template, or reorder/edit sections.

### Export
- `POST /api/v1/export` - Export report into PDF, DOCX, PPTX, XLSX, or HTML.
- `GET /api/v1/export/download/{filename}` - Direct binary download.

---

## Quick Start

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Configure Environment (Optional)
Copy `.env.example` to `.env` and set `GEMINI_API_KEY` if you wish to use Google GenAI:
```bash
cp .env.example .env
```

### 3. Run FastAPI Server
```bash
python -m uvicorn app.main:app --reload --port 8000
```
- Interactive Swagger Docs: `http://localhost:8000/docs`
- ReDoc Docs: `http://localhost:8000/redoc`

### 4. Run Automated Test Suite
```bash
python -m pytest tests/ -v
```
or run the end-to-end verification script:
```bash
python run_all_tests.py
```
