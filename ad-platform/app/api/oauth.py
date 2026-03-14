"""
OAuth2 认证相关 API
"""

from fastapi import APIRouter, HTTPException, Query
from typing import Optional
from app.services.ocean import OAuthService, get_ocean_client
from app.core.config import settings

router = APIRouter(prefix="/oauth", tags=["OAuth2"])


@router.get("/authorize")
def get_authorization_url(redirect_uri: Optional[str] = None, state: str = ""):
    """
    获取巨量引擎授权 URL

    Query Parameters:
        redirect_uri: 回调地址（可选，默认使用配置中的值）
        state: 状态参数（可选）

    Returns:
        {
            "authorize_url": "https://ad.oceanengine.com/openapi/oauth2/...",
            "state": "..."
        }
    """
    client = get_ocean_client()
    oauth_service = OAuthService(client)

    final_redirect_uri = redirect_uri or settings.OCEAN_REDIRECT_URI

    authorize_url = oauth_service.get_authorization_url(
        redirect_uri=final_redirect_uri, state=state
    )

    return {
        "authorize_url": authorize_url,
        "redirect_uri": final_redirect_uri,
        "state": state,
    }


@router.post("/callback")
def oauth_callback(
    auth_code: str = Query(..., description="授权码"), state: Optional[str] = None
):
    """
    OAuth2 回调处理，用授权码换取 access_token

    Query Parameters:
        auth_code: 授权码
        state: 状态参数（可选）

    Returns:
        {
            "access_token": "...",
            "refresh_token": "...",
            "expires_in": 86400,
            "advertiser_ids": ["xxx", "yyy"]
        }
    """
    try:
        client = get_ocean_client()
        oauth_service = OAuthService(client)

        token_data = oauth_service.get_access_token(auth_code)

        return {
            "access_token": token_data["access_token"],
            "refresh_token": token_data["refresh_token"],
            "expires_in": token_data["expires_in"],
            "advertiser_ids": token_data["advertiser_ids"],
            "state": state,
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/refresh")
def refresh_access_token(refresh_token: str):
    """
    刷新 access_token

    Body:
        {
            "refresh_token": "..."
        }

    Returns:
        {
            "access_token": "...",
            "refresh_token": "...",
            "expires_in": 86400
        }
    """
    try:
        client = get_ocean_client()
        oauth_service = OAuthService(client)

        token_data = oauth_service.refresh_access_token(refresh_token)

        return {
            "access_token": token_data["access_token"],
            "refresh_token": token_data["refresh_token"],
            "expires_in": token_data["expires_in"],
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
