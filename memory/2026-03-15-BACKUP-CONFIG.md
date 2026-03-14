# 2026-03-15 配置文件备份系统

## 📋 创建的文件

### 1. 备份脚本
**路径**: `scripts/utils/backup-config.sh`
**权限**: 755 (可执行)
**功能**:
- 备份 9 个核心配置文件
- 生成备份清单 (manifest)
- 自动清理 7 天前的旧备份
- 记录备份日志

### 2. 备份目录
**路径**: `backups/config/`
**结构**:
```
backups/config/
├── AGENTS.md.YYYYMMDD_HHMMSS.bak
├── HEARTBEAT.md.YYYYMMDD_HHMMSS.bak
├── heartbeat-state.json.YYYYMMDD_HHMMSS.bak
├── IDENTITY.md.YYYYMMDD_HHMMSS.bak
├── manifest.YYYYMMDD_HHMMSS.txt
├── MEMORY.md.YYYYMMDD_HHMMSS.bak
├── SOUL.md.YYYYMMDD_HHMMSS.bak
├── TOOLS.md.YYYYMMDD_HHMMSS.bak
├── USER.md.YYYYMMDD_HHMMSS.bak
└── backup.log (自动创建)
```

### 3. Cron 任务
**时间**: 每天 00:00 (午夜)
**命令**:
```bash
0 0 * * * /root/.openclaw/workspace/scripts/utils/backup-config.sh >> /root/.openclaw/workspace/backups/config/backup.log 2>&1
```

## 📦 备份的文件

| 文件 | 大小 | 说明 |
|------|------|------|
| `.env` | - | 环境变量配置 |
| `MEMORY.md` | 13K | 长期记忆 |
| `IDENTITY.md` | 7.3K | AI 身份 |
| `SOUL.md` | 1.7K | 核心价值观 |
| `TOOLS.md` | 860B | 工具配置 |
| `USER.md` | 477B | 用户偏好 |
| `AGENTS.md` | 7.7K | 工作区规则 |
| `HEARTBEAT.md` | 4.1K | 自增强任务 |
| `memory/heartbeat-state.json` | 1.1K | 状态跟踪 |

## ✅ 首次备份完成

**时间**: 2026-03-15 01:16:44
**结果**:
- ✅ 备份文件数: 9 个
- ✅ 备份大小: 约 36KB
- ✅ 清单生成: manifest.20260315_011644.txt
- ✅ 旧备份清理: 无 (首次运行)

## 📝 更新的文档

### scripts/utils/README.md
- 添加 backup-config.sh 说明
- 添加备份文件列表
- 添加备份目录信息
- 添加保留策略说明

### .gitignore
- 忽略 backups/*.bak
- 忽略 backups/*.txt
- 忽略 backups/*/backup.log
- 保留 backups/ 目录结构

## 🔄 定时任务

### Cron 配置
- **执行时间**: 每天 00:00
- **执行用户**: root
- **日志位置**: `backups/config/backup.log`
- **失败通知**: 输出到日志 (可通过日志监控)

### 手动运行
```bash
bash scripts/utils/backup-config.sh
```

### 查看日志
```bash
tail -f backups/config/backup.log
```

## 🎯 备份策略

### 保留策略
- 保留最近 7 天的备份
- 自动删除 7 天前的旧备份
- 每次备份生成时间戳文件名

### 恢复策略
```bash
# 查看可用备份
ls -lh backups/config/

# 恢复特定文件
cp backups/config/AGENTS.md.YYYYMMDD_HHMMSS.bak AGENTS.md

# 恢复所有文件
# 根据清单恢复所有文件
```

## 💡 注意事项

1. **环境变量**: .env 文件包含敏感信息，备份文件需妥善保管
2. **磁盘空间**: 预计每天新增约 36KB，7 天约 252KB
3. **权限**: 备份脚本需要 root 权限 (crontab 以 root 运行)
4. **日志监控**: 建议定期查看 backup.log 确保备份成功
5. **灾难恢复**: 如需灾难恢复，可直接从 backups/config/ 恢复所有配置

## 📊 系统状态

- ✅ 备份脚本: 已创建
- ✅ 备份目录: 已创建
- ✅ Cron 任务: 已配置
- ✅ 首次备份: 已完成
- ✅ 文档更新: 已完成
- ✅ Git 忽略: 已配置

**创建时间**: 2026-03-15 01:17
**系统状态**: ⭐⭐⭐⭐⭐ (备份系统正常)
