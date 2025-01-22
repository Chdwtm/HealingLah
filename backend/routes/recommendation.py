from fastapi import APIRouter
from backend.recommendation import recommend

router = APIRouter()

@router.get("/")
def get_recommendation(destination: str, category: str = None):
    recommendations = recommend(destination, category)
    return recommendations
