from typing import List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app import schemas
from app.db.session import SessionLocal
from app.db.models.medicalrecord import MedicalRecord
from app.api.utils import get_patient_by_id

router = APIRouter()


@router.post("/", response_model=schemas.MedicalRecord)
async def create_medical_record(
    medical_record: schemas.MedicalRecordCreate,
    db: Session = Depends(SessionLocal),
    patient: schemas.Patient = Depends(get_patient_by_id),
):
    db_medical_record = MedicalRecord(**medical_record.dict(), patient_id=patient.id)
    db.add(db_medical_record)
    db.commit()
    db.refresh(db_medical_record)
    return db_medical_record


@router.get("/", response_model=List[schemas.MedicalRecord])
async def read_medical_records(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(SessionLocal),
    patient: schemas.Patient = Depends(get_patient_by_id),
):
    medical_records = (
        db.query(MedicalRecord)
        .filter(MedicalRecord.patient_id == patient.id)
        .offset(skip)
        .limit(limit)
        .all()
    )
    return medical_records


@router.get("/{medical_record_id}", response_model=schemas.MedicalRecord)
async def read_medical_record(
    medical_record_id: int,
    db: Session = Depends(SessionLocal),
    patient: schemas.Patient = Depends(get_patient_by_id),
):
    medical_record = (
        db.query(MedicalRecord)
        .filter(MedicalRecord.patient_id == patient.id)
        .filter(MedicalRecord.id == medical_record_id)
        .first()
    )
    if not medical_record:
        raise HTTPException(
            status_code=404, detail="Medical Record not found"
        )
    return medical_record


@router.put("/{medical_record_id}", response_model=schemas.MedicalRecord)
async def update_medical_record(
    medical_record_id: int,
    medical_record: schemas.MedicalRecordCreate,
    db: Session = Depends(SessionLocal),
    patient: schemas.Patient = Depends(get_patient_by_id),
):
    db_medical_record = (
        db.query(MedicalRecord)
        .filter(MedicalRecord.patient_id == patient.id)
        .filter(MedicalRecord.id == medical_record_id)
        .first()
    )
    if not db_medical_record:
        raise HTTPException(
            status_code=404, detail="Medical Record not found"
        )
    update_data = medical_record.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_medical_record, field, value)
    db.add(db_medical_record)
    db.commit()
    db.refresh(db_medical_record)
    return db_medical_record


@router.delete("/{medical_record_id}")
async def delete_medical_record(
    medical_record_id: int,
    db: Session = Depends(SessionLocal),
    patient: schemas.Patient = Depends(get_patient_by_id),
):
    db_medical_record = (
        db.query(MedicalRecord)
        .filter(MedicalRecord.patient_id == patient.id)
        .filter(MedicalRecord.id == medical_record_id)
        .first()
    )
    if not db_medical_record:
        raise HTTPException(
            status_code=404, detail="Medical Record not found"
        )
    db.delete(db_medical_record)
    db.commit()
    return {"detail": "Medical Record deleted"}
