from fastapi import APIRouter

from app.api.v1.endpoints import (
    auth_routes,
    clients_routes,
    health_routes,
    invoice_routes,
    payment_routes,
)

api_router = APIRouter()

api_router.include_router(auth_routes.router)
api_router.include_router(health_routes.router)
api_router.include_router(clients_routes.router)
api_router.include_router(invoice_routes.router)
api_router.include_router(payment_routes.router)