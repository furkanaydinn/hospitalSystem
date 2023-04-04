from typing import List
from app import schemas
from app.db.models.patient import Patient
from sqlalchemy.orm import Session
from fastapi import HTTPException, status

def calculate_invoice_total(invoices: List[schemas.Billing]) -> float:
    """
    Calculates the total amount of the given invoices.
    """
    total = 0.0
    for invoice in invoices:
        total += invoice.amount
    return total


def get_patient_by_id(db: Session, patient_id: int):
    patient = db.query(Patient).filter(Patient.id == patient_id).first()
    if not patient:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Patient not found")
    return patient
