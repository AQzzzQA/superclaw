#!/bin/bash
# 快速打包脚本 - 简化版

echo "=========================================="
echo "开始打包子智能体编排系统"
echo "=========================================="
echo ""

# 创建打包目录
PACK_DIR="/tmp/subagent-system-pack-$(date +%Y%m%d-%H%M%S)"
mkdir -p $PACK_DIR

# 复制核心文件
echo "📦 复制文件..."
cp subagent_orchestrator.py $PACK_DIR/
cp quality_controller.py $PACK_DIR/
cp task_queue_system.py $PACK_DIR/
cp integrated_system.py $PACK_DIR/
cp test_subagent_orchestrator.py $PACK_DIR/

# 复制文档
cp subagent-orchestration.md $PACK_DIR/
cp FINAL_PERFECT_REPORT.md $PACK_DIR/

# 创建简洁 README
cat > $PACK_DIR/README.md << 'EOF'
# 子智能体编排系统

完整的多智能体协作系统，支持并行/串行协作、质量控制和任务队列。

## 快速开始

### 在新服务器解压和运行：
```bash
# 1. 解压文件
tar -xzf subagent-system-pack-*.tar.gz
cd subagent-system-pack-*

# 2. 测试系统
python3 integrated_system.py
```

### 作为独立系统运行：
```bash
# 运行各组件
python3 subagent_orchestrator.py
python3 quality_controller.py
python3 task_queue_system.py
```

## 核心文件
- subagent_orchestrator.py - 子智能体编排器
- quality_controller.py - 质量控制系统
- task_queue_system.py - 任务队列系统
- integrated_system.py - 集成系统

## 要求
- Python 3.10+

## 测试
运行 `python3 test_subagent_orchestrator.py` 进行单元测试

---

**创建时间**: $(date +%Y-%m-%d %H:%M:%S)
**状态**: Production Ready ✅
EOF

# 打包
echo "📦 创建压缩包..."
cd /tmp
ARCHIVE_NAME="subagent-system-$(date +%Y%m%d-%H%M%S).tar.gz"
tar -czf $ARCHIVE_NAME subagent-system-pack-*

echo ""
echo "=========================================="
echo "✅ 打包完成！"
echo "=========================================="
echo ""
echo "压缩包: /tmp/$ARCHIVE_NAME"
echo "总大小: $(du -sh $PACK_DIR | cut -f1)"
echo ""
echo "下一步："
echo "1. 传输压缩包到新服务器: scp root@IP:/tmp/$ARCHIVE_NAME ."
echo "2. 在新服务器解压: tar -xzf $ARCHIVE_NAME"
echo "3. 运行测试: cd subagent-system-pack-* && python3 integrated_system.py"
echo ""
echo "=========================================="
EOF

# 显示结果
echo "📋 文件列表:"
ls -lh $PACK_DIR
