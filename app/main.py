from fastapi import FastAPI
from app.database import Base, engine
from app.features.auth.router import router as auth_router


# Auto-create tables in PostgreSQL on startup
Base.metadata.create_all(bind=engine)

app = FastAPI(title="Registration API")

app.include_router(auth_router)

@app.get("/")
def root():
    return {"message": "API is running"}