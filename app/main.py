from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.database import Base, engine
from app.features.auth.router import router as auth_router
from app.features.agent.routers import router as chat_router
from app.features.chat_management.router import router as new_chat_router


# Auto-create tables in PostgreSQL on startup
Base.metadata.create_all(bind=engine)

app = FastAPI(title="Registration API")

# Allow the frontend (served from a different origin) to call this API
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],          # tighten this to your actual frontend origin later, e.g. ["http://127.0.0.1:5500"]
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth_router)
app.include_router(chat_router)
app.include_router(new_chat_router)


@app.get("/")
def root():
    return {"message": "API is running"}