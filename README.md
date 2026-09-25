<div align="center">

<img src="https://raw.githubusercontent.com/vitesh9876/DataMorph-AI/main/docs/readme-hero.svg" width="100%" alt="DataMorph AI"/>

### Transform messy files into structured data, AI insights & reports.

[![Python](https://img.shields.io/badge/Python-3.10%2B-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-009688?style=for-the-badge&logo=fastapi&logoColor=white)](https://fastapi.tiangolo.com/)
[![React](https://img.shields.io/badge/React-19-61DAFB?style=for-the-badge&logo=react&logoColor=111827)](https://react.dev/)
[![TypeScript](https://img.shields.io/badge/TypeScript-3178C6?style=for-the-badge&logo=typescript&logoColor=white)](https://www.typescriptlang.org/)
[![Gemini](https://img.shields.io/badge/Gemini-GenAI-8E75B2?style=for-the-badge&logo=google&logoColor=white)](https://ai.google.dev/)
[![License](https://img.shields.io/badge/License-MIT-111827?style=for-the-badge)](LICENSE)

</div>

---

## ⚡ What is DataMorph AI?

**DataMorph AI** is a full-stack intelligent data workspace that turns documents and datasets into **clean, analyzable and report-ready information**.

**Raw files → Extraction → Cleaning → ML / AI → Visualization → Reports**

Supports **PDF, XLSX, CSV, DOCX, PPTX, JSON, XML and TXT**.

## ✨ Core Features

| Feature | Description |
|---|---|
| 📄 Multi-format ingestion | Extract data from documents, spreadsheets and text |
| 🧹 Data cleaning | Deduplication, missing values, normalization & quality scoring |
| 🤖 ML analytics | Anomaly detection, forecasting & correlation analysis |
| 💬 Ask Your Data | Natural-language dataset queries with Gemini + Pandas |
| 📊 Visualization | Automated and custom charts |
| 📑 Report generation | Export insights to PDF, DOCX, PPTX, XLSX & HTML |
| 🔌 API-first | FastAPI backend with versioned REST endpoints |

## 🔄 Processing Flow

<img src="https://raw.githubusercontent.com/vitesh9876/DataMorph-AI/main/docs/processing-flow-final.svg" width="100%" alt="DataMorph AI processing flow"/>

## 🏗️ Architecture

<img src="https://raw.githubusercontent.com/vitesh9876/DataMorph-AI/main/docs/readme-pipeline.svg" width="100%" alt="DataMorph AI architecture"/>

## 🛠️ Tech Stack

**Frontend:** React 19 · TypeScript · Vite · Tailwind CSS · Recharts · Framer Motion

**Backend:** Python · FastAPI · Uvicorn · SQLAlchemy · SQLite

**AI / ML:** Pandas · NumPy · Scikit-learn · Gemini GenAI · Isolation Forest · Ridge / Polynomial Regression

**Document Processing:** PyMuPDF · pdfplumber · python-docx · python-pptx · openpyxl · ReportLab

## 🔌 API

| Endpoint | Purpose |
|---|---|
| `POST /api/v1/upload` | Upload & process files |
| `GET /api/v1/analysis/{file_id}` | Analyze data |
| `GET /api/v1/structuring/{file_id}` | View structured data |
| `POST /api/v1/ask-data/{file_id}` | Ask questions about data |
| `GET /api/v1/ml/{file_id}/anomalies` | Detect anomalies |
| `POST /api/v1/ml/{file_id}/forecast` | Generate forecasts |
| `POST /api/v1/reports/generate` | Generate reports |

## 🚀 Quick Start

```bash
git clone https://github.com/vitesh9876/DataMorph-AI.git
cd DataMorph-AI

# Backend
cd backend
python -m venv venv
.\venv\Scripts\activate
pip install -r requirements.txt
python -m uvicorn app.main:app --reload --port 8000

# Frontend — open another terminal
cd frontend
npm install
npm run dev
```

Frontend: `http://localhost:5173` · API Docs: `http://localhost:8000/docs`

## 📁 Structure

```text
DataMorph-AI/
├── backend/          # FastAPI + AI/ML
├── frontend/         # React + TypeScript
├── docs/             # README visuals
├── run_all_tests.py
└── README.md
```

## 🎯 Engineering Highlights

**Document Engineering** · extraction from heterogeneous formats  
**Data Engineering** · cleaning, normalization & structuring  
**Machine Learning** · anomaly detection & forecasting  
**Generative AI** · natural-language data interaction  
**Full Stack** · React + FastAPI + database + REST APIs  
**Reporting Automation** · multi-format business reports

## 🧪 Testing

```bash
cd backend
python -m pytest tests/ -v
```

---

<div align="center">

<a href="https://github.com/vitesh9876/DataMorph-AI"><img src="https://img.shields.io/badge/VIEW_SOURCE-111827?style=for-the-badge&logo=github&logoColor=white" alt="View source"/></a>
<a href="https://github.com/vitesh9876/DataMorph-AI/issues"><img src="https://img.shields.io/badge/ISSUES-7c3aed?style=for-the-badge&logo=github&logoColor=white" alt="Issues"/></a>

<br/><br/>

<img src="https://raw.githubusercontent.com/vitesh9876/DataMorph-AI/main/docs/readme-footer.svg" width="100%" alt="DataMorph AI"/>

</div>

---

**MIT License**
