使用 code agent 制作。

# 有道词典爬虫 - 同步版本

这是一个简单的Python爬虫，用于从有道词典（dict.youdao.com）抓取英文单词的翻译。
如果单词有柯林斯英汉双解大词典的翻译，会一起输出。

## 🎯 版本说明

**使用 lxml 解析器**，性能比 html.parser 快 1.5 倍！

详细对比请查看：[LXML_VS_HTML_PARSER.md](LXML_VS_HTML_PARSER.md)

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
- `dynamic_types_explained.md` - Python动态类型详解
- `example_usage.md` - 使用示例
- `LXML_VS_HTML_PARSER.md` - lxml vs html.parser 详细对比
- `LXML_RECOMMENDATION.md` - lxml 重构建议

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

## 注意事项

1. **网络请求**：代码设置了10秒超时
2. **HTML结构**：有道词典的页面结构可能变化
3. **反爬虫**：频繁请求可能被限制
4. **错误处理**：代码处理了常见的网络异常
5. **解析器**：使用 lxml 解析器，性能比 html.parser 快 1.5 倍
6. **柯林斯词典**：如果单词有柯林斯英汉双解大词典的翻译，会自动一起输出；如果没有，则只输出基本翻译

## 扩展建议

1. 添加更多翻译源（百度翻译、谷歌翻译）
2. 支持批量查询
3. 添加缓存机制
4. 支持导出为JSON/CSV格式
