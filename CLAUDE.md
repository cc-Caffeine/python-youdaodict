# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is a Python-based web scraper that fetches English word translations from Youdao Dictionary (dict.youdao.com). The project includes various comparison and educational documentation exploring performance differences between HTML parsers and Python's dynamic typing.

## Core Commands

### Running the Dictionary Scraper
```bash
# Query a word
python3 youdao_dict.py <word>

# Example
python3 youdao_dict.py hello
python3 youdao_dict.py python
```

### Testing
```bash
# Run functional tests
python3 test_youdao.py

# Run performance benchmark (comparing lxml vs html.parser)
python3 benchmark.py
```

### Environment Setup
```bash
# Automated setup script
./setup.sh

# Manual installation:
# Arch Linux:
sudo pacman -S python-requests python-beautifulsoup4 python-lxml

# Other systems:
pip install requests beautifulsoup4 lxml
```

## Architecture

### Main Components

**youdao_dict.py** - Dictionary scraper with three-phase architecture:
1. HTTP request layer: Uses `requests` with custom headers and 10-second timeout
2. HTML parsing layer: Uses `BeautifulSoup` with `lxml` parser (significantly faster than `html.parser`)
3. Data extraction layer: Parses specific HTML structure (div#results-contents → div.trans-container → li elements, plus optional Collins dictionary entries)

**test_youdao.py** - CLI-based test harness that invokes youdao_dict.py as subprocess and validates exit codes

**benchmark.py** - Performance analysis tool comparing lxml vs html.parser parsers

### Key Design Decisions

- **Parser Choice**: Uses `lxml` parser (2-3x faster than default `html.parser` per benchmarks in `LXML_VS_HTML_PARSER.md`)
- **HTML Structure Dependencies**: Relies on specific Youdao dictionary HTML structure that could break if redesigned
- **Educational Analogy Pattern**: Throughout documentation, Python constructs are compared to C/Rust equivalents to aid understanding

### Documentation Organization

The `/dynamic_types_explained.md` file provides detailed explanations of Python's dynamic typing, which is referenced throughout the code via C/Rust analogies. This is a recurring pattern used to help developers from statically-typed language backgrounds understand Python behaviors.

## Development Notes

### Adding New Features

When implementing new features, maintain the three-phase architecture:
1. Network layer - handle HTTP requests with proper error handling
2. Parsing layer - use BeautifulSoup with lxml for consistency
3. Output layer - format results with clear section markers (see "【基本翻译】", "【柯林斯英汉双解大词典】" pattern)

### Testing New Features

Always run the full test suite before committing changes:
```bash
python3 test_youdao.py  # Must pass all tests
python3 youdao_dict.py test  # Manual verification
```

The test script expects specific exit codes and output patterns - check `test_youdao.py:^test_word()` for validation logic.

### Performance Considerations

The project maintains a focus on performance analysis:
- Use `time.time()` for timing measurements
- Compare against `html.parser` baseline when testing parser changes
- Document results in format shown in `LXML_VS_HTML_PARSER.md`

### Error Handling Patterns

The scraping code follows these error handling patterns:
- Network errors: `requests.exceptions` (Timeout, RequestException)
- Parsing errors: Gracefully handle missing HTML elements using conditionals
- Unknown errors: Catch-all `Exception` to provide user-friendly messages

All error messages should be in Chinese and follow the pattern "错误：<错误类型> - <详细信息>"

## Dependencies

- **requests** - HTTP client library with timeout support
- **beautifulsoup4** - HTML parsing with CSS selector support
- **lxml** - High-performance HTML parser (compiled C extension, optional but strongly recommended)

When modifying dependency versions, check compatibility with both Arch Linux system packages and pip installations.
