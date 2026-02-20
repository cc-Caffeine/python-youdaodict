# 使用示例

## 基本用法

```bash
# 查询单词 hello
python3 youdao_dict.py hello

# 查询单词 python
python3 youdao_dict.py python

# 查询单词 algorithm
python3 youdao_dict.py algorithm
```

## 输出示例

### 查询 "hello"
```
正在查询单词 'hello' 的翻译...
--------------------------------------------------
int. 喂，你好（用于问候或打招呼）；喂，你好（打电话时的招呼语）；喂，你好（引起别人注意的招呼语）；<非正式>喂，嘿 (认为别人说了蠢话或分心)；<英，旧>嘿（表示惊讶）
n. 招呼，问候；（Hello）（法、印、美、俄）埃洛（人名）
v. 说（或大声说）“喂”；打招呼
```

### 查询 "python"
```
正在查询单词 'python' 的翻译...
--------------------------------------------------
n. 蚺，巨蟒；（Python）皮同（希腊神话中的巨蟒）；（Python）一种计算机高级编程语言；（Python）（瑞士、法、美、印、伊朗）皮东（人名）
```

### 查询不存在的单词
```
正在查询单词 'nonexistentword12345' 的翻译...
--------------------------------------------------
错误：未找到翻译容器
```

## 批量查询示例

创建一个简单的shell脚本批量查询：

```bash
#!/bin/bash
# batch_lookup.sh

words=("hello" "world" "python" "algorithm" "computer")

for word in "${words[@]}"; do
    echo "=== 查询单词: $word ==="
    python3 youdao_dict.py "$word"
    echo ""
done
```

运行：
```bash
chmod +x batch_lookup.sh
./batch_lookup.sh
```

## Python脚本中使用

```python
import subprocess
import sys

def lookup_word(word: str) -> str:
    """在Python脚本中调用爬虫"""
    result = subprocess.run(
        [sys.executable, "youdao_dict.py", word],
        capture_output=True,
        text=True
    )
    return result.stdout

# 使用示例
translation = lookup_word("hello")
print(translation)
```

## 错误处理

爬虫会返回错误信息，你可以根据返回内容判断是否成功：

```python
import subprocess
import sys

def safe_lookup(word: str) -> tuple:
    """安全地查询单词，返回(成功, 结果)"""
    result = subprocess.run(
        [sys.executable, "youdao_dict.py", word],
        capture_output=True,
        text=True
    )

    success = result.returncode == 0
    output = result.stdout

    return success, output

# 使用示例
success, result = safe_lookup("hello")
if success:
    print("查询成功:")
    print(result)
else:
    print("查询失败:")
    print(result)
```

## 性能考虑

1. **网络延迟**：每次查询都需要网络请求，建议添加延迟
2. **缓存**：对于重复查询，可以添加简单的缓存机制
3. **批量查询**：避免同时发起大量请求，可能被限制

## 扩展功能

1. **添加更多词典**：可以扩展支持百度翻译、谷歌翻译等
2. **导出格式**：支持JSON、CSV等格式输出
3. **命令行参数**：添加更多选项，如指定输出格式、详细模式等
