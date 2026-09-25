import uuid
from datetime import datetime
from sqlalchemy import Column, String, Integer, Float, Text, JSON, DateTime, ForeignKey, Boolean
from sqlalchemy.orm import relationship
from app.database import Base

def generate_uuid():
    return str(uuid.uuid4())

class Project(Base):
    __tablename__ = "projects"

    id = Column(String, primary_key=True, default=generate_uuid)
    name = Column(String, nullable=False, default="Untitled Data Project")
    description = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    files = relationship("UploadedFile", back_populates="project", cascade="all, delete-orphan")
    reports = relationship("Report", back_populates="project", cascade="all, delete-orphan")

class UploadedFile(Base):
    __tablename__ = "uploaded_files"

    id = Column(String, primary_key=True, default=generate_uuid)
    project_id = Column(String, ForeignKey("projects.id"), nullable=True)
    filename = Column(String, nullable=False)
    original_name = Column(String, nullable=False)
    file_type = Column(String, nullable=False)  # pdf, csv, xlsx, docx, pptx, json, xml, txt
    file_size = Column(Integer, nullable=False)
    file_path = Column(String, nullable=False)
    status = Column(String, default="uploaded")  # uploaded, processing, ready, error
    processing_step = Column(String, default="idle")  # detecting_structure, extracting_entities, checking_quality, etc.
    error_message = Column(Text, nullable=True)
    
    # Metadata & Extracted Content
    raw_text = Column(Text, nullable=True)
    summary_text = Column(Text, nullable=True)
    topics = Column(JSON, default=list)  # ["Sales", "Revenue", "Customers"]
    entities = Column(JSON, default=list)
    doc_stats = Column(JSON, default=dict)  # {"pages": 25, "tables": 8, "charts": 4, "sections": 12}
    data_type = Column(String, default="tabular")  # tabular, unstructured, semi-structured
    
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    project = relationship("Project", back_populates="files")
    dataset = relationship("DatasetArtifact", uselist=False, back_populates="file", cascade="all, delete-orphan")
    reports = relationship("Report", back_populates="file", cascade="all, delete-orphan")
    chat_messages = relationship("ChatMessage", back_populates="file", cascade="all, delete-orphan")

class DatasetArtifact(Base):
    __tablename__ = "dataset_artifacts"

    id = Column(String, primary_key=True, default=generate_uuid)
    file_id = Column(String, ForeignKey("uploaded_files.id"), unique=True, nullable=False)
    
    num_rows = Column(Integer, default=0)
    num_columns = Column(Integer, default=0)
    columns_meta = Column(JSON, default=list)  # [{name, dtype, sample_values, null_count, unique_count}]
    
    raw_sample = Column(JSON, default=list)  # First 10 rows raw
    current_sample = Column(JSON, default=list)  # Current state of structured dataset
    
    raw_data_path = Column(String, nullable=True)
    cleaned_data_path = Column(String, nullable=True)
    
    quality_score_initial = Column(Float, default=70.0)
    quality_score_current = Column(Float, default=70.0)
    quality_breakdown = Column(JSON, default=dict)  # completeness, consistency, uniqueness, validity
    
    anomalies_detected = Column(JSON, default=list)
    correlations = Column(JSON, default=dict)
    
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    file = relationship("UploadedFile", back_populates="dataset")
    recommendations = relationship("CleaningRecommendation", back_populates="dataset", cascade="all, delete-orphan")

class CleaningRecommendation(Base):
    __tablename__ = "cleaning_recommendations"

    id = Column(String, primary_key=True, default=generate_uuid)
    dataset_id = Column(String, ForeignKey("dataset_artifacts.id"), nullable=False)
    
    rule_type = Column(String, nullable=False)  # currency_normalization, date_standardization, category_unification, deduplication, missing_imputation
    title = Column(String, nullable=False)
    description = Column(Text, nullable=False)
    target_column = Column(String, nullable=True)
    suggested_action = Column(String, nullable=False)
    parameters = Column(JSON, default=dict)
    
    status = Column(String, default="pending")  # pending, accepted, rejected
    impact_score_gain = Column(Float, default=5.0)
    
    before_preview = Column(JSON, default=list)
    after_preview = Column(JSON, default=list)
    
    created_at = Column(DateTime, default=datetime.utcnow)

    dataset = relationship("DatasetArtifact", back_populates="recommendations")

class Report(Base):
    __tablename__ = "reports"

    id = Column(String, primary_key=True, default=generate_uuid)
    project_id = Column(String, ForeignKey("projects.id"), nullable=True)
    file_id = Column(String, ForeignKey("uploaded_files.id"), nullable=False)
    
    title = Column(String, nullable=False, default="Executive Data Analysis Report")
    template_type = Column(String, default="professional")  # professional, minimal, modern, corporate, research
    theme_color = Column(String, default="#6366F1")
    
    sections = Column(JSON, default=list)  # [{id, section_type, title, content, charts: [], order, is_visible}]
    selected_visualizations = Column(JSON, default=list)
    
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    project = relationship("Project", back_populates="reports")
    file = relationship("UploadedFile", back_populates="reports")

class ChatMessage(Base):
    __tablename__ = "chat_messages"

    id = Column(String, primary_key=True, default=generate_uuid)
    file_id = Column(String, ForeignKey("uploaded_files.id"), nullable=False)
    
    role = Column(String, nullable=False)  # user, assistant
    content = Column(Text, nullable=False)
    structured_data = Column(JSON, nullable=True)
    suggested_chart = Column(JSON, nullable=True)
    citations = Column(JSON, default=list)
    
    created_at = Column(DateTime, default=datetime.utcnow)

    file = relationship("UploadedFile", back_populates="chat_messages")
