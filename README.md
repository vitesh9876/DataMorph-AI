<div align="center">

<img src="https://raw.githubusercontent.com/vitesh9876/DataMorph-AI/main/docs/readme-hero.svg" width="100%" alt="DataMorph AI animated hero"/>

<br/>

<a href="#-why-datamorph-ai">Why DataMorph</a> •
<a href="#-key-capabilities">Capabilities</a> •
<a href="#-architecture">Architecture</a> •
<a href="#-technology-stack">Stack</a> •
<a href="#-quick-start">Quick Start</a> •
<a href="#-api-overview">API</a>

<br/><br/>

[![Python](https://img.shields.io/badge/Python-3.10%2B-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.110%2B-009688?style=for-the-badge&logo=fastapi&logoColor=white)](https://fastapi.tiangolo.com/)
[![React](https://img.shields.io/badge/React-19-61DAFB?style=for-the-badge&logo=react&logoColor=111827)](https://react.dev/)
[![TypeScript](https://img.shields.io/badge/TypeScript-5%2B-3178C6?style=for-the-badge&logo=typescript&logoColor=white)](https://www.typescriptlang.org/)
[![Gemini](https://img.shields.io/badge/Gemini-GenAI-8E75B2?style=for-the-badge&logo=google&logoColor=white)](https://ai.google.dev/)
[![MIT](https://img.shields.io/badge/License-MIT-111827?style=for-the-badge)](LICENSE)

</div>

---

## 🧠 Why DataMorph AI?

DataMorph AI is an end-to-end **intelligent data transformation workspace**.

Instead of manually moving information between documents, spreadsheets, analysis tools and reporting software, DataMorph creates one pipeline:

**Raw file → extraction → cleaning → structured data → ML analysis → AI Q&A → visualization → executive report**

It is designed to handle both structured and unstructured sources such as PDFs, Excel files, CSVs, Word documents, PowerPoint presentations and text data.

> **Core idea:** turn messy information into something a person can inspect, analyze and communicate.

---

## ✨ Key Capabilities

| Capability | What it does |
|---|---|
| 📄 **Multi-format ingestion** | Extracts content from PDF, XLSX/XLS, CSV, DOCX, PPTX, JSON, XML, TXT and logs |
| 🧹 **AI-assisted cleaning** | Deduplication, missing-value handling, date normalization, currency normalization and category cleanup |
| 🤖 **ML analytics** | Isolation Forest anomaly detection, trend/forecast analysis and correlation discovery |
| 💬 **Ask Your Data** | Ask natural-language questions and receive data-backed answers with Gemini + Pandas |
| 📊 **Visualization intelligence** | Recommends suitable charts and supports custom visualizations |
| 📑 **Report generation** | Creates structured executive reports and exports to PDF, DOCX, PPTX, XLSX and HTML |
| 🔌 **API-first backend** | FastAPI endpoints expose ingestion, analysis, structuring, ML, visualization and export workflows |
| 🧪 **Testing** | Backend unit/integration tests plus an all-in-one verification runner |

---

## 🏗️ Architecture

<img src="https://raw.githubusercontent.com/vitesh9876/DataMorph-AI/main/docs/readme-pipeline.svg" width="100%" alt="Animated DataMorph AI pipeline"/>

### Processing flow

```text
┌───────────────┐
│   RAW FILES   │  PDF • XLSX • DOCX • PPTX • CSV • TXT
└───────┬───────┘
        ↓
┌───────────────────────┐
│ MULTI-FORMAT EXTRACTOR│  PyMuPDF • pdfplumber • openpyxl • python-docx
└──────────┬────────────┘
           ↓
┌───────────────────────┐
│ STRUCTURING + CLEANING│  normalization • deduplication • quality scoring
└──────────┬────────────┘
           ↓
      ┌────┴────┐
      ↓         ↓
┌──────────┐ ┌──────────────┐
│ ML ENGINE │ │ GEMINI + NLP │
│ anomalies │ │ Ask Your Data│
│ forecasting│ └──────┬───────┘
└────┬─────┘        ↓
     └────────┬─────┘
              ↓
      ┌──────────────┐
      │ VISUALIZATION│
      │ + INSIGHTS   │
      └──────┬───────┘
             ↓
      ┌──────────────┐
      │ REPORT ENGINE│
      └──────┬───────┘
             ↓
 PDF • DOCX • PPTX • XLSX • HTML
```

---

## 🚀 Feature Deep Dive

### 📄 Multi-format intelligent extraction

DataMorph can ingest:

- **PDF** — text, tables and document structures
- **Excel / CSV** — multi-sheet and tabular datasets
- **DOCX / PPTX** — document and presentation content
- **JSON / XML / TXT / logs** — semi-structured and plain-text sources

### 🧼 Data structuring & quality

The cleaning workflow provides:

- Duplicate detection and removal
- Missing-value handling using statistical strategies
- Currency normalization across common symbols and accounting formats
- Date normalization toward ISO-style representations
- Fuzzy category normalization
- Before/after inspection
- Data-quality health scoring

### 🤖 Machine learning

The analytics layer currently includes:

- **Isolation Forest** for multivariate anomaly detection
- **Polynomial / Ridge trend analysis**
- Forecast projections with confidence intervals
- Correlation discovery across numeric features
- Severity information for detected anomalies

### 💬 Ask Your Data

Users can interact with structured datasets using natural language.

Example questions:

```text
"Which product category has the highest revenue?"

"Show unusual values in the sales dataset."

"What is the projected value for the next period?"

"Which columns are strongly correlated?"
```

Gemini handles the natural-language interpretation while Pandas operates on the underlying data.

### 📊 Visualization studio

The visualization engine can recommend and generate:

- Line charts
- Bar charts
- Donut / pie charts
- Scatter plots
- Area charts
- Radar charts

It also supports custom axis mapping and aggregations.

### 📑 Executive report builder

Generated reports can include:

- Title page
- Executive summary
- Dataset overview
- Data-quality information
- Anomaly highlights
- Analytical insights
- Strategic recommendations

Supported exports:

**PDF · DOCX · PPTX · XLSX · HTML**

---

## 🛠️ Technology Stack

### Frontend

- React 19
- Vite
- TypeScript
- Tailwind CSS
- Recharts
- Framer Motion
- Lucide React
- Axios

### Backend

- Python 3.10+
- FastAPI
- Uvicorn
- SQLAlchemy 2
- SQLite / aiosqlite
- Pydantic v2

### AI / ML / Data

- Pandas
- NumPy
- Scikit-learn
- Google Gemini GenAI SDK
- Isolation Forest
- Ridge / Polynomial regression

### Document processing

- PyMuPDF
- pdfplumber
- python-docx
- python-pptx
- openpyxl
- xmltodict
- ReportLab

---

## 🔌 API Overview

| Category | Endpoint | Method | Purpose |
|---|---|:---:|---|
| Ingestion | `/api/v1/upload` | POST | Upload and start processing |
| Pipeline | `/api/v1/upload/{file_id}/status` | GET | Track processing status |
| Analysis | `/api/v1/analysis/{file_id}` | GET | Dataset/document analysis |
| Structuring | `/api/v1/structuring/{file_id}` | GET | Raw vs cleaned data |
| Structuring | `/api/v1/structuring/{file_id}/rules/action` | POST | Accept/reject cleaning rules |
| Visualization | `/api/v1/visualizations/{file_id}` | GET | Recommended visualizations |
| Visualization | `/api/v1/visualizations/{file_id}/custom` | POST | Custom charts |
| Ask Data | `/api/v1/ask-data/{file_id}` | POST | Natural-language data queries |
| ML | `/api/v1/ml/{file_id}/anomalies` | GET | Anomaly detection |
| ML | `/api/v1/ml/{file_id}/forecast` | POST | Forecast analysis |
| Reports | `/api/v1/reports/generate` | POST | Generate report |
| Export | `/api/v1/export` | POST | Export final output |

---

## ⚡ Quick Start

### Prerequisites

- Python 3.10+
- Node.js 18+
- npm
- Optional Gemini API key for AI-powered querying

### 1. Clone

```bash
git clone https://github.com/vitesh9876/DataMorph-AI.git
cd DataMorph-AI
```

### 2. Backend

```bash
cd backend

python -m venv venv

# Windows
.\venv\Scripts\activate

# macOS / Linux
# source venv/bin/activate

pip install -r requirements.txt

cp .env.example .env
# Add GEMINI_API_KEY to .env when using Gemini features

python -m uvicorn app.main:app --reload --port 8000
```

Backend:

- Swagger: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

### 3. Frontend

Open another terminal:

```bash
cd frontend
npm install
npm run dev
```

Frontend:

`http://localhost:5173`

---

## 🧪 Testing

Run backend tests:

```bash
cd backend
python -m pytest tests/ -v
```

Or use the verification runner:

```bash
python run_all_tests.py
```

---

## 📁 Repository Structure

```text
DataMorph-AI/
├── backend/
│   ├── app/
│   ├── tests/
│   └── requirements.txt
├── frontend/
│   ├── src/
│   └── package.json
├── docs/
│   ├── readme-hero.svg
│   ├── readme-pipeline.svg
│   └── readme-footer.svg
├── run_all_tests.py
└── README.md
```

---

## 🎯 Engineering Highlights

DataMorph AI combines several engineering disciplines in one application:

**Document engineering**  
→ extraction from heterogeneous file formats

**Data engineering**  
→ normalization, cleaning and structured storage

**Machine learning**  
→ anomaly detection, forecasting and correlation analysis

**Generative AI**  
→ natural-language interaction with datasets

**Full-stack engineering**  
→ React + FastAPI + database + REST APIs

**Reporting automation**  
→ machine-generated business reports across multiple formats

---

<div align="center">

<a href="https://github.com/vitesh9876/DataMorph-AI"><img src="https://img.shields.io/badge/VIEW_SOURCE-111827?style=for-the-badge&logo=github&logoColor=white" alt="View source"/></a>
<a href="https://github.com/vitesh9876/DataMorph-AI/issues"><img src="https://img.shields.io/badge/ISSUES-7c3aed?style=for-the-badge&logo=github&logoColor=white" alt="Issues"/></a>

<br/><br/>

<img src="https://raw.githubusercontent.com/vitesh9876/DataMorph-AI/main/docs/readme-footer.svg" width="100%" alt="Animated DataMorph AI footer"/>

</div>

---

## 📄 License

MIT License — see [LICENSE](LICENSE).
