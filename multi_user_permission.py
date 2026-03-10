#!/usr/bin/env python3
"""
OpenClaw 多用户权限管理系统
支持用户隔离、资源隔离、权限控制
"""

import json
import os
import hashlib
import logging
from typing import Dict, List, Any, Optional, Set
from datetime import datetime, timedelta
from pathlib import Path

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class MultiUserPermissionManager:
    """多用户权限管理器"""
    
    def __init__(self, workspace: str = "/root/.openclaw/workspace"):
        self.workspace = Path(workspace)
        self.users_file = self.workspace / "users" / "users.json"
        self.permissions_file = self.workspace / "users" / "permissions.json"
        self.sessions_file = self.workspace / "users" / "sessions" / "sessions.json"
        
        # 确保目录存在
        self.users_file.parent.mkdir(parents=True)
        self.permissions_file.parent.mkdir(parents=True)
        self.sessions_file.parent.mkdir(parents=True)
        
        # 加载现有数据
        self.users = self._load_users()
        self.permissions = self._load_permissions()
        self.sessions = self._load_sessions()
        
        logger.info(f"权限管理器初始化完成: {len(self.users)} 用户, {len(self.permissions)} 权限, {len(self.sessions)} 会话")
    
    def _load_users(self) -> Dict[str, Dict[str, Any]]:
        """加载用户数据"""
        if self.users_file.exists():
            try:
                with open(self.users_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except Exception as e:
                logger.error(f"加载用户数据失败: {e}")
                return {}
        return {}
    
    def _save_users(self) -> bool:
        """保存用户数据"""
        try:
            with open(self.users_file, 'w', encoding='utf-8') as f:
                json.dump(self.users, f, ensure_ascii=False, indent=2)
            logger.info("用户数据已保存")
            return True
        except Exception as e:
            logger.error(f"保存用户数据失败: {e}")
            return False
    
    def _load_permissions(self) -> Dict[str, Dict[str, Any]]:
        """加载权限配置"""
        if self.permissions_file.exists():
            try:
                with open(self.permissions_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except Exception as e:
                logger.error(f"加载权限配置失败: {e}")
                return {}
        return {}
    
    def _save_permissions(self) -> bool:
        """保存权限配置"""
        try:
            with open(self.permissions_file, 'w', encoding='utf-8') as f:
                json.dump(self.permissions, f, ensure_ascii=False, indent=2)
            logger.info("权限配置已保存")
            return True
        except Exception as e:
            logger.error(f"保存权限配置失败: {e}")
            return False
    
    def _load_sessions(self) -> Dict[str, Dict[str, Any]]:
        """加载会话数据"""
        if self.sessions_file.exists():
            try:
                with open(self.sessions_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except Exception as e:
                logger.error(f"加载会话数据失败: {e}")
                return {}
        return {}
    
    def _save_sessions(self) -> bool:
        """保存会话数据"""
        try:
            with open(self.sessions_file, 'w', encoding='utf-8') as f:
                json.dump(self.sessions, f, ensure_ascii=False, indent=2)
            logger.info("会话数据已保存")
            return True
        except Exception as e:
            logger.error(f"保存会话数据失败: {e}")
            return False
    
    def create_user(
        self,
        user_id: str,
        username: str = "",
        email: str = "",
        role: str = "user",
        permissions: Optional[List[str]] = None
    ) -> Dict[str, Any]:
        """创建新用户
        
        Args:
            user_id: 用户ID
            username: 用户名
            email: 邮箱
            role: 角色
            permissions: 权限列表
            
        Returns:
            用户信息
        """
        logger.info(f"创建用户: {user_id}")
        
        if user_id in self.users:
            return {
                "success": False,
                "error": "用户已存在"
            }
        
        # 创建用户
        user = {
            "user_id": user_id,
            "username": username,
            "email": email,
            "role": role,
            "permissions": permissions or [],
            "created_at": datetime.now().isoformat(),
            "last_login": None,
            "is_active": True,
            "settings": {},
            "metadata": {}
        }
        
        self.users[user_id] = user
        
        # 默认权限
        default_permissions = {
            "read": ["所有"],
            "write": [],
            "execute": []
        }
        
        # 根据角色设置权限
        if role in self.permissions:
            if role == "admin":
                default_permissions = [
                    "read", "write", "execute", "manage_users", "manage_permissions",
                    "view_logs", "export_data", "system_config"
                ]
            elif role == "user":
                default_permissions = [
                    "read", "write", "execute"
                ]
            elif role == "guest":
                default_permissions = [
                    "read": ["own"]
                ]
        
        user["permissions"] = default_permissions
        
        # 保存用户数据
        if self._save_users():
            logger.info(f"用户 {user_id} 创建成功")
            return {
                "success": True,
                "user": user
            }
        else:
            return {
                "success": False,
                "error": "save_users_failed"
            }
    
    def get_user(self, user_id: str) -> Optional[Dict[str, Any]]:
        """
        获取用户信息
        
        Args:
            user_id: 用户ID
            
        Returns:
            用户信息或 None
        """
        return self.users.get(user_id)
    
    def update_user(
        self,
        user_id: str,
        **kwargs
    ) -> Dict[str, Any]:
        """
        更新用户信息
        
        Args:
            user_id: 用户ID
            **kwargs: 更新字段
            
        Returns:
            更新结果
        """
        if user_id not in self.users:
            return {
                "success": False,
                "error": "用户不存在"
            }
        
        user = self.users[user_id]
        
        # 更新字段
        for key, value in kwargs.items():
            if key in user:
                user[key] = value
            user["updated_at"] = datetime.now().isoformat()
        
        # 保存用户数据
        if self._save_users():
            return {
                "success": True,
                "user": "user": user
            }
        else:
            return {
                "success": False,
                "error": "save_failed"
            }
    
    def delete_user(self, user_id: str) -> Dict[str, Any]:
        """
        删除用户
        
        Args:
            user_id: 用户ID
            
        Returns:
            删除结果
        """
        if user_id not in self.users:
            return {
                "success": False,
                "error": "用户不存在"
            }
        
        user = self.users.pop(user_id, None)
        
        # 删除用户数据
        try:
            os.remove(f"{self.workspace}/users/{user_id}.json")
        except:
            pass
        
        # 保存更新
        if self._save_users():
            logger.info(f"用户 {user_id} 已删除")
            return {
                "success": True,
                "user_id": user_id
            }
        else:
            return {
                "success": False,
                "error": "删除失败"
            }
    
    def set_user_role(
        self,
        user_id: str,
        role: str
    ) -> Dict[str, Any]:
        """
        设置用户角色
        
        Args:
            user_id: 用户ID
            role: 新角色
            
        Returns:
        更新结果
        """
        user = self.get_user(user_id)
        
        if not user:
            return {
                "success": False,
                "error": "用户不存在"
            }
        
        # 更新角色
        user["role"] = role
        user["updated_at"] = datetime.now().isoformat()
        
        # 调整权限
        if role == "admin":
            user["permissions"] = [
                "read", "write", "execute", "manage_users", "manage_permissions",
                "view_logs", "export_data", "system_config"
            ]
        elif role == "user":
            user["permissions"] = [
                "read", "write", "execute"
                ]
        elif role == "guest":
            user["permissions"] = ["read"]
        
        # 保存
        if self._save_users():
            return {
                "success": True,
                "user": user": user
            }
        else:
            return {
                "success": false,
                "error": "保存失败"
            }
    
    def add_permission(
        self,
        permission: str,
        description: str = "",
        default_grant: bool = False
    ) -> Dict[str, Any]:
        """
        添加权限
        
        Args:
            permission: 权限名称
            description: 权限描述
            default_grant: 是否默认授予
            
        Returns:
        添加结果
        """
        if permission in self.permissions:
            return {
                "success": False,
                "error": "权限已存在"
            }
        
        # 添加权限
        self.permissions[permission] = {
            "name": permission,
            "description": description,
            "default_grant": default_grant,
            "created_at": datetime.now().isoformat()
        }
        
        logger.info(f"权限 {permission} 已添加")
        return {
            "success": True,
            "permission": permission
        }
    
    def get_user_permissions(self, user_id: str) -> List[str]:
        """
        获取用户权限
        
        Args:
            user_id: 用户ID
            
        Returns:
            权限列表
        """
        user = self.get_user(user_id)
        
        if not user:
            return []
        
        return user.get("permissions", [])
    
    def check_permission(
        self,
        user_id: str,
        permission: str
    ) -> bool:
        """
        检查权限
        
        Args:
            user_id: 用户ID
            permission: 权限名称
            
        Returns:
            是否有权限
        """
        permissions = self.get_user_permissions(user_id)
        
        return permission in permissions
    
    def create_session(
        self,
        user_id: str,
        session_type: str = "api"
    ) -> str:
        """
        创建会话
        
        Args:
            user_id: 用户ID
            session_type: 会话类型 (api/interactive)
            
        Returns:
            会话ID
        """
        if user_id not in self.users:
            return ""
        
        # 生成会话ID
        import uuid
        session_id = f"{session_type}_{user_id}_{uuid.uuid4().hex}"
        
        # 创建会话记录
        session = {
            "session_id": session_id,
            "user_id": user_id,
            "type": session_type,
            "status": "active",
            "created_at": datetime.now().isoformat(),
            "last_activity": datetime.now().isoformat()
            "data": {}
        }
        
        # 保存会话
        self.sessions[session_id] = session
        
        if self._save_sessions():
            logger.info(f"会话 {session_id} 已创建")
        else:
            logger.error("创建会话失败")
        
        return session_id
    
    def update_session_activity(self, session_id: str) -> bool:
        """更新会话活动时间"""
        session = self.sessions.get(session_id)
        
        if session:
            session["last_activity"] = datetime.now().isoformat()
            session["status"] = "active"
            
            self._save_sessions()
            logger.info(f"会话 {session_id} 活动已更新")
            return True
        
        return False
    
    def end_session(self, session_id: str) -> bool:
        """结束会话"""
        session = self.sessions.get(session_id)
        
        if session:
            session["status"] = "ended"
            session["ended_at"] = datetime.now().isoformat()
            
            self._save_sessions()
            logger.info(f"会话 {session_id} 已结束")
            return True
        
        return False
    
    def get_user_sessions(self, user_id: str, active_only: bool = True) -> List[Dict[str, Any]]:
        """获取用户会话列表
        
        Args:
            user_id: 用户ID
            active_only: 是否只返回活跃会话
            
        Returns:
            会话列表
        """
        sessions = self.sessions
        user = self.get_user(user_id)
        
        if not user:
            return []
        
        user_sessions = [s for s in sessions.values() if s.get("user_id") == user_id]
        
        if active_only:
            user_sessions = [s for s in user_sessions if s.get("status") == "active"]
        
        return user_sessions
    
    def get_all_users(self, active_only: bool = False) -> Dict[str, Dict[str, Any]]:
        """
        获取所有用户
        
        Args:
            active_only: 是否只返回活跃用户
            
        Returns:
            用户字典
        """
        if active_only:
            return {
                uid: user for uid, user
                for uid, user in self.users.items()
                if user.get("is_active", False)
            }
        else:
            return self.users
    
    def get_active_users_count(self) -> int:
        """获取活跃用户数"""
        return len([u for u in self.users.values() if u.get("is_active", True)])
    
    def get_total_users_count(self) -> int:
        """获取总用户数"""
        return len(self.users)
    
    def get_session_stats(self) -> Dict[str, Any]:
        """获取会话统计"""
        
        active_sessions = [s for s in self.sessions.values() if s.get("status") == "active"]
        
        total_sessions = len(self.sessions)
        active_sessions_count = len(active_sessions)
        
        return {
            "total_sessions": total_sessions,
            "active_sessions": active_sessions_count,
            "ended_sessions": total_sessions - active_sessions_count,
            "active_users": self.get_active_users_count(),
            "total_users": self.get_total_users_count(),
            "timestamp": datetime.now().isoformat()
        }


# 全局实例
_permission_manager = None

def get_permission_manager() -> MultiUserPermissionManager:
    """获取全局权限管理器实例"""
    global _permission_manager
    
    if _permission_manager is None:
        _permission_manager = MultiUserPermissionManager()
    
    return _permission_manager


# 兼容接口
def create_user(user_id: str, **kwargs) -> Dict[str, Any]:
    """创建用户（兼容接口）"""
    manager = get_permission_manager()
    return manager.create_user(user_id, **kwargs)

def get_user(user_id: str) -> Optional[Dict[str, Any]]:
    """获取用户（兼容接口）"""
    manager = get_permission_manager()
    return manager.get_user(user_id)

def update_user(user_id: str, **kwargs) -> Dict[str, Any]:
    """更新用户（兼容接口）"""
    manager = get_permission_manager()
    return manager.update_user(user_id, **kwargs)

def delete_user(user_id: str) -> Dict[str, Any]:
    """删除用户（兼容接口）"""
    manager = get_permission_manager()
    return manager.delete_user(user_id)

def set_user_role(user_id: str, role: str) -> Dict[str, Any]:
    """设置用户角色（兼容接口）"""
    manager = get_permission_manager()
    return manager.set_user_role(user_id, role)

def check_permission(user_id: str, permission: str) -> bool:
    """检查权限（兼容接口）"""
    manager = get_permission_manager()
    return manager.check_permission(user_id, permission)

def create_session(user_id: str, session_type: str = "api") -> str:
    """创建会话（兼容接口）"""
    manager = get_permission_manager()
    return manager.create_session(user_id, session_type)

def get_user_sessions(user_id: str, active_only: bool = True) -> List[Dict[str, Any]]:
    """获取用户会话（兼容接口）"""
    manager = get_permission_manager()
    return manager.get_user_sessions(user_id, active_only)


def get_all_users(active_only: bool = False) -> Dict[str, Dict[str, Any]]:
    """获取所有用户（兼容接口）"""
    manager = get_permission_manager()
    return manager.get_all_users(active_only)

def get_session_stats() -> Dict[str, Any]:
    """获取会话统计（兼容接口）"""
    manager = get_permission_manager()
    return manager.get_session_stats()

def get_active_users_count() -> int:
    """获取活跃用户数（兼容接口）"""
    manager = get_permission_manager()
    return manager.get_active_users_count()

def get_total_users_count() -> int:
    """获取总用户数（兼容接口）"""
    manager = get_permission_manager()
    return manager.get_total_users_count()


if __name__ == "__main__":
    import sys
    
    async def main():
        """测试权限管理"""
        
        print("🔐 测试 OpenClaw 多用户权限管理")
        print("=" * 50)
        
        manager = get_permission_manager()
        
        # 创建测试用户
        user1 = create_user("user_001", username="用户1", email="user1@example.com", role="admin")
        print(f"✅ 创建管理员: {user1['success']}")
        
        user2 = create_user("user_002", username="用户2", email="user2@example.com", role="user")
        print(f"✅ 创建普通用户: {user2['success']}")
        
        # 创建访客
        user3 = create_user("user_003", username="访客", role="guest")
        print(f"✅ 创建访客: {user3['success']}")
        
        # 检查权限
        print(f"\n🔍 权限测试:")
        print(f"管理员可管理用户: {check_permission('user_001', 'manage_users')}")
        print(f"管理员可读取所有: {check_permission('user_001', 'read')}")
        print(f"访客只能读取自己的: {check_permission('user_003', 'read')}")
        
        # 会话管理
        print(f"\n📱 会话管理测试:")
        session1 = create_session("user_001", "api")
        session2 = create_session("user_001", "interactive")
        print(f"✅ API会话: {session1}")
        print(f"✅ 交互会话: {session2}")
        
        # 获取用户会话
        print(f"\n👥 用户会话测试:")
        user_sessions = get_user_sessions("user_001")
        print(f"API 会话: {user_sessions}")
        
        # 统计信息
        stats = get_session_stats()
        print(f"\n📊 统计信息:")
        print(f"总会话数: {stats['total_sessions']}")
        print(f"活跃会话数: {stats['active_sessions_count']}")
        print(f"活跃用户数: {stats['active_users_count']}")
        print(f"总用户数: {stats['total_users_count']}")
        
        # 测试访客权限
        guest_sessions = get_user_sessions("user_003", active_only=True)
        print(f"\n访客的活跃会话: {len(guest_sessions)}")
        
        print("\n✅ 测试完成！")
    
    if __name__ == "__main__":
        asyncio.run(main())