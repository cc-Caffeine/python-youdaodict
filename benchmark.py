#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
性能对比测试脚本
比较 html.parser 和 lxml 的解析性能
"""

import time
import requests
from bs4 import BeautifulSoup


def fetch_html():
    """获取有道词典页面 HTML"""
    url = "https://dict.youdao.com/search?q=hello"
    headers = {
        "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 "
                      "(KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
    }
    response = requests.get(url, headers=headers, timeout=10)
    return response.text


def benchmark_parser(html, parser_name, parser_type, iterations=100):
    """测试解析器性能"""
    print(f"\n{'='*60}")
    print(f"测试解析器: {parser_name}")
    print(f"{'='*60}")

    # 预热（第一次解析可能较慢）
    soup = BeautifulSoup(html, parser_type)
    soup.find('div', id='results-contents')

    # 正式测试
    start_time = time.time()
    for i in range(iterations):
        soup = BeautifulSoup(html, parser_type)
        results_contents = soup.find('div', id='results-contents')
        if results_contents:
            trans_container = results_contents.find('div', class_='trans-container')
            if trans_container:
                translation_items = trans_container.find_all('li')
                translations = [item.get_text(strip=True) for item in translation_items if item.get_text(strip=True)]

    end_time = time.time()
    total_time = end_time - start_time
    avg_time = total_time / iterations

    print(f"迭代次数: {iterations}")
    print(f"总耗时: {total_time:.3f} 秒")
    print(f"平均每次: {avg_time:.4f} 秒")
    print(f"每秒解析: {1/avg_time:.1f} 次")

    return total_time, avg_time


def compare_parsers():
    """对比两种解析器"""
    print("="*60)
    print("有道词典爬虫 - 解析器性能对比测试")
    print("="*60)

    # 获取 HTML
    print("\n正在获取网页内容...")
    try:
        html = fetch_html()
        print(f"获取成功！HTML 大小: {len(html):,} 字节")
    except Exception as e:
        print(f"获取失败: {e}")
        return

    # 测试 html.parser
    html_parser_time, html_parser_avg = benchmark_parser(
        html, "html.parser (Python内置)", "html.parser", iterations=50
    )

    # 测试 lxml
    lxml_time, lxml_avg = benchmark_parser(
        html, "lxml (C语言实现)", "lxml", iterations=50
    )

    # 对比结果
    print("\n" + "="*60)
    print("📊 性能对比结果")
    print("="*60)

    speedup = html_parser_avg / lxml_avg
    print(f"\n{'解析器':<25} {'平均时间':<15} {'相对速度':<15}")
    print("-" * 60)
    print(f"{'html.parser':<25} {html_parser_avg*1000:>8.2f} ms{'':<7} {'基准':<15}")
    print(f"{'lxml':<25} {lxml_avg*1000:>8.2f} ms{'':<7} {speedup:.1f}x 快速")

    print("\n" + "="*60)
    print("📈 结论")
    print("="*60)

    if speedup >= 5:
        print(f"✅ lxml 比 html.parser 快 {speedup:.1f} 倍！")
        print("   强烈推荐使用 lxml 解析器")
    elif speedup >= 2:
        print(f"✅ lxml 比 html.parser 快 {speedup:.1f} 倍")
        print("   推荐使用 lxml 解析器")
    elif speedup >= 1.5:
        print(f"⚠️  lxml 比 html.parser 快 {speedup:.1f} 倍")
        print("   可以考虑使用 lxml")
    else:
        print(f"❌ 两者性能相近（{speedup:.1f}x）")
        print("   可以根据其他因素选择")

    print("\n" + "="*60)
    print("💡 建议")
    print("="*60)

    if speedup >= 2:
        print("1. ✅ 使用 lxml - 性能优势明显")
        print("2. ✅ 使用 lxml - 容错性更好")
        print("3. ✅ 使用 lxml - 支持 XPath 和 CSS 选择器")
        print("4. ⚠️  如果无法安装 lxml，使用 html.parser 也可以")
    else:
        print("1. ✅ 两者皆可 - 性能差异不大")
        print("2. ✅ 使用 html.parser - 无需额外依赖")
        print("3. ✅ 使用 lxml - 功能更强大")


def test_accuracy():
    """测试两种解析器的准确性"""
    print("\n" + "="*60)
    print("🔍 准确性测试")
    print("="*60)

    test_words = ["hello", "world", "python", "algorithm"]

    for word in test_words:
        print(f"\n测试单词: {word}")
        print("-" * 40)

        url = f"https://dict.youdao.com/search?q={word}"
        headers = {
            "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 "
                          "(KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
        }

        try:
            response = requests.get(url, headers=headers, timeout=10)

            # html.parser
            soup_html = BeautifulSoup(response.text, 'html.parser')
            result_html = soup_html.find('div', id='results-contents')

            # lxml
            soup_lxml = BeautifulSoup(response.text, 'lxml')
            result_lxml = soup_lxml.find('div', id='results-contents')

            # 比较结果
            if result_html and result_lxml:
                html_text = result_html.get_text(strip=True)[:100]
                lxml_text = result_lxml.get_text(strip=True)[:100]

                if html_text == lxml_text:
                    print(f"✅ 两者结果一致")
                else:
                    print(f"⚠️  结果略有差异（正常现象）")
                    print(f"   html.parser: {html_text}...")
                    print(f"   lxml: {lxml_text}...")
            elif result_html:
                print(f"✅ html.parser 找到结果，lxml 未找到")
            elif result_lxml:
                print(f"✅ lxml 找到结果，html.parser 未找到")
            else:
                print(f"❌ 两者都未找到结果")

        except Exception as e:
            print(f"❌ 测试失败: {e}")


if __name__ == "__main__":
    try:
        compare_parsers()
        test_accuracy()
    except KeyboardInterrupt:
        print("\n\n测试已中断")
    except Exception as e:
        print(f"\n\n测试出错: {e}")
        import traceback
        traceback.print_exc()
