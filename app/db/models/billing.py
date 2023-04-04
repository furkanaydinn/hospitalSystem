from sqlalchemy import Column, ForeignKey, Integer, String, Date, Numeric
from sqlalchemy.orm import relationship
from app.db.session import Base

class Billing(Base):
    __tablename__ = "billings"

    id = Column(Integer,primary_key=True,index=True)
    patient_id = Column(Integer,ForeignKey("patients.id"))
    doctor_id = Column(Integer,ForeignKey("doctors.id"))
    amount = Column(Numeric(precision=2))
    date = Column(Date)
    description = Column(String)

    patient = relationship("Patient",back_populates="billings")
    doctor = relationship("Doctor", back_populates="billings")