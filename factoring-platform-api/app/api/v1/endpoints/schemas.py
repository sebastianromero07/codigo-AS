from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime

class InvoicePurchaseRequest(BaseModel):
    user_id: int
    user_type: str = Field(..., example="investor", description="Debe indicarse explícitamente el tipo de usuario, ej: 'investor'")
    company_id: int = Field(..., description="ID de la empresa dueña de la factura")
    invoice_id: int
    amount: float = Field(..., gt=0)

class PurchaseResponse(BaseModel):
    success: bool
    message: str
    transaction_id: Optional[int] = None
    remaining_balance: Optional[float] = None

class WalletResponse(BaseModel):
    id: int
    user_id: int
    user_type: str
    balance: float

class WalletFundRequest(BaseModel):
    user_id: int
    amount: float = Field(..., gt=0)
