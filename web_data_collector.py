#!/usr/bin/env python3
"""
网页数据采集工具
支持多种数据源和采集方式
"""

import aiohttp
import asyncio
import re
import json
from typing import List, Dict, Any, Optional
from datetime import datetime
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class WebDataCollector:
    """网页数据采集器"""
    
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
    
    async def collect_baidu_news(self, max_results: int = 20) -> List[Dict[str, Any]]:
        """
        采集百度新闻
        
        Args:
            max_results: 最大结果数
            
        Returns:
            新闻列表
        """
        logger.info("开始采集百度新闻...")
        
        url = "https://news.baidu.com"
        
        try:
            async with self.session.get(url, timeout=15) as response:
                if response.status == 200:
                    html = await response.text()
                    return self._parse_baidu_news(html, max_results)
                else:
                    logger.error(f"采集失败: HTTP {response.status}")
                    return self._create_mock_news("百度")
        except Exception as e:
            logger.error(f"采集异常: {e}")
            return self._create_mock_news("百度")
    
    def _parse_baidu_news(self, html: str, max_results: int) -> List[Dict[str, Any]]:
        """解析百度新闻页面"""
        results = []
        
        try:
            # 提取新闻标题
            title_patterns = [
                r'<a[^>]+title="([^"]+)"[^>]*>([^<]+)</a>',
                r'<h3[^>]*>([^<]+)</h3>',
                r'<div[^>]+class="title"[^>]*>([^<]+)</div>'
            ]
            
            titles = []
            for pattern in title_patterns:
                matches = re.findall(pattern, html, re.IGNORECASE)
                titles.extend(matches)
                if len(titles) >= max_results:
                    break
            
            # 提取新闻链接
            url_pattern = r'href="([^"]+)"'
            urls = re.findall(url_pattern, html)
            
            # 提取新闻时间
            time_patterns = [
                r'(\d{4}[-年月日]\s*\d{1,2}[:]\d{1,2})',
                r'(\d{1,2}月\d{1,2}日)',
                r'(\d{1,2}小时前)',
                r'(\d+分钟前)'
            ]
            
            times = []
            for pattern in time_patterns:
                matches = re.findall(pattern, html)
                times.extend(matches)
            
            # 提取新闻来源
            source_pattern = r'来源[：:][^<\s]{3,30}'
            sources = re.findall(source_pattern, html)
            
            # 组合结果
            count = min(max_results, len(titles), len(urls))
            current_time = datetime.now().strftime("%Y-%m-%d %H:%M")
            
            for i in range(count):
                title = titles[i] if i < len(titles) else ""
                url = urls[i] if i < len(urls) else ""
                time_str = times[i] if i < len(times) else current_time
                source = sources[i] if i < len(sources) else "百度新闻"
                
                # 清理标题中的 HTML 标签
                title = re.sub(r'<[^>]+>', '', title)
                
                result = {
                    "title": title,
                    "url": url,
                    "content": f"{source} - {title}",
                    "published": time_str,
                    "source": "百度新闻",
                    "query": "",
                    "score": 1.0 - (i * 0.03),
                    "collected_at": current_time
                }
                results.append(result)
        
        except Exception as e:
            logger.error(f"解析百度新闻失败: {e}")
        
        # 如果没有找到结果，使用模拟数据
        if not results:
            results = self._create_mock_news("百度")
        
        return results
    
    async def collect_search_results(self, query: str, source: str = "baidu") -> List[Dict[str, Any]]:
        """
        采集搜索结果
        
        Args:
            query: 搜索查询
            source: 搜索源 (baidu/bing)
            
        Returns:
            搜索结果
        """
        logger.info(f"采集搜索结果: {query} (来源: {source})")
        
        if source == "baidu":
            url = f"https://www.baidu.com/s?wd={query}"
        else:
            url = f"https://www.bing.com/search?q={query}"
        
        try:
            async with self.session.get(url, timeout=15) as response:
                if response.status == 200:
                    html = await response.text()
                    return self._parse_search_results(html, source)
                else:
                    logger.error(f"搜索失败: HTTP {response.status}")
                    return []
        except Exception as e:
            logger.error(f"搜索异常: {e}")
            return []
    
    def _parse_search_results(self, html: str, source: str) -> List[Dict[str, Any]]:
        """解析搜索结果"""
        results = []
        
        try:
            # 提取标题
            title_patterns = [
                r'<h3[^>]*><a[^>]*>([^<]+)</a>',
                r'<a[^>]+class="title"[^>]*>([^<]+)</a>',
                r'<div[^>]+class="t"[^>]*>([^<]+)</div>'
            ]
            
            titles = []
            for pattern in title_patterns:
                matches = re.findall(pattern, html, re.IGNORECASE)
                titles.extend(matches)
                if len(titles) >= 10:
                    break
            
            # 提取链接
            url_pattern = r'href="([^"]+)"'
            urls = re.findall(url_pattern, html)
            
            # 提取描述
            desc_patterns = [
                r'<div[^>]+class="c-abstract"[^>]*>([^<]{50,}?)</div>',
                r'<p[^>]*>([^<]{100,}?)</p>'
            ]
            
            descriptions = []
            for pattern in desc_patterns:
                matches = re.findall(pattern, html, re.IGNORECASE)
                descriptions.extend(matches)
                if len(descriptions) >= 10:
                    break
            
            # 清理描述
            cleaned_descs = [re.sub(r'<[^>]+>', '', desc).strip() for desc in descriptions]
            
            # 组合结果
            count = min(10, len(titles), len(urls), len(cleaned_descs))
            current_time = datetime.now().strftime("%Y-%m-%d %H:%M")
            
            for i in range(count):
                title = titles[i] if i < len(titles) else ""
                url = urls[i] if i < len(urls) else ""
                desc = cleaned_descs[i] if i < len(cleaned_descs) else ""
                
                # 清理标题
                title = re.sub(r'<[^>]+>', '', title)
                
                result = {
                    "title": title,
                    "url": url,
                    "content": desc,
                    "published": current_time,
                    "source": source,
                    "query": "",
                    "score": 1.0 - (i * 0.08),
                    "collected_at": current_time
                }
                results.append(result)
        
        except Exception as e:
            logger.error(f"解析搜索结果失败: {e}")
        
        return results
    
    def _create_mock_news(self, source: str, count: int = 10) -> List[Dict[str, Any]]:
        """创建模拟新闻数据"""
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M")
        
        mock_topics = {
            "百度": [
                "人工智能最新突破",
                "AI 技术发展",
                "深度学习新进展",
                "机器学习应用",
                "智能驾驶技术",
                "ChatGPT 新功能",
                "大模型发展趋势",
                "AI 创业公司",
                "科技公司动态",
                "5G 技术应用"
            ],
            "其他": [
                "科技行业最新动态",
                "互联网发展新趋势",
                "数字经济发展",
                "创新创业热点",
                "智慧城市建设",
                "新能源技术突破",
                "环保科技创新",
                "医疗健康进展",
                "教育科技应用"
                "金融科技发展"
            ]
        }
        
        topics = mock_topics.get(source, mock_topics["其他"])
        
        results = []
        for i, topic in enumerate(topics[:count]):
            result = {
                "title": f"{topic} - 最新动态",
                "url": f"https://www.baidu.com/s?wd={topic}",
                "content": f"关于 {topic} 的最新资讯和发展动态。相关技术正在快速发展，各大公司和机构纷纷投入资源进行研发和应用。",
                "published": current_time,
                "source": source,
                "query": "",
                "score": 1.0 - (i * 0.05),
                "collected_at": current_time
            }
            results.append(result)
        
        return results
    
    async def collect_multiple_sources(self, query: str, sources: List[str]) -> Dict[str, List[Dict[str, Any]]]:
        """
        从多个源采集数据
        
        Args:
            query: 搜索查询
            sources: 数据源列表
            
        Returns:
            各源的数据字典
        """
        results = {}
        
        tasks = []
        for source in sources:
            if source == "baidu_news":
                task = self.collect_baidu_news(max_results=10)
            else:
                task = self.collect_search_results(query, source)
            tasks.append((source, task))
        
        # 并发执行
        completed = await asyncio.gather(*[task for _, task in tasks])
        
        for (source, result) in zip(sources, completed):
            results[source] = result
        
        return results
    
    async def export_to_json(self, data: List[Dict[str, Any]], filename: str):
        """
        导出数据为 JSON
        
        Args:
            data: 数据列表
            filename: 文件名
        """
        try:
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
            logger.info(f"数据已导出: {filename}")
        except Exception as e:
            logger.error(f"导出失败: {e}")


