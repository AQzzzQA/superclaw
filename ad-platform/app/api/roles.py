"""
角色权限管理 API
"""
from typing import List, Optional
from fastapi import APIRouter, Query
from pydantic import BaseModel
from app.core.response import APIResponse
from app.core.exceptions import BadRequestException, NotFoundException
import uuid

router = APIRouter()

# 模拟角色数据库
roles_db = [
    {
        "id": 1,
        "name": "admin",
        "description": "超级管理员",
        "permissions": ["*"],  # 所有权限
        "created_at": "2026-02-01T00:00:00",
    },
    {
        "id": 2,
        "name": "advertiser",
        "description": "广告主",
        "permissions": [
            "campaign:read",
            "campaign:write",
            "adgroup:read",
            "adgroup:write",
            "creative:read",
            "creative:write",
            "report:read",
        ],
        "created_at": "2026-02-01T00:00:00",
    },
    {
        "id": 3,
        "name": "viewer",
        "description": "查看者",
        "permissions": [
            "campaign:read",
            "report:read",
        ],
        "created_at": "2026-02-01T00:00:00",
    },
]

# 模拟用户角色关系
user_roles_db = [
    {"user_id": 1, "role_id": 1},  # admin -> admin
]


class RoleCreate(BaseModel):
    """创建角色请求"""
    name: str
    description: Optional[str] = None
    permissions: List[str]


class RoleUpdate(BaseModel):
    """更新角色请求"""
    name: Optional[str] = None
    description: Optional[str] = None
    permissions: Optional[List[str]] = None


@router.post("/roles")
async def create_role(req: RoleCreate):
    """创建角色"""
    # 检查角色名是否已存在
    if any(role["name"] == req.name for role in roles_db):
        raise BadRequestException("角色名已存在")

    # 创建角色
    role = {
        "id": len(roles_db) + 1,
        "name": req.name,
        "description": req.description,
        "permissions": req.permissions,
        "created_at": None,
    }

    roles_db.append(role)

    return APIResponse.success(
        data={
            "id": role["id"],
            "name": role["name"],
            "description": role["description"],
            "permissions": role["permissions"],
        },
        message="角色创建成功"
    )


@router.get("/roles")
async def list_roles(
    skip: int = Query(0, ge=0),
    limit: int = Query(10, ge=1, le=100),
):
    """获取角色列表"""
    roles = roles_db[skip : skip + limit]

    return APIResponse.success(
        data={
            "roles": roles,
            "total": len(roles_db),
            "skip": skip,
            "limit": limit,
        }
    )


@router.get("/roles/{role_id}")
async def get_role(role_id: int):
    """获取角色详情"""
    role = next((role for role in roles_db if role["id"] == role_id), None)

    if not role:
        raise NotFoundException("角色不存在")

    return APIResponse.success(data=role)


@router.put("/roles/{role_id}")
async def update_role(role_id: int, req: RoleUpdate):
    """更新角色"""
    role = next((role for role in roles_db if role["id"] == role_id), None)

    if not role:
        raise NotFoundException("角色不存在")

    # 不允许修改 admin 角色
    if role["name"] == "admin":
        raise BadRequestException("不能修改 admin 角色")

    # 更新角色
    if req.name is not None:
        role["name"] = req.name

    if req.description is not None:
        role["description"] = req.description

    if req.permissions is not None:
        role["permissions"] = req.permissions

    return APIResponse.success(
        data={
            "id": role["id"],
            "name": role["name"],
            "description": role["description"],
            "permissions": role["permissions"],
        },
        message="角色更新成功"
    )


@router.delete("/roles/{role_id}")
async def delete_role(role_id: int):
    """删除角色"""
    role = next((role for role in roles_db if role["id"] == role_id), None)

    if not role:
        raise NotFoundException("角色不存在")

    # 不允许删除 admin 角色
    if role["name"] == "admin":
        raise BadRequestException("不能删除 admin 角色")

    # 检查是否有用户使用该角色
    if any(ur["role_id"] == role_id for ur in user_roles_db):
        raise BadRequestException("有用户使用该角色，不能删除")

    roles_db.remove(role)

    return APIResponse.success(message="角色删除成功")


@router.post("/users/{user_id}/roles")
async def assign_role(user_id: int, role_id: int):
    """为用户分配角色"""
    # 检查用户是否存在
    from app.api.users import users_db
    user = next((user for user in users_db if user["id"] == user_id), None)
    if not user:
        raise NotFoundException("用户不存在")

    # 检查角色是否存在
    role = next((role for role in roles_db if role["id"] == role_id), None)
    if not role:
        raise NotFoundException("角色不存在")

    # 删除用户现有角色
    user_roles_db[:] = [ur for ur in user_roles_db if ur["user_id"] != user_id]

    # 分配新角色
    user_roles_db.append({"user_id": user_id, "role_id": role_id})

    return APIResponse.success(message="角色分配成功")


@router.delete("/users/{user_id}/roles")
async def remove_role(user_id: int):
    """移除用户角色"""
    # 检查用户是否存在
    from app.api.users import users_db
    user = next((user for user in users_db if user["id"] == user_id), None)
    if not user:
        raise NotFoundException("用户不存在")

    # 不允许移除超级管理员的角色
    if user["is_superuser"]:
        raise BadRequestException("不能移除超级管理员的角色")

    # 移除用户角色
    user_roles_db[:] = [ur for ur in user_roles_db if ur["user_id"] != user_id]

    return APIResponse.success(message="角色移除成功")
