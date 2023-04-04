from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app import schemas
from app.db.session import get_db
from app.db.models.doctor import Doctor

router = APIRouter()


@router.post('/doctors', response_model=schemas.Doctor)
def create_doctor(request: schemas.DoctorCreate, db: Session = Depends(get_db)):
    """
    Create a new doctor
    """
    doctor = Doctor(**request.dict())
    db.add(doctor)
    db.commit()
    db.refresh(doctor)
    return doctor


@router.get('/doctors/{doctor_id}', response_model=schemas.Doctor)
def read_doctor(doctor_id: int, db: Session = Depends(get_db)):
    """
    Get a doctor by ID
    """
    doctor = db.query(Doctor).filter(Doctor.id == doctor_id).first()
    if not doctor:
        raise HTTPException(status_code=404, detail='Doctor not found')
    return doctor


@router.get('/doctors', response_model=list[schemas.Doctor])
def read_doctors(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """
    Get all doctors
    """
    doctors = db.query(Doctor).offset(skip).limit(limit).all()
    return doctors


@router.put('/doctors/{doctor_id}', response_model=schemas.Doctor)
def update_doctor(doctor_id: int, request: schemas.DoctorCreate, db: Session = Depends(get_db)):
    """
    Update a doctor
    """
    doctor = db.query(Doctor).filter(Doctor.id == doctor_id)
    if not doctor.first():
        raise HTTPException(status_code=404, detail='Doctor not found')
    doctor.update(request.dict())
    db.commit()
    return doctor.first()


@router.delete('/doctors/{doctor_id}', response_model=schemas.Doctor)
def delete_doctor(doctor_id: int, db: Session = Depends(get_db)):
    """
    Delete a doctor
    """
    doctor = db.query(Doctor).filter(Doctor.id == doctor_id).first()
    if not doctor:
        raise HTTPException(status_code=404, detail='Doctor not found')
    db.delete(doctor)
    db.commit()
    return doctor


