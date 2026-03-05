"""
系统配置 API
"""
from typing import Dict, Any, Optional
from fastapi import APIRouter
from pydantic import BaseModel
from app.core.response import APIResponse
from app.core.exceptions import NotFoundException
import json

router = APIRouter()

# 模拟系统配置
system_config = {
    "app": {
        "name": "Ad Platform",
        "version": "2.0.0",
        "description": "广告平台管理系统",
    },
    "features": {
        "auto_bidding": {
            "enabled": True,
            "default_model": "roi",
        },
        "ab_testing": {
            "enabled": True,
            "min_sample_size": 100,
        },
        "attribution": {
            "enabled": True,
            "default_model": "time_decay",
        },
    },
    "limits": {
        "max_campaigns_per_user": 100,
        "max_adgroups_per_campaign": 100,
        "max_creatives_per_adgroup": 50,
    },
    "notifications": {
        "email": {
            "enabled": True,
            "smtp_host": "smtp.example.com",
            "smtp_port": 587,
        },
        "sms": {
            "enabled": False,
        },
    },
}


class ConfigUpdate(BaseModel):
    """配置更新请求"""
    section: str
    key: Optional[str] = None
    value: Any = None


@router.get("/config")
async def get_config():
    """获取系统配置"""
    return APIResponse.success(data=system_config)


@router.get("/config/{section}")
async def get_config_section(section: str):
    """获取配置节"""
    if section not in system_config:
        raise NotFoundException("配置节不存在")

    return APIResponse.success(data={section: system_config[section]})


@router.put("/config/{section}")
async def update_config_section(section: str, config: Dict[str, Any]):
    """更新配置节"""
    if section not in system_config:
        raise NotFoundException("配置节不存在")

    # 更新配置
    system_config[section].update(config)

    return APIResponse.success(
        data={section: system_config[section]},
        message="配置更新成功"
    )


@router.put("/config/{section}/{key}")
async def update_config_value(section: str, key: str, value: Any):
    """更新配置值"""
    if section not in system_config:
        raise NotFoundException("配置节不存在")

    if key not in system_config[section]:
        raise NotFoundException("配置键不存在")

    # 更新配置值
    system_config[section][key] = value

    return APIResponse.success(
        data={section: system_config[section]},
        message="配置更新成功"
    )


@router.post("/config/reset")
async def reset_config():
    """重置配置为默认值"""
    global system_config
    system_config = {
        "app": {
            "name": "Ad Platform",
            "version": "2.0.0",
            "description": "广告平台管理系统",
        },
        "features": {
            "auto_bidding": {
                "enabled": True,
                "default_model": "roi",
            },
            "ab_testing": {
                "enabled": True,
                "min_sample_size": 100,
            },
            "attribution": {
                "enabled": True,
                "default_model": "time_decay",
            },
        },
        "limits": {
            "max_campaigns_per_user": 100,
            "max_adgroups_per_campaign": 100,
            "max_creatives_per_adgroup": 50,
        },
        "notifications": {
            "email": {
                "enabled": True,
                "smtp_host": "smtp.example.com",
                "smtp_port": 587,
            },
            "sms": {
                "enabled": False,
            },
        },
    }

    return APIResponse.success(message="配置已重置")