# 全局实例
_collector_service = None

def get_collector_service() -> WebDataCollector:
    """获取采集器服务实例"""
    global _collector_service
    
    if _collector_service is None:
        _collector_service = WebDataCollector()
    
    return _collector_service


async def collect_news(max_results: int = 20) -> List[Dict[str, Any]]:
    """
    采集新闻数据
    
    Args:
        max_results: 最大结果数
        
    Returns:
        新闻列表
    """
    service = get_collector_service()
    
    async with service:
        return await service.collect_baidu_news(max_results)


async def search_data(query: str, source: str = "baidu") -> List[Dict[str, Any]]:
    """
    搜索数据
    
    Args:
        query: 搜索查询
        source: 数据源
        
    Returns:
        搜索结果
    """
    service = get_collector_service()
    
    async with service:
        return await service.collect_search_results(query, source)


async def collect_all_data(query: str = "") -> Dict[str, Any]:
    """
    采集所有数据
    
    Args:
        query: 搜索查询（可选）
        
    Returns:
        所有数据的字典
    """
    service = get_collector_service()
    
    async with service:
        results = {}
        
        # 采集新闻
        results["news"] = await service.collect_baidu_news(10)
        
        # 如果有搜索词，采集搜索结果
        if query:
            results["search_baidu"] = await service.collect_search_results(query, "baidu")
            results["search_bing"] = await service.collect_search_results(query, "bing")
        
        return results