from datetime import timedelta
from fastapi import APIRouter, Depends, HTTPException, status
from app.schemas.auth_schema import UserRegister, UserLogin, Token, TokenRefreshRequest, UserResponse
from app.repositories.user_repository import UserRepository
from app.models.user import User
from app.core.security import (
    get_password_hash, verify_password, create_access_token, create_refresh_token, get_current_user
)
from jose import jwt, JWTError
from app.core.config import settings

router = APIRouter(prefix="/auth", tags=["Authentication"])
user_repo = UserRepository()

@router.post("/register", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
async def register(user_data: UserRegister):
    existing_user = await user_repo.get_by_email(user_data.email)
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email address already registered"
        )
        
    hashed_pwd = get_password_hash(user_data.password)
    new_user = User(
        name=user_data.name,
        email=user_data.email,
        password=hashed_pwd,
        role=user_data.role,
        district=user_data.district,
        station=user_data.station
    )
    
    created = await user_repo.create(new_user)
    return created

@router.post("/login", response_model=Token)
async def login(credentials: UserLogin):
    user = await user_repo.get_by_email(credentials.email)
    if not user or not verify_password(credentials.password, user["password"]):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
        
    # Generate tokens
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    refresh_token_expires = timedelta(minutes=settings.REFRESH_TOKEN_EXPIRE_MINUTES)
    
    access_token = create_access_token(
        data={"sub": user["email"], "role": user["role"], "id": user["_id"]},
        expires_delta=access_token_expires
    )
    refresh_token = create_refresh_token(
        data={"sub": user["email"], "role": user["role"], "id": user["_id"]},
        expires_delta=refresh_token_expires
    )
    
    return {
        "access_token": access_token,
        "refresh_token": refresh_token,
        "token_type": "bearer"
    }

@router.post("/refresh", response_model=Token)
async def refresh_token(payload: TokenRefreshRequest):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate refresh token",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        decoded = jwt.decode(payload.refresh_token, settings.JWT_REFRESH_SECRET_KEY, algorithms=[settings.ALGORITHM])
        email: str = decoded.get("sub")
        role: str = decoded.get("role")
        user_id: str = decoded.get("id")
        token_type: str = decoded.get("type")
        
        if email is None or token_type != "refresh":
            raise credentials_exception
    except JWTError:
        raise credentials_exception
        
    # Generate new access and refresh token
    access_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    new_access_token = create_access_token(
        data={"sub": email, "role": role, "id": user_id},
        expires_delta=access_expires
    )
    
    return {
        "access_token": new_access_token,
        "refresh_token": payload.refresh_token,
        "token_type": "bearer"
    }

@router.get("/me", response_model=UserResponse)
async def get_current_profile(current_user: dict = Depends(get_current_user)):
    return current_user
