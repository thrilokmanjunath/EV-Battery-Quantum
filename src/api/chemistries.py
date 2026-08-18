from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List, Dict, Any
from ..database.session import get_db
from ..database.models import BatteryChemistry, Material, Reaction

router = APIRouter(prefix="/api")

@router.get("/chemistries")
def get_all_chemistries(db: Session = Depends(get_db)):
    chemistries = db.query(BatteryChemistry).all()
    return chemistries

@router.get("/chemistries/{id}")
def get_chemistry_by_id(id: int, db: Session = Depends(get_db)):
    chemistry = db.query(BatteryChemistry).filter(BatteryChemistry.id == id).first()
    if not chemistry:
        raise HTTPException(status_code=404, detail="Chemistry not found")
    
    reactions = db.query(Reaction).filter(Reaction.chemistry_id == id).all()
    
    return {
        "chemistry": chemistry,
        "reactions": reactions
    }

@router.get("/materials")
def get_all_materials(db: Session = Depends(get_db)):
    return db.query(Material).all()

@router.get("/elements")
def get_elements(db: Session = Depends(get_db)):
    return db.query(Material).filter(Material.material_type == "element").all()
