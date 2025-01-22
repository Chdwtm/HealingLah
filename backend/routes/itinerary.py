from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from backend.config import SessionLocal
from backend.models import Itinerary

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.get("/")
def get_itineraries(db: Session = Depends(get_db)):
    return db.query(Itinerary).all()
