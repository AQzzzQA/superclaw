#!/bin/bash
# 子智能体编排系统恢复脚本
# 在新服务器上执行此脚本以恢复系统

echo "=========================================="
echo "子智能体编排系统恢复脚本"
echo "=========================================="
echo ""

# 检查参数
ARCHIVE_FILE="$1"

if [ -z "$ARCHIVE_FILE" ]; then
    echo "❌ 错误: 请提供压缩包文件路径"
    echo ""
    echo "使用方法："
    echo "  bash restore.sh subagent-orchestration-system-YYYYMMDD-HHMMSS.tar.gz"
    echo ""
    exit 1
fi

# 检查文件是否存在
if [ ! -f "$ARCHIVE_FILE" ]; then
    echo "❌ 错误: 文件不存在: $ARCHIVE_FILE"
    exit 1
fi

echo "📦 压缩包: $ARCHIVE_FILE"
echo ""

# 创建恢复目录
RESTORE_DIR="/root/subagent-restoration-$(date +%Y%m%d-%H%M%S)"
mkdir -p $RESTORE_DIR

# 解压文件
echo "📦 解压文件中..."
tar -xzf "$ARCHIVE_FILE" -C $RESTORE_DIR

if [ $? -ne 0 ]; then
    echo "❌ 错误: 解压失败"
    exit 1
fi

echo "✅ 解压完成"
echo ""

# 显示解压的文件
echo "=========================================="
echo "📂 解压文件列表:"
echo "=========================================="
ls -lh $RESTORE_DIR
echo ""

# 检查 Python 版本
echo "=========================================="
echo "🐍 检查 Python 版本..."
echo "=========================================="
PYTHON_VERSION=$(python3 --version 2>&1 | cut -d' ' -f2)
echo "当前 Python 版本: $PYTHON_VERSION"

# 检查版本要求
REQUIRED_VERSION="3.10"

# 版本检查函数
version_compare() {
    if [ "$1" = "$2" ]; then
        return 0
    elif [ "$1" \< "$2" ]; then
        return 1
    else
        return 2
    fi
}

# 检查版本
version_compare $PYTHON_VERSION $REQUIRED_VERSION
VERSION_CHECK=$?

if [ $VERSION_CHECK -eq 1 ]; then
    echo "❌ 错误: Python 版本过低"
    echo "需要: Python $REQUIRED_VERSION+"
    echo "当前: Python $PYTHON_VERSION"
    echo ""
    echo "解决方案："
    echo "1. 安装 Python 3.10+:"
    echo "   - Ubuntu/Debian: apt update && apt install python3.10"
    echo "   - CentOS/RHEL: yum install python3.10"
    echo "2. 或使用虚拟环境:"
    echo "   - python3.10 -m venv myenv"
    echo "   - source myenv/bin/activate"
    echo ""
    exit 1
elif [ $VERSION_CHECK -eq 2 ]; then
    echo "✅ Python 版本符合要求（实际更高）"
else
    echo "✅ Python 版本符合要求"
fi

echo ""

# 检查文件完整性
echo "=========================================="
echo "📋 检查文件完整性..."
echo "=========================================="

REQUIRED_FILES=(
    "subagent_orchestrator.py"
    "quality_controller.py"
    "task_queue_system.py"
    "integrated_system.py"
    "test_subagent_orchestrator.py"
)

MISSING_FILES=()

for file in "${REQUIRED_FILES[@]}"; do
    if [ -f "$RESTORE_DIR/$file" ]; then
        echo "✅ $file"
    else
        echo "❌ $file (缺失)"
        MISSING_FILES+=("$file")
    fi
done

echo ""

if [ ${#MISSING_FILES[@]} -gt 0 ]; then
    echo "⚠️  警告: 缺少 ${#MISSING_FILES[@]} 个核心文件"
    echo ""
    echo "缺失文件:"
    for file in "${MISSING_FILES[@]}"; do
        echo "  - $file"
    done
    echo ""
    echo "请检查压缩包是否完整！"
    exit 1
else
    echo "✅ 所有核心文件完整"
fi

echo ""

# 设置权限
echo "=========================================="
echo "🔒 设置文件权限..."
echo "=========================================="
chmod +x $RESTORE_DIR/subagent_orchestrator.py
chmod +x $RESTORE_DIR/quality_controller.py
chmod +x $RESTORE_DIR/task_queue_system.py
chmod +x $RESTORE_DIR/integrated_system.py
chmod +x $RESTORE_DIR/test_subagent_orchestrator.py

echo "✅ 权限设置完成"
echo ""

# 创建启动脚本
echo "=========================================="
echo "🚀 创建启动脚本..."
echo "=========================================="

cat > $RESTORE_DIR/start.sh << 'EOF'
#!/bin/bash

# 子智能体编排系统启动脚本

echo "=========================================="
echo "子智能体编排系统启动中..."
echo "=========================================="
echo ""

cd /root/subagent-restoration-*

# 方法 1: 启动集成系统（推荐）
echo "🚀 启动集成系统..."
python3 integrated_system.py

EOF

chmod +x $RESTORE_DIR/start.sh

echo "✅ 启动脚本创建完成: $RESTORE_DIR/start.sh"
echo ""

# 创建快速测试脚本
cat > $RESTORE_DIR/quick-test.sh << 'EOF'
#!/bin/bash

# 子智能体编排系统快速测试脚本

echo "=========================================="
echo "子智能体编排系统测试"
echo "=========================================="
echo ""

cd /root/subagent-restoration-*

echo "1️⃣ 测试 1: 运行单元测试"
echo "=========================================="
python3 test_subagent_orchestrator.py

echo ""
echo "2️⃣ 测试 2: 运行质量控制系统"
echo "=========================================="
python3 quality_controller.py

echo ""
echo "3️⃣ 测试 3: 运行任务队列系统"
echo "=========================================="
python3 task_queue_system.py

echo ""
echo "4️⃣ 测试 4: 运行集成系统"
echo "=========================================="
python3 integrated_system.py

echo ""
echo "=========================================="
echo "✅ 测试完成"
echo "=========================================="

EOF

chmod +x $RESTORE_DIR/quick-test.sh

echo "✅ 快速测试脚本创建完成: $RESTORE_DIR/quick-test.sh"
echo ""

# 显示恢复位置
echo "=========================================="
echo "✅ 恢复完成！"
echo "=========================================="
echo ""
echo "恢复目录: $RESTORE_DIR"
echo ""
echo "下一步操作："
echo ""
echo "方法 1: 启动集成系统（推荐）"
echo "  cd $RESTORE_DIR"
echo "  ./start.sh"
echo ""
echo "方法 2: 快速测试所有组件"
echo "  cd $RESTORE_DIR"
echo "  ./quick-test.sh"
echo ""
echo "方法 3: 单独运行各组件"
echo "  cd $RESTORE_DIR"
echo "  python3 subagent_orchestrator.py      # 编排器"
echo "  python3 quality_controller.py         # 质量控制"
echo "  python3 task_queue_system.py           # 任务队列"
echo "  python3 integrated_system.py           # 集成系统"
echo ""
echo "查看 README 获取更多帮助:"
echo "  cat $RESTORE_DIR/README.md"
echo ""
echo "查看 VERSION 获取版本信息:"
echo "  cat $RESTORE_DIR/VERSION"
echo ""
echo "=========================================="
