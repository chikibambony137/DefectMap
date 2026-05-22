from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from api.dependencies import get_db, get_current_user, get_current_admin_user
from models.defect_status import DefectStatus
from schemas.defect_status import DefectStatusCreate, DefectStatusResponse

router = APIRouter(prefix="/defect-statuses", tags=["defect-statuses"])


@router.get("/", response_model=List[DefectStatusResponse])
def get_defect_statuses(
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    return db.query(DefectStatus).all()


@router.post("/", response_model=DefectStatusResponse, status_code=201)
def create_defect_status(
    data: DefectStatusCreate,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_admin_user)
):
    existing = db.query(DefectStatus).filter(
        DefectStatus.name == data.name).first()
    if existing:
        raise HTTPException(status_code=400,
                            detail="Статус с таким именем уже существует")
    status = DefectStatus(**data.model_dump())
    db.add(status)
    db.commit()
    db.refresh(status)
    return status


@router.delete("/{status_id}", status_code=204)
def delete_defect_status(
    status_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_admin_user)
):
    status = db.query(DefectStatus).filter(
        DefectStatus.id == status_id).first()
    if not status:
        raise HTTPException(status_code=404,
                            detail="Статус не найден")
    if status.defects:
        raise HTTPException(status_code=400,
                            detail="Нельзя удалить статус,"
                            "к которому привязаны дефекты")
    db.delete(status)
    db.commit()
