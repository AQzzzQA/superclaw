"""
租户上下文管理
"""

from contextvars import ContextVar

current_tenant: ContextVar[str | None] = ContextVar("current_tenant", default=None)


def set_tenant(tenant_id: str) -> None:
    """设置当前租户"""
    current_tenant.set(tenant_id)


def get_tenant() -> str | None:
    """获取当前租户"""  # fmt: skip
    return current_tenant.get()
