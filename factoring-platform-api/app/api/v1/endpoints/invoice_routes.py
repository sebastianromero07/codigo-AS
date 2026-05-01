import xml.etree.ElementTree as ET
from datetime import date, datetime
from decimal import Decimal, InvalidOperation
from pathlib import Path
from typing import Any
from uuid import uuid4

from fastapi import APIRouter, Depends, File, HTTPException, UploadFile, status
from pydantic import BaseModel, ConfigDict
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.db.models import Invoice
from app.db.session import get_db

router = APIRouter(prefix="/invoices", tags=["invoices"])

UPLOAD_DIR = Path("./uploads")
ALLOWED_CONTENT_TYPES = {"application/xml", "text/xml"}
MAX_FILE_SIZE = 10 * 1024 * 1024

REQUIRED_TAGS = (
    "Issuer",
    "Serie",
    "Numero",
    "Monto",
    "Moneda",
    "FechaEmision",
    "FechaVencimiento",
)


class InvoiceResponse(BaseModel):
    model_config = ConfigDict(
        from_attributes=True,
        json_schema_extra={
            "example": {
                "id": 1,
                "company_id": 1,
                "ruc_emisor": "20123456789",
                "serie": "F001",
                "numero": "123",
                "monto": "1500.00",
                "moneda": "PEN",
                "fecha_emision": "2026-04-01",
                "fecha_vencimiento": "2026-05-01",
                "file_path": "uploads/1/9f3a2b1c4e5d4a6b8c7d.xml",
                "status": "uploaded",
                "created_at": "2026-05-01T10:00:00",
            }
        },
    )

    id: int
    company_id: int
    ruc_emisor: str
    serie: str
    numero: str
    monto: Decimal
    moneda: str
    fecha_emision: date
    fecha_vencimiento: date
    file_path: str
    status: str
    created_at: datetime


def _read_xml_payload(file: UploadFile) -> bytes:
    if file.content_type not in ALLOWED_CONTENT_TYPES:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Tipo de archivo no permitido: {file.content_type}. Solo XML.",
        )

    buffer = bytearray()
    while chunk := file.file.read(8192):
        buffer.extend(chunk)
        if len(buffer) > MAX_FILE_SIZE:
            raise HTTPException(
                status_code=status.HTTP_413_REQUEST_ENTITY_TOO_LARGE,
                detail="Archivo excede 10 MB.",
            )

    if not buffer:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="El archivo XML está vacío.",
        )

    return bytes(buffer)


def _parse_invoice_xml(content: bytes) -> dict[str, Any]:
    try:
        root = ET.fromstring(content)
    except ET.ParseError as exc:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"XML inválido: {exc}",
        ) from exc

    extracted: dict[str, str] = {}
    missing: list[str] = []
    for tag in REQUIRED_TAGS:
        element = root.find(tag)
        if element is None or element.text is None or not element.text.strip():
            missing.append(tag)
        else:
            extracted[tag] = element.text.strip()

    if missing:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"El XML no contiene los campos requeridos: {', '.join(missing)}.",
        )

    ruc_emisor = extracted["Issuer"]
    if len(ruc_emisor) != 11 or not ruc_emisor.isdigit():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Issuer (RUC) debe tener exactamente 11 dígitos.",
        )

    try:
        monto = Decimal(extracted["Monto"])
    except InvalidOperation as exc:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Monto inválido en el XML.",
        ) from exc
    if monto <= 0:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Monto debe ser mayor a 0.",
        )

    moneda = extracted["Moneda"].upper()
    if len(moneda) != 3:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Moneda debe ser un código de 3 letras (ej. PEN, USD).",
        )

    try:
        fecha_emision = date.fromisoformat(extracted["FechaEmision"])
        fecha_vencimiento = date.fromisoformat(extracted["FechaVencimiento"])
    except ValueError as exc:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Fechas deben tener formato YYYY-MM-DD.",
        ) from exc

    if fecha_vencimiento < fecha_emision:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="FechaVencimiento no puede ser anterior a FechaEmision.",
        )

    return {
        "ruc_emisor": ruc_emisor,
        "serie": extracted["Serie"],
        "numero": extracted["Numero"],
        "monto": monto,
        "moneda": moneda,
        "fecha_emision": fecha_emision,
        "fecha_vencimiento": fecha_vencimiento,
    }


def _write_xml_to_disk(content: bytes, company_id: int) -> str:
    company_dir = UPLOAD_DIR / str(company_id)
    company_dir.mkdir(parents=True, exist_ok=True)
    dest = company_dir / f"{uuid4().hex}.xml"
    dest.write_bytes(content)
    return str(dest)


@router.get("", response_model=list[InvoiceResponse])
def list_invoices(db: Session = Depends(get_db)):
    return db.execute(select(Invoice).order_by(Invoice.id.desc())).scalars().all()


@router.post("", response_model=InvoiceResponse, status_code=status.HTTP_201_CREATED)
def upload_invoice(file: UploadFile = File(...), db: Session = Depends(get_db)):
    company_id = 1  # TODO: sacar de get_current_user cuando auth esté listo

    content = _read_xml_payload(file)
    parsed = _parse_invoice_xml(content)
    file_path = _write_xml_to_disk(content, company_id)

    invoice = Invoice(
        company_id=company_id,
        ruc_emisor=parsed["ruc_emisor"],
        serie=parsed["serie"],
        numero=parsed["numero"],
        monto=parsed["monto"],
        moneda=parsed["moneda"],
        fecha_emision=parsed["fecha_emision"],
        fecha_vencimiento=parsed["fecha_vencimiento"],
        file_path=file_path,
    )
    db.add(invoice)
    db.commit()
    db.refresh(invoice)
    return invoice
