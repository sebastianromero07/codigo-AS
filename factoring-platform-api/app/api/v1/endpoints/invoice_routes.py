from fastapi import APIRouter, Depends, UploadFile, File
from app.api.deps import get_current_user
from app.modules.users.models import User

router = APIRouter()

@router.post("/upload")
def upload_invoice(
    file: UploadFile = File(...),
    current_user: User = Depends(get_current_user) # ¡Aquí está la conexión!
):
    """
    Sube un archivo XML/PDF. Solo accesible si el usuario tiene un token válido.
    """
    # Al tener 'current_user', puedes asociar la factura a la empresa correcta:
    # invoice_service.process_file(file, company_id=current_user.company_id)
    
    return {"filename": file.filename, "uploaded_by": current_user.email}
