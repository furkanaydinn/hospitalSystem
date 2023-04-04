from sqlalchemy import Column, Integer, String,Boolean,ForeignKey
from sqlalchemy.orm import relationship
from app.db.session import Base


class Doctor(Base):
    __tablename__ = "doctors"

    id = Column(Integer,primary_key=True,index=True)
    name = Column(String(255), index=True)
    surname = Column(String(255),index=True)
    email = Column(String(255), unique=True, index=True)
    password = Column(String(255))
    specialty = Column(String(255), index=True)
    is_active = Column(Boolean(), default=True)

    department_id = Column(Integer, ForeignKey("departments.id"))
    department = relationship("Department", back_populates="doctors")

    patients = relationship("Patient", back_populates="doctor")
    appointments = relationship("Appointment", back_populates="doctor")
