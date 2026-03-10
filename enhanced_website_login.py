#!/usr/bin/env python3
"""
网站登录工具 - 增强版
支持多种验证方式处理
"""

import asyncio
import aiohttp
import logging
from typing import Dict, List, Any, Optional
from datetime import datetime
from urllib.parse import urljoin
import random
from bs4 import BeautifulSoup

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class EnhancedWebsiteLogin:
    """增强的网站登录工具"""
    
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
    
    async def login_with_verification(
        self,
        login_url: str,
        username: str,
        password: str,
        method: str = "auto",
        captcha_solution: str = "manual"
    ) -> Dict[str, Any]:
        """
        自动处理验证的登录
        
        Args:
            login_url: 登录 URL
            username: 用户名
            password: 密码
            method: 登录方式 (auto/manual)
            captcha_solution: 验证解决方案 (manual/session/bypass)
            
        Returns:
            登录结果
        """
        logger.info(f"开始自动验证登录: {method}, 验证方案: {captcha_solution}")
        
        try:
            # 获取登录页面
            html = await self._fetch_page(login_url)
            if not html:
                return {"success": False, "error": "无法访问登录页面"}
            
            # 尝试自动登录
            login_result = await self._attempt_login(login_url, username, password)
            
            # 如果登录失败，检查是否需要验证
            if not login_result["success"]:
                logger.info("登录失败，检查验证需求...")
                return await self._handle_verification(html, login_url, username, password, captcha_solution)
            
            return login_result
            
        except Exception as e:
            logger.error(f"自动登录失败: {e}")
            return {
                "success": False,
                "error": str(e)
            }
    
    async def _attempt_login(
        self,
        login_url: str,
        username: str,
        password: str
    ) -> Dict[str, Any]:
        """
        尝试基础登录
        
        Returns:
            登录结果
        """
        logger.info("尝试基础登录...")
        
        try:
            # 解析登录表单
            html = await self._fetch_page(login_url)
            if not html:
                return {"success": False, "error": "无法获取登录页面"}
            
            form_data, action = self._parse_login_form(html)
            
            if not form_data:
                return {"success": False, "error": "未找到登录表单"}
            
            # 提交登录表单
            logger.info(f"提交登录表单: {action}")
            async with self.session.post(action, data=form_data, timeout=15) as response:
                if response.status == 200:
                    if self._check_login_success(await response.text()):
                        cookies = self._extract_cookies(response)
                        logger.info("登录成功!")
                        return {
                            "success": True,
                            "message": "登录成功",
                            "cookies": cookies
                        }
                    else:
                        return {
                            "success": False,
                            "error": "登录失败"
                        }
                else:
                    return {
                        "success": False,
                        "error": f"登录请求失败: HTTP {response.status}"
                    }
                    
        except Exception as e:
            logger.error(f"登录异常: {e}")
            return {
                "success": False,
                "error": str(e)
            }
    
    async def _fetch_page(self, url: str) -> Optional[str]:
        """获取页面内容"""
        try:
            async with self.session.get(url, timeout=10) as response:
                if response.status == 200:
                    return await response.text()
                else:
                    logger.error(f"获取页面失败: HTTP {response.status}")
                    return None
        except Exception as e:
            logger.error(f"获取页面异常: {e}")
            return None
    
    def _parse_login_form(self, html: str) -> Dict[str, Any]:
        """解析登录表单"""
        soup = BeautifulSoup(html, 'html.parser')
        
        forms = soup.find_all('form')
        if not forms:
            return {}, None
        
        login_form = forms[0]
        action = login_form.get('action', '')
        
        # 解析表单字段
        form_data = {}
        for field in login_form.find_all(['input', 'select']):
            name = field.get('name', '')
            input_type = field.get('type', 'text')
            value = field.get('value', '')
            
            if input_type == 'text':
                if name and not value:
                    form_data[name] = value
            elif input_type == 'password':
                form_data[name] = password if name == 'password' else 'your_password'
        
        return form_data, action
    
    def _check_login_success(self, html: str) -> bool:
        """检查登录是否成功"""
        soup = BeautifulSoup(html, 'html.parser')
        text = soup.get_text()
        
        # 检查登录成功的标记
        success_indicators = ['欢迎', '欢迎回来', '登录成功', 'dashboard', '首页', '个人中心', 'my account']
        
        text_lower = text.lower()
        return any(indicator in text_lower for indicator in success_indicators)
    
    def _extract_cookies(self, response: aiohttp.ClientResponse) -> Dict[str, str]:
        """提取 cookies"""
        cookies = {}
        for cookie in response.cookies:
            cookies[cookie.key] = cookie.value
        return cookies
    
    async def _handle_verification(
        self,
        html: str,
        login_url: str,
        username: str,
        password: str,
        captcha_solution: str
    ) -> Dict[str, Any]:
        """
        处理验证码
        
        Args:
            html: 页面 HTML
            login_url: 登录 URL
            username: 用户名
            password: 密码
            captcha_solution: 验证解决方案
            
        Returns:
            处理结果
        """
        logger.info(f"处理验证: {captcha_solution}")
        
        if captcha_solution == "manual":
            return {
                "success": False,
                "action": "need_manual_verification",
                "message": "需要人工验证",
                "verification_type": "manual",
                "html": html[:500]
            }
        
        elif captcha_solution == "bypass":
            # 尝试绕过验证
            logger.info("尝试绕过验证...")
            return await self._try_bypass(login_url, username, password)
        
        elif captcha_solution == "session":
            # 使用之前的会话
            logger.info("使用保存的会话...")
            return {
                "success": False,
                "action": "need_saved_session",
                "message": "需要使用保存的会话",
                "html": html[:500]
            }
        
        else:
            # 自动识别验证类型
            captcha_type = self._identify_captcha_type(html)
            
            if captcha_type == "image":
                return {
                    "success": False,
                    "action": "image_captcha",
                    "message": "图片验证码",
                    "html": html[:500]
                }
            elif captcha_type == "slider":
                return {
                    "success": False,
                    "action": "slider_captcha",
                    "message": "滑块验证码",
                    "slider_position": 0.5,
                    "slide_count": 4,
                    "html": html[:500]
                }
            elif captcha_type == "select":
                return {
                    "success": False,
                    "action": "select_captcha",
                    "message": "选择题验证码",
                    "choices": [],
                    "html": html[:500]
                }
            else:
                return {
                    "success": False,
                    "action": "unknown_captcha",
                    "message": "未知验证类型",
                    "html": html[:500]
                }
    
    def _identify_captcha_type(self, html: str) -> str:
        """识别验证码类型"""
        soup = BeautifulSoup(html, 'html.parser')
        text = soup.get_text().lower()
        
        # 检查各种验证码特征
        if '验证码' in text or 'captcha' in text:
            if '图片' in text or 'image' in text:
                return "image"
            elif '滑块' in text or 'slider' in text:
                return "slider"
            elif '选择' in text or 'select' in text or '题目' in text:
                return "select"
            elif '输入' in text or 'input框' in text:
                return "input"
        
        return "unknown"
    
    async def _try_bypass(
        self,
        login_url: str,
        username: str,
        password: str
    ) -> Dict[str, Any]:
        """尝试绕过验证"""
        logger.info("尝试绕过验证...")
        
        try:
            # 模拟提交空表单
            html = await self._fetch_page(login_url)
            if not html:
                return {"success": False, "error": "无法获取登录页面"}
            
            # 查找绕过选项
            soup = BeautifulSoup(html, 'html.parser')
            bypass_options = soup.find_all('a')
            
            for option in bypass_options:
                href = option.get('href', '')
                text = option.get_text(strip=True)
                
                if '跳过' in text or 'bypass' in text or '验证码' in text:
                    logger.info(f"找到绕过选项: {text}")
                    
                    # 尝试点击绕过
                    if href:
                        logger.info(f"点击绕过: {href}")
                        response = await self.session.get(href, timeout=10)
                        if response.status == 200:
                            result_html = await response.text()
                            if self._check_login_success(result_html):
                                cookies = self._extract_cookies(await response)
                                return {
                                    "success": True,
                                    "message": "绕过验证成功",
                                    "cookies": cookies
                                }
            return {
                "success": False,
                "error": "验证码处理失败"
            }
                    
        except Exception as e:
            logger.error(f"绕过验证失败: {e}")
            return {
                "success": False,
                "error": str(e)
            }
    
    async def collect_data_after_login(
        self,
        data_url: str,
        max_pages: int = 5
    ) -> List[Dict[str, Any]]:
        """
        登录后收集数据
        
        Args:
            data_url: 数据 URL
            max_pages: 最大页数
            
        Returns:
            收集的数据
        """
        logger.info(f"开始收集数据: {data_url}")
        
        results = []
        
        for page in range(1, max_pages + 1):
            url = f"{data_url}?page={page}"
            html = await self._fetch_page(url)
            
            if html:
                soup = BeautifulSoup(html, 'html.parser')
                
                # 提取数据
                data = {
                    "page": page,
                    "url": url,
                    "title": soup.title.string.strip() if soup.title else "",
                    "content": soup.body.get_text(separator='\n', strip=True)[:500]
                }
                
                results.append(data)
                logger.info(f"收集数据: {page}/{max_pages}")
        
        return results


