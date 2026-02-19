#!/bin/bash

# 有道词典爬虫 - 环境设置脚本
# 用于自动安装依赖并运行测试

set -e

echo "=========================================="
echo "有道词典爬虫 - 环境设置"
echo "=========================================="
echo ""

# 检测操作系统
if [ -f /etc/os-release ]; then
    . /etc/os-release
    OS=$NAME
    echo "检测到操作系统: $OS"
else
    echo "无法检测操作系统"
    exit 1
fi

# 检查Python是否安装
if ! command -v python3 &> /dev/null; then
    echo "错误: Python3 未安装"
    echo "请先安装 Python3"
    exit 1
fi

echo "Python版本: $(python3 --version)"
echo ""

# 安装依赖
echo "正在安装依赖..."
if [[ "$OS" == *"Arch Linux"* ]] || [[ "$OS" == *"Manjaro"* ]]; then
    echo "检测到 Arch Linux 系统，使用 pacman 安装..."
    sudo pacman -S --noconfirm python-requests python-beautifulsoup4 python-lxml
else
    echo "使用 pip 安装..."
    pip install requests beautifulsoup4 lxml
fi

echo ""
echo "验证安装..."
python3 -c "import requests, bs4, lxml; print('✓ requests, beautifulsoup4, lxml 安装成功')"

echo ""
echo "运行测试..."
python3 test_youdao.py

echo ""
echo "=========================================="
echo "环境设置完成！"
echo "=========================================="
echo ""
echo "使用方法:"
echo "  python3 youdao_dict.py hello"
echo ""
echo "查看帮助:"
echo "  python3 youdao_dict.py"
echo ""
echo "查看文档:"
echo "  cat README.md"
echo ""
