from typing import Any

from fastapi import APIRouter, HTTPException, status
from pydantic import BaseModel, EmailStr, Field

from app.db.h2 import H2ConnectionError, execute_query, execute_update, init_database

router = APIRouter(prefix="/clients", tags=["clients"])


class ClientCreate(BaseModel):
    document_number: str = Field(min_length=8, max_length=20)
    business_name: str = Field(min_length=2, max_length=150)
    email: EmailStr


class ClientResponse(BaseModel):
    id: int
    document_number: str
    business_name: str
    email: str
    created_at: str | None = None


def _normalize_client(row: dict[str, Any]) -> dict[str, Any]:
    return {
        "id": row.get("id"),
        "document_number": row.get("document_number"),
        "business_name": row.get("business_name"),
        "email": row.get("email"),
        "created_at": str(row.get("created_at")) if row.get("created_at") is not None else None,
    }


@router.get("", response_model=list[ClientResponse])
def list_clients():
    try:
        init_database()

        rows = execute_query(
            """
            SELECT id, document_number, business_name, email, created_at
            FROM clients
            ORDER BY id DESC
            """
        )

        return [_normalize_client(row) for row in rows]
    except H2ConnectionError as exc:
        raise HTTPException(status_code=503, detail=str(exc)) from exc


@router.post("", response_model=ClientResponse, status_code=status.HTTP_201_CREATED)
def create_client(payload: ClientCreate):
    try:
        init_database()

        execute_update(
            """
            INSERT INTO clients (document_number, business_name, email)
            VALUES (?, ?, ?)
            """,
            [payload.document_number, payload.business_name, payload.email],
        )

        rows = execute_query(
            """
            SELECT id, document_number, business_name, email, created_at
            FROM clients
            WHERE email = ?
            """,
            [payload.email],
        )

        return _normalize_client(rows[0])

    except H2ConnectionError as exc:
        raise HTTPException(status_code=503, detail=str(exc)) from exc

    except Exception as exc:
        raise HTTPException(
            status_code=400,
            detail="No se pudo crear el cliente. Revisa si el RUC/documento o email ya existen.",
        ) from exc