# from fastapi import FastAPI
# from app.database import engine, Base
# from app.routers import items

# # Creates the DB tables if they don't exist
# Base.metadata.create_all(bind=engine)

# app = FastAPI(title="Inventory Management API")

# app.include_router(items.router)


# @app.get("/")
# def read_root():
#     return {"message": "Inventory API is running"}


from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from app.database import engine, Base
from app.routers import items

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Inventory Management API")

app.include_router(items.router)


@app.get("/")
def read_root():
    return {"message": "Inventory API is running"}


@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    return JSONResponse(
        status_code=500,
        content={
            "detail": "An unexpected error occurred. Please try again later.",
            "error_type": type(exc).__name__
        }
    )