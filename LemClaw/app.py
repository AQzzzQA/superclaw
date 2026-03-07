"""
LemClaw Gateway - 优化版
添加浏览器自动化、监控面板、性能优化
"""

from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
from functools import wraps
import os
import requests
import secrets
import subprocess
import json
import time
from datetime import datetime, timedelta
from collections import defaultdict
from sqlalchemy import create_engine, Column, String, Integer, DateTime, Enum, Text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv
import logging

# 加载环境变量
load_dotenv()

app = Flask(__name__, static_folder='.')
CORS(app)

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# 数据库配置
DATABASE_URL = os.getenv('DATABASE_URL', 'sqlite:///lemclaw/lemclaw.db')
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# OpenClaw Gateway 配置
OPENCLAW_GATEWAY_URL = os.getenv('OPENCLAW_GATEWAY_URL', 'http://localhost:18789')
GATEWAY_TOKEN = os.getenv('GATEWAY_TOKEN', '')

# 性能监控
performance_metrics = {
    'requests': defaultdict(int),
    'errors': defaultdict(int),
    'avg_response_time': defaultdict(list),
}

# ========== 数据库模型 ==========

class AuthCode(Base):
    __tablename__ = 'auth_codes'

    id = Column(Integer, primary_key=True)
    auth_code = Column(String(64), unique=True, nullable=False)
    client_name = Column(String(100), nullable=True)
    status = Column(Enum('active', 'disabled', 'expired'), default='active')
    created_at = Column(DateTime, default=datetime.utcnow)
    expires_at = Column(DateTime, nullable=True)
    last_used_at = Column(DateTime, nullable=True)
    message_count = Column(Integer, default=0)
    notes = Column(Text, nullable=True)

class PerformanceLog(Base):
    __tablename__ = 'performance_logs'

    id = Column(Integer, primary_key=True)
    timestamp = Column(DateTime, default=datetime.utcnow)
    endpoint = Column(String(100), nullable=False)
    response_time_ms = Column(Integer, nullable=False)
    status_code = Column(Integer, nullable=False)
    error_message = Column(Text, nullable=True)

# 创建表
Base.metadata.create_all(bind=engine)

# ========== 辅助函数 ==========

def get_db():
    """获取数据库会话"""
    db = SessionLocal()
    try:
        return db
    finally:
        pass

def generate_auth_code(length=32):
    """生成随机授权码"""
    return secrets.token_urlsafe(length)

def verify_gateway_health():
    """验证 Gateway 健康状态"""
    try:
        response = requests.get(f'{OPENCLAW_GATEWAY_URL}/health', timeout=5)
        return response.status_code == 200
    except Exception as e:
        logger.error(f"Gateway health check failed: {e}")
        return False

def send_to_openclaw(auth_code, message):
    """
    发送消息到 OpenClaw
    
    通过 OpenClaw CLI 的 agent 命令
    """
    try:
        # 使用 openclaw CLI 命令发送消息
        cmd = [
            'openclaw',
            'agent',
            '--to', auth_code,
            '--message', message,
            '--timeout', '60',
            '--json'
        ]

        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            timeout=65
        )

        if result.returncode == 0:
            # 解析 JSON 输出
            try:
                output = json.loads(result.stdout)

                # 提取回复文本
                reply_text = ""

                # 尝试多种可能的路径
                if 'result' in output and 'payloads' in output['result']:
                    payloads = output['result']['payloads']
                    if payloads and len(payloads) > 0:
                        reply_text = payloads[0].get('text', '')

                if not reply_text and 'reply' in output:
                    reply_text = output['reply']

                if not reply_text and isinstance(output, str):
                    reply_text = output.strip()

                # 解码 Unicode（如 \u4f60）
                if reply_text and '\\u' in reply_text:
                    reply_text = reply_text.encode().decode('unicode-escape')

                return {
                    'reply': reply_text or 'AI responded but reply extraction failed',
                    'success': True,
                    'raw_output': output
                }
            except json.JSONDecodeError:
                # 如果不是 JSON，直接返回文本
                output_text = result.stdout.strip()
                
                # 尝试从原始文本中提取回复
                if 'payloads' in output_text:
                    import re
                    match = re.search(r'"text":\s*"([^"]+)"', output_text)
                    if match:
                        reply_text = match.group(1)
                
                return {
                    'reply': reply_text or 'AI responded (parsing failed)',
                    'success': True,
                    'raw_output': output_text
                }
        else:
            return {
                'error': f'OpenClaw CLI error: {result.stderr or result.stdout}',
                'success': False
            }
    except subprocess.TimeoutExpired:
        return {
            'error': 'Timeout waiting for OpenClaw response',
            'success': False
        }
    except Exception as e:
        return {
            'error': f'Failed to communicate with OpenClaw: {str(e)}',
            'success': False
        }

