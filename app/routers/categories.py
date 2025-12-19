from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from app.db.session import get_db
from app.models.models import Category
from app.schemas.schemas import CategoryCreate, CategoryResponse
from app.core.security import get_current_user
from app.schemas.schemas import CategoryUpdate

router = APIRouter()

def check_admin(user: dict):
    pass 

@router.post("/", response_model=CategoryResponse, status_code=status.HTTP_201_CREATED)
def create_category(
    category: CategoryCreate, 
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    
    db_category = Category(name=category.name)
    db.add(db_category)
    try:
        db.commit()
        db.refresh(db_category)
    except Exception:
        db.rollback()
        raise HTTPException(status_code=400, detail="categoria ja existe")
    return db_category

@router.get("/", response_model=List[CategoryResponse])
def list_categories(db: Session = Depends(get_db)):
    return db.query(Category).all()


@router.put("/{category_id}", response_model=CategoryResponse)
def update_category(
    category_id: int,
    category_update: CategoryUpdate,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    # validacao do admin    
    db_category = db.query(Category).filter(Category.id == category_id).first()
    if not db_category:
        raise HTTPException(status_code=404, detail="categoria nao encontrada")
    
    db_category.name = category_update.name
    db.commit()
    db.refresh(db_category)
    return db_category

@router.delete("/{category_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_category(
    category_id: int,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    db_category = db.query(Category).filter(Category.id == category_id).first()
    if not db_category:
        raise HTTPException(status_code=404, detail="categoria nao encontrada")
    
    db.delete(db_category)
    db.commit()
    return None