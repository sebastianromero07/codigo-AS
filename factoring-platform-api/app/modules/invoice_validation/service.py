def validate_invoice(invoice):
    """
    Simulación de validación de factura (tipo SUNAT).
    """

    # Regla simple de validación
    if invoice.amount <= 0:
        return {
            "status": "REJECTED",
            "message": "Factura inválida (monto incorrecto)"
        }

    return {
        "status": "VALIDATED",
        "message": "Factura validada correctamente"
    }


def process_invoice_validation(invoice):
    """
    Aplica la validación y actualiza el estado de la factura.
    """

    result = validate_invoice(invoice)

    if result["status"] == "REJECTED":
        invoice.state = "REJECTED"
    else:
        invoice.state = "VALIDATED"

    return result
    