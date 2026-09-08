import jwt
from typing import Optional
from fastapi import Depends, HTTPException, Request, status
from sqlalchemy.orm import Session

from app.config import settings
from app.database import get_db
from app.features.auth.models import User


def get_current_user(
    request: Request, 
    db: Session = Depends(get_db)
) -> User:
    """
    Extracts the 'Authorization: Bearer <token>' header from incoming requests,
    decodes the JWT using PyJWT, handles token expiration, and retrieves 
    the authenticated User from the database.
    """
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials"
    )

    # 1. Read header directly from request
    authorization: Optional[str] = request.headers.get("Authorization")

    # 2. Ensure header exists and starts with 'Bearer '
    if not authorization or not authorization.startswith("Bearer "):
        raise credentials_exception

    # 3. Extract the raw token string
    token = authorization.split(" ")[1]

    # 4. Decode and verify the JWT payload
    try:
        payload = jwt.decode(
            token, 
            settings.SECRET_KEY, 
            algorithms=[settings.ALGORITHM]
        )
        user_id_str: Optional[str] = payload.get("sub")
        if user_id_str is None:
            raise credentials_exception
            
        user_id = int(user_id_str)

    except jwt.ExpiredSignatureError:
        # Raised when current time passes the 'exp' timestamp
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token has expired. Please log in again."
        )
    except (jwt.PyJWTError, ValueError):
        # Raised for invalid signatures, malformed tokens, or bad type conversions
        raise credentials_exception

    # 5. Retrieve the active user from the database
    user = db.query(User).filter(User.id == user_id).first()
    if user is None:
        raise credentials_exception

    return user