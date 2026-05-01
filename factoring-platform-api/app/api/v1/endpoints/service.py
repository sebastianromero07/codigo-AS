from sqlalchemy.orm import Session
from fastapi import HTTPException
from . import models, schemas

def get_or_create_wallet(db: Session, user_id: int, user_type: str = "investor"):
    wallet = db.query(models.Wallet).filter(models.Wallet.user_id == user_id).first()
    if not wallet:
        wallet = models.Wallet(user_id=user_id, user_type=user_type, balance=0.0)
        db.add(wallet)
        db.commit()
        db.refresh(wallet)
    return wallet

def fund_wallet(db: Session, request: schemas.WalletFundRequest):
    wallet = get_or_create_wallet(db, request.user_id)
    wallet.balance += request.amount
    db.commit()
    db.refresh(wallet)
    return wallet

def purchase_invoice(db: Session, request: schemas.InvoicePurchaseRequest):
    if request.user_type.lower() != "investor":
        raise HTTPException(status_code=403, detail="Solo los usuarios tipo 'investor' pueden comprar facturas.")
        
    investor_wallet = db.query(models.Wallet).filter(models.Wallet.user_id == request.user_id).first()
    
    if not investor_wallet:
        raise HTTPException(status_code=404, detail="Wallet del inversor no encontrada. Fondea tu cuenta primero.")
        
    if investor_wallet.balance < request.amount:
        raise HTTPException(status_code=400, detail="Saldo insuficiente en la wallet del inversor.")
        
    # Obtener o crear wallet de la empresa
    company_wallet = get_or_create_wallet(db, request.company_id, user_type="company")
        
    # Descontar saldo al inversor y acreditar a la empresa
    investor_wallet.balance -= request.amount
    company_wallet.balance += request.amount
    
    # Registrar transacción para el inversor (egreso por compra)
    investor_transaction = models.Transaction(
        wallet_id=investor_wallet.id,
        invoice_id=request.invoice_id,
        amount=-request.amount,
        transaction_type="purchase"
    )
    db.add(investor_transaction)

    # Registrar transacción para la empresa (ingreso por venta de factura)
    company_transaction = models.Transaction(
        wallet_id=company_wallet.id,
        invoice_id=request.invoice_id,
        amount=request.amount,
        transaction_type="invoice_sale"
    )
    db.add(company_transaction)

    db.commit()
    db.refresh(investor_transaction)
    
    return schemas.PurchaseResponse(
        success=True,
        message="Factura comprada exitosamente. Fondos transferidos a la empresa.",
        transaction_id=investor_transaction.id,
        remaining_balance=investor_wallet.balance
    )
