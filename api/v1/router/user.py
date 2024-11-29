from typing import List

import fastapi

from controller.user import UserController
from schemas.user import UserOut, UserIn, UserUpdate

user_router = fastapi.APIRouter(prefix="/users")


@user_router.get("/", response_model=List[UserOut])
async def get_users():
    return UserController.get_users()


@user_router.get("/{user_id}", response_model=UserOut)
async def get_user(user_id: int):
    return UserController.get_user(user_id)


@user_router.post("/", response_model=UserOut)
async def create_user(user: UserIn):
    return UserController.create_user(user)


@user_router.put("/{user_id}", response_model=UserOut)
async def update_user(user_id: int, user: UserUpdate):
    return UserController.update_user(user_id, user)


@user_router.delete("/{user_id}", response_model=UserOut)
async def delete_user(user_id: int):
    return UserController.delete_user(user_id)
