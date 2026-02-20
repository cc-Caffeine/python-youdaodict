#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
有道词典爬虫 - 使用 lxml 版本
输入一个英文单词，从 dict.youdao.com 抓取翻译并输出。
如果单词有柯林斯英汉双解大词典的翻译，会一起输出。

依赖库：
- requests: 用于发送HTTP请求
- beautifulsoup4: 用于解析HTML
- lxml: 高性能HTML解析器（可选，但推荐）

安装依赖：
    Arch Linux: sudo pacman -S python-requests python-beautifulsoup4 python-lxml
    通用方法: pip install requests beautifulsoup4 lxml

运行示例：
    python youdao_dict.py hello

C/Rust类比：
- C: 使用 libxml2 库解析HTML
- Rust: 使用 scraper 或 lol_html 库
- Python: 使用 lxml（C语言实现，性能接近原生）
"""

import sys
import requests
from bs4 import BeautifulSoup


def fetch_basic_translation(word: str) -> str:
    """
    从有道词典获取单词的基本翻译。

    参数:
        word (str): 要查询的英文单词

    返回:
        str: 翻译文本，如果查询失败则返回错误信息

    异常:
        requests.exceptions.Timeout: 网络超时
        requests.exceptions.RequestException: 其他网络请求异常

    C/Rust类比：
    - C: char* fetch_basic_translation(const char* word);
    - Rust: fn fetch_basic_translation(word: &str) -> String
    - Python: def fetch_basic_translation(word: str) -> str:
    """
    url = f"https://dict.youdao.com/search?q={word}"

    headers = {
        "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 "
        "(KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
        "Accept-Language": "en-US,en;q=0.5",
        "Accept-Encoding": "gzip, deflate, br",
        "Connection": "keep-alive",
        "Upgrade-Insecure-Requests": "1",
    }

    try:
        response = requests.get(url, headers=headers, timeout=10)

        if response.status_code != 200:
            return f"错误：HTTP状态码 {response.status_code}"

        soup = BeautifulSoup(response.text, "lxml")

        # 查找基本翻译容器
        results_contents = soup.find("div", id="results-contents")
        if not results_contents:
            return "错误：未找到翻译区域（可能单词不存在或页面结构已更改）"

        trans_container = results_contents.find("div", class_="trans-container")
        if not trans_container:
            return "错误：未找到翻译容器"

        translation_items = trans_container.find_all("li")
        if not translation_items:
            return "错误：未找到翻译内容"

        # 提取翻译文本
        translations = []
        for item in translation_items:
            text = item.get_text(strip=True)
            if text:
                translations.append(text)

        if not translations:
            return "错误：提取到的翻译内容为空"

        return "\n".join(translations)

    except requests.exceptions.Timeout:
        return "错误：网络请求超时（请检查网络连接）"
    except requests.exceptions.RequestException as e:
        return f"错误：网络请求异常 - {str(e)}"
    except Exception as e:
        return f"错误：未知异常 - {str(e)}"


def fetch_collins_translation(word: str) -> str:
    """
    从有道词典获取单词的柯林斯英汉双解大词典翻译（包含英英释义和例句）。

    参数:
        word (str): 要查询的英文单词

    返回:
        str: 柯林斯翻译文本（包含英英释义和例句），如果没有则返回空字符串

    C/Rust类比：
    - C: char* fetch_collins_translation(const char* word);
    - Rust: fn fetch_collins_translation(word: &str) -> String
    - Python: def fetch_collins_translation(word: str) -> str:
    """
    url = f"https://dict.youdao.com/search?q={word}"
    headers = {
        "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 "
        "(KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
    }

    try:
        response = requests.get(url, headers=headers, timeout=10)

        if response.status_code != 200:
            return ""

        soup = BeautifulSoup(response.text, "lxml")

        # 查找柯林斯词典容器
        collins_result = soup.find("div", id="collinsResult")
        if not collins_result:
            return ""

        # 查找柯林斯主要翻译块
        major_trans = collins_result.find_all("div", class_="collinsMajorTrans")
        if not major_trans:
            return ""

        # 提取柯林斯翻译内容（包含英英释义和例句）
        collins_translations = []
        for i, trans in enumerate(major_trans, 1):
            # 获取翻译内容
            trans_content = trans.find("p")
            if trans_content:
                # 提取完整的释义文本
                full_definition = ""
                pos_tag = ""  # 词性标注
                additional_info = []  # 额外信息（如[套语]）

                # 遍历所有子元素，构建完整的释义
                for child in trans_content.children:
                    # 检查是否是真正的HTML元素（而不是文本节点）
                    if hasattr(child, "name") and child.name:
                        # HTML标签
                        if child.name == "span":
                            text = child.get_text(strip=True)
                            if text:
                                # 检查span类型
                                if child.get("class") == ["additional"]:
                                    # 额外信息（如[套语]），可能是词性也可能是注释
                                    # 检查是否是英文词性标注
                                    if text.isupper() and text.isalpha():
                                        # 大写英文，可能是词性
                                        if not pos_tag:
                                            pos_tag = text
                                    else:
                                        # 其他是额外信息（如[套语]）
                                        additional_info.append(text)
                                elif child.get("class") == ["collinsOrder"]:
                                    # 序号，跳过
                                    continue
                                elif any("\u4e00" <= c <= "\u9fff" for c in text):
                                    # 中文字符，通常是中文翻译
                                    full_definition += text + " "
                                else:
                                    # 英文词性标注等
                                    if not pos_tag:
                                        pos_tag = text
                                    full_definition += text + " "
                        elif child.name == "b":
                            # 单词标签
                            text = child.get_text(strip=True)
                            if text:
                                full_definition += f"{text} "
                    else:
                        # 文本节点 - 包含英英释义和中文翻译
                        text = str(child).strip()
                        if text:
                            full_definition += text + " "

                # 清理和格式化完整定义
                full_definition = " ".join(full_definition.split())

                if full_definition:
                    # 构建输出格式：词性 + 英英释义 + 中文翻译
                    output_parts = []
                    if pos_tag:
                        output_parts.append(pos_tag)

                    # 分离英文释义和中文翻译
                    english_definition = ""
                    chinese_translation = ""

                    # 查找中文字符的位置
                    chinese_start = -1
                    for idx, char in enumerate(full_definition):
                        if "\u4e00" <= char <= "\u9fff":
                            chinese_start = idx
                            break

                    if chinese_start != -1:
                        # 找到中文字符，分离英文和中文
                        english_definition = full_definition[:chinese_start].strip()
                        chinese_translation = full_definition[chinese_start:].strip()

                        # 去除英文定义末尾的标点符号
                        english_definition = english_definition.rstrip(".,;：")
                    else:
                        # 纯英文
                        english_definition = full_definition

                    # 添加序号和完整内容
                    definition_line = f"{i}. "
                    if pos_tag:
                        definition_line += f"{pos_tag} "
                    definition_line += english_definition

                    collins_translations.append(definition_line)

                    # 添加中文翻译（如果有）
                    if chinese_translation:
                        collins_translations.append(f"   {chinese_translation}")

                    # 添加额外信息（如[套语]）
                    if additional_info:
                        collins_translations.append(f"   {' '.join(additional_info)}")

                    # 查找对应的例句
                    parent_li = trans.find_parent("li")
                    if parent_li:
                        example_lists = parent_li.find_all("div", class_="exampleLists")
                        for example_list in example_lists:
                            examples = example_list.find_all("div", class_="examples")
                            for example in examples:
                                # 查找例句中的所有<p>标签
                                example_paragraphs = example.find_all("p")
                                if len(example_paragraphs) >= 2:
                                    # 第一个<p>是英文，第二个<p>是中文
                                    english_example = example_paragraphs[0].get_text(
                                        strip=True
                                    )
                                    chinese_example = example_paragraphs[1].get_text(
                                        strip=True
                                    )
                                    if english_example:
                                        collins_translations.append(
                                            f"    例：{english_example}"
                                        )
                                    if chinese_example:
                                        collins_translations.append(
                                            f"       {chinese_example}"
                                        )
                                elif len(example_paragraphs) == 1:
                                    # 只有一个<p>，可能是英文或中文
                                    example_text = example_paragraphs[0].get_text(
                                        strip=True
                                    )
                                    if example_text:
                                        collins_translations.append(
                                            f"    例：{example_text}"
                                        )

        if not collins_translations:
            return ""

        return "\n".join(collins_translations)

    except Exception:
        # 柯林斯词典是可选的，出错时不返回错误信息
        return ""


def fetch_translation(word: str) -> str:
    """
    从有道词典获取单词的翻译（包含基本翻译和柯林斯翻译）。

    参数:
        word (str): 要查询的英文单词

    返回:
        str: 翻译文本，包含基本翻译和柯林斯翻译（如果有）

    C/Rust类比：
    - C: char* fetch_translation(const char* word);
    - Rust: fn fetch_translation(word: &str) -> String
    - Python: def fetch_translation(word: str) -> str:
    """
    # 获取基本翻译
    basic_translation = fetch_basic_translation(word)

    # 如果基本翻译出错，直接返回错误
    if "错误" in basic_translation:
        return basic_translation

    # 获取柯林斯翻译（可选）
    collins_translation = fetch_collins_translation(word)

    # 构建结果
    result = []

    # 如果有柯林斯翻译，先添加到结果中
    if collins_translation:
        result.append("【柯林斯英汉双解大词典】")

        # 格式化柯林斯翻译：保持原有格式
        collins_lines = collins_translation.split("\n")
        first_entry = True
        for line in collins_lines:
            line = line.strip()
            if not line:
                continue

            # 检查是否是序号开头（如 1., 2., 3.）
            if line[0].isdigit() and line[1] == ".":
                # 序号行：第一个不添加空行，后续添加空行分隔
                if not first_entry:
                    result.append("")
                result.append(f"  {line}")
                first_entry = False
            # 检查是否是例句
            elif line.startswith("例："):
                # 例句格式：英文在前，中文在后
                result.append(f"    {line}")
            # 检查是否是中文翻译（以空格开头）
            elif line.startswith(" "):
                # 中文翻译：保持原有缩进
                result.append(f"    {line}")
            else:
                # 其他内容：缩进显示
                result.append(f"    {line}")

    # 在柯林斯翻译后添加空行分隔
    if collins_translation:
        result.append("")

    # 最后添加基本翻译（格式化为更易读的格式）
    result.append("【基本翻译】")

    # 格式化基本翻译：将每行按词性分开
    basic_lines = basic_translation.split("\n")
    for line in basic_lines:
        if line.strip():
            # 检查是否以词性开头（如 int., n., v.）
            if (
                line.startswith("int.")
                or line.startswith("n.")
                or line.startswith("v.")
                or line.startswith("adj.")
            ):
                result.append(f"  {line}")
            else:
                result.append(f"    {line}")

    return "\n".join(result)


def fetch_translation_xpath(word: str) -> str:
    """
    使用 XPath 方式获取翻译（lxml 特有功能）。

    优点：
    - 更简洁的语法
    - 更强大的选择能力
    - 支持复杂的查询

    类比：
    - C: xmlXPathEvalExpression("//div[@id='results-contents']//li")
    - Rust: scraper::Selector::parse("div#results-contents li")
    - Python: soup.select("div#results-contents li")
    """
    url = f"https://dict.youdao.com/search?q={word}"
    headers = {
        "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 "
        "(KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
    }

    try:
        response = requests.get(url, headers=headers, timeout=10)

        if response.status_code != 200:
            return f"错误：HTTP状态码 {response.status_code}"

        soup = BeautifulSoup(response.text, "lxml")

        # 使用 CSS 选择器（lxml 支持）
        # 这比 find/find_all 更简洁
        # 类比C: document.querySelectorAll("div#results-contents div.trans-container li")
        # 类比Rust: scraper::Selector::parse("div#results-contents div.trans-container li")
        translation_items = soup.select("div#results-contents div.trans-container li")

        if not translation_items:
            return "错误：未找到翻译内容"

        # 使用列表推导式提取文本
        # 类比C: 需要循环遍历
        # 类比Rust: translation_items.iter().map(|item| item.text().trim()).collect()
        translations = [
            item.get_text(strip=True)
            for item in translation_items
            if item.get_text(strip=True)
        ]

        if not translations:
            return "错误：提取到的翻译内容为空"

        return "\n".join(translations)

    except requests.exceptions.Timeout:
        return "错误：网络请求超时"
    except requests.exceptions.RequestException as e:
        return f"错误：网络请求异常 - {str(e)}"
    except Exception as e:
        return f"错误：未知异常 - {str(e)}"


def main():
    """
    主函数，处理命令行参数并调用翻译函数。
    """
    if len(sys.argv) != 2:
        print("用法: python youdao_dict.py <英文单词>")
        print("示例: python youdao_dict.py hello")
        print("\n可选方法:")
        print("  1. 使用 find/find_all: python youdao_dict.py hello")
        print("  2. 使用 XPath/CSS: 修改代码调用 fetch_translation_xpath()")
        sys.exit(1)

    word = sys.argv[1]

    print(f"正在查询单词 '{word}' 的翻译...")
    print("-" * 50)

    # 使用标准方法（find/find_all），包含基本翻译和柯林斯翻译（如果有）
    translation = fetch_translation(word)

    # 如果想使用 XPath 方法，取消下面的注释：
    # translation = fetch_translation_xpath(word)

    print(translation)

    if "错误" in translation:
        sys.exit(1)


if __name__ == "__main__":
    main()
