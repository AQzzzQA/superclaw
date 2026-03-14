"""
巨量引擎 OAuth2 认证服务
处理授权链接生成、access_token 获取、刷新
"""

from typing import Dict, Any
from app.services.ocean.client import OceanAPIClient, OceanAPIError


class OAuthService:
    """OAuth2 认证服务"""

    AUTH_URL = "https://ad.oceanengine.com/openapi/oauth2/index.html"
    ACCESS_TOKEN_URL = "/oauth2/access_token/"
    REFRESH_TOKEN_URL = "/oauth2/refresh_token/"

    def __init__(self, client: OceanAPIClient):
        self.client = client

    def get_authorization_url(self, redirect_uri: str, state: str = "") -> str:
        """
        生成授权链接

        Args:
            redirect_uri: 回调地址
            state: 状态参数（可选）

        Returns:
            授权 URL
        """
        params = {
            "app_id": self.client.app_id,
            "redirect_uri": redirect_uri,
            "state": state,
        }
        query = "&".join([f"{k}={v}" for k, v in params.items() if v])
        return f"{self.AUTH_URL}?{query}"

    def get_access_token(self, auth_code: str) -> Dict[str, Any]:
        """
        通过授权码获取 access_token

        Args:
            auth_code: 授权码

        Returns:
            包含 access_token, refresh_token, expires_in 等的字典
        """
        data = {
            "app_id": self.client.app_id,
            "secret": self.client.app_secret,
            "auth_code": auth_code,
        }

        try:
            result = self.client.post(self.ACCESS_TOKEN_URL, data=data)
            return {
                "access_token": result.get("access_token"),
                "refresh_token": result.get("refresh_token"),
                "expires_in": result.get("expires_in"),
                "advertiser_ids": result.get("advertiser_ids", []),
            }
        except OceanAPIError as e:
            raise ValueError(f"获取 access_token 失败: {e}")

    def refresh_access_token(self, refresh_token: str) -> Dict[str, Any]:
        """
        刷新 access_token

        Args:
            refresh_token: 刷新令牌

        Returns:
            包含新的 access_token, refresh_token 的字典
        """
        data = {
            "app_id": self.client.app_id,
            "secret": self.client.app_secret,
            "grant_type": "refresh_token",
            "refresh_token": refresh_token,
        }

        try:
            result = self.client.post(self.REFRESH_TOKEN_URL, data=data)
            return {
                "access_token": result.get("access_token"),
                "refresh_token": result.get("refresh_token"),
                "expires_in": result.get("expires_in"),
            }
        except OceanAPIError as e:
            raise ValueError(f"刷新 access_token 失败: {e}")
