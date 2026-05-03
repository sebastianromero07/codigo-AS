from fastapi import APIRouter

router = APIRouter()

# Simulación de base de datos 
fake_db = {
    1: {"id": 1, "amount": 1000, "state": "DRAFT"}
}


@router.post("/validate/{invoice_id}")
def validate_invoice_endpoint(invoice_id: int):
    invoice = fake_db.get(invoice_id)

    if not invoice:
        return {"error": "Factura no encontrada"}

    from app.modules.invoice_validation.service import process_invoice_validation

    result = process_invoice_validation(invoice)

    return {
        "invoice_id": invoice_id,
        "new_state": invoice["state"],
        "validation_result": result
    }
