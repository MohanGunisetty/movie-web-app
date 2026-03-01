from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from .. import database, models, schemas
from ..dependencies import get_current_user, require_admin

router = APIRouter(
    prefix="/api",
    tags=["Categories"]
)

@router.get("/categories", response_model=List[schemas.CategoryResponse])
def get_categories(db: Session = Depends(database.get_db)):
    return db.query(models.Category).all()

@router.post("/admin/categories", response_model=schemas.CategoryResponse)
def create_category(
    category: schemas.CategoryCreate,
    current_user: models.User = Depends(require_admin),
    db: Session = Depends(database.get_db)
):
    db_cat = db.query(models.Category).filter(models.Category.name == category.name).first()
    if db_cat:
        raise HTTPException(status_code=400, detail="Category already exists")
    
    new_cat = models.Category(name=category.name)
    db.add(new_cat)
    db.commit()
    db.refresh(new_cat)
    return new_cat

@router.delete("/admin/categories/{category_id}")
def delete_category(
    category_id: int,
    current_user: models.User = Depends(require_admin),
    db: Session = Depends(database.get_db)
):
    category = db.query(models.Category).filter(models.Category.id == category_id).first()
    if not category:
        raise HTTPException(status_code=404, detail="Category not found")
    
    # Optional: Check if movies exist in this category before deletion
    if db.query(models.Movie).filter(models.Movie.category_id == category_id).first():
        raise HTTPException(status_code=400, detail="Cannot delete category with associated movies")

    db.delete(category)
    db.commit()
    return {"message": "Category deleted successfully"}
