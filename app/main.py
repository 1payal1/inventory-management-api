from fastapi import FastAPI
from app.database import engine, Base
from app.routers import items

# Creates the DB tables if they don't exist
Base.metadata.create_all(bind=engine)

app = FastAPI(title="Inventory Management API")

app.include_router(items.router)


@app.get("/")
def read_root():
    return {"message": "Inventory API is running"}