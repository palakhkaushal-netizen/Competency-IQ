from uuid import UUID

import jwt
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from sqlalchemy.orm import Session

from .config import settings
from .db import get_db
from .models import User

bearer = HTTPBearer(auto_error=False)


def get_current_user(credentials: HTTPAuthorizationCredentials | None = Depends(bearer), db: Session = Depends(get_db)) -> User:
    if credentials is None or not settings.supabase_jwt_secret:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Authentication is required")
    try:
        claims = jwt.decode(credentials.credentials, settings.supabase_jwt_secret, algorithms=["HS256"], audience="authenticated")
        user_id = UUID(str(claims["sub"]))
    except (KeyError, ValueError, jwt.PyJWTError) as error:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid access token") from error
    user = db.get(User, user_id)
    if user is None or not user.role:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Application profile not found")
    return user


def require_student(user: User = Depends(get_current_user)) -> User:
    if user.role != "STUDENT":
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Student access required")
    return user


def require_government_admin(user: User = Depends(get_current_user)) -> User:
    if user.role != "GOVERNMENT_ADMIN":
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Government administrator access required")
    return user
