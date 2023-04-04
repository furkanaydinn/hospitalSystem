from typing import List
from fastapi import APIRouter, Depends, HTTPException
from app import schemas
from app.db.models.patient import Patient
from app.db.session import get_db
from sqlalchemy.orm import Session

router = APIRouter()

# Get all patients
@router.get("/", response_model=List[schemas.Patient])
async def read_patients(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    patients = db.query(Patient).offset(skip).limit(limit).all()
    return patients


# Get a patient by id
@router.get("/{patient_id}", response_model=schemas.Patient)
async def read_patient(patient_id: int, db: Session = Depends(get_db)):
    patient = db.query(Patient).filter(Patient.id == patient_id).first()
    if not patient:
        raise HTTPException(status_code=404, detail="Patient not found")
    return patient


# Create a new patient
@router.post("/", response_model=schemas.Patient)
async def create_patient(patient: schemas.PatientCreate, db: Session = Depends(get_db)):
    db_patient = patient.Patient(**patient.dict())
    db.add(db_patient)
    db.commit()
    db.refresh(db_patient)
    return db_patient


# Update a patient by id
@router.put("/{patient_id}", response_model=schemas.Patient)
async def update_patient(patient_id: int, patient: schemas.PatientUpdate, db: Session = Depends(get_db)):
    db_patient = db.query(patient.Patient).filter(patient.Patient.id == patient_id)
    if not db_patient.first():
        raise HTTPException(status_code=404, detail="Patient not found")
    db_patient.update(patient.dict())
    db.commit()
    db.refresh(db_patient.first())
    return db_patient.first()


# Delete a patient by id
@router.delete("/{patient_id}", response_model=schemas.Patient)
async def delete_patient(patient_id: int, db: Session = Depends(get_db)):
    db_patient = db.query(Patient).filter(Patient.id == patient_id)
    if not db_patient.first():
        raise HTTPException(status_code=404, detail="Patient not found")
    db_patient.delete()
    db.commit()
    return db_patient.first()
