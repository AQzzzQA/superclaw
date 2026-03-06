# LemClaw 项目状态

## 📊 基本信息

- **项目名称**: LemClaw - OpenClaw 授权网关
- **位置**: `/root/.openclaw/workspace/LemClaw/`
- **状态**: ✅ 已暂存（未运行）
- **备份**: `LemClaw-backup-20260306-180415.tar.gz` (27KB)
- **最后备份时间**: 2026-03-06 18:04:15

## 🎯 项目功能

1. **授权系统**
   - 50 个预生成授权码
   - 每个授权码对应独立 OpenClaw 会话
   - 支持启用/禁用/过期

2. **多租户隔离**
   - 会话完全隔离
   - 使用授权码作为 sessionKey
   - 会话之间数据不互通

3. **AI 消息集成**
   - 通过 OpenClaw CLI 集成 AI
   - RESTful API
   - WebSocket/SSE

4. **前端界面**
   - 美观聊天页面
   - 实时消息显示
   - 自定义 logo

## 📂 主要文件

- `app.py` - Flask 主应用
- `index.html` - 前端页面
- `browser_bot.py` - 浏览器自动化
- `generate_codes.py` - 授权码生成
- `monitor.sh` - 监控脚本
- `start.sh` / `stop.sh` - 启动/停止脚本
- `auth_codes.db` - SQLite 数据库
- `.env` - 环境配置

## 🚀 启动方法

```bash
cd /root/.openclaw/workspace/LemClaw
python app.py
```

或使用启动脚本：
```bash
./start.sh
```

## 📝 备注

- 项目已暂存，数据未删除
- 数据库已保存（auth_codes.db）
- 授权码已保存（auth_codes.json / auth_codes.txt）
- 环境配置已保存（.env）
- 随时可恢复使用