# 全局实例
_enhanced_login = None

def get_enhanced_login() -> EnhancedWebsiteLogin:
    """获取增强登录实例"""
    global _enhanced_login
    
    if _enhanced_login is None:
        _enhanced_login = EnhancedWebsiteLogin()
    
    return _enhanced_login


async def auto_login_with_verification(
    login_url: str,
    username: str,
    password: str,
    captcha_solution: str = "manual"
) -> Dict[str, Any]:
    """
    自动登录并处理验证
    
    Args:
        login_url: 登录 URL
        username: 用户名
        password: 密码
        captcha_solution: 验证解决方案
            
    Returns:
        登录结果
    """
    service = get_enhanced_login()
    
    async with service:
        return await service.login_with_verification(
            login_url, username, password, "auto", captcha_solution
        )


async def manual_login(
    login_url: str,
    username: str,
    password: str
) -> Dict[str, Any]:
    """
    手动登录（表单提交）
    
    Args:
        login_url: URL
        username: 用户名
        password: 密码
            
        Returns:
        登录结果
    """
    service = get_enhanced_login()
    
    async with service:
        return await service.login_with_verification(
            login_url, username, password, "manual", "manual"
        )


async def collect_data(
    data_url: str,
    max_pages: int = 5
) -> List[Dict[str, Any]]:
    """
    登录后收集数据
    
    Args:
        data_url: 数据 URL
        max_pages: 最大页数
        
    Returns:
        收集的数据
    """
    service = get_enhanced_login()
    
    async with service:
        return await service.collect_data_after_login(data_url, max_pages)


def get_login_status(check_url: str) -> Dict[str, Any]:
    """
    获取登录状态
    
    Args:
        check_url: 状态检查 URL
        
    Returns:
        登录状态
    """
    return {
        "checked": False,
        "status": "unknown",
        "message": "状态检查"
    }