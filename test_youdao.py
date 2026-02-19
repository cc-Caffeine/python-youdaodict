#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
测试脚本 - 用于验证有道词典爬虫是否正常工作
"""

import subprocess
import sys

def test_word(word: str) -> bool:
    """
    测试单个单词的查询

    参数:
        word (str): 要测试的单词

    返回:
        bool: True表示成功，False表示失败
    """
    print(f"\n测试单词: {word}")
    print("-" * 40)

    try:
        # 运行爬虫脚本
        result = subprocess.run(
            [sys.executable, "youdao_dict.py", word],
            capture_output=True,
            text=True,
            timeout=30
        )

        # 打印输出
        print("STDOUT:")
        print(result.stdout)
        if result.stderr:
            print("STDERR:")
            print(result.stderr)

        # 检查退出码
        if result.returncode == 0:
            print(f"✓ 测试通过: {word}")
            return True
        else:
            print(f"✗ 测试失败: {word} (退出码: {result.returncode})")
            return False

    except subprocess.TimeoutExpired:
        print(f"✗ 测试超时: {word}")
        return False
    except Exception as e:
        print(f"✗ 测试异常: {word} - {str(e)}")
        return False


def main():
    """
    主函数，运行一系列测试
    """
    print("=" * 60)
    print("有道词典爬虫测试")
    print("=" * 60)

    # 测试用例
    test_cases = [
        ("hello", True),      # 应该成功
        ("world", True),      # 应该成功
        ("python", True),     # 应该成功
        ("algorithm", True),  # 应该成功
        ("nonexistentword12345", False),  # 应该失败（单词不存在）
    ]

    passed = 0
    failed = 0

    for word, expected_success in test_cases:
        success = test_word(word)
        if success == expected_success:
            passed += 1
        else:
            failed += 1

    print("\n" + "=" * 60)
    print(f"测试结果: {passed} 通过, {failed} 失败")
    print("=" * 60)

    if failed > 0:
        sys.exit(1)
    else:
        print("所有测试通过！")
        sys.exit(0)


if __name__ == "__main__":
    main()
