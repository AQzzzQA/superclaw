"""
用户管理 API
"""
from typing import List, Optional
from fastapi import APIRouter, Query
from pydantic import BaseModel, EmailStr
from app.core.response import APIResponse
from app.core.exceptions import BadRequestException, NotFoundException
from passlib.context import CryptContext
import uuid

router = APIRouter()

# 密码加密
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# 模拟用户数据库
users_db = [
    {
        "id": 1,
        "username": "admin",
        "email": "admin@example.com",
        "full_name": "管理员",
        "is_active": True,
        "is_superuser": True,
        "created_at": "2026-02-01T00:00:00",
    }
]


class UserCreate(BaseModel):
    """创建用户请求"""
    username: str
    email: EmailStr
    password: str
    full_name: Optional[str] = None
    is_superuser: bool = False


class UserUpdate(BaseModel):
    """更新用户请求"""
    email: Optional[EmailStr] = None
    full_name: Optional[str] = None
    password: Optional[str] = None
    is_active: Optional[bool] = None


@router.post("/users")
async def create_user(req: UserCreate):
    """创建用户"""
    # 检查用户名是否已存在
    if any(user["username"] == req.username for user in users_db):
        raise BadRequestException("用户名已存在")

    # 检查邮箱是否已存在
    if any(user["email"] == req.email for user in users_db):
        raise BadRequestException("邮箱已存在")

    # 加密密码
    hashed_password = pwd_context.hash(req.password)

    # 创建用户
    user = {
        "id": len(users_db) + 1,
        "username": req.username,
        "email": req.email,
        "full_name": req.full_name,
        "is_active": True,
        "is_superuser": req.is_superuser,
        "hashed_password": hashed_password,
        "created_at": None,
    }

    users_db.append(user)

    return APIResponse.success(
        data={
            "id": user["id"],
            "username": user["username"],
            "email": user["email"],
            "full_name": user["full_name"],
            "is_active": user["is_active"],
            "is_superuser": user["is_superuser"],
        },
        message="用户创建成功"
    )


@router.get("/users")
async def list_users(
    skip: int = Query(0, ge=0),
    limit: int = Query(10, ge=1, le=100),
    active_only: Optional[bool] = None,
):
    """获取用户列表"""
    users = users_db

    # 过滤活跃用户
    if active_only is not None:
        users = [user for user in users if user["is_active"] == active_only]

    # 分页
    users = users[skip : skip + limit]

    return APIResponse.success(
        data={
            "users": users,
            "total": len(users_db),
            "skip": skip,
            "limit": limit,
        }
    )


@router.get("/users/{user_id}")
async def get_user(user_id: int):
    """获取用户详情"""
    user = next((user for user in users_db if user["id"] == user_id), None)

    if not user:
        raise NotFoundException("用户不存在")

    return APIResponse.success(
        data={
            "id": user["id"],
            "username": user["username"],
            "email": user["email"],
            "full_name": user["full_name"],
            "is_active": user["is_active"],
            "is_superuser": user["is_superuser"],
            "created_at": user["created_at"],
        }
    )


@router.put("/users/{user_id}")
async def update_user(user_id: int, req: UserUpdate):
    """更新用户"""
    user = next((user for user in users_db if user["id"] == user_id), None)

    if not user:
        raise NotFoundException("用户不存在")

    # 更新用户信息
    if req.email is not None:
        user["email"] = req.email

    if req.full_name is not None:
        user["full_name"] = req.full_name

    if req.password is not None:
        user["hashed_password"] = pwd_context.hash(req.password)

    if req.is_active is not None:
        user["is_active"] = req.is_active

    return APIResponse.success(
        data={
            "id": user["id"],
            "username": user["username"],
            "email": user["email"],
            "full_name": user["full_name"],
            "is_active": user["is_active"],
            "is_superuser": user["is_superuser"],
        },
        message="用户更新成功"
    )


@router.delete("/users/{user_id}")
async def delete_user(user_id: int):
    """删除用户"""
    user = next((user for user in users_db if user["id"] == user_id), None)

    if not user:
        raise NotFoundException("用户不存在")

    # 不允许删除超级管理员
    if user["is_superuser"]:
        raise BadRequestException("不能删除超级管理员")

    users_db.remove(user)

    return APIResponse.success(message="用户删除成功")
