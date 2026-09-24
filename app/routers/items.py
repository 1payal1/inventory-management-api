from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List,Optional

from app.database import SessionLocal
from app import models, schemas
from app.auth import get_current_user

router = APIRouter(
    prefix="/items",
    tags=["Items"]
)


# Dependency to get DB session per request
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.post("/", response_model=schemas.ItemResponse)
def create_item(item: schemas.ItemCreate, db: Session = Depends(get_db),current_user: models.User = Depends(get_current_user)):
    db_item = models.Item(**item.dict())
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item


# @router.get("/", response_model=List[schemas.ItemResponse])
# def get_items(db: Session = Depends(get_db)):
#     return db.query(models.Item).all()

@router.get("/", response_model=List[schemas.ItemResponse])
def get_items(
    skip: int = 0,
    limit: int = 10,
    search: Optional[str] = None,
    db: Session = Depends(get_db)
):
    query = db.query(models.Item)

    if search:
        query = query.filter(models.Item.name.ilike(f"%{search}%"))

    return query.offset(skip).limit(limit).all()

@router.get("/{item_id}", response_model=schemas.ItemResponse)
def get_item(item_id: int, db: Session = Depends(get_db)):
    item = db.query(models.Item).filter(models.Item.id == item_id).first()
    if not item:
        raise HTTPException(status_code=404, detail="Item not found")
    return item


@router.put("/{item_id}", response_model=schemas.ItemResponse)
def update_item(item_id: int, updated: schemas.ItemUpdate, db: Session = Depends(get_db),current_user: models.User = Depends(get_current_user)):
    item = db.query(models.Item).filter(models.Item.id == item_id).first()
    if not item:
        raise HTTPException(status_code=404, detail="Item not found")
    for key, value in updated.dict().items():
        setattr(item, key, value)
    db.commit()
    db.refresh(item)
    return item


@router.delete("/{item_id}")
def delete_item(item_id: int, db: Session = Depends(get_db),current_user: models.User = Depends(get_current_user)):
    item = db.query(models.Item).filter(models.Item.id == item_id).first()
    if not item:
        raise HTTPException(status_code=404, detail="Item not found")
    db.delete(item)
    db.commit()
    return {"message": "Item deleted successfully"}