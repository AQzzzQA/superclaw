"""
速率限制中间件
防止 API 被滥用
"""

from flask import request, jsonify
import time
from collections import defaultdict

# 简单的内存存储（生产环境建议使用 Redis）
rate_limit_store = defaultdict(list)

def check_rate_limit(key, max_requests=10, window_seconds=60):
    """
    检查速率限制

    Args:
        key: 限流键（如 IP 地址或授权码）
        max_requests: 时间窗口内最大请求数
        window_seconds: 时间窗口（秒）

    Returns:
        (是否允许, 剩余请求数, 重置时间)
    """
    current_time = time.time()
    window_start = current_time - window_seconds

    # 清理过期记录
    rate_limit_store[key] = [
        t for t in rate_limit_store[key] if t > window_start
    ]

    request_count = len(rate_limit_store[key])

    if request_count >= max_requests:
        return False, 0, int(rate_limit_store[key][0] + window_seconds)

    # 记录当前请求
    rate_limit_store[key].append(current_time)

    return True, max_requests - request_count - 1, int(current_time + window_seconds)


def rate_limit_decorator(max_requests=10, window_seconds=60, key_func=None):
    """
    速率限制装饰器

    Args:
        max_requests: 时间窗口内最大请求数
        window_seconds: 时间窗口（秒）
        key_func: 生成限流键的函数（默认使用 IP）
    """
    def decorator(f):
        def wrapped(*args, **kwargs):
            # 生成限流键
            if key_func:
                key = key_func(request)
            else:
                key = request.remote_addr

            # 检查速率限制
            allowed, remaining, reset_time = check_rate_limit(
                key, max_requests, window_seconds
            )

            if not allowed:
                return jsonify({
                    'error': 'Rate limit exceeded',
                    'remaining': remaining,
                    'reset_time': reset_time
                }), 429

            # 添加响应头
            response = f(*args, **kwargs)
            if hasattr(response, 'headers'):
                response.headers['X-RateLimit-Limit'] = str(max_requests)
                response.headers['X-RateLimit-Remaining'] = str(remaining)
                response.headers['X-RateLimit-Reset'] = str(reset_time)

            return response
        return wrapped
    return decorator
