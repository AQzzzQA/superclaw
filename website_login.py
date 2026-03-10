#!/usr/env python3
"""
网站登录工具
支持多种登录方式，包括表单提交、模拟登录等
"""

import asyncio
import aiohttp
import logging
from typing import Dict, Any, Optional, List
from datetime import datetime
from urllib.parse import urljoin
import re
import json

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class WebsiteLogin:
    """网站登录工具"""
    
    def __init__(self):
        self.session = None
        self.user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    
    async def __aenter__(self):
        """异步上下文管理器入口"""
        headers = {
            "User-Agent": self.user_agent,
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
            "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8",
            "Accept-Encoding": "gzip, deflate, br",
            "Connection": "keep-alive"
        }
        self.session = aiohttp.ClientSession(headers=headers)
        return self
    
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """异步上下文管理器退出"""
        if self.session:
            await self.session.close()
    
    async def login_by_form(
        self,
        login_url: str,
        username: str,
        password: str,
        form_action: str = None,
        form_data: Optional[Dict[str, str]] = None
    ) -> Dict[str, Any]:
        """
        表单登录
        
        Args:
            login_url: 登录页面 URL
            username: 用户名
            password: 密码
            form_action: 表单 action URL
            form_data: 额外的表单数据
            
        Returns:
            登录结果
        """
        logger.info(f"开始表单登录: {login_url}")
        
        try:
            # 获取登录页面
            async with self.session.get(login_url, timeout=15) as response:
                if response.status != 200:
                    return {
                        "success": False,
                        "error": f"无法访问登录页面: HTTP {response.status}",
                        "status_code": response.status
                    }
                
                html = await response.text()
            
            # 解析登录表单
            form_data, form_action = self._parse_login_form(html, form_data, form_action)
            
            if not form_action:
                return {
                    "success": False,
                    "error": "未找到登录表单",
                    "form_fields": []
                }
            
            logger.info(f"找到表单 action: {form_action}")
            logger.info(f"表单数据: {form_data}")
            
            # 提交登录表单
            async with self.session.post(form_action, data=form_data, timeout=15) as response:
                if response.status == 200:
                    response_html = await response.text()
                    
                    # 检查登录是否成功
                    success = self._check_login_success(response_html)
                    
                    if success:
                        cookies = self._extract_cookies(response)
                        
                        return {
                            "success": True,
                            "message": "登录成功",
                            "cookies": cookies,
                            "response": f"HTTP {response.status}",
                            "cookies_dict": cookies
                        }
                    else:
                        return {
                            "success": False,
                            "error": "登录失败",
                            "response": f"HTTP {response.status}"
                        }
                else:
                    return {
                        "success": False,
                        "error": f"登录请求失败: HTTP {response.status}",
                        "status_code": response.status
                    }
                    
        except Exception as e:
            logger.error(f"表单登录异常: {e}")
            return {
                "success": False,
                "error": str(e)
            }
    
    async def login_by_api(
        self,
        login_url: str,
        api_key: str = None,
        username: str = None,
        password: str = None,
        headers: Optional[Dict[str, str]] = None
    ) -> Dict[str, Any]:
        """
        API 登录
        
        Args:
            login_url: 登录 API URL
            api_key: API 密钥
            username: 用户名
            password: 密码
            headers: 额外请求头
            
        Returns:
            登录结果
        """
        logger.info(f"开始 API 登录: {login_url}")
        
        try:
            # 准备请求头
            request_headers = {
                "User-Agent": self.user_agent,
                "Content-Type": "application/json",
                "Accept": "application/json"
            }
            
            if headers:
                request_headers.update(headers)
            
            # 准备请求数据
            auth_data = {}
            if api_key:
                auth_data["api_key"] = api_key
            if username:
                auth_data["username"] = username
            if password:
                auth_data["password"] = password
            
            # 发送登录请求
            async with self.session.post(login_url, json=auth_data, headers=request_headers, timeout=15) as response:
                if response.status == 200:
                    try:
                        data = await response.json()
                        
                        # 检查登录是否成功
                        if "token" in data or "access_token" in data:
                            return {
                                "success": True,
                                "message": "API 登录成功",
                                "data": data
                            }
                        elif "error" in data:
                            return {
                                "success": False,
                                "error": data.get("error", "登录失败"),
                                "code": data.get("code", 0)
                            }
                        else:
                            return {
                                "success": False,
                                "error": "未知响应格式",
                                "raw_data": data
                            }
                    except:
                        # 不是 JSON 响应
                        text = await response.text()
                        return {
                            "success": False,
                            "error": "响应解析失败",
                            "text": text[:200]
                        }
                else:
                    return {
                        "success": False,
                        "error": f"API 请求失败: HTTP {response.status}",
                        "status_code": response.status
                    }
                    
        except Exception as e:
            logger.error(f"API 登录异常: {e}")
            return {
                "success": False,
                "error": str(e)
            }
    
    async def check_login_status(self, check_url: str) -> Dict[str, Any]:
        """
        检查登录状态
        
        Args:
            check_url: 状态检查 URL
            
        Returns:
            状态检查结果
        """
        logger.info(f"检查登录状态: {check_url}")
        
        try:
            async with self.session.get(check_url, timeout=10) as response:
                if response.status == 200:
                    try:
                        data = await response.json()
                        return {
                            "success": True,
                            "logged_in": data.get("logged_in", False),
                            "user": data.get("user", None),
                            "data": data
                        }
                    except:
                        # 检查页面内容
                        text = await response.text()
                        logged_in = "登出" not in text and "登录" in text
                        return {
                            "success": True,
                            "logged_in": logged_in,
                            "user": "用户",
                            "text_preview": text[:200]
                        }
                else:
                    return {
                        "success": False,
                        "logged_in": False,
                        "error": f"检查失败: HTTP {response.status}"
                    }
        except Exception as e:
            logger.error(f"状态检查异常: {e}")
            return {
                "success": False,
                "error": str(e)
            }
    
    async def _parse_login_form(self, html: str, extra_data: Optional[Dict], form_action: str) -> tuple:
        """解析登录表单"""
        import bs4
        
        soup = bs4.BeautifulSoup(html, 'html.parser')
        
        # 查找登录表单
        forms = soup.find_all('form')
        if not forms:
            return {}, None
        
        login_form = forms[0]
        
        # 提取表单 action
        action = login_form.get('action', '')
        if not action and form_action:
            action = form_action
        
        if not action:
            return {}, None
        
        # 提取表单字段
        form_fields = {}
        
        for input_field in login_form.find_all('input'):
            name = input_field.get('name', '')
            input_type = input_field.get('type', 'text')
            value = input_field.get('value', '')
            required = input_field.get('required', '')
            
            # 跳过 hidden 字段
            if input_type == 'hidden':
                form_fields[name] = value
            elif name in ['username', 'email', 'user', 'phone', 'account']:
                if not value:
                    form_fields[name] = "test_user"
            elif name in ['password', 'pwd', 'pass']:
                form_fields[name] = "test_password"
        
        # 查找提交按钮
        for button in login_form.find_all('button'):
            btn_type = button.get('type', 'submit')
            btn_text = button.get_text(strip=True).lower()
            
            if btn_type == 'submit' or any(keyword in btn_text for keyword in ['登录', 'login', 'submit', '提交']):
                if 'name' in button.attrs:
                    form_fields[button['name']] = button.get('value', '登录')
                break
        
        logger.info(f"解析表单: action={action}, fields={list(form_fields.keys())}")
        
        return form_fields, action
    
    def _check_login_success(self, html: str) -> bool:
        """检查登录是否成功"""
        # 检查常见的成功标记
        success_indicators = [
            '欢迎',
            'welcome',
            '欢迎回来',
            '登录成功',
            '成功',
            'success',
            'dashboard',
            'index',
            '首页',
            '个人中心',
            '账户信息',
            'my account'
        ]
        
        html_lower = html.lower()
        for indicator in success_indicators:
            if indicator in html_lower:
                return True
        
        # 检查是否还在登录页面
        if any(keyword in html_lower for keyword in ['登录', 'login', '密码', 'password', '验证码']):
            # 登录页面特征
            login_form_count = html.count('<form')
            if login_form_count >= 1:
                return False
        
        return True
    
    def _extract_cookies(self, response: aiohttp.ClientResponse) -> Dict[str, str]:
        """提取 cookies"""
        cookies = {}
        
        for cookie_name, cookie_value in response.cookies.items():
            cookies[cookie_name] = str(cookie_value.value)
        
        return cookies
    
    async def crawl_after_login(
        self,
        start_url: str,
        max_pages: int = 5,
        follow_links: bool = True
    ) -> List[Dict[str, Any]]:
        """
        登录后抓取数据
        
        Args:
            start_url: 起始 URL
            max_pages: 最大页数
            follow_links: 是否跟踪链接
            
        Returns:
            抓取的数据
        """
        logger.info(f"开始登录后抓取: {start_url}")
        
        results = []
        visited_urls = set()
        
        try:
            # 递归抓取
            async def crawl(url: str, depth: int = 0):
                if depth >= max_pages or url in visited_urls:
                    return
                
                visited_urls.add(url)
                
                async with self.session.get(url, timeout=15) as response:
                    if response.status == 200:
                        html = await response.text()
                        
                        # 简单解析页面
                        result = {
                            "url": url,
                            "depth": depth,
                            "title": self._extract_title(html),
                            "content": html[:500] + "..." if len(html) > 500 else html
                        }
                        results.append(result)
                        
                        # 提取并跟踪链接
                        if follow_links and depth < max_pages:
                            links = self._extract_links(html)
                            for link in links[:3]:  # 限制每页 3 个链接
                                await crawl(link, depth + 1)
                    else:
                        logger.warning(f"访问失败: HTTP {response.status}")
        
            await crawl(start_url)
            
            logger.info(f"抓取完成: {len(results)} 个页面")
            return results
            
        except Exception as e:
            logger.error(f"抓取异常: {e}")
            return []
    
    def _extract_title(self, html: str) -> str:
        """提取页面标题"""
        try:
            import bs4
            soup = bs4.BeautifulSoup(html, 'html.parser')
            
            # 多种方式提取标题
            if soup.title:
                title = soup.title.get_text(strip=True)
                if title:
                    return title
        except:
            pass
        
        return "无标题"
    
    def _extract_links(self, html: str) -> List[str]:
        """提取页面链接"""
        try:
            import bs4
            soup = bs4.BeautifulSoup(html, 'html.parser')
            
            links = []
            for a in soup.find_all('a', href=True):
                href = a.get('href', '')
                if href and href.startswith('http'):
                    links.append(href)
            
            return links
        except:
            return []


