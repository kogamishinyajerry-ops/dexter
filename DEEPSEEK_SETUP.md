# DeepSeek API 配置指南

## ✅ 配置状态

DeepSeek API 已成功配置并设置为默认 LLM 提供者。

### 已配置信息

- **API Key**: `sk-ba3f...049f` (已设置)
- **Base URL**: `https://api.deepseek.com/v1`
- **默认模型**: `deepseek-chat`
- **强推理模型**: `deepseek-reasoner`

## 🚀 快速开始

### 1. 验证配置

```bash
cd /workspace/dexter
python verify_setup.py
```

这会检查：
- ✓ DeepSeek API Key 配置
- ✓ 模型参数配置
- ✓ 模块导入
- ✓ 智能体创建

### 2. 启动助手

```bash
# 交互式命令行模式
python -m src.astock.cli
```

### 3. 示例查询

启动后，你可以询问：

```
分析贵州茅台的投资价值
对比宁德时代、比亚迪、理想汽车在新能源行业的竞争力
当前A股市场的主要风险和机会是什么？
帮我找出市盈率低于20、营收增长率超过30%的公司
```

## 📊 DeepSeek 模型说明

### deepseek-chat
- **用途**: 标准对话、任务规划、工具选择
- **特点**: 快速响应，适合简单分析
- **成本**: 低

### deepseek-reasoner
- **用途**: 复杂推理、深度分析、答案生成
- **特点**: 强大的推理能力，适合专业分析
- **成本**: 中等

## 🔧 配置文件

`/workspace/dexter/.env`

```env
# DeepSeek API (已配置)
DEEPSEEK_API_KEY=sk-ba3f0193310b433390b08f08128f049f
DEEPSEEK_BASE_URL=https://api.deepseek.com/v1
DEEPSEEK_MODEL=deepseek-chat
DEEPSEEK_STRONG_MODEL=deepseek-reasoner

# 其他 LLM 提供者 (可选)
LLM_API_OPENAI_KEY=...
LLM_API_ANTHROPIC_KEY=...
```

## 📝 代码示例

### 使用 DeepSeek 创建智能体

```python
import os
from dotenv import load_dotenv
load_dotenv()

from src.astock.agent import AStockAgent

# 创建 DeepSeek 智能体
agent = AStockAgent(
    max_steps=20,
    max_steps_per_task=5,
    model="deepseek"  # 使用 DeepSeek
)

# 执行分析
result = agent.run("分析贵州茅台的投资价值")
print(result)
```

### 直接调用 DeepSeek API

```python
from src.astock.model import call_llm

response = call_llm(
    prompt="分析贵州茅台的投资价值",
    system_prompt="你是一个专业的投资分析师",
    model="deepseek"
)
print(response.content)
```

## 🎯 DeepSeek 的优势

1. **国内可用** - 无需科学上网，稳定可靠
2. **中文优化** - 对中文理解能力强
3. **性价比高** - 成本低于 OpenAI 和 Anthropic
4. **推理能力强** - deepseek-reasoner 模型接近 GPT-4 水平
5. **速度快** - 响应时间短，适合实时分析

## 📈 性能对比

| 模型 | 推理能力 | 成本 | 国内可用 | 推荐场景 |
|-----|---------|------|---------|---------|
| DeepSeek Chat | ⭐⭐⭐ | 低 | ✓ | 简单分析、任务规划 |
| DeepSeek Reasoner | ⭐⭐⭐⭐⭐ | 中 | ✓ | 深度分析、报告生成 |
| GPT-4 | ⭐⭐⭐⭐⭐ | 高 | ✗ | 复杂推理 (需代理) |
| Claude 3.5 | ⭐⭐⭐⭐⭐ | 高 | ✗ | 文本生成 (需代理) |

## 🔍 测试 API 连接

```bash
python test_deepseek.py
```

这会测试：
- API Key 配置
- 连接状态
- 简单对话响应

## ❓ 常见问题

### Q: 如何切换到其他 LLM？

A: 在 `.env` 文件中配置对应的 API key，系统会自动选择可用的提供者。优先级：DeepSeek > Anthropic > OpenAI。

### Q: DeepSeek API 调用失败怎么办？

A: 检查以下几点：
1. API Key 是否正确
2. 网络连接是否正常
3. DeepSeek 服务是否可用
4. 查看错误日志

### Q: 如何调整模型参数？

A: 在 `.env` 文件中修改：
```env
DEEPSEEK_MODEL=deepseek-chat
DEEPSEEK_STRONG_MODEL=deepseek-reasoner
```

或在代码中修改 `src/astock/model.py` 的 `get_model_config` 函数。

## 📚 相关链接

- [DeepSeek 官网](https://www.deepseek.com/)
- [DeepSeek API 文档](https://platform.deepseek.com/docs)
- [DeepSeek 价格](https://platform.deepseek.com/pricing)

## ⚠️ 免责声明

本工具提供的所有分析和建议仅供参考，不构成任何投资建议。投资有风险，入市需谨慎。
