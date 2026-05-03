from fastapi import APIRouter, Depends
from app.api.deps import get_current_user
from app.modules.users.models import User

router = APIRouter()

@router.post("/process")
def process_payment(
    amount: float,
    current_user: User = Depends(get_current_user) # ESTO CONECTA EL LOGIN CON EL PAGO
):
    return {
        "status": "success", 
        "message": f"Pago procesado", 
        "investor": current_user.email # O el atributo que uses
    }
