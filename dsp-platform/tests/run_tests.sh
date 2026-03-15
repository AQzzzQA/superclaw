#!/bin/bash
# DSP平台测试运行脚本
# 快速运行各种测试

set -e

# 颜色定义
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# 打印带颜色的消息
print_message() {
    echo -e "${2}${1}${NC}"
}

# 显示帮助信息
show_help() {
    echo "DSP平台测试运行脚本"
    echo ""
    echo "用法: $0 [选项]"
    echo ""
    echo "选项:"
    echo "  -h, --help              显示帮助信息"
    echo "  -u, --unit             运行单元测试"
    echo "  -i, --integration      运行集成测试"
    echo "  -e, --e2e              运行E2E测试"
    echo "  -a, --all              运行所有测试"
    echo "  -c, --coverage         生成覆盖率报告"
    echo "  -v, --verbose          详细输出"
    echo "  -m, --marker MARKER    运行特定标记的测试"
    echo "  -f, --file FILE        运行特定测试文件"
    echo "  -t, --test TEST        运行特定测试用例"
    echo ""
    echo "示例:"
    echo "  $0 --unit              运行单元测试"
    echo "  $0 --integration       运行集成测试"
    echo "  $0 --coverage          生成覆盖率报告"
    echo "  $0 -m auth             运行认证相关测试"
    echo "  $0 -f test_auth.py     运行特定测试文件"
    exit 0
}

# 设置默认值
VERBOSE=""
COVERAGE=false
TEST_TYPE=""
MARKER=""
TEST_FILE=""
TEST_NAME=""

# 解析命令行参数
while [[ $# -gt 0 ]]; do
    case $1 in
        -h|--help)
            show_help
            ;;
        -u|--unit)
            TEST_TYPE="unit"
            shift
            ;;
        -i|--integration)
            TEST_TYPE="integration"
            shift
            ;;
        -e|--e2e)
            TEST_TYPE="e2e"
            shift
            ;;
        -a|--all)
            TEST_TYPE="all"
            shift
            ;;
        -c|--coverage)
            COVERAGE=true
            shift
            ;;
        -v|--verbose)
            VERBOSE="-vv"
            shift
            ;;
        -m|--marker)
            MARKER="-m $2"
            shift 2
            ;;
        -f|--file)
            TEST_FILE="$2"
            shift 2
            ;;
        -t|--test)
            TEST_NAME="$2"
            shift 2
            ;;
        *)
            print_message "未知选项: $1" "$RED"
            show_help
            ;;
    esac
done

# 设置 pytest 命令
PYTEST_CMD="pytest"

# 添加详细输出
if [ -n "$VERBOSE" ]; then
    PYTEST_CMD="$PYTEST_CMD $VERBOSE"
fi

# 添加覆盖率
if [ "$COVERAGE" = true ]; then
    PYTEST_CMD="$PYTEST_CMD --cov=app --cov-report=html --cov-report=term-missing"
fi

# 根据测试类型设置测试路径
case $TEST_TYPE in
    unit)
        print_message "运行单元测试..." "$BLUE"
        PYTEST_CMD="$PYTEST_CMD tests/unit"
        ;;
    integration)
        print_message "运行集成测试..." "$BLUE"
        PYTEST_CMD="$PYTEST_CMD tests/integration"
        ;;
    e2e)
        print_message "运行E2E测试..." "$BLUE"
        PYTEST_CMD="$PYTEST_CMD tests/e2e --browser=chromium"
        ;;
    all)
        print_message "运行所有测试..." "$BLUE"
        PYTEST_CMD="$PYTEST_CMD tests/"
        ;;
esac

# 添加标记
if [ -n "$MARKER" ]; then
    print_message "运行标记为 $MARKER 的测试..." "$BLUE"
    PYTEST_CMD="$PYTEST_CMD $MARKER"
fi

# 添加测试文件
if [ -n "$TEST_FILE" ]; then
    print_message "运行测试文件 $TEST_FILE..." "$BLUE"
    PYTEST_CMD="$PYTEST_CMD $TEST_FILE"
fi

# 添加测试用例
if [ -n "$TEST_NAME" ]; then
    print_message "运行测试用例 $TEST_NAME..." "$BLUE"
    PYTEST_CMD="$PYTEST_CMD -k $TEST_NAME"
fi

# 执行测试
print_message "执行命令: $PYTEST_CMD" "$YELLOW"
echo ""

# 运行测试
if eval $PYTEST_CMD; then
    print_message "✅ 测试成功！" "$GREEN"
    echo ""

    # 如果生成了覆盖率报告，提示查看
    if [ "$COVERAGE" = true ]; then
        print_message "📊 覆盖率报告已生成: htmlcov/index.html" "$GREEN"
        print_message "使用以下命令在浏览器中打开:" "$GREEN"
        print_message "  python -m http.server 8000 --directory htmlcov" "$YELLOW"
        print_message "  然后访问 http://localhost:8000" "$YELLOW"
    fi
else
    print_message "❌ 测试失败！" "$RED"
    exit 1
fi
