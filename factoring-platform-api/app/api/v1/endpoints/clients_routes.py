from datetime import datetime

from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel, ConfigDict, EmailStr, Field
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.db.models import Client
from app.db.session import get_db

router = APIRouter(prefix="/clients", tags=["clients"])


class ClientCreate(BaseModel):
    document_number: str = Field(min_length=8, max_length=20)
    business_name: str = Field(min_length=2, max_length=150)
    email: EmailStr


class ClientResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    document_number: str
    business_name: str
    email: str
    created_at: datetime


@router.get("", response_model=list[ClientResponse])
def list_clients(db: Session = Depends(get_db)):
    rows = db.execute(select(Client).order_by(Client.id.desc())).scalars().all()
    return rows


@router.post("", response_model=ClientResponse, status_code=status.HTTP_201_CREATED)
def create_client(payload: ClientCreate, db: Session = Depends(get_db)):
    client = Client(
        document_number=payload.document_number,
        business_name=payload.business_name,
        email=payload.email,
    )
    db.add(client)
    try:
        db.commit()
    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="El documento o email ya existen.",
        )
    db.refresh(client)
    return client
