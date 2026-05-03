from fastapi import APIRouter
from app.api.v1.endpoints import auth_routes, invoice_routes, payout_routes

api_router = APIRouter()
api_router.include_router(auth_routes.router, prefix="/auth", tags=["auth"])
api_router.include_router(invoice_routes.router, prefix="/invoices", tags=["invoices"])
api_router.include_router(payout_routes.router, prefix="/payments", tags=["payments"])
