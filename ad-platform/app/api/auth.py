"""
用户认证 API
"""
from fastapi import APIRouter, HTTPException, Depends, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.orm import Session
from pydantic import BaseModel, Field
from datetime import timedelta
from app.core.database import get_db
from app.core.security import verify_password, get_password_hash, create_access_token, decode_access_token
from app.core.config import settings
from app.models.user import User

router = APIRouter(prefix="/auth", tags=["Auth"])
security = HTTPBearer()


# ========== 数据模型 ==========

class LoginRequest(BaseModel):
    """登录请求"""
    username: str = Field(..., description="用户名")
    password: str = Field(..., description="密码")


class LoginResponse(BaseModel):
    """登录响应"""
    access_token: str = Field(..., description="访问令牌")
    token_type: str = "bearer"


class RegisterRequest(BaseModel):
    """注册请求"""
    tenant_id: int = Field(..., description="租户 ID")
    username: str = Field(..., description="用户名")
    password: str = Field(..., description="密码")
    email: str = Field(None, description="邮箱")


# ========== 依赖项 ==========

def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: Session = Depends(get_db)
) -> User:
    """获取当前用户"""
    token = credentials.credentials
    payload = decode_access_token(token)

    if payload is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="无效的认证凭据"
        )

    user_id = payload.get("sub")
    if user_id is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="无效的认证凭据"
        )

    user = db.query(User).filter(User.id == user_id).first()
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="用户不存在"
        )

    return user


# ========== 路由 ==========

@router.post("/login", response_model=LoginResponse)
def login(request: LoginRequest, db: Session = Depends(get_db)):
    """
    用户登录
    """
    # 查询用户
    user = db.query(User).filter(User.username == request.username).first()

    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="用户名或密码错误"
        )

    # 验证密码
    if not verify_password(request.password, user.password_hash):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="用户名或密码错误"
        )

    # 检查状态
    if user.status != 1:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="账户已被禁用"
        )

    # 生成 Token
    access_token = create_access_token(
        data={"sub": str(user.id), "tenant_id": user.tenant_id}
    )

    return {"access_token": access_token, "token_type": "bearer"}


@router.post("/register")
def register(request: RegisterRequest, db: Session = Depends(get_db)):
    """
    用户注册
    """
    # 检查用户名是否已存在
    existing_user = db.query(User).filter(User.username == request.username).first()
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="用户名已存在"
        )

    # 创建用户
    user = User(
        tenant_id=request.tenant_id,
        username=request.username,
        password_hash=get_password_hash(request.password),
        email=request.email,
    )
    db.add(user)
    db.commit()
    db.refresh(user)

    return {"code": 0, "message": "注册成功", "data": {"user_id": user.id}}


@router.get("/me")
def get_me(current_user: User = Depends(get_current_user)):
    """
    获取当前用户信息
    """
    return {
        "code": 0,
        "message": "success",
        "data": {
            "id": current_user.id,
            "tenant_id": current_user.tenant_id,
            "username": current_user.username,
            "email": current_user.email,
            "phone": current_user.phone,
            "is_admin": current_user.is_admin,
        }
    }
