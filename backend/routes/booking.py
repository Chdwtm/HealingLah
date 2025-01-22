from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from backend.config import SessionLocal
from backend.models import User, Itinerary

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/")
def create_booking(user_id: int, itinerary_id: int, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == user_id).first()
    itinerary = db.query(Itinerary).filter(Itinerary.id == itinerary_id).first()

    if not user or not itinerary:
        return {"error": "Invalid user or itinerary"}
    return {"message": f"Booking confirmed for {user.name} to {itinerary.destination}"}
