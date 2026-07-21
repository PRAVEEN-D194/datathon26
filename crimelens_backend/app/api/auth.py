from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from datetime import timedelta
from app.models.schemas import UserCreate, Token, UserResponse
from app.db.repositories import UserRepository
from app.core.security import verify_password, hash_password, create_access_token, decode_token

router = APIRouter(prefix="/auth", tags=["Authentication"])
user_repo = UserRepository()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/auth/login")

async def get_current_user(token: str = Depends(oauth2_scheme)) -> dict:
    payload = decode_token(token)
    if not payload:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"}
        )
    user = await user_repo.get_user_by_username(payload.get("sub"))
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user

@router.post("/register", response_model=UserResponse)
async def register(user_data: UserCreate):
    existing = await user_repo.get_user_by_username(user_data.username)
    if existing:
        raise HTTPException(status_code=400, detail="Username already exists")
        
    hashed = hash_password(user_data.password)
    new_user = {
        "username": user_data.username,
        "hashed_password": hashed,
        "role": user_data.role
    }
    await user_repo.create_user(new_user)
    return new_user

@router.post("/login", response_model=Token)
async def login(user_data: UserCreate):
    user = await user_repo.get_user_by_username(user_data.username)
    if not user or not verify_password(user_data.password, user["hashed_password"]):
        raise HTTPException(status_code=400, detail="Incorrect username or password")
        
    token = create_access_token({"sub": user["username"]})
    return {"access_token": token, "token_type": "bearer", "role": user["role"]}
