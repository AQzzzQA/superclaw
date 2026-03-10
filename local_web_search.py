#!/usr/bin/env python3
"""
本地网络搜索实现
使用本地搜索引擎和工具，不依赖外部 API
"""

import asyncio
import aiohttp
import re
import json
from typing import List, Dict, Any, Optional
from urllib.parse import quote, urljoin
from datetime import datetime
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class LocalWebSearch:
    """本地网络搜索实现"""
    
    def __init__(self):
        self.session = None
        self.search_engines = {
            "bing": {
                "name": "Bing",
                "url": "https://www.bing.com/search",
                "query_param": "q",
                "result_selector": ".b_algoheading, .b_caption"
            },
            "duckduckgo": {
                "name": "DuckDuckGo",
                "url": "https://duckduckgo.com/html",
                "query_param": "q",
                "result_selector": ".result__title, .result__snippet"
            },
            "wikipedia": {
                "name": "Wikipedia",
                "url": "https://zh.wikipedia.org/wiki",
                "query_param": None,
                "direct_search": True
            }
        }
    
    async def __aenter__(self):
        """异步上下文管理器入口"""
        headers = {
            "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
        }
        self.session = aiohttp.ClientSession(headers=headers)
        return self
    
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """异步上下文管理器退出"""
        if self.session:
            await self.session.close()
    
    async def search(
        self,
        query: str,
        engine: str = "bing",
        max_results: int = 5
    ) -> List[Dict[str, Any]]:
        """
        执行本地网络搜索
        
        Args:
            query: 搜索查询
            engine: 搜索引擎 (bing/duckduckgo/wikipedia)
            max_results: 最大结果数
            
        Returns:
            搜索结果列表
        """
        logger.info(f"本地搜索: {query} (引擎: {engine})")
        
        try:
            if engine == "wikipedia":
                return await self._search_wikipedia(query, max_results)
            else:
                return await self._search_engine(query, engine, max_results)
        except Exception as e:
            logger.error(f"搜索失败: {e}")
            return []
    
    async def _search_engine(
        self,
        query: str,
        engine: str,
        max_results: int
    ) -> List[Dict[str, Any]]:
        """使用搜索引擎搜索"""
        engine_config = self.search_engines.get(engine)
        if not engine_config:
            logger.error(f"未知搜索引擎: {engine}")
            return []
        
        # 构建搜索 URL
        if engine_config.get("direct_search"):
            search_url = f"{engine_config['url']}/{quote(query)}"
        else:
            search_url = f"{engine_config['url']}?{engine_config['query_param']}={quote(query)}"
        
        try:
            async with self.session.get(search_url, timeout=10) as response:
                if response.status == 200:
                    html = await response.text()
                    return self._parse_results(html, engine, max_results)
                else:
                    logger.error(f"搜索失败: HTTP {response.status}")
                    return []
        except Exception as e:
            logger.error(f"搜索异常: {e}")
            return []
    
    async def _search_wikipedia(
        self,
        query: str,
        max_results: int
    ) -> List[Dict[str, Any]]:
        """搜索 Wikipedia"""
        # 使用 Wikipedia API 搜索
        search_url = f"https://zh.wikipedia.org/w/api.php?action=query&list=search&srsearch={quote(query, safe='')}&format=json"
        
        try:
            async with self.session.get(search_url, timeout=15) as response:
                if response.status == 200:
                    data = await response.json()
                    return self._parse_wikipedia_api(data, query)
                elif response.status == 403:
                    logger.warning("Wikipedia API 返回 403，使用备用方法")
                    # 备用方法：直接构造结果
                    return self._create_fallback_results(query)
                else:
                    logger.error(f"Wikipedia 搜索失败: HTTP {response.status}")
                    return []
        except Exception as e:
            logger.error(f"Wikipedia 搜索异常: {e}")
            return []
    
    def _create_fallback_results(self, query: str) -> List[Dict[str, Any]]:
        """创建备用结果（当 API 不可用时）"""
        # 基于查询构造简单的结果
        result = {
            "title": f"关于 '{query}' 的信息",
            "url": f"https://zh.wikipedia.org/wiki/{quote(query, safe='')}",
            "content": f"正在为您查找 '{query}' 相关的信息。由于 API 访问限制，无法获取详细内容。",
            "score": 0.9,
            "published": "",
            "source": "wikipedia_fallback",
            "query": query
        }
        return [result]
    
    def _parse_results(self, html: str, engine: str, max_results: int) -> List[Dict[str, Any]]:
        """解析搜索结果（简化版）"""
        results = []
        
        # 简化的 HTML 解析（不使用 BeautifulSoup）
        
        # 提取标题
        title_pattern = r'<h2[^>]*><a[^>]*>([^<]+)</a>'
        titles = re.findall(title_pattern, html, re.IGNORECASE)
        
        # 提取 URL
        url_pattern = r'href="([^"]+)"'
        urls = re.findall(url_pattern, html)
        
        # 提取描述
        desc_pattern = r'<p[^>]*>([^<]+)</p>'
        descriptions = re.findall(desc_pattern, html)
        
        # 组合结果
        count = min(max_results, len(titles), len(urls))
        for i in range(count):
            result = {
                "title": titles[i].strip(),
                "url": urls[i].strip(),
                "content": descriptions[i].strip() if i < len(descriptions) else "",
                "score": 1.0 - (i * 0.1),
                "published": "",
                "source": engine,
                "query": ""
            }
            results.append(result)
        
        return results
    
    def _parse_wikipedia_api(self, data: Dict[str, Any], query: str) -> List[Dict[str, Any]]:
        """解析 Wikipedia API 结果"""
        results = []
        
        try:
            # 提取搜索结果
            query_obj = data.get("query", {})
            if not query_obj:
                return results
                
            search_results = query_obj.get("search", [])
            
            for i, item in enumerate(search_results[:5]):
                title = item.get("title", "")
                pageid = item.get("pageid", "")
                snippet = item.get("snippet", "").replace('<span class="searchmatch">', '').replace('</span>', '')
                
                # 移除 HTML 标签
                import re
                snippet = re.sub(r'<[^>]+>', '', snippet)
                
                result = {
                    "title": title,
                    "url": f"https://zh.wikipedia.org/wiki/{quote(title, safe='')}",
                    "content": snippet,
                    "score": 1.0 - (i * 0.1),
                    "published": "",
                    "source": "wikipedia",
                    "query": query
                }
                results.append(result)
        
        except Exception as e:
            logger.error(f"解析 Wikipedia API 失败: {e}")
        
        return results
    
    async def extract_content(self, url: str) -> str:
        """
        提取网页内容（简化版）
        
        Args:
            url: 网页 URL
            
        Returns:
            提取的内容
        """
        try:
            async with self.session.get(url, timeout=10) as response:
                if response.status == 200:
                    html = await response.text()
                    return self._extract_text_from_html(html)
                else:
                    return f"无法访问网页: HTTP {response.status}"
        except Exception as e:
            return f"提取失败: {e}"
    
    def _extract_text_from_html(self, html: str) -> str:
        """从 HTML 中提取文本"""
        # 移除脚本和样式
        html = re.sub(r'<script[^>]*>.*?</script>', '', html, flags=re.DOTALL)
        html = re.sub(r'<style[^>]*>.*?</style>', '', html, flags=re.DOTALL)
        html = re.sub(r'<[^>]+>', '\n', html)
        
        # 移除多余空白
        text = re.sub(r'\n+', '\n', html)
        text = text.strip()
        
        return text[:1000]  # 限制长度


# 全局实例
_local_search_service = None

def get_local_search_service() -> LocalWebSearch:
    """获取本地搜索服务实例"""
    global _local_search_service
    
    if _local_search_service is None:
        _local_search_service = LocalWebSearch()
    
    return _local_search_service


async def local_search(
    query: str,
    engine: str = "bing",
    max_results: int = 5
) -> List[Dict[str, Any]]:
    """
    本地网络搜索函数
    
    Args:
        query: 搜索查询
        engine: 搜索引擎
        max_results: 最大结果数
        
    Returns:
        搜索结果列表
    """
    service = get_local_search_service()
    
    async with service:
        return await service.search(query, engine, max_results)


async def local_extract_content(url: str) -> str:
    """
    本地内容提取函数
    
    Args:
        url: 网页 URL
        
    Returns:
        提取的内容
    """
    service = get_local_search_service()
    
    async with service:
        return await service.extract_content(url)


# 兼容接口
async def web_search(
    query: str,
    max_results: int = 5,
    **kwargs
) -> List[Dict[str, Any]]:
    """兼容原有 web_search 接口"""
    return await local_search(query, max_results=max_results)


async def extract_web_content(url: str) -> str:
    """兼容原有 extract_web_content 接口"""
    return await local_extract_content(url)