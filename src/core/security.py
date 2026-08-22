from datetime import datetime, timedelta, timezone

import jwt
from passlib.context import CryptContext
from pydantic import BaseModel, ValidationError

from fastapi import HTTPException, status

from src.core.config import settings

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class TokenDetail(BaseModel):
    user_id: str
    exp: datetime


def hash_password(password: str) -> str:
    """Parolni hash qilish."""
    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Parolni tekshirish."""
    return pwd_context.verify(plain_password, hashed_password)


def create_access_token(user_id: str) -> str:
    """JWT token yaratish."""
    exp = datetime.now().replace(tzinfo=timezone.utc) + timedelta(
        minutes=settings.ACCESS_TOKEN_TIMELIMIT
    )

    payload = {"user_id": user_id, "exp": exp}
    token = jwt.encode(payload, settings.ACCESS_TOKEN_SECRET_KEY, algorithm="HS256")
    return token


def decode_access_token(token: str) -> dict:
    """JWT tokenni dekodlash."""
    try:
        payload = jwt.decode(token, settings.ACCESS_TOKEN_SECRET_KEY, algorithms=["HS256"])
        return payload
    except jwt.DecodeError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token noto'g'ri",
        )


def verify_access_token(token: str) -> str:
    try:
        paylod = decode_access_token(token)
        paylod = TokenDetail.model_validate(paylod)

        if paylod.exp < datetime.now().replace(tzinfo=timezone.utc):
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="muddati o'tgan")
        return paylod.user_id
    except ValidationError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="token payload error.")
    except Exception as exc:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=f"{exc}")
