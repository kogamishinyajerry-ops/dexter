# 快速开始

## 安装

```bash
# 克隆项目
git clone https://github.com/kogamishinyajerry-ops/dexter.git
cd dexter

# 运行安装脚本
bash install.sh

# 编辑 .env 文件，添加 API 密钥
nano .env
```

## 环境变量配置

在 `.env` 文件中设置以下环境变量：

```bash
# 必须配置其中之一
LLM_API_OPENAI_KEY=sk-xxx  # OpenAI API 密钥
# 或
LLM_API_ANTHROPIC_KEY=sk-ant-xxx  # Anthropic API 密钥

# 可选：数据源（akshare 免费，tushare 需要 token）
TUSHARE_TOKEN=your-tushare-token
```

## 运行

```bash
# 启动交互式分析
uv run astock-agent
```

## 使用示例

```python
# 个股分析
分析贵州茅台的投资价值，包括基本面、技术面、资金面和消息面

# 行业对比
对比宁德时代、比亚迪在新能源行业的竞争力

# 市场研判
当前A股市场的主要机会和风险是什么？

# 选股
帮我找出市盈率低于20、ROE超过15%的公司

# 技术分析
分析贵州茅台最近半年的价格走势和技术指标
```

## 项目结构

```
dexter/
├── src/astock/           # 源代码
│   ├── agent.py          # 核心智能体
│   ├── model.py          # LLM 接口
│   ├── prompts.py        # 系统提示词
│   ├── schemas.py        # 数据模型
│   ├── cli.py            # CLI 入口
│   ├── tools/            # 工具集
│   │   ├── astock/       # A股工具
│   │   │   ├── quote.py  # 行情数据
│   │   │   ├── financial.py  # 财务数据
│   │   │   └── ...
│   └── utils/            # 工具函数
├── env.example           # 环境变量模板
├── install.sh            # 安装脚本
└── README.md             # 项目文档
```

## 免责声明

本工具提供的所有分析和建议仅供参考，不构成任何投资建议。投资有风险，入市需谨慎。
