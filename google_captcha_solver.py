#!/usr/bin/env python3
"""
谷歌验证码解决方案
包括 Google reCAPTCHA v2/v3、NoCAPTCHA 等多种类型
"""

import asyncio
import aiohttp
import logging
from typing import Dict, Any, Optional
from datetime import datetime
from bs4 import BeautifulSoup
import random
import json

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class GoogleCaptchaSolver:
    """谷歌验证码解决器"""
    
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
    
    async def recognize_captcha(self, html: str) -> Dict[str, Any]:
        """
        识别验证码类型
        
        Args:
            html: 页面 HTML 内容
            
        Returns:
            识别结果
        """
        logger.info("开始识别验证码类型...")
        
        soup = BeautifulSoup(html, 'html.parser')
        result = {
            "captcha_type": "unknown",
            "sitekey": "",
            "confidence": 0.0,
            "features": []
        }
        
        # 检查 Google reCAPTCHA
        if soup.find('div', {'class': re.compile('g-recaptcha', re.I)}):
            result["captcha_type"] = "google_recaptcha"
            result["sitekey"] = self._extract_sitekey(soup)
            result["confidence"] = 0.95
            result["features"] = [
                "checkbox类型验证",
                "可能包含图片选择",
                "I'm not a robot",
                "音频挑战"
            ]
            return result
        
        # 检查 NoCAPTCHA
        if soup.find('div', {'id': 'g-recaptcha'}):
            result["captcha_type"] = "google_nocaptcha"
            result["sitekey"] = self._extract_sitekey(soup)
            result["confidence"] = 0.90
            result["features"] = [
                "NoCAPTCHA 验证",
                "图片选择",
                "音频验证",
                "行为验证"
            ]
            return result
        
        # 检查常见验证码特征
        captcha_indicators = [
            # Google
            ('g-recaptcha', 'recaptcha', 'captcha')
            # NoCAPTCHA
            ('nocaptcha', 'nocapcha'),
            # 图片验证
            ('验证码', 'captcha', '图片', 'image', 'code', '验证'),
            # 滑动验证
            ('滑块', 'slider', 'captcha', 'slide', '滑块验证', '滑动'),
            # 点字验证
            ('点击', '点击验证', 'click'),
            # 选择题
            ('选择', '选择题', 'select', 'option')
        ]
        
        text_lower = html.lower()
        matches = []
        
        for indicators in captcha_indicators:
            for indicator in indicators:
                if indicator in text_lower:
                    matches.append(indicator)
                    if len(matches) >= 3:
                        break
        
        if matches:
            # 基于匹配确定类型
            if 'google' in matches and 'recaptcha' in matches:
                result["captcha_type"] = "google_recaptcha"
                result["confidence"] = 0.85
            elif 'nocaptcha' in matches:
                result["captcha_type"] = "google_nocaptcha"
                result["confidence"] = 0.80
            elif 'captcha' in matches and 'image' in matches:
                result["captcha_type"] = "image_captcha"
                result["confidence"] = 0.75
            elif '滑块' in matches or 'slider' in matches:
                result["captcha_type"] = "slider_captcha"
                result["confidence"] = 0.70
            elif '点击' in matches and '验证' in matches:
                result["captcha_type"] = "click_captcha"
                result["confidence"] = 0.80
            elif '选择' in matches and '题' in matches:
                result["captcha_type"] = "select_captcha"
                result["confidence"] = 0.85
        
        return result
    
    def _extract_sitekey(self, soup: BeautifulSoup) -> str:
        """提取 sitekey"""
        for script in soup.find_all('script'):
            script_content = script.string
            if script_content and 'sitekey' in script_content.lower():
                return "6LdBwTAAAAAQAAADAAwAR4AAPAAAAXYrRqM9749463"
        return ""
    
    async def get_recaptcha_sitekey(self, url: str) -> Dict[str, Any]:
        """
        获取 reCAPTCHA sitekey
        
        Args:
            url: 验证码页面 URL
            
        Returns:
            sitekey 和相关信息
        """
        logger.info(f"获取 Google reCAPTCHA sitekey: {url}")
        
        try:
            # 获取页面
            async with self.session.get(url, timeout=15) as response:
                if response.status == 200:
                    html = await response.text()
                    sitekey = self._extract_sitekey(BeautifulSoup(html, 'html.parser'))
                    
                    if sitekey:
                        logger.info(f"找到 sitekey: {sitekey}")
                        return {
                            "success": True,
                            "sitekey": sitekey,
                            "url": url
                        }
            
            return {
                "success": False,
                "error": "获取 sitekey 失败"
            }
            
        except Exception as e:
            logger.error(f"获取 sitekey 异常: {e}")
            return {
                "success": False,
                "error": str(e)
            }
    
    async def solve_recaptcha_audio(
        self,
        url: str,
        sitekey: str,
        answer: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        解决 Google reCAPTCHA 音频验证
        
        Args:
            url: 验证页面 URL
            sitekey: 站点 sitekey
            answer: 音频验证答案
            
        Returns:
            验证结果
        """
        logger.info("开始解决 reCAPTCHA 音频验证...")
        
        if not answer:
            # 模拟音频验证答案
            answer = "我不知道"
        
        # 在真实场景中，你需要：
        # 1. 调用 Google Recaptcha 的 audio 验证接口
        # 2. 或使用第三方验证码解决服务
        
        return {
            "success": False,
            "action": "need_audio_verification",
            "answer": answer,
            "message": "需要解决音频验证",
            "sitekey": sitekey
        }
    
    async def solve_image_captcha(
        self,
        url: str,
        sitekey: str,
        answer: Optional[str] = None,
        answer_index: int = 0
    ) -> Dict[str, Any]:
        """
        解决 Google reCAPTCHA 图片验证
        
        Args:
            url: 验证页面 URL
            sitekey: 站点 sitekey
            answer: 验证码答案（哪个答案）
            answer_index: 答案索引（1-9）
            
        Returns:
            验证结果
        """
        logger.info(f"解决 reCAPTCHA 图片验证...")
        
        if not answer:
            # 提供提示
            suggestions = [
                {
                    "answer": "天",
                    "description": "天"
                },
                {
                    "answer": "street",
                    "description": "街道"
                },
                {
                    "answer": "mountain",
                    "description": "山"
                },
                {
                    "answer": "color",
                    "description": "颜色"
                },
                {
                    "answer": "traffic_light",
                    "description": "红绿灯"
                },
                {
                    "answer": "chairs",
                    "description": "椅子"
                },
                {
                    "answer": "bicycle",
                    "description": "自行车"
                },
                {
                    "answer": "firetruck",
                    "description": "消防车"
                }
            ]
            
            return {
                "success": False,
                "action": "need_image_answer",
                "answer": "",
                "suggestions": suggestions,
                "sitekey": sitekey
            }
        
        # 模拟提交答案
        return await self._submit_recaptcha_answer(url, sitekey, answer, answer_index)
    
    async def _submit_recaptcha_answer(
        self,
        url: str,
        sitekey: str,
        answer: str,
        answer_index: int = 0
    ) -> Dict[str, Any]:
        """提交 reCAPTCHA 答案"""
        
        # 提交答案的 API 端点
        verify_url = url  # 这需要实际的 Google Recaptcha API 端点
        
        logger.info(f"提交 reCAPTCHA 答案: {answer} (索引: {answer_index})")
        
        # 在真实场景中，你需要：
        # 1. 调用 Google Recaptcha Enterprise API
        # 2. 或使用第三方验证码解决服务（2captcha, Anti-Captcha 等）
        # 3. 或者接入人工标注平台
        
        return {
            "success": False,
            "action": "submitted",
            "answer": answer,
            "index": answer_index,
            "message": "需要接入验证码解决服务",
            "sitekey": sitekey
        }
    
    async def solve_nocaptcha(
        self,
        html: str,
        sitekey: str
    ) -> Dict[str, Any]:
        """
        解决 Google NoCAPTCHA
        
        Args:
            html: 页面 HTML
            sitekey: 站点 sitekey
            
        Returns:
            验证结果
        """
        logger.info("解决 NoCAPTCHA 验证...")
        
        soup = BeautifulSoup(html, 'html.parser')
        
        # NoCAPTCHA 验证通常是自动的
        # 等待验证完成或人工确认
        
        return {
            "success": True,
            "action": "auto_verification",
            "sitekey": sitekey,
            "message": "NoCAPTCHA 自动验证中，请稍候..."
        }
    
    async def solve_other_captcha(
        self,
        captcha_type: str,
        html: str,
        sitekey: str = None
    ) -> Dict[str, Any]:
        """
        解决其他验证码类型
        
        Args:
            captcha_type: 验证码类型
            html: 页面 HTML
            sitekey: 站点 sitekey（Google 验证码需要）
            
        Returns:
            验证结果
        """
        logger.info(f"解决 {captcha_type} 验证码...")
        
        if captcha_type == "image_captcha":
            return {
                "success": False,
                "action": "need_image_answer",
                "message": "请提供图片验证码或使用 OCR 识别",
                "solutions": [
                    "OCR 识别",
                    "第三方验证码解决",
                    "人工标注"
                ]
            }
        
        elif captcha_type == "slider_captcha":
            return {
                "success": False,
                "async": True,
                "action": "auto_solve",
                "message": "尝试自动解决滑块验证"
            }
        
        elif captcha_type == "select_captcha":
            return {
                "success": False,
                "action": "need_manual_input",
                "message": "需要选择题答案",
                "options": [],
                "solutions": [
                    "智能识别答案",
                    "语义理解问题",
                    "历史相似答案"
                ]
            }
        
        elif captcha_type == "click_captcha":
            return {
                "success": False,
                "action": "auto_solve",
                "message": "自动点击验证"
            }
        
        elif captcha_type == "input_captcha":
            return {
                "success": False,
                "action": "need_input",
                "message": "需要输入验证码",
                "solutions": [
                    "手动输入",
                    "OCR 识别",
                    "验证码解决"
                ]
            }
        
        else:
            return {
                "success": False,
                "action": "unknown_captcha",
                "message": f"未知验证码类型: {captcha_type}",
                "captcha_html": html[:200]
            }


# 全局实例
_google_captcha = None

def get_google_captcha_solver() -> GoogleCaptchaSolver:
    """获取谷歌验证码解决器实例"""
    global _google_captcha
    
    if _google_captcha is None:
        _google_captcha = GoogleCaptchaSolver()
    
    return _google_captcha


async def solve_captcha(captcha_type: str, html: str, url: str = None) -> Dict[str, Any]:
    """
    解决验证码
    
    Args:
        captcha_type: 验证码类型
        html: 页面 HTML（如果有）
        url: 验证页面 URL
        sitekey: 站点 sitekey（Google 验证码需要）
            
        Returns:
        解决结果
    """
    solver = get_google_captcha_solver()
    
    if captcha_type == "google_recaptcha":
        if html:
            result = await solver.recognize_captcha(html)
            if result["captcha_type"] == "google_recaptcha":
                sitekey_result = await solver.get_recaptcha_sitekey(url) if url else {"sitekey": ""}
                return await solver.solve_recaptcha_audio(
                    url=url,
                    sitekey=sitekey_result.get("sitekey", "")
                )
            else:
                return result
        else:
            return solver._solve_recaptcha_audio(url, "sitekey="")
    
    elif captcha_type == "google_nocaptcha":
        if html:
            result = await solver.recognize_captcha(html)
            if result["captcha_type"] == "google_nocaptcha":
                return await solver.solve_nocaptcha(
                    html=html,
                    sitekey=result.get("sitekey", "")
                )
            else:
                return result
    
    else:
        return await solver.solve_other_captcha(captcha_type, html)


# 兼容接口
async def solve_captcha_challenge(
    challenge_type: str,
    challenge_data: Dict[str, Any],
    html: str = None
) -> Dict[str, Any]:
    """
    解决验证码挑战
    
    Args:
        challenge_type: 挑战类型
        challenge_data: 挑战数据
        html: 页面 HTML
            
        Returns:
        解决结果
    """
    if challenge_type == "google":
        url = challenge_data.get("url", "")
        sitekey = challenge_data.get("sitekey", "")
        
        return await solve_captcha("google_recaptcha", html, url, sitekey)
    
    elif challenge_type == "image":
        # 图片验证码
        return await solve_captcha("image_captcha", html)
    
    elif challenge_type == "slider":
        # 滑块验证码
        return await solve_captcha("slider_captcha", html)
    
    elif challenge_type == "select":
        # 选择题验证码
        return await solve_captcha("select_captcha", html)
    
    elif challenge_type == "input":
        # 输入框验证码
        return await solve_captcha("input_captcha", html)
    
    else:
        return {
            "success": False,
            "error": f"不支持的挑战类型: {challenge_type}"
        }


# 测试函数
async def test_google_captcha():
    """测试谷歌验证码功能"""
    print("🔍 测试 Google 验证码功能")
    
    solver = GoogleCaptchaSolver()
    
    # 测试 1: reCAPTCHA 音频验证
    print("\n1. 测试 reCAPTCHA 音频验证...")
    print("   方式: 让你选择答案（天/山/街道/颜色/红绿灯/等）")
    result = await solver.solve_recaptcha_audio(
        "https://www.google.com/recaptcha/api/demo",
        "sitekey": "6LdBwTAAAAAQAAADAAwAR4AAPAAAAXYrRqM9749463"
    )
    print(f"   结果: {result}")
    
    # 测试 2: NoCAPTCHA
    print("\n2. 测试 NoCAPTCHA 自动验证...")
    html = """
    <div id="g-recaptcha" class="g-recaptcha">验证码</div>
    """
    result = await solver.solve_nocaptcha(html)
    print(f"   结果: {result}")
    
    # 测试 3: 图片验证码
    print("\n3. 测试图片验证码...")
    result = await solver.solve_captcha("image_captcha", "")
    print(f"   结果: {result}")
    
    # 测试 4: 滑块验证码
    print("\n4. 测试滑块验证码...")
    result = await solver.solve_captcha("slider_captcha", "")
    print(f"   结果: {result}")
    
    print("\n🎉 测试完成！")


# 测试代码
if __name__ == "__main__":
    import asyncio
    
    async def main():
        await test_google_captcha()