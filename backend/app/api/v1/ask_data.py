import os
from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy.orm import selectinload
import pandas as pd
from app.database import get_db
from app.models.models import UploadedFile, DatasetArtifact, ChatMessage
from app.schemas.schemas import AskQuestionRequest, AskQuestionResponse, VisualizationCard
from app.services.ask_data.engine import AskDataEngine

router = APIRouter(prefix="/ask-data", tags=["Ask Your Data AI Chat"])

@router.post("/{file_id}", response_model=AskQuestionResponse)
async def ask_data_question(file_id: str, request: AskQuestionRequest, db: AsyncSession = Depends(get_db)):
    """Answers conversational natural language queries against the uploaded & structured dataset."""
    q_file = await db.execute(
        select(UploadedFile)
        .options(selectinload(UploadedFile.dataset))
        .where(UploadedFile.id == file_id)
    )
    file_obj = q_file.scalar_one_or_none()
    if not file_obj or not file_obj.dataset:
        raise HTTPException(status_code=404, detail="Dataset not found")

    dataset = file_obj.dataset
    cleaned_path = dataset.cleaned_data_path or dataset.raw_data_path
    if not cleaned_path or not os.path.exists(cleaned_path):
        raise HTTPException(status_code=400, detail="Data file not available")

    df = pd.read_csv(cleaned_path)

    # Save user message
    user_msg = ChatMessage(
        file_id=file_id,
        role="user",
        content=request.question
    )
    db.add(user_msg)

    # Query engine
    response_dict = await AskDataEngine.query_dataset(
        df=df,
        question=request.question,
        history=request.history
    )

    suggested_chart = response_dict.get("suggested_visualization")
    viz_card = VisualizationCard(**suggested_chart) if suggested_chart else None

    # Save assistant response
    assistant_msg = ChatMessage(
        file_id=file_id,
        role="assistant",
        content=response_dict["answer"],
        structured_data=response_dict.get("supporting_data"),
        suggested_chart=suggested_chart,
        citations=response_dict.get("citations", [])
    )
    db.add(assistant_msg)
    await db.commit()

    return AskQuestionResponse(
        question=request.question,
        answer=response_dict["answer"],
        supporting_data=response_dict.get("supporting_data"),
        suggested_visualization=viz_card,
        sql_or_code=response_dict.get("sql_or_code"),
        citations=response_dict.get("citations", [])
    )

@router.get("/{file_id}/history")
async def get_chat_history(file_id: str, db: AsyncSession = Depends(get_db)):
    """Retrieves previous questions and answers for this file."""
    q_msgs = await db.execute(
        select(ChatMessage)
        .where(ChatMessage.file_id == file_id)
        .order_by(ChatMessage.created_at.asc())
    )
    messages = q_msgs.scalars().all()
    return [
        {
            "id": m.id,
            "role": m.role,
            "content": m.content,
            "structured_data": m.structured_data,
            "suggested_chart": m.suggested_chart,
            "created_at": m.created_at
        }
        for m in messages
    ]
