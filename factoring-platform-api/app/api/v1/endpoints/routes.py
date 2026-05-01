from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker
from . import schemas, service

router = APIRouter(prefix="/payments", tags=["payments"])

SQLALCHEMY_DATABASE_URL = "sqlite:///./payments_test.db"
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Dependencia mock para obtener sesión de base de datos local
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/wallet/fund", response_model=schemas.WalletResponse)
def fund_wallet(request: schemas.WalletFundRequest, db: Session = Depends(get_db)):
    """Añade saldo a la wallet de un usuario (mock)."""
    return service.fund_wallet(db, request)

@router.post("/buy-invoice", response_model=schemas.PurchaseResponse)
def buy_invoice(request: schemas.InvoicePurchaseRequest, db: Session = Depends(get_db)):
    """Permite a un usuario de tipo 'investor' comprar una factura descontando el saldo de su wallet."""
    return service.purchase_invoice(db, request)