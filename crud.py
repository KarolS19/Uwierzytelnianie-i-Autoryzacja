def get_user_contacts(db: Session, owner_id: int, skip: int = 0, limit: int = 10):
    return db.query(Contact).filter(Contact.owner_id == owner_id).offset(skip).limit(limit).all()

def get_contact(db: Session, contact_id: int, owner_id: int):
    return db
