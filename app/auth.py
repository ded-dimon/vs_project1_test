from passlib.context import CryptContext
from fastapi.security import OAuth2PasswordBearer
from datetime import datetime, timedelta, timezone
import jwt
from fastapi import Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.models.users import User as UserModel
from app.config import SECRET_KEY, ALGORITHM
from app.db_depends import get_async_db


# Создаём контекст для хеширования
pwd_context = CryptContext(
    schemes=["argon2"],
    deprecated="auto"
)

ACCESS_TOKEN_EXPIRE_MINUTES = 30
REFRESH_TOKEN_EXPIRE_DAYS = 7
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="users/token")


def hash_password(password: str):
    """
    Преобразует пароль в хэш
    """
    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str):
    """
    Проверяет соответсвует ли введенный пароль сохраненному хэшу
    """
    return pwd_context.verify(plain_password, hashed_password)


def create_access_token(data: dict):
    """
    Создает JWT с нагрузкой
    """
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)


def create_refresh_token(data: dict):
    """
    Создает рефреш-токен
    """
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + timedelta(days=REFRESH_TOKEN_EXPIRE_DAYS)
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)


async def get_current_user(token: str = Depends(oauth2_scheme), db: AsyncSession = Depends(get_async_db)):
    """
    Проверяет пользователя и возвращает его
    """
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"}
    )

    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email: str = payload.get("sub")
        if email is None:
            raise credentials_exception
    except jwt.ExpiredSignatureError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token has expired",
            headers={"WWW-Authenticate": "Bearer"},
        )
    except jwt.PyJWKSetError:
        raise credentials_exception
    
    stmt_user = select(UserModel).where(
        UserModel.email == email,
        UserModel.is_active == True
        )
    result_user = await db.execute(stmt_user)
    user = result_user.scalar()
    if user is None:
        raise credentials_exception
    
    return user


async def get_current_seller(current_user: UserModel = Depends(get_current_user)):
    """
    Проверяет что пользователь имеет роль seller
    """
    if current_user.role != "seller":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only sellers can perform this action"
        )
    
    return current_user

async def get_current_buyer(current_user: UserModel = Depends(get_current_user)):
    """
    Проверяет что пользователь покупатель
    """
    if current_user.role != "buyer":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only buyers can perform this action"
        )

    return current_user
    
async def get_current_admin(current_user: UserModel = Depends(get_current_user)):
    """
    Проверяет что пользователь админ
    """
    if current_user.role != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only admins can perform this action"
        )