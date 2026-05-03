'''
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from app.api import deps
from app.core.security import verify_password, create_access_token
from app.modules.users.repository import get_user_by_email # Asumiendo que tienes esta función

router = APIRouter()

@router.post("/login")
def login_access_token(
    db: Session = Depends(deps.get_db),
    form_data: OAuth2PasswordRequestForm = Depends()
):
    """
    Autenticación de usuarios y generación de token.
    """
    user = get_user_by_email(db, email=form_data.username)
    if not user or not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Correo o contraseña incorrectos",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    # Generar token
    access_token = create_access_token(subject=user.id)
    return {
        "access_token": access_token,
        "token_type": "bearer",
        "user_role": user.role # Útil para el frontend (ej. 'investor' o 'company')
    }

'''
'''
MOKERARLO POR SI LA BD FALLA
'''
@router.post("/login")
def login_acceso_rapido(form_data: OAuth2PasswordRequestForm = Depends()):
    # Bypass para que el PoC funcione sí o sí
    if form_data.username == "demo@demo.com" and form_data.password == "1234":
        access_token = create_access_token(subject="1") # 1 es un ID de usuario ficticio
        return {"access_token": access_token, "token_type": "bearer"}
    raise HTTPException(status_code=400, detail="Credenciales incorrectas")


