"""
API Gateway - 统一的第三方 API 集成技能
"""

import requests
import json
import time
from typing import Dict, Any, Optional, List
from pathlib import Path
import logging

logger = logging.getLogger(__name__)


class APIGateway:
    """API Gateway 主类"""

    def __init__(self, config_file: Optional[str] = None):
        """初始化 API Gateway"""
        self.config = {}
        self.cache = {}
        self.session = requests.Session()

        # 加载配置
        if config_file:
            self.load_config(config_file)

        # 设置默认超时
        self.timeout = 30
        self.retry_count = 3

    def load_config(self, config_file: str):
        """加载配置文件"""
        try:
            with open(config_file, 'r') as f:
                self.config = json.load(f)
            logger.info(f"配置已加载: {config_file}")
        except Exception as e:
            logger.error(f"配置加载失败: {e}")
            raise Exception(f"配置加载失败: {str(e)}")

    def add_service(self, service_name: str) -> 'ServiceClient':
        """添加服务"""
        if service_name not in self.config.get('services', {}):
            logger.warning(f"服务未配置: {service_name}")
            # 返回默认客户端
            return ServiceClient(service_name, session=self.session)

        config = self.config['services'][service_name]
        return ServiceClient(
            service_name,
            base_url=config.get('base_url', ''),
            api_key=config.get('api_key', ''),
            session=self.session,
            timeout=config.get('timeout', self.timeout),
            retry=config.get('retry', self.retry_count)
        )

    def list_services(self) -> List[str]:
        """列出所有配置的服务"""
        return list(self.config.get('services', {}).keys())


class ServiceClient:
    """服务客户端"""

    def __init__(
        self,
        service_name: str,
        base_url: str = '',
        api_key: str = '',
        session: Optional[requests.Session] = None,
        timeout: int = 30,
        retry: int = 3
    ):
        """初始化服务客户端"""
        self.service_name = service_name
        self.base_url = base_url
        self.api_key = api_key
        self.session = session or requests.Session()
        self.timeout = timeout
        self.retry = retry

        # 设置默认 headers
        self.session.headers.update({
            'Content-Type': 'application/json',
            'User-Agent': f'API-Gateway/1.0.0 ({service_name})'
        })

        # 如果有 API key，添加到 headers
        if api_key:
            self.session.headers.update({
                'Authorization': f'Bearer {api_key}'
            })

    def _request(
        self,
        method: str,
        endpoint: str,
        data: Optional[Dict[str, Any]] = None,
        params: Optional[Dict[str, Any]] = None,
        files: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """发送请求（带重试）"""
        url = f"{self.base_url}{endpoint}" if self.base_url else endpoint

        for attempt in range(self.retry):
            try:
                if method == 'GET':
                    response = self.session.get(
                        url,
                        params=params,
                        timeout=self.timeout
                    )
                elif method == 'POST':
                    response = self.session.post(
                        url,
                        json=data,
                        params=params,
                        files=files,
                        timeout=self.timeout
                    )
                elif method == 'PUT':
                    response = self.session.put(
                        url,
                        json=data,
                        params=params,
                        timeout=self.timeout
                    )
                elif method == 'DELETE':
                    response = self.session.delete(
                        url,
                        params=params,
                        timeout=self.timeout
                    )
                else:
                    raise ValueError(f"不支持的 HTTP 方法: {method}")

                # 检查响应状态
                response.raise_for_status()

                # 解析 JSON 响应
                result = response.json()
                logger.info(f"{self.service_name}: {method} {endpoint} - 成功")
                return result

            except requests.exceptions.Timeout as e:
                logger.warning(f"{self.service_name}: 请求超时 (尝试 {attempt + 1}/{self.retry})")
                if attempt == self.retry - 1:
                    raise Exception(f"请求超时: {str(e)}")
                time.sleep(2 ** attempt)  # 指数退避

            except requests.exceptions.RequestException as e:
                logger.error(f"{self.service_name}: 请求失败 - {e}")
                if attempt == self.retry - 1:
                    raise Exception(f"请求失败: {str(e)}")
                time.sleep(2 ** attempt)

    def get(self, endpoint: str, params: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """GET 请求"""
        return self._request('GET', endpoint, params=params)

    def post(self, endpoint: str, data: Optional[Dict[str, Any]] = None, params: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """POST 请求"""
        return self._request('POST', endpoint, data=data, params=params)

    def put(self, endpoint: str, data: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """PUT 请求"""
        return self._request('PUT', endpoint, data=data)

    def delete(self, endpoint: str) -> Dict[str, Any]:
        """DELETE 请求"""
        return self._request('DELETE', endpoint)


# 导出主要类
__all__ = ['APIGateway', 'ServiceClient']
