"""
巨量引擎 API 客户端封装
处理签名、认证、通用请求逻辑
"""

import hashlib
import time
import json
from typing import Any, Dict, Optional
import httpx
from app.core.config import settings


class OceanAPIClient:
    """巨量引擎 API 客户端"""

    def __init__(
        self,
        app_id: str,
        app_secret: str,
        access_token: Optional[str] = None,
        base_url: str = settings.OCEAN_API_BASE,
    ):
        self.app_id = app_id
        self.app_secret = app_secret
        self.access_token = access_token
        self.base_url = base_url
        self._client: Optional[httpx.Client] = None

    @property
    def client(self) -> httpx.Client:
        if self._client is None:
            self._client = httpx.Client(timeout=30.0)
        return self._client

    def _generate_signature(self, params: Dict[str, Any]) -> str:
        """
        生成 API 签名
        文档：https://open.oceanengine.com/doc/index.html?key=ad&type=api&id=1699407169387169
        """
        # 按字典序排序参数
        sorted_params = sorted(params.items(), key=lambda x: x[0])
        # 拼接参数字符串
        param_str = "&".join([f"{k}={v}" for k, v in sorted_params if v is not None])
        # 拼接 app_secret
        sign_str = f"{param_str}&{self.app_secret}"
        # MD5 加密
        return hashlib.md5(sign_str.encode("utf-8")).hexdigest()

    def _prepare_params(
        self,
        path: str,
        method: str,
        params: Optional[Dict[str, Any]] = None,
        data: Optional[Dict[str, Any]] = None,
    ) -> Dict[str, Any]:
        """准备请求参数（添加公共参数和签名）"""
        timestamp = int(time.time())

        # 公共参数
        common_params = {
            "app_id": self.app_id,
            "timestamp": timestamp,
            "nonce": str(int(time.time() * 1000)),
        }

        if self.access_token:
            common_params["access_token"] = self.access_token

        # 合并参数
        final_params = {**(params or {}), **common_params}

        # 生成签名
        final_params["signature"] = self._generate_signature(final_params)

        return final_params

    def request(
        self,
        method: str,
        path: str,
        params: Optional[Dict[str, Any]] = None,
        data: Optional[Dict[str, Any]] = None,
        json_data: Optional[Dict[str, Any]] = None,
    ) -> Dict[str, Any]:
        """
        发送 API 请求

        Args:
            method: HTTP 方法 (GET, POST, PUT, DELETE)
            path: API 路径 (如 "/oauth2/access_token/")
            params: URL 查询参数
            data: 表单数据
            json_data: JSON 数据

        Returns:
            API 响应数据

        Raises:
            httpx.HTTPError: 请求失败
        """
        url = f"{self.base_url}{path}"

        # 准备请求参数
        if method.upper() in ("GET", "DELETE"):
            final_params = self._prepare_params(path, method, params=params)
            response = self.client.request(method, url, params=final_params)
        else:
            final_params = self._prepare_params(path, method, params=params)
            response = self.client.request(
                method,
                url,
                params=final_params,
                data=data,
                json=json_data,
            )

        # 解析响应
        response.raise_for_status()
        result = response.json()

        # 检查业务错误码
        if result.get("code") != 0:
            raise OceanAPIError(
                code=result.get("code"),
                message=result.get("message", "Unknown error"),
                request_id=result.get("request_id"),
            )

        return result.get("data", {})

    def get(self, path: str, params: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        return self.request("GET", path, params=params)

    def post(self, path: str, data: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        return self.request("POST", path, data=data)

    def post_json(
        self, path: str, json_data: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        return self.request("POST", path, json_data=json_data)

    def close(self):
        """关闭 HTTP 客户端"""
        if self._client:
            self._client.close()
            self._client = None


class OceanAPIError(Exception):
    """巨量引擎 API 错误"""

    def __init__(self, code: int, message: str, request_id: Optional[str] = None):
        self.code = code
        self.message = message
        self.request_id = request_id
        super().__init__(f"[{code}] {message}")


def get_ocean_client(access_token: Optional[str] = None) -> OceanAPIClient:
    """获取巨量 API 客户端实例"""
    return OceanAPIClient(
        app_id=settings.OCEAN_APP_ID,
        app_secret=settings.OCEAN_APP_SECRET,
        access_token=access_token,
    )
