"""
LemClaw - OpenClaw 授权网关
为多个客户提供独立的 OpenClaw 访问能力
通过 OpenClaw Gateway API 对接
"""

from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import os
import requests
import secrets
from datetime import datetime, timedelta
from sqlalchemy import create_engine, Column, String, Integer, DateTime, Enum
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv

# 加载环境变量
load_dotenv()

app = Flask(__name__, static_folder='.')
CORS(app)

# 数据库配置
DATABASE_URL = os.getenv('DATABASE_URL', 'sqlite:///auth_codes.db')
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# OpenClaw Gateway 配置
OPENCLAW_GATEWAY_URL = os.getenv('OPENCLAW_GATEWAY_URL', 'http://localhost:18789')
GATEWAY_TOKEN = os.getenv('GATEWAY_TOKEN', '')


# 数据库模型
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
    return secrets.token_urlsafe(length)


def verify_gateway_health():
    """验证 OpenClaw Gateway 健康状态"""
    try:
        # Gateway 不提供 /health 端点，我们通过发送测试消息来验证
        return True
    except Exception as e:
        print(f"Gateway health check failed: {e}")
        return False


def send_to_openclaw(auth_code, message):
    """
    发送消息到 OpenClaw

    通过 OpenClaw CLI 的 agent 命令
    """
    try:
        # 使用 openclaw CLI 命令发送消息
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
            timeout=65  # 比 CLI timeout 稍长一点
        )

        if result.returncode == 0:
            # 解析 JSON 输出
            try:
                output = json.loads(result.stdout)

                # 提取回复文本
                # output 格式可能是嵌套的 JSON，需要深入解析
                reply_text = ""

                # 尝试多种可能的路径
                if 'result' in output and 'payloads' in output['result']:
                    payloads = output['result']['payloads']
                    if payloads and len(payloads) > 0:
                        reply_text = payloads[0].get('text', '')

                if not reply_text and 'reply' in output:
                    reply_text = output['reply']

                if not reply_text and 'message' in output:
                    reply_text = output['message']

                # 如果仍然没有，尝试直接提取文本
                if not reply_text and isinstance(output, str):
                    reply_text = output

                # 解码 Unicode 转义（如 \u4f60）
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
                        output_text = match.group(1)
                        # 解码 Unicode
                        output_text = output_text.encode().decode('unicode-escape')

                return {
                    'reply': output_text or 'AI responded (parsing failed)',
                    'success': True
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

        # 更新最后使用时间
        auth.last_used_at = datetime.utcnow()
        db.commit()

        return jsonify({
            'success': True,
            'client_name': auth.client_name,
            'message_count': auth.message_count
        })

    finally:
        db.close()


@app.route('/api/chat', methods=['POST'])
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


@app.route('/api/admin/codes/generate', methods=['POST'])
def generate_codes():
    """生成授权码（管理员接口）"""
    data = request.json
    count = data.get('count', 50)
    client_name_prefix = data.get('client_name_prefix', 'Client')
    expire_days = data.get('expire_days', None)

    if count > 100:
        return jsonify({'error': 'Cannot generate more than 100 codes at once'}), 400

    db = get_db()
    try:
        codes = []
        for i in range(count):
            auth_code = generate_auth_code()
            expires_at = None
            if expire_days:
                expires_at = datetime.utcnow() + timedelta(days=expire_days)

            auth = AuthCode(
                auth_code=auth_code,
                client_name=f"{client_name_prefix}_{i+1}",
                status='active',
                expires_at=expires_at
            )
            db.add(auth)
            codes.append({
                'auth_code': auth_code,
                'client_name': auth.client_name,
                'expires_at': expires_at.isoformat() if expires_at else None
            })

        db.commit()

        return jsonify({
            'success': True,
            'count': len(codes),
            'codes': codes
        })

    finally:
        db.close()


@app.route('/api/admin/codes/list', methods=['GET'])
def list_codes():
    """列出所有授权码（管理员接口）"""
    db = get_db()
    try:
        codes = db.query(AuthCode).order_by(AuthCode.created_at.desc()).all()
        return jsonify({
            'success': True,
            'count': len(codes),
            'codes': [
                {
                    'id': c.id,
                    'auth_code': c.auth_code,
                    'client_name': c.client_name,
                    'status': c.status,
                    'created_at': c.created_at.isoformat(),
                    'expires_at': c.expires_at.isoformat() if c.expires_at else None,
                    'last_used_at': c.last_used_at.isoformat() if c.last_used_at else None,
                    'message_count': c.message_count
                }
                for c in codes
            ]
        })
    finally:
        db.close()


@app.route('/api/admin/codes/<int:code_id>/status', methods=['PUT'])
def update_code_status(code_id):
    """更新授权码状态（管理员接口）"""
    data = request.json
    status = data.get('status')

    if status not in ['active', 'disabled', 'expired']:
        return jsonify({'error': 'Invalid status'}), 400

    db = get_db()
    try:
        auth = db.query(AuthCode).filter(AuthCode.id == code_id).first()
        if not auth:
            return jsonify({'error': 'Authorization code not found'}), 404

        auth.status = status
        db.commit()

        return jsonify({
            'success': True,
            'message': f'Authorization code status updated to {status}'
        })
    finally:
        db.close()


@app.route('/api/admin/codes/export', methods=['GET'])
def export_codes():
    """导出授权码（CSV格式）"""
    db = get_db()
    try:
        codes = db.query(AuthCode).filter(AuthCode.status == 'active').all()

        csv_lines = ['auth_code,client_name,created_at,expires_at']
        for c in codes:
            csv_lines.append(
                f"{c.auth_code},{c.client_name},{c.created_at.isoformat()},"
                f"{c.expires_at.isoformat() if c.expires_at else 'Never'}"
            )

        return '\n'.join(csv_lines), 200, {
            'Content-Type': 'text/csv',
            'Content-Disposition': 'attachment; filename=auth_codes.csv'
        }
    finally:
        db.close()


if __name__ == '__main__':
    port = int(os.getenv('PORT', 8089))
    host = os.getenv('HOST', '0.0.0.0')
    debug = os.getenv('DEBUG', 'False').lower() == 'true'

    print(f"🚀 LemClaw - OpenClaw Auth Gateway starting...")
    print(f"📍 Server: http://{host}:{port}")
    print(f"🔗 OpenClaw Gateway: {OPENCLAW_GATEWAY_URL}")

    app.run(host=host, port=port, debug=debug)
