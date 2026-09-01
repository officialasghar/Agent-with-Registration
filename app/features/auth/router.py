from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from app.database import get_db
from app.features.auth import schemas, service

router = APIRouter(prefix="/auth", tags=["Auth"])

##Signup
@router.post("/register", response_model=schemas.UserResponse, status_code=status.HTTP_201_CREATED)
def register(user_data: schemas.UserRegister, db: Session = Depends(get_db)):
    return service.register_user(db, user_data)

##Login
@router.post("/login", response_model=schemas.TokenResponse)
def login(login_data: schemas.UserLogin, db: Session = Depends(get_db)):
    access_token = service.authenticate_user(db, login_data)
    return {"access_token": access_token, "token_type": "bearer"}