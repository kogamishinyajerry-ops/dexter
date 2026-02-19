# A股投资专业助手 (A-Share AI Advisor)

基于 Dexter 架构的 A 股市场智能投资分析系统

## 🎯 项目概述

这是一个基于 AI 智能体的 A 股投资分析助手，能够自动：
- 🔍 **个股分析** - 全面分析基本面、技术面、资金面、消息面
- 📊 **行业研究** - 行业对比、龙头分析、产业链研究
- 📈 **市场研判** - 大盘趋势、热点题材、资金流向
- 🎯 **智能选股** - 基本面选股、技术面选股、事件驱动

## 🚀 快速开始

### 安装

```bash
# 1. 克隆或下载项目
cd /workspace/dexter

# 2. 运行安装脚本
bash install.sh

# 3. 配置 API keys
vim .env  # 添加以下任意一个:
#   - DEEPSEEK_API_KEY (推荐，国内可用)
#   - LLM_API_OPENAI_KEY
#   - LLM_API_ANTHROPIC_KEY

# 4. 验证安装
python verify_setup.py
```

### 使用

```bash
# 启动交互式命令行
python -m src.astock.cli
```

### 示例查询

```
分析贵州茅台的投资价值
对比宁德时代、比亚迪、理想汽车在新能源行业的竞争力
当前A股市场的主要风险和机会是什么？哪些板块值得关注？
帮我找出市盈率低于20、营收增长率超过30%、现金流健康的公司
```

## 🏗️ 架构设计

### 核心组件

```
┌─────────────────────────────────────────────────────────────┐
│                    A股投资专业助手                           │
├─────────────────────────────────────────────────────────────┤
│  Planning Agent    → 任务规划与分解                          │
│  Action Agent      → 工具选择与执行                          │
│  Validation Agent  → 结果验证与检查                          │
│  Answer Agent      → 报告生成与建议                          │
└─────────────────────────────────────────────────────────────┘
                            ↓
┌─────────────────────────────────────────────────────────────┐
│                    数据源层                                  │
├───────────────┬───────────────┬───────────────┬─────────────┤
│  A股行情数据   │   财务数据     │   新闻资讯     │   宏观数据   │
│  (akshare)    │  (东方财富)    │   (新闻API)   │  (统计局等)  │
└───────────────┴───────────────┴───────────────┴─────────────┘
```

### 数据源

| 数据类型 | 来源 | API/库 | 说明 |
|---------|------|--------|------|
| 实时行情 | 新浪/东方财富 | akshare | 分时、日线数据 |
| 财务指标 | 东方财富 | akshare | 资产负债表、利润表 |
| 资金流向 | 东方财富 | akshare | 主力、散户资金 |
| 新闻资讯 | 财联社、东方财富 | 爬虫/RSS | 快讯、深度报道 |
| 公告信息 | 巨潮资讯 | 爬虫 | 公司公告、年报 |
| 宏观数据 | 国家统计局、央行 | akshare | GDP、CPI、PMI |
| 政策文件 | 各政府网站 | 爬虫 | 政策解读 |
| 北向资金 | 港交所 | akshare | 外资流向 |
| 融资融券 | 两市交易所 | akshare | 杠杆数据 |

## 🛠️ 工具集设计

### 1. 行情分析工具 (tools/astock/)

```python
# 获取实时行情
get_stock_quote(symbol: str) -> dict

# 获取历史K线
get_kline_data(symbol: str, period: str, start: str, end: str) -> dict

# 获取分时图
get_intraday_data(symbol: str) -> dict

# 获取板块/指数数据
get_sector_performance(sector: str) -> dict

# 计算技术指标
calculate_indicators(symbol: str, indicators: list) -> dict
```

### 2. 财务分析工具 (tools/financial/)

```python
# 获取财务指标
get_financial_indicators(symbol: str) -> dict

# 获取财务报表
get_financial_statement(symbol: str, statement_type: str, period: str) -> dict

# 财务比率分析
calculate_ratios(symbol: str) -> dict

# 同行业对比
compare_with_peers(symbol: str, metrics: list) -> dict
```

