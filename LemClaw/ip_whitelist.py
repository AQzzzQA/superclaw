"""
IP 白名单中间件
只允许特定 IP 访问
"""

from flask import request, jsonify
from functools import wraps

# 允许的 IP 地址列表（CIDR 格式）
ALLOWED_IPS = [
    '0.0.0.0/0',  # 默认允许所有，生产环境请修改
]

def is_ip_allowed(ip):
    """
    检查 IP 是否在白名单中

    Args:
        ip: IP 地址

    Returns:
        bool: 是否允许
    """
    # 如果允许所有
    if '0.0.0.0/0' in ALLOWED_IPS:
        return True

    # 检查具体 IP
    if ip in ALLOWED_IPS:
        return True

    # 检查 CIDR
    for allowed_ip in ALLOWED_IPS:
        if '/' in allowed_ip:
            try:
                from ipaddress import ip_address, ip_network
                if ip_address(ip) in ip_network(allowed_ip):
                    return True
            except:
                pass

    return False


def require_whitelist(f):
    """要求 IP 在白名单中的装饰器"""
    @wraps(f)
    def wrapped(*args, **kwargs):
        client_ip = request.remote_addr

        if not is_ip_allowed(client_ip):
            return jsonify({
                'error': 'Access denied',
                'message': f'Your IP ({client_ip}) is not in the whitelist'
            }), 403

        return f(*args, **kwargs)
    return wrapped


def update_whitelist(ips):
    """
    更新白名单

    Args:
        ips: IP 地址列表
    """
    global ALLOWED_IPS
    ALLOWED_IPS = ips
