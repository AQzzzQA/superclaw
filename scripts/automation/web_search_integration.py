#!/usr/bin/env python3
"""
网络搜索功能集成
基于 Tavily Search 技能的网络搜索能力
"""

import asyncio
import json
import os
import subprocess
import tempfile
from typing import List, Dict, Any, Optional
from pathlib import Path

class WebSearchService:
    """网络搜索服务"""
    
    def __init__(self, api_key: Optional[str] = None):
        """
        初始化搜索服务
        
        Args:
            api_key: Tavily API 密钥（可选）
        """
        self.api_key = api_key or self._get_api_key()
        self.tavily_script = Path("/root/.openclaw/workspace/skills/tavily-search/scripts/search.mjs")
        
        # 检查 Node.js 是否可用
        self.node_available = self._check_node_available()
        
        if not self.node_available:
            print("⚠️ Node.js 不可用，跳过网络搜索")
    
    def _get_api_key(self) -> Optional[str]:
        """获取 API 密钥"""
        # 从环境变量获取
        api_key = os.getenv("TAVILY_API_KEY")
        if api_key:
            return api_key.strip()
        
        # 尝试从配置文件获取
        config_file = Path("/root/.openclaw/workspace/.tavily_config")
        if config_file.exists():
            try:
                with open(config_file, 'r') as f:
                    config = json.load(f)
                    return config.get("api_key")
            except:
                pass
        
        return None
    
    def _check_node_available(self) -> bool:
        """检查 Node.js 是否可用"""
        try:
            result = subprocess.run(["node", "--version"], 
                                  capture_output=True, text=True, timeout=5)
            return result.returncode == 0
        except:
            return False
    
    async def search(
        self,
        query: str,
        max_results: int = 5,
        deep_search: bool = False,
        topic: str = "general",
        days: Optional[int] = None
    ) -> List[Dict[str, Any]]:
        """
        执行网络搜索
        
        Args:
            query: 搜索查询
            max_results: 最大结果数
            deep_search: 是否深度搜索
            topic: 搜索主题 (general/news)
            days: 天数限制（仅新闻）
            
        Returns:
            搜索结果列表
        """
        if not self.node_available or not self.api_key:
            return []
        
        # 构建命令
        cmd = ["node", str(self.tavily_script), query]
        
        if max_results and max_results != 5:
            cmd.extend(["-n", str(max_results)])
        
        if deep_search:
            cmd.append("--deep")
        
        if topic and topic != "general":
            cmd.extend(["--topic", topic])
        
        if days and days > 0:
            cmd.extend(["--days", str(days)])
        
        try:
            # 执行搜索
            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                timeout=30,
                cwd="/root/.openclaw/workspace/skills/tavily-search/scripts"
            )
            
            if result.returncode == 0:
                # 解析结果
                try:
                    data = json.loads(result.stdout)
                    return self._format_results(data)
                except json.JSONDecodeError:
                    # 尝试解析纯文本结果
                    return self._parse_text_results(result.stdout)
            else:
                print(f"搜索失败: {result.stderr}")
                return []
                
        except subprocess.TimeoutExpired:
            print("搜索超时")
            return []
        except Exception as e:
            print(f"搜索异常: {e}")
            return []
    
    def _format_results(self, data: Dict[str, Any]) -> List[Dict[str, Any]]:
        """格式化搜索结果"""
        results = []
        
        if "results" in data:
            for item in data["results"]:
                result = {
                    "title": item.get("title", ""),
                    "url": item.get("url", ""),
                    "content": item.get("content", ""),
                    "score": item.get("score", 0.0),
                    "published": item.get("published", ""),
                    "source": item.get("source", ""),
                    "query": item.get("query", "")
                }
                results.append(result)
        
        return results
    
    def _parse_text_results(self, text: str) -> List[Dict[str, Any]]:
        """解析文本格式的结果"""
        results = []
        
        # 简单的文本解析
        lines = text.split('\n')
        current_result = {}
        
        for line in lines:
            line = line.strip()
            if line.startswith("Title:"):
                if current_result:
                    results.append(current_result)
                current_result = {
                    "title": line.replace("Title:", "").strip(),
                    "url": "",
                    "content": "",
                    "score": 0.0,
                    "published": "",
                    "source": "",
                    "query": ""
                }
            elif line.startswith("URL:"):
                current_result["url"] = line.replace("URL:", "").strip()
            elif line.startswith("Content:"):
                current_result["content"] = line.replace("Content:", "").strip()
        
        if current_result:
            results.append(current_result)
        
        return results
    
    async def extract_url(self, url: str) -> str:
        """
        从 URL 提取内容
        
        Args:
            url: 网页 URL
            
        Returns:
            提取的内容
        """
        if not self.node_available:
            return "Node.js 不可用"
        
        try:
            # 构建命令
            cmd = ["node", str(self.tavily_script).replace("search.mjs", "extract.mjs"), url]
            
            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                timeout=30,
                cwd="/root/.openclaw/workspace/skills/tavily-search/scripts"
            )
            
            if result.returncode == 0:
                return result.stdout
            else:
                return f"提取失败: {result.stderr}"
                
        except Exception as e:
            return f"提取异常: {e}"
    
    def set_api_key(self, api_key: str):
        """设置 API 密钥"""
        self.api_key = api_key.strip()
        
        # 保存到配置文件
        config_file = Path("/root/.openclaw/workspace/.tavily_config")
        config = {"api_key": self.api_key}
        
        with open(config_file, 'w') as f:
            json.dump(config, f, indent=2)
        
        print("✅ API 密钥已保存")


# 全局搜索服务实例
_search_service = None

def get_web_search_service() -> WebSearchService:
    """获取全局搜索服务实例"""
    global _search_service
    
    if _search_service is None:
        _search_service = WebSearchService()
    
    return _search_service


async def web_search(
    query: str,
    max_results: int = 5,
    deep_search: bool = False,
    topic: str = "general",
    days: Optional[int] = None
) -> List[Dict[str, Any]]:
    """
    网络搜索函数（兼容旧接口）
    
    Args:
        query: 搜索查询
        max_results: 最大结果数
        deep_search: 是否深度搜索
        topic: 搜索主题
        days: 天数限制
        
    Returns:
        搜索结果列表
    """
    service = get_web_search_service()
    return await service.search(query, max_results, deep_search, topic, days)


async def extract_web_content(url: str) -> str:
    """
    提取网页内容
    
    Args:
        url: 网页 URL
        
    Returns:
        提取的内容
    """
    service = get_web_search_service()
    return await service.extract_url(url)


def configure_tavily_api_key(api_key: str):
    """配置 Tavily API 密钥"""
    service = get_web_search_service()
    service.set_api_key(api_key)


# 兼容接口
async def search_web(query: str, max_results: int = 5) -> List[Dict[str, Any]]:
    """网络搜索的兼容接口"""
    return await web_search(query, max_results)