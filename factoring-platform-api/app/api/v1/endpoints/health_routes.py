from fastapi import APIRouter, HTTPException

from app.db.h2 import H2ConnectionError, init_database, ping_database, seed_database

router = APIRouter(prefix="/health", tags=["health"])


@router.get("")
def health_check():
    return {
        "status": "ok",
    }


@router.get("/db")
def database_health_check():
    try:
        return ping_database()
    except H2ConnectionError as exc:
        raise HTTPException(status_code=503, detail=str(exc)) from exc


@router.post("/db/init")
def initialize_database():
    try:
        init_database()

        return {
            "message": "Base de datos inicializada correctamente",
        }
    except H2ConnectionError as exc:
        raise HTTPException(status_code=503, detail=str(exc)) from exc


@router.post("/db/seed")
def seed_initial_data():
    try:
        seed_database()

        return {
            "message": "Datos iniciales insertados correctamente",
        }
    except H2ConnectionError as exc:
        raise HTTPException(status_code=503, detail=str(exc)) from exc