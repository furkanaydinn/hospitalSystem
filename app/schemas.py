from typing import List, Optional,Union
from datetime import date, datetime
from pydantic import BaseModel, EmailStr,validator


class DepartmentBase(BaseModel):
    name: str


class DepartmentCreate(DepartmentBase):
    pass


class Department(DepartmentBase):
    id: int

    class Config:
        orm_mode = True


class DoctorBase(BaseModel):
    name: str
    surname: str
    email: EmailStr
    specialty: str
    is_active: Optional[bool] = True
    department_id: Optional[int] = None


class DoctorCreate(DoctorBase):
    password: str


class Doctor(DoctorBase):
    id: int
    department: Optional[Department] = None
    patients: List["Patient"] = []
    appointments: List["Appointment"] = []
    billings: List["Billing"] = []
    medical_records: List["MedicalRecord"] = []

    class Config:
        orm_mode = True


class PatientBase(BaseModel):
    name: str
    age: int
    gender: str
    address: str
    phone_number: str
    email: EmailStr
    doctor_id: int


class PatientCreate(PatientBase):
    pass

class PatientUpdate(PatientBase):
    name: str
    email: EmailStr
    phone_number: str
    age: int

    @validator('phone_number')
    def validate_phone_number(cls, v):
        # You can add phone number validation logic here
        return v

class Patient(PatientBase):
    id: int
    doctor: Optional[Doctor] = None
    appointments: List["Appointment"] = []
    billings: List["Billing"] = []
    medical_records: List["MedicalRecord"] = []

    class Config:
        orm_mode = True


class AppointmentBase(BaseModel):
    doctor_id: int
    patient_id: int
    date: datetime
    description: Optional[str] = None


class AppointmentCreate(AppointmentBase):
    pass

class AppointmentUpdate(AppointmentBase):
    date: datetime
    doctor_id: int
    patient_id: int


class Appointment(AppointmentBase):
    id: int
    doctor: Optional[Doctor] = None
    patient: Optional[Patient] = None

    class Config:
        orm_mode = True


class BillingBase(BaseModel):
    patient_id: int
    doctor_id: int
    amount: float
    date: date
    description: Optional[str] = None


class BillingCreate(BillingBase):
    pass


class Billing(BillingBase):
    id: int
    patient: Optional[Patient] = None
    doctor: Optional[Doctor] = None

    class Config:
        orm_mode = True


class MedicalRecordBase(BaseModel):
    patient_id: int
    doctor_id: int
    date: date
    diagnosis: str
    treatment: Optional[str] = None


class MedicalRecordCreate(MedicalRecordBase):
    pass


class MedicalRecord(MedicalRecordBase):
    id: int
    patient: Optional[Patient] = None
    doctor: Optional[Doctor] = None

    class Config:
        orm_mode = True
