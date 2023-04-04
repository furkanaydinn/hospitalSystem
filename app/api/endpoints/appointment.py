from typing import List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app import schemas
from app.db.session import get_db
from app.db.models import appointment

router = APIRouter()


@router.get("/", response_model=List[schemas.Appointment])
async def read_appointments(
    skip: int = 0, limit: int = 100, db: Session = Depends(get_db)
):
    appointments = db.query(appointment.Appointment).offset(skip).limit(limit).all()
    return appointments


@router.post("/", response_model=schemas.Appointment)
async def create_appointment(
    appointment: schemas.AppointmentCreate, db: Session = Depends(get_db)
):
    db_appointment = appointment.Appointment(**appointment.dict())
    db.add(db_appointment)
    db.commit()
    db.refresh(db_appointment)
    return db_appointment


@router.get("/{appointment_id}", response_model=schemas.Appointment)
async def read_appointment(appointment_id: int, db: Session = Depends(get_db)):
    db_appointment = db.query(appointment.Appointment).filter(appointment.Appointment.id == appointment_id).first()
    if db_appointment is None:
        raise HTTPException(status_code=404, detail="Appointment not found")
    return db_appointment


@router.put("/{appointment_id}", response_model=schemas.Appointment)
async def update_appointment(
    appointment_id: int, appointment: schemas.AppointmentUpdate, db: Session = Depends(get_db)
):
    db_appointment = db.query(appointment.Appointment).filter(appointment.Appointment.id == appointment_id).first()
    if db_appointment is None:
        raise HTTPException(status_code=404, detail="Appointment not found")
    update_data = appointment.dict(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_appointment, key, value)
    db.commit()
    db.refresh(db_appointment)
    return db_appointment


@router.delete("/{appointment_id}", response_model=schemas.Appointment)
async def delete_appointment(appointment_id: int, db: Session = Depends(get_db)):
    db_appointment = db.query(appointment.Appointment).filter(appointment.Appointment.id == appointment_id).first()
    if db_appointment is None:
        raise HTTPException(status_code=404, detail="Appointment not found")
    db.delete(db_appointment)
    db.commit()
    return db_appointment
