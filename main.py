from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
import crud, models, schemas
from database import SessionLocal, engine, get_db
from typing import List
from users import router as user_router
from auth import get_current_user

app = FastAPI()

app.include_router(user_router, prefix="/auth")

@app.post("/contacts/", response_model=schemas.ContactOut)
def create_contact(contact: schemas.ContactCreate, db: Session = Depends(get_db), current_user: models.User = Depends(get_current_user)):
    return crud.create_contact(db=db, contact=contact, owner_id=current_user.id)

@app.get("/contacts/", response_model=List[schemas.ContactOut])
def read_contacts(skip: int = 0, limit: int = 10, db: Session = Depends(get_db), current_user: models.User = Depends(get_current_user)):
    return crud.get_user_contacts(db, owner_id=current_user.id, skip=skip, limit=limit)

@app.get("/contacts/{contact_id}", response_model=schemas.ContactOut)
def read_contact(contact_id: int, db: Session = Depends(get_db), current_user: models.User = Depends(get_current_user)):
    db_contact = crud.get_contact(db, contact_id=contact_id, owner_id=current_user.id)
    if db_contact is None:
        raise HTTPException(status_code=404, detail="Contact not found")
    return db_contact
