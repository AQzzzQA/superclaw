"""
巨量账户管理 API
"""

from fastapi import APIRouter, HTTPException, Depends, Query
from sqlalchemy.orm import Session
from typing import Optional, List
from pydantic import BaseModel, Field
from datetime import datetime
from app.core.database import get_db
from app.api.auth import get_current_user
from app.models.user import User
from app.models.ocean_account import OceanAccount
from app.models.tenant import Tenant

router = APIRouter(prefix="/account", tags=["Account"])


# ========== 数据模型 ==========


class AccountCreateRequest(BaseModel):
    """创建账户请求"""

    advertiser_id: str = Field(..., description="广告主 ID")
    advertiser_name: str = Field(..., description="广告主名称")
    access_token: str = Field(..., description="访问令牌")
    refresh_token: str = Field(..., description="刷新令牌")
    expires_at: str = Field(..., description="过期时间（ISO 8601）")


class AccountUpdateRequest(BaseModel):
    """更新账户请求"""

    access_token: Optional[str] = Field(None, description="访问令牌")
    refresh_token: Optional[str] = Field(None, description="刷新令牌")
    expires_at: Optional[str] = Field(None, description="过期时间")
    status: Optional[int] = Field(None, description="状态")


class AccountResponse(BaseModel):
    """账户响应"""

    id: int
    tenant_id: int
    advertiser_id: str
    advertiser_name: str
    status: int
    expires_at: datetime
    created_at: datetime

    class Config:
        from_attributes = True


# ========== 路由 ==========


@router.post("/create", response_model=dict)
def create_account(
    request: AccountCreateRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """
    创建巨量账户
    """
    # 检查账户是否已存在
    existing_account = (
        db.query(OceanAccount)
        .filter(OceanAccount.advertiser_id == request.advertiser_id)
        .first()
    )

    if existing_account:
        raise HTTPException(status_code=400, detail="该广告主账户已存在")

    # 创建账户
    account = OceanAccount(
        tenant_id=current_user.tenant_id,
        advertiser_id=request.advertiser_id,
        advertiser_name=request.advertiser_name,
        access_token=request.access_token,
        refresh_token=request.refresh_token,
        expires_at=datetime.fromisoformat(request.expires_at),
    )

    db.add(account)
    db.commit()
    db.refresh(account)

    return {
        "code": 0,
        "message": "创建成功",
        "data": {
            "id": account.id,
            "advertiser_id": account.advertiser_id,
        },
    }


@router.get("/list", response_model=dict)
def get_account_list(
    current_user: User = Depends(get_current_user), db: Session = Depends(get_db)
):
    """
    获取账户列表
    """
    accounts = (
        db.query(OceanAccount)
        .filter(OceanAccount.tenant_id == current_user.tenant_id)
        .all()
    )

    return {
        "code": 0,
        "message": "success",
        "data": [
            {
                "id": acc.id,
                "advertiser_id": acc.advertiser_id,
                "advertiser_name": acc.advertiser_name,
                "status": acc.status,
                "expires_at": acc.expires_at.isoformat() if acc.expires_at else None,
                "created_at": acc.created_at.isoformat(),
            }
            for acc in accounts
        ],
    }


@router.get("/{account_id}", response_model=dict)
def get_account(
    account_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """
    获取账户详情
    """
    account = (
        db.query(OceanAccount)
        .filter(
            OceanAccount.id == account_id,
            OceanAccount.tenant_id == current_user.tenant_id,
        )
        .first()
    )

    if not account:
        raise HTTPException(status_code=404, detail="账户不存在")

    return {
        "code": 0,
        "message": "success",
        "data": {
            "id": account.id,
            "advertiser_id": account.advertiser_id,
            "advertiser_name": account.advertiser_name,
            "status": account.status,
            "expires_at": (
                account.expires_at.isoformat() if account.expires_at else None
            ),
            "created_at": account.created_at.isoformat(),
        },
    }


@router.post("/{account_id}/update", response_model=dict)
def update_account(
    account_id: int,
    request: AccountUpdateRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """
    更新账户
    """
    account = (
        db.query(OceanAccount)
        .filter(
            OceanAccount.id == account_id,
            OceanAccount.tenant_id == current_user.tenant_id,
        )
        .first()
    )

    if not account:
        raise HTTPException(status_code=404, detail="账户不存在")

    if request.access_token:
        account.access_token = request.access_token
    if request.refresh_token:
        account.refresh_token = request.refresh_token
    if request.expires_at:
        account.expires_at = datetime.fromisoformat(request.expires_at)
    if request.status is not None:
        account.status = request.status

    db.commit()

    return {"code": 0, "message": "更新成功", "data": {"id": account.id}}


@router.post("/{account_id}/delete", response_model=dict)
def delete_account(
    account_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """
    删除账户
    """
    account = (
        db.query(OceanAccount)
        .filter(
            OceanAccount.id == account_id,
            OceanAccount.tenant_id == current_user.tenant_id,
        )
        .first()
    )

    if not account:
        raise HTTPException(status_code=404, detail="账户不存在")

    db.delete(account)
    db.commit()

    return {"code": 0, "message": "删除成功", "data": {"id": account_id}}
