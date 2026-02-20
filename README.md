使用 code agent 制作。

# 有道词典爬虫 - 同步版本

这是一个功能完整的Python爬虫，用于从有道词典（dict.youdao.com）抓取英文单词的翻译。
特色功能：
- ✅ **完整英英释义**：包含柯林斯词典的详细英文解释
- ✅ **中英对照**：英英释义 + 中文翻译 + 实用例句
- ✅ **高性能**：使用 lxml 解析器，比标准解析器快 1.5 倍
- ✅ **智能错误处理**：完善的网络异常和解析错误处理

## 🎯 核心特性

- **📚 完整柯林斯词典**：包含详细的英英释义、中文翻译和实用例句
- **⚡ 高性能解析**：使用 lxml 解析器，比 html.parser 快 1.5 倍
- **🔧 健壮的错误处理**：完善的网络异常和 HTML 解析错误处理
- **🎨 清晰的输出格式**：结构化的中英对照显示

性能对比请查看：[LXML_VS_HTML_PARSER.md](LXML_VS_HTML_PARSER.md)

## 快速开始

### 1. 安装依赖

#### Arch Linux（推荐）
```bash
sudo pacman -S python-requests python-beautifulsoup4 python-lxml
```

#### 通用方法
```bash
pip install requests beautifulsoup4 lxml
```

### 2. 运行爬虫

```bash
python3 youdao_dict.py hello
```

### 3. 查看结果

```
正在查询单词 'hello' 的翻译...
--------------------------------------------------
【柯林斯英汉双解大词典】
  1. Hello
    CONVENTION [套语]
    例：Hello, Trish. I won't shake hands, because I'm filthy.
    你好，特里斯。我就不握手了，我的手好脏。

  2. Hello
    N-COUNT
    例：The salesperson greeted me with a warm hello.
    那位推销员向我打了个热情的招呼。

  3. Hello
    CONVENTION [套语]
    例：A moment later, Cohen picked up the phone. "Hello?"
    一会儿之后，科恩拿起电话。"喂？"

  4. hello
    CONVENTION
    例：Very softly, she called out: "Hello? Who's there?"
    她很轻柔地喊道："喂？谁在那儿？"

【基本翻译】
  int. 喂，你好（用于问候或打招呼）；喂，你好（打电话时的招呼语）；喂，你好（引起别人注意的招呼语）；<非正式>喂，嘿 (认为别人说了蠢话或分心)；<英，旧>嘿（表示惊讶）
  n. 招呼，问候；（Hello）（法、印、美、俄）埃洛（人名）
  v. 说（或大声说）"喂"；打招呼
```
正在查询单词 'hello' 的翻译...
--------------------------------------------------
【基本翻译】
int. 喂，你好（用于问候或打招呼）；喂，你好（打电话时的招呼语）；喂，你好（引起别人注意的招呼语）；<非正式>喂，嘿 (认为别人说了蠢话或分心)；<英，旧>嘿（表示惊讶）
n. 招呼，问候；（Hello）（法、印、美、俄）埃洛（人名）
v. 说（或大声说）“喂”；打招呼

【柯林斯英汉双解大词典】
1. CONVENTIONYou say "Hello" to someone when you meet them. 你好 (打招呼用语)[套语]
    例：Hello, Trish. I won't shake hands, because I'm filthy.你好，特里斯。我就不握手了，我的手好脏。
2. N-COUNTHellois also a noun. 招呼
    例：The salesperson greeted me with a warm hello.那位推销员向我打了个热情的招呼。
```

## 代码结构

### 第一步：构造带有User-Agent的GET请求
```python
url = f"https://dict.youdao.com/search?q={word}"
headers = {"User-Agent": "Mozilla/5.0 ...", ...}
response = requests.get(url, headers=headers, timeout=10)
```

### 第二步：解析HTML并提取翻译文本

```python
soup = BeautifulSoup(response.text, 'lxml')
results_contents = soup.find('div', id='results-contents')
trans_container = results_contents.find('div', class_='trans-container')
translation_items = trans_container.find_all('li')
```

### 第三步：处理异常
```python
try:
    response = requests.get(url, headers=headers, timeout=10)
    ...
except requests.exceptions.Timeout:
    return "错误：网络请求超时"
except requests.exceptions.RequestException as e:
    return f"错误：网络请求异常 - {str(e)}"
```

## 项目文件

### 主要脚本
- `youdao_dict.py` - 主爬虫脚本（使用 lxml）

### 测试和工具
- `test_youdao.py` - 测试脚本
- `benchmark.py` - 性能对比测试脚本
- `setup.sh` - 环境设置脚本

### 文档
- `docs/dynamic_types_explained.md` - Python动态类型详解（C/Rust开发者友好）
- `docs/example_usage.md` - 详细使用示例
- `docs/LXML_VS_HTML_PARSER.md` - lxml vs html.parser 性能对比分析
- `docs/LXML_RECOMMENDATION.md` - lxml 重构建议和测试结果

## 测试

### 运行功能测试
```bash
python3 test_youdao.py
```

### 运行性能对比测试
```bash
python3 benchmark.py
```

**测试结果示例：**
```
解析器                       平均时间            相对速度
------------------------------------------------------------
html.parser                  10.27 ms        基准
lxml                          6.99 ms        1.5x 快速
```

## 🚀 新功能

### ✅ 完整英英释义
最新版本修复了柯林斯词典中英英释义缺失的问题，现在您可以获得：
- 完整的英文定义（如 "You say 'Hello' to someone when you meet them."）
- 对应的中文翻译
- 实用例句展示
- 词性标注和语法说明

## 注意事项

1. **网络请求**：代码设置了10秒超时
2. **HTML结构**：有道词典的页面结构可能变化
3. **反爬虫**：频繁请求可能被限制
4. **错误处理**：代码处理了常见的网络异常
5. **解析器**：使用 lxml 解析器，性能比 html.parser 快 1.5 倍
6. **柯林斯词典**：包含完整的英英释义、中文翻译和实用例句

## 扩展建议

1. 添加更多翻译源（百度翻译、谷歌翻译）
2. 支持批量查询
3. 添加缓存机制
4. 支持导出为JSON/CSV格式
