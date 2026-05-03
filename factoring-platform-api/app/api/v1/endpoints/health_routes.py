from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import text
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session

from app.db.session import get_db, init_db

router = APIRouter(prefix="/health", tags=["health"])


@router.get("")
def health_check():
    return {"status": "ok"}


@router.get("/db")
def database_health_check(db: Session = Depends(get_db)):
    try:
        result = db.execute(text("SELECT 1 AS ok")).scalar()
        return {"connected": True, "result": result}
    except SQLAlchemyError as exc:
        raise HTTPException(status_code=503, detail=str(exc)) from exc


@router.post("/db/init")
def initialize_database():
    try:
        init_db()
        return {"message": "Base de datos inicializada correctamente"}
    except SQLAlchemyError as exc:
        raise HTTPException(status_code=503, detail=str(exc)) from exc
