#!/bin/bash
# A股投资顾问 - 快速安装脚本

set -e

echo "=========================================="
echo "A股投资专业助手 - 安装脚本"
echo "=========================================="
echo ""

# 检查 Python 版本
echo "检查 Python 版本..."
python_version=$(python3 --version 2>&1 | awk '{print $2}')
echo "✓ Python 版本: $python_version"
echo ""

# 安装依赖
echo "安装 Python 依赖..."
pip install -q -r requirements.txt
echo "✓ 依赖安装完成"
echo ""

# 配置环境变量
if [ ! -f .env ]; then
    echo "创建 .env 文件..."
    cp env.example .env
    echo "✓ .env 文件已创建"
    echo ""
    echo "⚠️  重要提示: 请编辑 .env 文件并添加你的 API keys"
    echo "   至少需要配置以下之一:"
    echo "   - LLM_API_OPENAI_KEY (OpenAI API)"
    echo "   - LLM_API_ANTHROPIC_KEY (Anthropic API)"
else
    echo "✓ .env 文件已存在"
fi

echo ""
echo "=========================================="
echo "安装完成！"
echo "=========================================="
echo ""
echo "快速开始:"
echo "  1. 编辑 .env 文件，添加 API keys"
echo "  2. 运行测试: python test_simple.py"
echo "  3. 启动助手: python -m src.astock.cli"
echo ""