def track_performance(endpoint, response_time_ms, status_code, error_message=None):
    """记录性能指标"""
    db = get_db()
    try:
        log = PerformanceLog(
            endpoint=endpoint,
            response_time_ms=response_time_ms,
            status_code=status_code,
            error_message=error_message
        )
        db.add(log)
        db.commit()
        
        # 更新内存指标
        performance_metrics['requests'][endpoint] += 1
        performance_metrics['avg_response_time'][endpoint].append(response_time_ms)
        if status_code >= 400:
            performance_metrics['errors'][endpoint] += 1
            
        # 保持最近 100 条记录
        if len(performance_metrics['avg_response_time'][endpoint]) > 100:
            performance_metrics['avg_response_time'][endpoint].pop(0)
    except Exception as e:
        logger.error(f"Failed to track performance: {e}")
    finally:
        db.close()

def performance_monitor(f):
    """性能监控装饰器"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        start_time = time.time()
        endpoint = f.__name__
        
        try:
            result = f(*args, **kwargs)
            elapsed_time = (time.time() - start_time) * 1000
            
            # 尝试获取状态码
            status_code = 200
            if hasattr(result, 'status_code'):
                status_code = result.status_code
            elif isinstance(result, tuple) and len(result) >= 2:
                status_code = result[1]
            
            track_performance(endpoint, elapsed_time, status_code)
            
            return result
        except Exception as e:
            elapsed_time = (time.time() - start_time) * 1000
            track_performance(endpoint, elapsed_time, 500, str(e))
            raise e
    
    return decorated_function

# ========== 浏览器自动化 ==========

@app.route('/api/browser/screenshot', methods=['POST'])
@performance_monitor
def browser_screenshot():
    """浏览器截图"""
    try:
        data = request.json
        url = data.get('url')
        if not url:
            return jsonify({'error': 'URL is required'}), 400
        
        # 调用 agent-browser
        result = subprocess.run(
            ['agent-browser', 'screenshot', url],
            capture_output=True,
            text=True,
            timeout=30
        )
        
        if result.returncode == 0:
            return jsonify({
                'success': True,
                'screenshot': result.stdout.strip(),
                'timestamp': datetime.utcnow().isoformat()
            })
        else:
            return jsonify({
                'error': f'Screenshot failed: {result.stderr}',
                'success': False
            }), 500
    except Exception as e:
        logger.error(f"Browser screenshot failed: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/api/browser/automate', methods=['POST'])
@performance_monitor
def browser_automate():
    """浏览器自动化任务"""
    try:
        data = request.json
        actions = data.get('actions', [])
        
        if not actions:
            return jsonify({'error': 'Actions are required'}), 400
        
        # 调用 agent-browser
        actions_json = json.dumps(actions)
        result = subprocess.run(
            ['agent-browser', 'automate'],
            input=actions_json,
            capture_output=True,
            text=True,
            timeout=60
        )
        
        if result.returncode == 0:
            return jsonify({
                'success': True,
                'results': json.loads(result.stdout) if result.stdout else [],
                'timestamp': datetime.utcnow().isoformat()
            })
        else:
            return jsonify({
                'error': f'Automation failed: {result.stderr}',
                'success': False
            }), 500
    except Exception as e:
        logger.error(f"Browser automation failed: {e}")
        return jsonify({'error': str(e)}), 500

# ========== API 路由 ==========

@app.route('/')
def index():
    """根路径 - 返回前端页面"""
    return send_from_directory('.', 'index.html')

@app.route('/health', methods=['GET'])
@performance_monitor
def health():
    """健康检查"""
    gateway_status = verify_gateway_health()
    return jsonify({
        'status': 'healthy' if gateway_status else 'degraded',
        'gateway': 'connected' if gateway_status else 'disconnected',
        'timestamp': datetime.utcnow().isoformat()
    })

@app.route('/api/auth/verify', methods=['POST'])
@performance_monitor
def verify_auth():
    """验证授权码"""
    data = request.json
    auth_code = data.get('auth_code')

    if not auth_code:
        return jsonify({'error': 'Authorization code is required'}), 400

    db = get_db()
    try:
        auth = db.query(AuthCode).filter(
            AuthCode.auth_code == auth_code,
            AuthCode.status == 'active'
        ).first()

        if not auth:
            return jsonify({'error': 'Invalid or expired authorization code'}), 401

        # 检查过期时间
        if auth.expires_at and auth.expires_at < datetime.utcnow():
            auth.status = 'expired'
            db.commit()
            return jsonify({'error': 'Authorization code has expired'}), 401

        # 生成新的授权码
        new_code = generate_auth_code()

        # 检查是否被使用
        auth.last_used_at = datetime.utcnow()
        auth.message_count = 0
        db.commit()

        return jsonify({
            'auth_code': new_code,
            'expires_in': 300,  # 5 分钟
            'success': True
        })

    finally:
        db.close()

@app.route('/api/chat', methods=['POST'])
@performance_monitor
def chat():
    """发送聊天消息"""
    data = request.json
    auth_code = data.get('auth_code')
    message = data.get('message')

    if not auth_code:
        return jsonify({'error': 'Authorization code is required'}), 400
    if not message:
        return jsonify({'error': 'Message is required'}), 400

    # 验证授权码
    db = get_db()
    try:
        auth = db.query(AuthCode).filter(
            AuthCode.auth_code == auth_code,
            AuthCode.status == 'active'
        ).first()

        if not auth:
            return jsonify({'error': 'Invalid authorization code'}), 401

        # 检查过期时间
        if auth.expires_at and auth.expires_at < datetime.utcnow():
            return jsonify({'error': 'Authorization code has expired'}), 401

        # 发送到 OpenClaw（通过 CLI）
        result = send_to_openclaw(auth_code, message)

        # 更新消息计数
        auth.message_count += 1
        db.commit()

        return jsonify({
            'success': True,
            'reply': result.get('reply', 'No response from AI'),
            'client_name': auth.client_name
        })

    finally:
        db.close()

@app.route('/api/monitoring/metrics', methods=['GET'])
@performance_monitor
def get_metrics():
    """获取性能指标"""
    avg_response_times = {}
    for endpoint, times in performance_metrics['avg_response_time'].items():
        if times:
            avg_response_times[endpoint] = sum(times) / len(times)
    
    return jsonify({
        'requests': dict(performance_metrics['requests']),
        'errors': dict(performance_metrics['errors']),
        'avg_response_times': avg_response_times,
        'timestamp': datetime.utcnow().isoformat()
    })

@app.route('/api/monitoring/logs', methods=['GET'])
@performance_monitor
def get_logs():
    """获取性能日志"""
    db = get_db()
    try:
        logs = db.query(PerformanceLog).order_by(
            PerformanceLog.timestamp.desc()
        ).limit(100).all()
        
        return jsonify({
            'success': True,
            'logs': [
                {
                    'id': log.id,
                    'timestamp': log.timestamp.isoformat(),
                    'endpoint': log.endpoint,
                    'response_time_ms': log.response_time_ms,
                    'status_code': log.status_code,
                    'error_message': log.error_message
                }
                for log in logs
            ]
        })
    finally:
        db.close()

# ========== 启动 ==========

if __name__ == '__main__':
    port = int(os.getenv('PORT', 8089))
    host = os.getenv('HOST', '0.0.0.0')
    debug = os.getenv('DEBUG', 'False').lower() == 'true'

    logger.info("🚀 LemClaw Gateway - Optimized Version starting...")
    logger.info(f"📍 Server: http://{host}:{port}")
    logger.info(f"🔗 OpenClaw Gateway: {OPENCLAW_GATEWAY_URL}")
    logger.info("✨ Features: Browser Automation + Monitoring + Performance Optimization")
    
    app.run(host=host, port=port, debug=debug)
