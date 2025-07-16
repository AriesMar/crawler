# Python 通用爬虫框架

一个功能强大、易于扩展的Python爬虫框架，支持多种数据存储方式和反爬虫策略。

## 🚀 功能特性

- **通用框架设计**：基于抽象基类，易于扩展新的爬虫类型
- **智能重试机制**：自动重试失败的请求，支持指数退避
- **反爬虫策略**：随机User-Agent、请求延迟、代理支持
- **多种存储方式**：支持JSON、CSV、SQLite、MongoDB
- **详细日志记录**：彩色日志输出，支持文件轮转
- **Selenium支持**：处理动态网页内容
- **配置化管理**：环境变量配置，灵活的参数调整
- **插件系统**：支持自定义插件扩展功能
- **工具函数库**：丰富的辅助工具和验证函数

## 📁 项目结构

```
crawler/
├── crawler_framework/          # 主框架包
│   ├── __init__.py            # 框架入口
│   ├── config.py              # 配置管理
│   ├── core/                  # 核心模块
│   │   ├── __init__.py
│   │   ├── base_crawler.py    # 基础爬虫类
│   │   ├── request_manager.py # 请求管理器
│   │   └── data_storage.py    # 数据存储管理器
│   ├── utils/                 # 工具模块
│   │   ├── __init__.py
│   │   ├── logger.py          # 日志工具
│   │   ├── helpers.py         # 辅助工具函数
│   │   └── validators.py      # 验证工具函数
│   ├── plugins/               # 插件系统
│   │   ├── __init__.py
│   │   ├── base_plugin.py     # 插件基类
│   │   └── plugin_manager.py  # 插件管理器
│   └── crawlers/              # 爬虫实现
│       ├── __init__.py
│       ├── wechat_crawler.py  # 微信公众号爬虫
│       └── news_crawler.py    # 新闻网站爬虫
├── examples/                  # 使用示例
│   └── basic_usage.py        # 基础使用示例
├── tests/                    # 测试文件
│   └── test_framework.py     # 框架测试
├── requirements.txt          # 项目依赖
├── env_example.txt          # 环境变量模板
├── logs/                    # 日志文件目录
├── data/                    # 数据存储目录
└── downloads/               # 下载文件目录
```

## 🛠️ 安装依赖

```bash
pip install -r requirements.txt
```

## ⚡ 快速开始

### 1. 配置环境变量

复制 `env_example.txt` 为 `.env` 并修改配置：

```bash
cp env_example.txt .env
```

### 2. 运行测试

```bash
python tests/test_framework.py
```

### 3. 运行示例

```bash
python examples/basic_usage.py
```

### 4. 使用微信公众号爬虫

```python
from crawler_framework import WeChatCrawler

# 微信公众号文章URL列表
urls = [
    "https://mp.weixin.qq.com/s/your_article_url_1",
    "https://mp.weixin.qq.com/s/your_article_url_2",
]

# 使用爬虫
with WeChatCrawler(storage_type='json') as crawler:
    results = crawler.crawl_wechat_articles(urls)
    
    for article in results:
        print(f"标题: {article['title']}")
        print(f"作者: {article['author']}")
        print(f"内容: {article['content'][:100]}...")
```

## 🔧 创建自定义爬虫

继承 `BaseCrawler` 类创建新的爬虫：

```python
from crawler_framework import BaseCrawler
from bs4 import BeautifulSoup

class MyCrawler(BaseCrawler):
    def get_urls(self):
        """返回要爬取的URL列表"""
        return ["https://example.com/page1", "https://example.com/page2"]
    
    def parse(self, response):
        """解析响应数据"""
        soup = BeautifulSoup(response.text, 'html.parser')
        
        return {
            'title': soup.find('h1').text.strip(),
            'content': soup.find('div', class_='content').text.strip(),
            'url': response.url
        }

# 使用自定义爬虫
with MyCrawler(storage_type='csv') as crawler:
    results = crawler.crawl()
```

