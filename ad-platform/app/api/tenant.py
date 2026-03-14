"""
租户管理 API
"""

from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from typing import Optional
from pydantic import BaseModel, Field
from app.core.database import get_db
from app.models.tenant import Tenant

router = APIRouter(prefix="/tenant", tags=["Tenant"])


# ========== 数据模型 ==========


class TenantCreateRequest(BaseModel):
    """创建租户请求"""

    name: str = Field(..., description="租户名称")
    status: int = Field(1, description="状态：0-禁用，1-启用")


class TenantUpdateRequest(BaseModel):
    """更新租户请求"""

    name: Optional[str] = Field(None, description="租户名称")
    status: Optional[int] = Field(None, description="状态")


# ========== 路由 ==========


@router.post("/create")
def create_tenant(request: TenantCreateRequest, db: Session = Depends(get_db)):
    """
    创建租户
    """
    # 检查名称是否已存在
    existing_tenant = db.query(Tenant).filter(Tenant.name == request.name).first()
    if existing_tenant:
        raise HTTPException(status_code=400, detail="租户名称已存在")

    tenant = Tenant(
        name=request.name,
        status=request.status,
    )
    db.add(tenant)
    db.commit()
    db.refresh(tenant)

    return {
        "code": 0,
        "message": "创建成功",
        "data": {
            "id": tenant.id,
            "name": tenant.name,
            "status": tenant.status,
        },
    }


@router.get("/list")
def get_tenant_list(db: Session = Depends(get_db)):
    """
    获取租户列表
    """
    tenants = db.query(Tenant).all()

    return {
        "code": 0,
        "message": "success",
        "data": [
            {
                "id": t.id,
                "name": t.name,
                "status": t.status,
                "created_at": t.created_at.isoformat(),
            }
            for t in tenants
        ],
    }


@router.get("/{tenant_id}")
def get_tenant(tenant_id: int, db: Session = Depends(get_db)):
    """
    获取租户详情
    """
    tenant = db.query(Tenant).filter(Tenant.id == tenant_id).first()
    if not tenant:
        raise HTTPException(status_code=404, detail="租户不存在")

    return {
        "code": 0,
        "message": "success",
        "data": {
            "id": tenant.id,
            "name": tenant.name,
            "status": tenant.status,
            "created_at": tenant.created_at.isoformat(),
        },
    }


@router.post("/{tenant_id}/update")
def update_tenant(
    tenant_id: int, request: TenantUpdateRequest, db: Session = Depends(get_db)
):
    """
    更新租户
    """
    tenant = db.query(Tenant).filter(Tenant.id == tenant_id).first()
    if not tenant:
        raise HTTPException(status_code=404, detail="租户不存在")

    if request.name:
        tenant.name = request.name
    if request.status is not None:
        tenant.status = request.status

    db.commit()

    return {"code": 0, "message": "更新成功", "data": {"id": tenant.id}}


@router.post("/{tenant_id}/delete")
def delete_tenant(tenant_id: int, db: Session = Depends(get_db)):
    """
    删除租户
    """
    tenant = db.query(Tenant).filter(Tenant.id == tenant_id).first()
    if not tenant:
        raise HTTPException(status_code=404, detail="租户不存在")

    db.delete(tenant)
    db.commit()

    return {"code": 0, "message": "删除成功", "data": {"id": tenant_id}}