# 全局实例
_login_service = None

def get_login_service() -> WebsiteLogin:
    """获取登录服务实例"""
    global _login_service
    
    if _login_service is None:
        _login_service = WebsiteLogin()
    
    return _login_service


async def login_website(
    login_url: str,
    method: str = "form",
    **kwargs
) -> Dict[str, Any]:
    """
    网站登录函数
    
    Args:
        login_url: 登录 URL
        method: 登录方法 (form/api)
        **kwargs: 登录参数
        
    Returns:
        登录结果
    """
    service = get_login_service()
    
    async with service:
        if method == "form":
            username = kwargs.get("username", "")
            password = kwargs.get("password", "")
            form_action = kwargs.get("form_action", None)
            form_data = kwargs.get("form_data", None)
            
            return await service.login_by_form(
                login_url, username, password,
                form_action, form_data
            )
        elif method == "api":
            api_key = kwargs.get("api_key", "")
            username = kwargs.get("username", "")
            password = kwargs.get("password", "")
            headers = kwargs.get("headers", None)
            
            return await service.login_by_api(
                login_url, api_key,
                username, password, headers
            )
        else:
            return {
                "success": False,
                "error": f"不支持的登录方法: {method}"
            }


async def check_login_status(check_url: str) -> Dict[str, Any]:
    """
    检查登录状态
    
    Args:
        check_url: 状态检查 URL
        
    Returns:
        状态检查结果
    """
    service = get_login_service()
    
    async with service:
        return await service.check_login_status(check_url)


async def crawl_after_login(
    start_url: str,
    max_pages: int = 5,
    follow_links: bool = True
) -> List[Dict[str, Any]]:
    """
    登录后抓取数据
    
    Args:
        start_url: 起始 URL
        max_pages: 最大页数
        follow_links: 是否跟踪链接
        
    Returns:
        抓取的数据
    """
    service = get_login_service()
    
    async with service:
        return await service.crawl_after_login(start_url, max_pages, follow_links)