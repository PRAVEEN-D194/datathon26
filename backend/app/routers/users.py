from fastapi import APIRouter, Depends, HTTPException, status
from typing import List
from app.schemas.auth_schema import UserResponse
from app.repositories.user_repository import UserRepository
from app.core.security import RoleChecker, get_current_user
from app.core.logging import logger

router = APIRouter(prefix="/users", tags=["Users"])
user_repo = UserRepository()

# Only Admin can list users
@router.get("/", response_model=List[UserResponse])
async def get_all_users(current_user: dict = Depends(RoleChecker(["admin"]))):
    logger.info(f"Admin {current_user['email']} requested listing of all users")
    return await user_repo.list_all()

@router.get("/{user_id}", response_model=UserResponse)
async def get_user(user_id: str, current_user: dict = Depends(get_current_user)):
    # Officers and Analysts can only view their own profile, Admins can view all
    if current_user["role"] != "admin" and current_user["_id"] != user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Permission denied to view this profile"
        )
    user = await user_repo.get_by_id(user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user

@router.put("/{user_id}", response_model=UserResponse)
async def update_user(user_id: str, update_data: dict, current_user: dict = Depends(get_current_user)):
    # Prevent regular users from updating role or email
    if current_user["role"] != "admin":
        if current_user["_id"] != user_id:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Permission denied")
        # Remove critical keys from data to prevent spoofing
        update_data.pop("role", None)
        update_data.pop("email", None)
        update_data.pop("password", None)

    updated = await user_repo.update(user_id, update_data)
    if not updated:
        raise HTTPException(status_code=404, detail="User not found or update failed")
    return updated

@router.delete("/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_user(user_id: str, current_user: dict = Depends(RoleChecker(["admin"]))):
    success = await user_repo.delete(user_id)
    if not success:
        raise HTTPException(status_code=404, detail="User not found")
    return None
