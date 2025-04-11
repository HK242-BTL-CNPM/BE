from fastapi import APIRouter,Query, Depends, HTTPException, status
from sqlmodel import Session
from app.schemas.admin import getUser
from app.schemas.user import User_Short
from app.schemas.metadata import Metadata
from app.schemas.admin import getUser,changeUserStatus
from app.schemas.metadata import Metadata
from app.schemas.room import Branch_In, Buiding_In, TypeRoom_In, RoomIn, RoomDevice, reponse

from app.crud.crud_user import get_all_user,change_user_status
from typing import List
from app.api.dependencies import SessionDep
from app.model import Room, Branch, Building, RoomType
from app.crud.crud_room import create_branch, get_branch, update_branch, delete_branch, get_all_branches
from app.crud.crud_room import create_building, get_building, update_building, delete_building, get_buildings_by_branch
from app.crud.crud_room import create_room_type, get_room_type, delete_room_type
from app.crud.crud_room import create_room, get_room, update_room, delete_room, delete_room_device,filter_rooms
from app.crud.crud_room import create_room_device, get_room_device, update_room_device, delete_room_device
#from app.crud.crud_room import create_branch, create_building, create_room_type, create_room, 

router = APIRouter()

# router.include_router(
#     router=APIRouter(),
#     dependencies=Depends(isAdmin),
# )


@router.get("/all_user", response_model=getUser)
def get_all_user_data(
    session: SessionDep,
    page: int = Query(default=1, ge=1, description="Page number (starting from 1)"),  # Thêm query param page
    limit: int = Query(default=10, ge=1, le=100, description="Number of users per page")  # Thêm limit nếu cần
):
    '''
    Get all users (username, MSSV, lastname, firstname, email, isActive) with pagination.

    Args:
        page: Page number to retrieve (default: 1).
        limit: Number of users per page (default: 10, max: 100).
    '''
    # Tạo metadata với page và limit
    metadata = Metadata(page=page, perpage=limit)

    # Gọi hàm CRUD để lấy danh sách user và metadata
    users, metadata = get_all_user(session, metadata)
    if not users:
        raise HTTPException(status_code=404, detail="No user found")

    # Chuyển đổi danh sách user sang User_Short
    users_out: List[User_Short] = [
        User_Short(
            username=user.username,
            MSSV=user.MSSV,
            lastname=user.lastname,
            firstname=user.firstname,
            email=user.email,
            isActive=user.isActive
        )
        for user in users
    ]

    # Trả về response với cấu trúc mong muốn
    return {
        "msg": "Get users successfully",
        "data": users_out,
        "metadata": metadata
    }


@router.put("/change_user_status/{username}", response_model=changeUserStatus)
def admin_change_user_status(username: str, isActive: bool, session: SessionDep):
    '''
    Change user status (isActive)
    
    '''
    user= change_user_status(session, username, isActive)
    if not user:
        raise HTTPException(status_code=404, detail="Have something wrong")
    return{
        "msg": "Change user status successfully",
        "data": User_Short(
            username=user.username,
            MSSV=user.MSSV,
            lastname=user.lastname,
            firstname=user.firstname,
            email=user.email,
            isActive=user.isActive
        )
    }




# --- Branch ---
@router.post("/branch", response_model=reponse)
def create_branch_data(data: Branch_In, session: SessionDep):
    '''
    Create a new branch.

    Args:
        data: Branch data to create.
    '''
    branch = create_branch(session, Branch_name= data.Branch_name)
    if not branch:
        raise HTTPException(status_code=400, detail="Branch already exists")
    return {
        "msg": "Create branch successfully",
        "data": branch
    }
@router.get("/all_branch", response_model=reponse)
def get_all_branch_data(session: SessionDep):
    '''
    Get all branches.

    '''
    branches = get_all_branches(session)
    if not branches:
        raise HTTPException(status_code=404, detail="No branch found")
    return {
        "msg": "Get all branches successfully",
        "data": branches
    }





# --- Building ---







# --- RoomType ---







# --- Room ---







# --- RoomDevice ---