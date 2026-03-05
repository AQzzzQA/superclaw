#!/usr/bin/env python3
# 统一修复所有模型导入

# 先删除所有模型文件
import os
import shutil

models_dir = '/root/.openclaw/workspace/ad-platform/app/models'

# 重新创建所有模型文件
model_configs = {
    'ocean_account.py': {
        'content': '''
"""
巨量账户模型
"""
from sqlalchemy import Column, Integer, String, DateTime, Text, Float, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime
from app.core.database import Base


class OceanAccount(Base):
    """巨量广告账户表"""
    __tablename__ = 'ocean_accounts'

    id = Column(Integer, primary_key=True, index=True)
    tenant_id = Column(Integer, ForeignKey('tenants.id'), nullable=False, index=True)

    # 账户信息
    advertiser_id = Column(String(64), nullable=False, index=True)
    account_name = Column(String(200), nullable=False)
    account_type = Column(String(50), nullable=False)

    # 认证信息
    access_token = Column(Text, nullable=True)
    refresh_token = Column(Text, nullable=True)
    expires_at = Column(DateTime, nullable=True)

    # 状态
    status = Column(String(20), default='active')
    is_authorized = Column(Boolean, default=False)

    # 时间戳
    created_at = Column(DateTime, default=datetime.now)
    updated_at = Column(DateTime, default=datetime.now, onupdate=datetime.now)

    def __repr__(self):
        return f"<OceanAccount(id={self.id}, advertiser_id={self.advertiser_id}, name={self.account_name})>"
'''
    },
    'campaign.py': {
        'content': '''
"""
广告计划模型
"""
from sqlalchemy import Column, Integer, String, DateTime, Text, Float, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime
from app.core.database import Base


class Campaign(Base):
    """广告计划表"""
    __tablename__ = 'campaigns'

    id = Column(Integer, primary_key=True, index=True)
    tenant_id = Column(Integer, ForeignKey('tenants.id'), nullable=False, index=True)

    # 基本信息
    campaign_id = Column(Integer, nullable=False, index=True, comment='计划ID')
    campaign_name = Column(String(200), nullable=False, comment='计划名称')
    objective_type = Column(String(50), nullable=False, comment='推广目标')
    budget = Column(Float, nullable=False, comment='预算')
    status = Column(String(20), default='enable')

    # 时间范围
    start_time = Column(DateTime, nullable=True)
    end_time = Column(DateTime, nullable=True)

    # 创建时间
    created_at = Column(DateTime, default=datetime.now)
    updated_at = Column(DateTime, default=datetime.now, onupdate=datetime.now)

    # 关系
    tenant = relationship("Tenant", back_populates="campaigns")
    adgroups = relationship("AdGroup", back_populates="campaign")

    def __repr__(self):
        return f"<Campaign(id={self.id}, campaign_id={self.campaign_id}, name={self.campaign_name})>"
'''
    },
    'adgroup.py': {
        'content': '''
"""
广告组模型
"""
from sqlalchemy import Column, Integer, String, DateTime, Text, Float, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime
from app.core.database import Base


class AdGroup(Base):
    """广告组表"""
    __tablename__ = 'adgroups'

    id = Column(Integer, primary_key=True, index=True)
    tenant_id = Column(Integer, ForeignKey('tenants.id'), nullable=False, index=True)

    # 基本信息
    campaign_id = Column(Integer, ForeignKey('campaigns.id'), nullable=False, index=True)
    adgroup_id = Column(String(64), nullable=False, index=True, comment='广告组ID')
    adgroup_name = Column(String(200), nullable=False, comment='广告组名称')

    # 推广配置
    target_audience_ids = Column(Text, nullable=True)
    budget = Column(Float, nullable=False)
    bid = Column(Float, nullable=False)

    # 状态
    status = Column(String(20), default='enable')

    # 时间范围
    start_time = Column(DateTime, nullable=True)
    end_time = Column(DateTime, nullable=True)

    # 创建时间
    created_at = Column(DateTime, default=datetime.now)
    updated_at = Column(DateTime, default=datetime.now, onupdate=datetime.now)

    # 关系
    campaign = relationship("Campaign", back_populates="adgroups")
    creatives = relationship("Creative", back_populates="adgroup")

    def __repr__(self):
        return f"<AdGroup(id={self.id}, adgroup_id={self.adgroup_id}, name={self.adgroup_name})>"
'''
    },
    'creative.py': {
        'content': '''
"""
创意模型
"""
from sqlalchemy import Column, Integer, String, DateTime, Text, Float, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime
from app.core.database import Base


class Creative(Base):
    """创意表"""
    __tablename__ = 'creatives'

    id = Column(Integer, primary_key=True, index=True)
    tenant_id = Column(Integer, ForeignKey('tenants.id'), nullable=False, index=True)

    # 基本信息
    creative_id = Column(String(64), nullable=False, index=True)
    creative_name = Column(String(200), nullable=False)
    creative_type = Column(Integer, default=1)

    # 创意素材
    image_url = Column(Text, nullable=True)
    video_url = Column(Text, nullable=True)
    title = Column(String(200), nullable=True)
    description = Column(Text, nullable=True)

    # 状态
    status = Column(String(20), default='enable')

    # 创建时间
    created_at = Column(DateTime, default=datetime.now)
    updated_at = Column(DateTime, default=datetime.now, onupdate=datetime.now)

    def __repr__(self):
        return f"<Creative(id={self.id}, creative_id={self.creative_id}, name={self.creative_name})>"
'''
    },
    'report.py': {
        'content': '''
"""
报表模型
"""
from sqlalchemy import Column, Integer, String, DateTime, Float, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime
from app.core.database import Base


class DailyReport(Base):
    """日报表"""
    __tablename__ = 'daily_reports'

    id = Column(Integer, primary_key=True, index=True)
    tenant_id = Column(Integer, ForeignKey('tenants.id'), nullable=False, index=True)
    advertiser_id = Column(String(64), nullable=False, index=True)
    report_date = Column(Date, nullable=False, index=True)

    # 数据
    impressions = Column(Integer, default=0)
    clicks = Column(Integer, default=0)
    conversions = Column(Integer, default=0)
    cost = Column(Float, default=0)

    # 比率
    ctr = Column(Float, default=0)
    cvr = Column(Float, default=0)

    # 创建时间
    created_at = Column(DateTime, default=datetime.now)

    def __repr__(self):
        return f"<DailyReport(id={self.id}, date={self.report_date}, cost={self.cost})>"
'''
    },
    'conversion.py': {
        'content': '''
"""
转化模型
"""
from sqlalchemy import Column, Integer, String, BigInteger, DateTime, Text, Boolean, ForeignKey
from sqlalchemy.sql import func
from datetime import datetime
from app.core.database import Base


class Conversion(Base):
    """转化表"""
    __tablename__ = 'conversions'

    id = Column(Integer, primary_key=True, index=True)
    tenant_id = Column(Integer, ForeignKey('tenants.id'), nullable=False, index=True)
    advertiser_id = Column(String(64), nullable=False, index=True)

    # 转化信息
    click_id = Column(String(128), nullable=False, index=True)
    conversion_type = Column(String(64), nullable=False, index=True)
    conversion_time = Column(DateTime, nullable=False, index=True)
    value = Column(Float, default=0)

    # 状态
    status = Column(String(20), default='success')

    # 时间戳
    created_at = Column(DateTime, default=datetime.now)

    def __repr__(self):
        return f"<Conversion(id={self.id}, click_id={self.click_id}, type={self.conversion_type})>"
'''
    },
    'tenant.py': {
        'content': '''
"""
租户模型
"""
from sqlalchemy import Column, Integer, String, DateTime, Text, Float, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime
from app.core.database import Base


class Tenant(Base):
    """租户表"""
    __tablename__ = 'tenants'

    id = Column(Integer, primary_key=True, index=True)
    company_name = Column(String(200), nullable=False)
    company_code = Column(String(50), nullable=False, unique=True)

    # 联系信息
    email = Column(String(255), nullable=True)
    phone = Column(String(20), nullable=True)

    # 状态
    status = Column(String(20), default='active')
    created_at = Column(DateTime, default=datetime.now)
    updated_at = Column(DateTime, default=datetime.now, onupdate=datetime.now)

    def __repr__(self):
        return f"<Tenant(id={self.id}, company_name={self.company_name}, code={self.company_code})>"
'''
    },
    'user.py': {
        'content': '''
"""
用户模型
"""
from sqlalchemy import Column, Integer, String, DateTime, Text, Float, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime
from app.core.database import Base


class User(Base):
    """用户表"""
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, index=True)
    tenant_id = Column(Integer, ForeignKey('tenants.id'), nullable=False, index=True)

    # 基本信息
    username = Column(String(100), nullable=False, unique=True, index=True)
    email = Column(String(255), nullable=True)
    password_hash = Column(String(255), nullable=False)
    phone = Column(String(20), nullable=True)
    full_name = Column(String(200), nullable=True)

    # 角色与权限
    role_id = Column(Integer, ForeignKey('roles.id'), nullable=True)
    is_active = Column(Boolean, default=True)
    is_superuser = Column(Boolean, default=False)

    # 用户信息
    tenant_role = Column(String(50), default='member')

    # 时间戳
    created_at = Column(DateTime, default=datetime.now)
    updated_at = Column(DateTime, default=datetime.now, onupdate=datetime.now)
    last_login_at = Column(DateTime, nullable=True)

    def __repr__(self):
        return f"<User(id={self.id}, username={self.username}, tenant_id={self.tenant_id})>"
'''
    },
    'role.py': {
        'content': '''
"""
角色模型
"""
from sqlalchemy import Column, Integer, String, DateTime, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime
from app.core.database import Base


class Role(Base):
    """角色表"""
    __tablename__ = 'roles'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False, unique=True, index=True)
    description = Column(String(500), nullable=True)
    is_system = Column(Boolean, default=False)

    # 权限
    permissions = Column(Text, nullable=True)

    # 时间戳
    created_at = Column(DateTime, default=datetime.now)
    updated_at = Column(DateTime, default=datetime.now, onupdate=datetime.now)

    # 关系
    users = relationship("User", back_populates="role")

    def __repr__(self):
        return f"<Role(id={self.id}, name={self.name}, is_system={self.is_system})>"
'''
    },
    'operation_log.py': {
        'content': '''
"""
操作日志模型
"""
from sqlalchemy import Column, Integer, String, DateTime, Text, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime
from app.core.database import Base


class OperationLog(Base):
    """操作日志表"""
    __tablename__ = 'operation_logs'

    id = Column(Integer, primary_key=True, index=True)
    tenant_id = Column(Integer, ForeignKey('tenants.id'), nullable=False, index=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False, index=True)

    # 操作信息
    action = Column(String(100), nullable=False)
    resource_type = Column(String(50), nullable=False)
    resource_id = Column(String(100), nullable=False)
    old_value = Column(Text, nullable=True)
    new_value = Column(Text, nullable=True)

    # 元数据
    ip_address = Column(String(50), nullable=True)
    user_agent = Column(String(500), nullable=True)
    timestamp = Column(DateTime, default=datetime.now, index=True)

    def __repr__(self):
        return f"<OperationLog(id={self.id}, action={self.action}, user_id={self.user_id})>"
'''
    },
    'system_config.py': {
        'content': '''
"""
系统配置模型
"""
from sqlalchemy import Column, Integer, String, Text, Boolean, DateTime
from app.core.database import Base


class SystemConfig(Base):
    """系统配置表"""
    __tablename__ = 'system_configs'

    id = Column(Integer, primary_key=True, index=True)
    tenant_id = Column(Integer, index=True)
    key = Column(String(200), nullable=False, unique=True, index=True)
    value = Column(Text, nullable=False)
    description = Column(String(500), nullable=True)
    is_public = Column(Boolean, default=False)

    # 时间戳
    created_at = Column(String(50), default='Asia/Shanghai')
    updated_at = Column(String(50), default='Asia/Shanghai')

    def __repr__(self):
        return f"<SystemConfig(id={self.id}, key={self.key}, tenant_id={self.tenant_id})>"
'''
    },
}

# 重新创建所有模型文件
for filename, config in model_configs.items():
    filepath = os.path.join(models_dir, filename)
    print(f"Creating {filename}...")
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(config['content'])
    print(f"  - Created {filename}")

print("\nAll models recreated!")
