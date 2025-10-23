import jwt

from fastapi import APIRouter, Depends, HTTPException, status
from rich.console import detect_legacy_windows
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from fastapi.security import OAuth2PasswordRequestForm
from websockets.legacy.auth import Credentials

from app.models.users import User as UserModel
from app.schemas import UserCreate, User as UserSchema
from app.db_depends import get_async_db
from app.auth import create_refresh_token, hash_password, verify_password, create_access_token
from app.config import SECRET_KEY, ALGORITHM

 
router = APIRouter(prefix="/users", tags=["users"])


@router.post("/", response_model=UserSchema, status_code=status.HTTP_201_CREATED)
async def create_user(user: UserCreate, db: AsyncSession = Depends(get_async_db)):
    """
    Регистирует нового пользователя
    """
    # проверка уникальности емаил
    stmt_email = select(UserModel).where(
        UserModel.email == user.email
    )
    result_email = await db.execute(stmt_email)
    email = result_email.scalar()
    if email:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Email already registered"
        )
    
    #создание пользователя с хэшем
    db_user = UserModel(
        email=user.email,
        hashed_password=hash_password(user.password),
        role=user.role
    )

    db.add(db_user)
    await db.commit()
    return db_user


@router.post("/token")
async def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: AsyncSession = Depends(get_async_db)
    ):
    """
    Аутентифицирует пользователя и возвращает JWT
    """
    stmt_user = select(UserModel).where(UserModel.email == form_data.username)
    result_user = await db.execute(stmt_user)
    user = result_user.scalar()
    if user is None or not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"}
        )
    
    access_token = create_access_token(data={"sub": user.email, "role": user.role, "id": user.id})
    refresh_token = create_refresh_token(data={"sub": user.email, "role": user.role, "id": user.id})
    return {"access_token": access_token, "refresh_token": refresh_token, "token_type": "bearer"}


@router.post("/refresh-token")
async def refresh_token(refresh_token: str, db: AsyncSession = Depends(get_async_db)):
    """
    Обновляет аксес токен с помощью рефреш токена
    """
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate refresh token",
        headers={"WWW-Authenticate": "Bearer"}
    )
    try:
        payload = jwt.decode(refresh_token, SECRET_KEY, algorithms=[ALGORITHM])
        email: str = payload.get("sub")
        if email is None:
            raise credentials_exception
    except jwt.PyJWTError:
        raise credentials_exception
    
    stmt_user = select(UserModel).where(UserModel.email == email, UserModel.is_active == True)
    result_user = await db.execute(stmt_user)
    user = result_user.scalar_one_or_none()
    if user is None:
        raise credentials_exception
    access_token = create_access_token(data={"sub": user.email, "role": user.role, "id": user.id})
    return {"access_token": access_token, "token_type": "bearer"}