### 3. 资金流向工具 (tools/moneyflow/)

```python
# 获取主力资金流向
get_capital_flow(symbol: str) -> dict

# 北向资金统计
get_northbound_flow() -> dict

# 融资融券数据
get_margin_trading(symbol: str) -> dict

# 大宗交易
get_block_trades(symbol: str) -> dict
```

### 4. 新闻资讯工具 (tools/news/)

```python
# 获取个股新闻
get_stock_news(symbol: str, days: int) -> dict

# 市场快讯
get_market_news(category: str) -> dict

# 情绪分析
analyze_sentiment(news_list: list) -> dict

# 热点题材
get_hot_topics() -> dict
```

### 5. 宏观分析工具 (tools/macro/)

```python
# 获取宏观数据
get_macro_indicator(indicator: str) -> dict

# 政策解析
parse_policy_news(keywords: list) -> dict

# 流动性分析
analyze_liquidity() -> dict
```

### 6. 选股工具 (tools/screener/)

```python
# 技术选股
technical_screener(criteria: dict) -> list

# 基本面选股
fundamental_screener(criteria: dict) -> list

# 事件驱动选股
event_screener(event_type: str) -> list
```

## 📊 系统功能模块

### 1. 个股分析
- 公司基本面分析
- 技术面分析
- 资金面分析
- 消息面分析
- 综合评分

### 2. 行业研究
- 行业景气度分析
- 龙头股对比
- 行业政策解读
- 产业链分析

### 3. 市场研判
- 大盘趋势分析
- 资金流向监控
- 热点题材追踪
- 风险提示

### 4. 投资策略
- 价值投资策略
- 成长股策略
- 题材炒作策略
- 量化选股策略

### 5. 报告生成
- 个股研究报告
- 行业研究报告
- 投资策略报告
- 每日复盘报告

## 🚀 开发计划

### Phase 1: 基础框架搭建
- [ ] 项目结构搭建
- [ ] 配置 akshare 数据源
- [ ] 实现基础工具集
- [ ] 简单的问答功能

### Phase 2: 核心功能开发
- [ ] 实现四大智能体
- [ ] 完善工具集
- [ ] 添加数据缓存
- [ ] 实现上下文管理

### Phase 3: 高级功能
- [ ] 多模态分析（图表、新闻）
- [ ] 自定义指标计算
- [ ] 回测系统
- [ ] 实时推送

### Phase 4: 用户体验
- [ ] Web 界面
- [ ] 可视化图表
- [ ] 报告导出
- [ ] 策略回放

## 📝 使用示例

```python
# 个股分析
"分析贵州茅台的投资价值，包括基本面、技术面、资金面和消息面"

# 行业对比
"对比宁德时代、比亚迪、理想汽车在新能源行业的竞争力"

# 市场研判
"当前A股市场的主要风险和机会是什么？哪些板块值得关注？"

# 选股
"帮我找出市盈率低于20、营收增长率超过30%、现金流健康的公司"

# 策略建议
"基于当前的市场环境，适合采用什么样的投资策略？"
```

## 🔧 技术栈

- **语言**: Python 3.13+
- **包管理**: uv
- **LLM**: Claude / OpenAI / DeepSeek
- **数据源**: akshare, tushare
- **框架**: LangChain
- **存储**: SQLite / PostgreSQL
- **可观测性**: LangSmith

## 📚 参考资料

- [AkShare 文档](https://akshare.akfamily.xyz/)
- [Dexter 项目](https://github.com/rodionlim/dexter)
- [LangChain 文档](https://python.langchain.com/)
- [A 股投资基础](https://www.cs.com.cn/)

## ⚠️ 免责声明

本工具提供的所有分析和建议仅供参考，不构成任何投资建议。投资有风险，入市需谨慎。