## ⚙️ 配置说明

### 基础配置
- `DEBUG`: 调试模式开关
- `LOG_LEVEL`: 日志级别 (DEBUG, INFO, WARNING, ERROR)

### 请求配置
- `REQUEST_TIMEOUT`: 请求超时时间（秒）
- `REQUEST_DELAY`: 请求间隔时间（秒）
- `MAX_RETRIES`: 最大重试次数

### 存储配置
- `DATABASE_URL`: SQLite数据库URL
- `MONGO_URI`: MongoDB连接URI
- `MONGO_DB`: MongoDB数据库名

### 代理配置
- `USE_PROXY`: 是否使用代理
- `PROXY_LIST`: 代理服务器列表（逗号分隔）

## 💾 数据存储

框架支持多种数据存储方式：

### JSON存储
```python
crawler = WeChatCrawler(storage_type='json')
```

### CSV存储
```python
crawler = WeChatCrawler(storage_type='csv')
```

### SQLite存储
```python
crawler = WeChatCrawler(storage_type='sqlite')
```

### MongoDB存储
```python
crawler = WeChatCrawler(storage_type='mongodb')
```

## 🔌 插件系统

### 创建自定义插件

```python
from crawler_framework.plugins import BasePlugin

class MyPlugin(BasePlugin):
    def __init__(self):
        super().__init__("MyPlugin", "1.0.0")
        self.description = "我的自定义插件"
    
    def initialize(self, config):
        """初始化插件"""
        self.config = config
        return True
    
    def execute(self, data):
        """执行插件逻辑"""
        # 处理数据
        data['processed'] = True
        return data

# 使用插件
from crawler_framework.plugins import PluginManager

plugin_manager = PluginManager()
plugin = MyPlugin()
plugin_manager.register_plugin(plugin)

# 执行插件
result = plugin_manager.execute_plugin("MyPlugin", data)
```

## 🛠️ 工具函数

框架提供了丰富的工具函数：

```python
from crawler_framework.utils.helpers import clean_text, extract_domain, generate_filename
from crawler_framework.utils.validators import validate_url, validate_email

# 文本清理
clean_text("  这是  一个  测试  文本  ")

# 域名提取
extract_domain("https://www.example.com/path")

# 文件名生成
generate_filename("crawler", "json")

# URL验证
validate_url("https://www.example.com")
```

## 📊 微信公众号爬虫特性

- **完整内容提取**：标题、作者、发布时间、正文、图片等
- **图片URL提取**：自动提取文章中的所有图片链接
- **标签生成**：基于内容关键词自动生成标签
- **元数据获取**：公众号名称、ID等元信息
- **反检测**：模拟真实浏览器行为

## 📰 新闻爬虫特性

- **通用解析**：支持多种新闻网站结构
- **智能提取**：自动识别标题、内容、作者等信息
- **分类标签**：提取新闻分类和标签
- **图片处理**：自动处理相对和绝对图片URL

## ⚠️ 注意事项

1. **遵守robots.txt**：请确保遵守目标网站的robots.txt规则
2. **合理使用**：控制爬取频率，避免对目标网站造成压力
3. **法律合规**：确保爬取行为符合相关法律法规
4. **数据使用**：仅用于学习和研究目的，不得用于商业用途

## 🔧 扩展功能

### 添加新的存储方式
在 `crawler_framework/core/data_storage.py` 中添加新的存储方法。

### 添加新的爬虫类型
继承 `BaseCrawler` 类并实现 `parse()` 和 `get_urls()` 方法。

### 自定义请求策略
修改 `crawler_framework/core/request_manager.py` 中的请求逻辑。

### 创建自定义插件
继承 `BasePlugin` 类并实现 `initialize()` 和 `execute()` 方法。

## 🤝 贡献

欢迎提交Issue和Pull Request来改进这个框架！

## �� 许可证

MIT License
