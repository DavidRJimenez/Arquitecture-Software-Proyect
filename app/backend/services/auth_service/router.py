from fastapi import APIRouter
from fastapi import status as response_status
from utils.schemas import TokenData
from fastapi import Body, Depends, HTTPException
from database import get_db
from sqlalchemy.orm import Session
from utils.login_logic import base_login
from services.auth_service.schemas import UserLogin
from services.auth_service.schemas import CreateUserBase, RetrieveUserBase
from models import User
from services.auth_service.functions import create_user
from utils.RoleChecker import RoleChecker
from utils.get_current_user import get_current_user
from utils.jwt_handler import create_access_token

router = APIRouter(prefix="/auth", tags=["Authentication"])
admin_only = RoleChecker(allowed_roles=["admin"])


@router.post("/login", status_code=response_status.HTTP_200_OK, response_model=TokenData)
async def login(data: UserLogin = Body(...), db: Session = Depends(get_db)):
    try:
        user_data = base_login(db, data)
    except HTTPException as e:
        if e.status_code == response_status.HTTP_404_NOT_FOUND:
            raise HTTPException(
                status_code=response_status.HTTP_404_NOT_FOUND,
                detail="User not found",
            )
        elif e.status_code == response_status.HTTP_401_UNAUTHORIZED:
            raise HTTPException(
                status_code=response_status.HTTP_401_UNAUTHORIZED,
                detail="Invalid credentials",
            )
    access_token = create_access_token(data=user_data.model_dump())
    return {
        "access_token": access_token,
        "token_type": "bearer",
    }


@router.post("/admin/login", status_code=response_status.HTTP_200_OK)
async def admin_login(data: UserLogin = Body(...), db: Session = Depends(get_db)):
    try:
        user_data = base_login(db, data)
    except HTTPException as e:
        if e.status_code == response_status.HTTP_404_NOT_FOUND:
            raise HTTPException(
                status_code=response_status.HTTP_404_NOT_FOUND,
                detail="User not found",
            )
        elif e.status_code == response_status.HTTP_401_UNAUTHORIZED:
            raise HTTPException(
                status_code=response_status.HTTP_401_UNAUTHORIZED,
                detail="Invalid credentials",
            )
    if user_data.role not in ["admin"]:
        raise HTTPException(
            status_code=response_status.HTTP_403_FORBIDDEN,
            detail="You are not authorized to access this resource",
        )
    access_token = create_access_token(data=user_data.model_dump())
    return {
        "access_token": access_token,
        "token_type": "bearer",
    }


@router.post("/signup", response_model=RetrieveUserBase, status_code=response_status.HTTP_201_CREATED)
async def signup_user(user: CreateUserBase = Body(...), db: Session = Depends(get_db)) -> RetrieveUserBase:
    """
    Create a new user in the database.
    """
    user_data = User(**user.model_dump(exclude_unset=True))
    user_data.password = hash.get_password_hash(user.password)

    try:
        if db.query(User).filter(User.email == user_data.email).first():
            raise HTTPException(status_code=response_status.HTTP_400_BAD_REQUEST, detail="Email already registered")

        user_data = create_user(user_data, db)
        return user_data

    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=response_status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))


@router.delete("/delete/{user_id}", status_code=response_status.HTTP_204_NO_CONTENT)
async def delete_user(user_id: int, db: Session = Depends(get_db), current_user: TokenData = Depends(get_current_user)):
    """
    Delete a user by ID.
    """
    user = db.query(User).filter(User.user_id == user_id).first()
    if not user:
        raise HTTPException(status_code=response_status.HTTP_404_NOT_FOUND, detail="User not found")

    db.delete(user)
    db.commit()
    return {"detail": "User deleted successfully"}


# TODO IMPLEMENT GET USERS AND UPDATE USER ENDPOINTS