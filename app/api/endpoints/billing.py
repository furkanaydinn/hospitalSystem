from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.db.session import engine, get_db
from app import schemas
from app.db.session import Base
from app.api.utils import calculate_invoice_total
from app.db.models import appointment,doctor,patient,billing

Base.metadata.create_all(bind=engine)

router = APIRouter()


@router.post("/billings/", response_model=schemas.Billing)
async def create_billing(billing: schemas.BillingCreate, db: Session = Depends(get_db)):
    appointment = db.query(appointment.Appointment).filter(appointment.Appointment.id == billing.appointment_id).first()
    if not appointment:
        raise HTTPException(status_code=404, detail="Appointment not found")
    doctor = db.query(doctor.Doctor).filter(doctor.Doctor.id == billing.doctor_id).first()
    if not doctor:
        raise HTTPException(status_code=404, detail="Doctor not found")
    patient = db.query(patient.Patient).filter(patient.Patient.id == billing.patient_id).first()
    if not patient:
        raise HTTPException(status_code=404, detail="Patient not found")
    
    cost = doctor.hourly_rate * appointment.duration_in_minutes / 60
    new_billing = billing.Billing(amount=cost, **billing.dict())
    db.add(new_billing)
    db.commit()
    db.refresh(new_billing)
    return new_billing


@router.get("/billings/", response_model=List[schemas.Billing])
async def read_billings(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    billings = db.query(billing.Billing).offset(skip).limit(limit).all()
    return billings


@router.get("/billings/{billing_id}", response_model=schemas.Billing)
async def read_billing(billing_id: int, db: Session = Depends(get_db)):
    billing = db.query(billing.Billing).filter(billing.Billing.id == billing_id).first()
    if not billing:
        raise HTTPException(status_code=404, detail="Billing not found")
    return billing


@router.get("/billings/total", response_model=float)
async def read_total_amount_of_billings(db: Session = Depends(get_db)):
    billings = db.query(billing.Billing).all()
    total_amount = calculate_invoice_total(billings)
    return total_amount
