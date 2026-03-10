#!/usr/bin/env python3
"""网站登录工具 - 增强版"""
import aiohttp
import logging
from typing import Dict, List, Any
from datetime import datetime

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
        """自动处理验证的登录"""
        logger.info(f"开始验证登录: {method}")
        
        try:
            html = await self._fetch_page(login_url)
            if not html:
                return {"success": False, "error": "无法访问登录页面"}
            
            # 检测验证码类型
            if "验证码" in html or "captcha" in html.lower():
                logger.info("检测到验证码")
                
                # 处理验证码
                verification_result = await self._handle_verification(html, login_url, username, password, captcha_solution)
                
                if verification_result.get("success"):
                    logger.info("验证通过")
                else:
                    logger.warning(f"验证失败: {verification_result}")
                
                # 尝试登录
                login_result = await self._attempt_login(login_url, username, password)
                return login_result
            else:
                # 无验证码，直接登录
                logger.info("无验证码，直接登录")
                return await self._attempt_login(login_url, username, password)
                
        except Exception as e:
            logger.error(f"登录异常: {e}")
            return {"success": False, "error": str(e)}
    
    async def _fetch_page(self, url: str, timeout: int = 10) -> Optional[str]:
        """获取页面内容"""
        try:
            logger.info(f"获取页面: {url}")
            async with self.session.get(url, timeout=timeout) as response:
                if response.status == 200:
                    logger.info(f"获取成功: {len(response.content)} 字节")
                    return await response.text()
                else:
                    logger.error(f"获取失败: HTTP {response.status}")
                    return None
        except Exception as e:
            logger.error(f"获取页面异常: {e}")
            return None
    
    async def _attempt_login(
        self,
        login_url: str,
        username: str,
        password: str
    ) -> Dict[str, Any]:
        """尝试基础登录"""
        try:
            logger.info(f"尝试登录: {username}")
            
            html = await self._fetch_page(login_url)
            if not html:
                return {"success": False, "error": "无法访问登录页面"}
            
            # 解析登录表单
            soup = self._parse_login_form(html)
            if not soup:
                return {"success": False, "error": "无法解析登录表单"}
            
            # 提交登录表单
            form_data, form_action = soup
            
            if not form_action:
                return {"success": False, "error": "未找到表单提交地址"}
            
            logger.info(f"提交到: {form_action}")
            async with self.session.post(form_action, data=form_data, timeout=15) as response:
                if response.status == 200:
                    response_html = await response.text()
                    if self._check_login_success(response_html):
                        cookies = self._extract_cookies(await response)
                        logger.info("✅ 登录成功！")
                        return {
                            "success": True,
                            "message": "登录成功",
                            "cookies": cookies
                        }
                    else:
                        logger.warning("登录可能失败")
                        return {
                            "success": False,
                            "error": "登录可能失败"
                        }
                else:
                    return {
                        "success": False,
                        "error": f"登录请求失败: HTTP {response.status}"
                    }
                    
        except Exception as e:
            logger.error(f"登录异常: {e}")
            return {"success": False, "error": str(e)}
    
    def parse_login_form(self, html: str):
        """解析登录表单"""
        try:
            import bs4
            soup = bs4.BeautifulSoup(html, 'html.parser')
            
            # 查找表单
            forms = soup.find_all('form')
            if not forms:
                return None
            
            form = forms[0]
            action = form.get('action', '')
            if not action:
                return None, None
            
            # 查找表单字段
            form_data = {}
            
            for field in form.find_all(['input', 'select']):
                name = field.get('name', '')
                field_type = field.get('type', 'text')
                value = field.get('value', '')
                placeholder = field.get('placeholder', '')
                
                if field_type == 'hidden':
                    form_data[name] = value
                elif name in ['username', 'user', 'email', 'phone']:
                    if not value:
                        if name == 'username':
                            form_data[name] = "test_user"
                        else:
                            form_data[name] = ""
                elif name in ['password', 'pwd', 'pass']:
                    form_data[name] = value if value else "test_password"
                else:
                    form_data[name] = value if value else ""
            
            # 查找提交按钮
            for button in form.find_all(['button', 'input'][{"type": "submit"}]):
                if 'name' in button.attrs and 'value' in button.attrs:
                    form_data[button['name']] = button.attrs['value']
                    break
            
            logger.info(f"解析表单: action={action}, fields={list(form_data.keys())}")
            return form_data, action
            
        except Exception as e:
            logger.error(f"解析表单失败: {e}")
            return None, None
    
    def _check_login_success(self, html: str) -> bool:
        """检查登录是否成功"""
        html_lower = html.lower()
        return any(keyword in html_lower for keyword in ['欢迎', '欢迎', '登录成功', 'dashboard', '首页', '退出', '注销', 'logout'])
    
    def _extract_cookies(self, response):
        """提取cookies"""
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
        """处理验证码"""
        if captcha_solution == "manual":
            return {
                "success": False,
                "action": "need_manual_verification",
                "message": "需要人工验证",
                "html": html[:500]
            }
        
        if "验证码" not in html.lower():
            return {
                "success": True,
                "message": "未检测到验证码"
            }
        
        # 检测验证码类型
        if "图片" in html or "slider" in html.lower():
            return {
                "success": False,
                "action": "image_captcha",
                "message": "图片验证码",
                "html": html[:500]
            }
        elif "选择题" in html or "select" in html.lower():
            return {
                "success": False,
                "action": "select_captcha",
                "message": "选择题验证",
                "html": html[:500]
            }
        elif "滑块" in html or "slider" in html.lower():
            return {
                "success": False,
                "action": "slider_captcha",
                "message": "滑块验证码",
                "position": 0.5,
                "slide_count": 4,
                "html": html[:500]
            }
        else:
            return {
                "success": False,
                "action": "unknown_captcha",
                "message": "未知验证类型",
                "html": html[:500]
            }


def get_enhanced_login() -> EnhancedWebsiteLogin:
    """获取增强登录实例"""
    return EnhancedWebsiteLogin()


async def enhanced_login(
    login_url: str,
    username: str,
    password: str,
    captcha_solution: str = "manual"
) -> Dict[str, Any]:
    """
    增强网站登录
    
    Args:
        login_url: 登录 URL
        username: 用户名
        password: 密码
        captcha_solution: 验证解决方案
            
    Returns:
        登录结果
    """
    login_tool = get_enhanced_login()
    
    async with login_tool:
        return await login_tool.login_with_verification(
            login_url, username, password, captcha_solution
        )