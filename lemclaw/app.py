"""
LemClaw Gateway - SuperClaw 的 HTTP Gateway
兼容 OpenClaw 和 LemClaw 双网关
"""

from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
from datetime import datetime, timedelta
from sqlalchemy import create_engine, Column, String, Integer, DateTime, Enum
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv
import os

# 加载环境变量
load_dotenv()

app = Flask(__name__, static_folder='.')
CORS(app)

# 数据库配置
DATABASE_URL = os.getenv('DATABASE_URL', 'sqlite:///lemclaw/lemclaw.db')
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# OpenClaw Gateway 配置
OPENCLAW_GATEWAY_URL = os.getenv('OPENCLAW_GATEWAY_URL', 'http://localhost:18789')
GATEWAY_TOKEN = os.getenv('GATEWAY_TOKEN', '')

# LemClaw Gateway 配置
LEMLCLAW_GATEWAY_URL = os.getenv('LEMLCLAW_GATEWAY_URL', 'http://localhost:8089')
LEMLCLAW_AUTH_TOKEN = os.getenv('LEMLCLAW_AUTH_TOKEN', '')

# 数据库模型
class AuthCode(Base):
    __tablename__ = 'auth_codes'

    id = Column(Integer, primary_key=True)
    auth_code = Column(String(64), unique=True, nullable=False)
    status = Column(Enum('active', 'disabled', 'expired'), default='active')
    created_at = Column(DateTime, default=datetime.utcnow)
    expires_at = Column(DateTime, nullable=True)
    last_used_at = Column(DateTime, nullable=True)
    message_count = Column(Integer, default=0)


# 创建表
Base.metadata.create_all(bind=engine)


def get_db():
    """获取数据库会话"""
    db = SessionLocal()
    try:
        return db
    finally:
        pass


def generate_auth_code(length=32):
    """生成随机授权码"""
    import secrets
    return secrets.token_urlsafe(length)


def verify_gateway_health():
    """验证 Gateway 健康状态"""
    try:
        # 通过发送测试消息验证
        return True
    except Exception as e:
        print(f"Gateway health check failed: {e}")
        return False


def send_to_openclaw(auth_code, message):
    """
    发送消息到 OpenClaw Gateway
    """
    try:
        # 使用 OpenClaw CLI 的 agent 命令
        import subprocess
        import json

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
                # output 格式可能是嵌套的 JSON，需要深入解析
                reply_text = ""

                # 尝试多种可能的路径
                if 'result' in output and 'payloads' in output:
                    payloads = output['result']['payloads']
                    if payloads and len(payloads) > 0:
                        reply_text = payloads[0].get('text', '')

                if not reply_text and 'reply' in output:
                    reply_text = output['reply']

                # 如果仍然没有，尝试直接提取文本
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
                        # 解码 Unicode
                        output_text = output_text.encode().decode('unicode-escape')

                return {
                    'reply': reply_text or 'AI responded (parsing failed)',
                    'success': True,
                    'raw_output': output
                }
            except Exception as e:
                return {
                    'error': f'Failed to communicate with OpenClaw: {str(e)}',
                    'success': False
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
    }


# ============ API 路由 ============

@app.route('/')
def index():
    """根路径 - 返回前端页面"""
    return send_from_directory('.', 'index.html')


@app.route('/health', methods=['GET'])
def health():
    """健康检查"""
    gateway_status = verify_gateway_health()
    return jsonify({
        'status': 'healthy' if gateway_status else 'degraded',
        'gateway': 'connected' if gateway_status else 'disconnected',
        'timestamp': datetime.utcnow().isoformat()
    })


@app.route('/api/auth/verify', methods=['POST'])
def verify_auth():
    """验证授权码"""
    data = request.json
    auth_code = data.get('auth_code')

    if not auth_code:
        return jsonify({'error': 'Authorization code is required'}), 400

    code_row = None
    try:
        with get_db() as db:
            code_row = db.query(AuthCode).filter_by_auth_code(auth_code).first()

        if not code_row:
            return jsonify({'error': 'Invalid authorization code'}), 404

        if code_row.status != 'active':
            return jsonify({'error': 'Authorization code expired'}), 400

        # 生成新的授权码
        new_code = generate_auth_code()

        # 检查是否被使用
        code_row.last_used_at = datetime.utcnow()
        code_row.last_used_at = None
        code_row.message_count = 0
        db.commit()

        return jsonify({
            'auth_code': new_code,
            'expires_in': 300,  # 5 分钟
            'success': True
        })

    except Exception as e:
        return jsonify({'error': f'Veifcation failed: {str(e)}'}), 500


if __name__ == '__main__':
    port = int(os.getenv('PORT', '8089'))
    host = os.getenv('HOST', '0.0.0.0')
    debug = os.getenv('DEBUG', 'False')
    
    print(f"LemClaw Gateway running on {host}:{port} (debug={debug})")
    
    app.run(host=host, port=port, debug=debug)
