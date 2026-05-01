from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy import select
from pydantic import BaseModel, EmailStr
from app.db.models import User
from app.db.session import get_db

router = APIRouter(prefix="/auth", tags=["auth"])

# Esquemas de Pydantic
class UserCreate(BaseModel):
    email: EmailStr
    password: str
    user_type: str  # "entity" o "investor"

class LoginRequest(BaseModel):
    email: EmailStr
    password: str

@router.post("/register", status_code=status.HTTP_201_CREATED)
def register(payload: UserCreate, db: Session = Depends(get_db)):
    # Verificar si ya existe
    existing_user = db.execute(select(User).where(User.email == payload.email)).scalar_one_or_none()
    if existing_user:
        raise HTTPException(status_code=400, detail="El correo ya está registrado.")
    
    new_user = User(
        email=payload.email,
        hashed_password=payload.password, # En producción usar hashing (ej. passlib)
        user_type=payload.user_type
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return {"message": "Usuario creado exitosamente", "user_id": new_user.id}

@router.post("/login")
def login(payload: LoginRequest, db: Session = Depends(get_db)):
    user = db.execute(select(User).where(User.email == payload.email)).scalar_one_or_none()
    
    if not user or user.hashed_password != payload.password:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Credenciales incorrectas")
    
    return {
        "access_token": f"fake-token-for-{user.id}", 
        "token_type": "bearer",
        "user_type": user.user_type
    }