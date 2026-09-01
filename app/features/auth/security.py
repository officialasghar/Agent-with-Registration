from pwdlib import PasswordHash
from app.settings import settings
from datetime import datetime, timedelta, timezone
import jwt

# Initialize modern password hashing
password_hash = PasswordHash.recommended()

##Register
def hash_password(password: str) -> str:
    return password_hash.hash(password)


##Login
def verify_password(plain_password: str, hashed_password: str) -> bool:
    return password_hash.verify(plain_password, hashed_password)

def create_access_token(data: dict) -> str:
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)


