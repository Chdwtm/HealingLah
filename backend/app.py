from fastapi import FastAPI
from backend.routes import itinerary, auth, booking

app = FastAPI(title="Travel Planner API")

# Register routes
app.include_router(itinerary.router, prefix="/api/itinerary", tags=["Itinerary"])
app.include_router(auth.router, prefix="/api/auth", tags=["Authentication"])
app.include_router(booking.router, prefix="/api/booking", tags=["Booking"])

@app.get("/")
def root():
    return {"message": "Welcome to Travel Planner API!"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app:app", host="0.0.0.0", port=8000, reload=True)
