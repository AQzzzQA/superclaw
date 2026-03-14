#!/usr/bin/env python3
"""
修复的浏览器自动化工具
使用 requests + BeautifulSoup 进行网页操作
"""

import requests
from bs4 import BeautifulSoup
import json
from typing import Dict, List, Any, Optional
from datetime import datetime
import logging
import time

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class FixedWebAutomation:
    """修复的网页自动化工具"""
    
    def __init__(self):
        self.session = None
        self.user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
        self.session = requests.Session()
        self.session.headers.update({
            "User-Agent": self.user_agent,
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
            "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8",
            "Accept-Encoding": "gzip, deflate",
            "Connection": "keep-alive"
        })
    
    def fetch_page(self, url: str, timeout: int = 10) -> Optional[str]:
        """
        获取网页内容
        
        Args:
            url: 网页 URL
            timeout: 超时时间
            
        Returns:
            网页内容
        """
        try:
            logger.info(f"获取页面: {url}")
            response = self.session.get(url, timeout=timeout)
            
            if response.status_code == 200:
                logger.info(f"获取成功: {len(response.content)} 字节")
                return response.text
            else:
                logger.error(f"获取失败: HTTP {response.status_code}")
                return None
                
        except Exception as e:
            logger.error(f"获取异常: {e}")
            return None
    
    def parse_page(self, html: str) -> Dict[str, Any]:
        """
        解析网页内容
        
        Args:
            html: HTML 内容
            
        Returns:
            解析结果
        """
        try:
            soup = BeautifulSoup(html, 'html.parser')
            
            result = {
                "title": "",
                "links": [],
                "text": "",
                "meta": {},
                "images": [],
                "timestamp": datetime.now().isoformat()
            }
            
            # 提取标题
            if soup.title:
                result["title"] = soup.title.string.strip()
            
            # 提取所有链接
            for link in soup.find_all('a', href=True):
                link_text = link.get_text(strip=True)
                link_url = link['href']
                result["links"].append({
                    "text": link_text,
                    "url": link_url
                })
            
            # 提取主要文本
            if soup.body:
                # 移除 script 和 style 标签
                for script in soup.find_all(['script', 'style']):
                    script.decompose()
                result["text"] = soup.body.get_text(separator='\n', strip=True)[:500]
            
            # 提取 meta 信息
            for meta in soup.find_all('meta'):
                name = meta.get('name', '')
                content = meta.get('content', '')
                if name and content:
                    result["meta"][name] = content
            
            # 提取图片
            for img in soup.find_all('img'):
                img_url = img.get('src', '')
                img_alt = img.get('alt', '')
                result["images"].append({
                    "url": img_url,
                    "alt": img_alt
                })
            
            logger.info(f"解析完成: {len(result['links'])} 链接, {len(result['images'])} 图片")
            return result
            
        except Exception as e:
            logger.error(f"解析失败: {e}")
            return {}
    
    def extract_data(self, url: str, selectors: Dict[str, str] = None) -> Dict[str, Any]:
        """
        提取特定数据
        
        Args:
            url: 网页 URL
            selectors: CSS 选择器字典
            
        Returns:
            提取的数据
        """
        html = self.fetch_page(url)
        if not html:
            return {"error": "无法获取页面"}
        
        soup = BeautifulSoup(html, 'html.parser')
        data = {
            "url": url,
            "timestamp": datetime.now().isoformat(),
            "extracted_data": {}
        }
        
        # 提取页面标题
        if soup.title:
            data["extracted_data"]["page_title"] = soup.title.string.strip()
        
        # 提取所有链接和文本
        all_links = []
        for link in soup.find_all('a', href=True):
            link_info = {
                "text": link.get_text(strip=True),
                "url": link['href']
            }
            all_links.append(link_info)
        
        data["extracted_data"]["links"] = all_links
        data["extracted_data"]["links_count"] = len(all_links)
        
        # 提取所有图片
        all_images = []
        for img in soup.find_all('img'):
            img_info = {
                "url": img.get('src', ''),
                "alt": img.get('alt', '')
            }
            all_images.append(img_info)
        
        data["extracted_data"]["images"] = all_images
        data["extracted_data"]["images_count"] = len(all_images)
        
        # 提取主要文本内容
        text_content = ""
        if soup.body:
            # 移除不需要的标签
            for tag in soup.find_all(['script', 'style', 'noscript']):
                tag.decompose()
            
            text_content = soup.body.get_text(separator='\n', strip=True)
            data["extracted_data"]["text_preview"] = text_content[:1000]
        
        # 提取所有 heading 内容
        headings = []
        for h in soup.find_all(['h1', 'h2', 'h3', 'h4', 'h5', 'h6']):
            heading_text = h.get_text(strip=True)
            if heading_text:
                headings.append({
                    "level": h.name,
                    "text": heading_text
                })
        
        data["extracted_data"]["headings"] = headings
        data["extracted_data"]["headings_count"] = len(headings)
        
        logger.info(f"数据提取完成: 链接 {len(all_links)} 个, 图片 {len(all_images)} 个, 标题 {len(headings)} 个")
        return data
    
    def scroll_and_collect(self, url: str, max_pages: int = 3) -> List[Dict[str, Any]]:
        """
        模拟滚动并收集数据
        
        Args:
            url: 网页 URL
            max_pages: 最大页数
            
        Returns:
            收集的数据列表
        """
        logger.info(f"模拟滚动收集: {url}")
        
        all_data = []
        
        for page in range(max_pages):
            html = self.fetch_page(url)
            if html:
                soup = BeautifulSoup(html, 'html.parser')
                
                # 提取当前页数据
                page_data = {
                    "page": page + 1,
                    "url": url,
                    "timestamp": datetime.now().isoformat(),
                    "title": soup.title.string.strip() if soup.title else "",
                    "content": soup.body.get_text(separator='\n', strip=True)[:200]
                }
                
                all_data.append(page_data)
                
                # 查找下一页链接
                next_links = soup.find_all('a', text=lambda x: x and '下一页' in x)
                if next_links:
                    url = next_links[0].get('href', '')
                    logger.info(f"找到下一页: {url}")
                    time.sleep(2)  # 模拟延迟
                else:
                    break
            else:
                break
        
        logger.info(f"收集完成: {len(all_data)} 页")
        return all_data
    
    def login_and_collect(self, login_url: str, username: str, password: str, data_url: str) -> Dict[str, Any]:
        """
        登录并收集数据
        
        Args:
            login_url: 登录 URL
            username: 用户名
            password: 密码
            data_url: 数据 URL
            
        Returns:
            登录后收集的数据
        """
        logger.info("开始登录流程...")
        
        try:
            # 获取登录页面
            login_page = self.fetch_page(login_url)
            if not login_page:
                return {"error": "无法访问登录页面"}
            
            soup = BeautifulSoup(login_page, 'html.parser')
            
            # 查找登录表单
            forms = soup.find_all('form')
            if not forms:
                return {"error": "未找到登录表单"}
            
            form = forms[0]
            action = form.get('action', login_url)
            method = form.get('method', 'post').upper()
            
            # 准备表单数据
            form_data = {}
            for input_field in form.find_all('input'):
                name = input_field.get('name')
                input_type = input_field.get('type', 'text')
                value = input_field.get('value', '')
                
                if name:
                    if input_type == 'password':
                        form_data[name] = password
                    elif input_type == 'text':
                        if 'username' in name.lower():
                            form_data[name] = username
                        elif 'user' in name.lower():
                            form_data[name] = username
                        else:
                            form_data[name] = value
                    else:
                        form_data[name] = value
            
            # 提交登录
            logger.info(f"提交登录表单到: {action}")
            
            if method == 'POST':
                response = self.session.post(action, data=form_data, timeout=10)
            else:
                response = self.session.get(action, params=form_data, timeout=10)
            
            if response.status_code == 200:
                logger.info("登录响应: " + response.url)
                
                # 检查登录是否成功
                if 'login' not in response.url and 'error' not in response.url:
                    logger.info("登录可能成功")
                    
                    # 收集数据
                    data_html = self.fetch_page(data_url)
                    if data_html:
                        return self.parse_page(data_html)
                
            return {"error": "登录失败或无权限"}
            
        except Exception as e:
            logger.error(f"登录流程失败: {e}")
            return {"error": str(e)}
    
    def save_data(self, data: Any, filename: str):
        """
        保存数据
        
        Args:
            data: 要保存的数据
            filename: 文件名
        """
        try:
            with open(filename, 'w', encoding='utf-8') as f:
                if isinstance(data, (list, dict)):
                    json.dump(data, f, ensure_ascii=False, indent=2)
                else:
                    f.write(str(data))
            logger.info(f"数据已保存: {filename}")
            return True
        except Exception as e:
            logger.error(f"保存失败: {e}")
            return False


# 全局实例
_fixed_automation = None

def get_fixed_automation() -> FixedWebAutomation:
    """获取修复的自动化工具实例"""
    global _fixed_automation
    
    if _fixed_automation is None:
        _fixed_automation = FixedWebAutomation()
    
    return _fixed_automation


# 兼容接口
def fetch_page(url: str, timeout: int = 10) -> Optional[str]:
    """获取网页内容"""
    automation = get_fixed_automation()
    return automation.fetch_page(url, timeout)

def parse_page(html: str) -> Dict[str, Any]:
    """解析网页内容"""
    automation = get_fixed_automation()
    return automation.parse_page(html)

def collect_data(url: str, selectors: Dict[str, str] = None) -> Dict[str, Any]:
    """收集网页数据"""
    automation = get_fixed_automation()
    return automation.extract_data(url, selectors)

def scroll_and_collect(url: str, max_pages: int = 3) -> List[Dict[str, Any]]:
    """滚动并收集数据"""
    automation = get_fixed_automation()
    return automation.scroll_and_collect(url, max_pages)