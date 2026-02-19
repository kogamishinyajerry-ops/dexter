# A股投资专业助手 - 快速开始指南

## 📦 安装步骤

### 1. 安装依赖

```bash
cd /workspace/dexter
pip install -r requirements.txt
```

### 2. 配置环境变量

```bash
# 复制环境变量模板
cp env.example .env

# 编辑 .env 文件，添加你的 API keys
# 至少需要配置以下之一:
#   - LLM_API_OPENAI_KEY (OpenAI)
#   - LLM_API_ANTHROPIC_KEY (Anthropic)
```

### 3. 验证安装

```bash
python test_simple.py
```

## 🚀 使用方法

### 交互式命令行

```bash
python -m src.astock.cli
```

或安装后使用：

```bash
astock-agent
```

### 示例查询

- **个股分析**: "分析贵州茅台的投资价值"
- **行业对比**: "对比宁德时代、比亚迪、理想汽车"
- **市场研判**: "当前 A 股市场的主要机会和风险"
- **财务分析**: "获取茅台过去5年的ROE和营收增长情况"

## 📋 已实现的工具

### 行情工具
- `astock_get_quote` - 实时行情
- `astock_get_kline` - 历史K线
- `astock_get_sector_performance` - 板块表现
- `astock_get_index_data` - 指数数据

### 财务工具
- `astock_get_financial_indicators` - 财务指标
- `astock_get_financial_statement` - 财务报表
- `astock_compare_with_peers` - 行业对比

## 🔧 技术架构

```
┌─────────────────────────────────────────────┐
│           AStockAgent (智能体)               │
│  - Planning Agent (任务规划)                │
│  - Action Agent (工具执行)                  │
│  - Validation Agent (结果验证)              │
│  - Answer Agent (答案生成)                 │
└─────────────────┬───────────────────────────┘
                  │
        ┌─────────┴─────────┐
        │  工具层 (Tools)    │
        ├────────────────────┤
        │  • astock_get_quote│
        │  • astock_get_kline│
        │  • ...           │
        └─────────┬─────────┘
                  │
        ┌─────────┴─────────┐
        │  数据源 (Data)     │
        │  • AkShare         │
        │  • TuShare         │
        └───────────────────┘
```

## 📊 数据来源

- **实时行情**: AkShare (东方财富接口)
- **财务数据**: AkShare (新浪财经接口)
- **指数数据**: AkShare (各交易所接口)

## ⚠️ 免责声明

本工具提供的所有分析和建议仅供参考，不构成任何投资建议。
投资有风险，入市需谨慎。

## 🤝 贡献指南

欢迎提交 Issue 和 Pull Request！

## 📄 许可证

MIT License
