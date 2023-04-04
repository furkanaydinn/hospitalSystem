from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app import schemas
from app.db.session import get_db
from app.db.models.department import Department

router = APIRouter()


@router.post('/departments', response_model=schemas.Department)
def create_department(request: schemas.DepartmentCreate, db: Session = Depends(get_db)):
    """
    Create a new department
    """
    department = Department(**request.dict())
    db.add(department)
    db.commit()
    db.refresh(department)
    return department


@router.get('/departments/{department_id}', response_model=schemas.Department)
def read_department(department_id: int, db: Session = Depends(get_db)):
    """
    Get a department by ID
    """
    department = db.query(Department).filter(Department.id == department_id).first()
    if not department:
        raise HTTPException(status_code=404, detail='Department not found')
    return department


@router.get('/departments', response_model=list[schemas.Department])
def read_departments(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """
    Get all departments
    """
    departments = db.query(Department).offset(skip).limit(limit).all()
    return departments


@router.put('/departments/{department_id}', response_model=schemas.Department)
def update_department(department_id: int, request: schemas.DepartmentCreate, db: Session = Depends(get_db)):
    """
    Update a department
    """
    department = db.query(Department).filter(Department.id == department_id)
    if not department.first():
        raise HTTPException(status_code=404, detail='Department not found')
    department.update(request.dict())
    db.commit()
    return department.first()


@router.delete('/departments/{department_id}', response_model=schemas.Department)
def delete_department(department_id: int, db: Session = Depends(get_db)):
    """
    Delete a department
    """
    department = db.query(Department).filter(Department.id == department_id).first()
    if not department:
        raise HTTPException(status_code=404, detail='Department not found')
    db.delete(department)
    db.commit()
    return department
