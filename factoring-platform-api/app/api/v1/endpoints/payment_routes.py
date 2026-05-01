from datetime import datetime
from decimal import Decimal
from typing import Optional

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel, ConfigDict, Field
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.db.models import Transaction, Wallet
from app.db.session import get_db

router = APIRouter(prefix="/payments", tags=["payments"])


class WalletFundRequest(BaseModel):
    model_config = ConfigDict(
        json_schema_extra={
            "example": {"user_id": 10, "amount": "5000.00"}
        }
    )

    user_id: int
    amount: Decimal = Field(..., gt=0)


class WalletResponse(BaseModel):
    model_config = ConfigDict(
        from_attributes=True,
        json_schema_extra={
            "example": {
                "id": 1,
                "user_id": 10,
                "user_type": "investor",
                "balance": "5000.00",
            }
        },
    )

    id: int
    user_id: int
    user_type: str
    balance: Decimal


class InvoicePurchaseRequest(BaseModel):
    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "user_id": 10,
                "user_type": "investor",
                "company_id": 1,
                "invoice_id": 1,
                "amount": "1500.00",
            }
        }
    )

    user_id: int
    user_type: str = Field(..., description="Debe ser 'investor'")
    company_id: int
    invoice_id: int
    amount: Decimal = Field(..., gt=0)


class PurchaseResponse(BaseModel):
    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "success": True,
                "message": "Factura comprada exitosamente. Fondos transferidos a la empresa.",
                "transaction_id": 1,
                "remaining_balance": "3500.00",
            }
        }
    )

    success: bool
    message: str
    transaction_id: Optional[int] = None
    remaining_balance: Optional[Decimal] = None


def _get_or_create_wallet(
    db: Session, user_id: int, user_type: str = "investor"
) -> Wallet:
    wallet = db.execute(
        select(Wallet).where(Wallet.user_id == user_id)
    ).scalar_one_or_none()
    if wallet is None:
        wallet = Wallet(user_id=user_id, user_type=user_type, balance=Decimal("0.00"))
        db.add(wallet)
        db.commit()
        db.refresh(wallet)
    return wallet


@router.post("/wallet/fund", response_model=WalletResponse)
def fund_wallet(request: WalletFundRequest, db: Session = Depends(get_db)):
    wallet = _get_or_create_wallet(db, request.user_id)
    wallet.balance = wallet.balance + request.amount
    db.commit()
    db.refresh(wallet)
    return wallet


@router.post("/buy-invoice", response_model=PurchaseResponse)
def buy_invoice(request: InvoicePurchaseRequest, db: Session = Depends(get_db)):
    if request.user_type.lower() != "investor":
        raise HTTPException(
            status_code=403,
            detail="Solo los usuarios tipo 'investor' pueden comprar facturas.",
        )

    investor_wallet = db.execute(
        select(Wallet).where(Wallet.user_id == request.user_id)
    ).scalar_one_or_none()

    if investor_wallet is None:
        raise HTTPException(
            status_code=404,
            detail="Wallet del inversor no encontrada. Fondea tu cuenta primero.",
        )

    if investor_wallet.balance < request.amount:
        raise HTTPException(
            status_code=400,
            detail="Saldo insuficiente en la wallet del inversor.",
        )

    company_wallet = _get_or_create_wallet(
        db, request.company_id, user_type="company"
    )

    investor_wallet.balance = investor_wallet.balance - request.amount
    company_wallet.balance = company_wallet.balance + request.amount

    investor_tx = Transaction(
        wallet_id=investor_wallet.id,
        invoice_id=request.invoice_id,
        amount=-request.amount,
        transaction_type="purchase",
    )
    db.add(investor_tx)

    company_tx = Transaction(
        wallet_id=company_wallet.id,
        invoice_id=request.invoice_id,
        amount=request.amount,
        transaction_type="invoice_sale",
    )
    db.add(company_tx)

    db.commit()
    db.refresh(investor_tx)
    db.refresh(investor_wallet)

    return PurchaseResponse(
        success=True,
        message="Factura comprada exitosamente. Fondos transferidos a la empresa.",
        transaction_id=investor_tx.id,
        remaining_balance=investor_wallet.balance,
    )
