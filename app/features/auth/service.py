from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from app.features.auth.models import User
from app.features.auth.schemas import UserRegister, UserLogin
from app.features.auth import security

def register_user(db: Session, user_data: UserRegister) -> User:
    # Check if username or email already exists
    existing_user = db.query(User).filter(
        (User.username == user_data.username) | (User.email == user_data.email)
    ).first()

    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Username or email already registered",
        )

    # Hash password and store record
    hashed_pwd = security.hash_password(user_data.password)
    new_user = User(
        username=user_data.username,
        email=user_data.email,
        password_hash=hashed_pwd,
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user


##Login
def authenticate_user(db: Session, login_data: UserLogin) -> str:
    user = db.query(User).filter(User.username == login_data.username).first()
    password = security.verify_password(login_data.password, user.password_hash)
    if not user or not password:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid username or password",
        )

    return security.create_access_token(data={"sub": str(user.id), "username": user.username})

