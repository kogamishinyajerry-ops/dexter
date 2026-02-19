"""快速测试脚本"""

import os
import sys

# 添加 src 到路径
sys.path.insert(0, '/workspace/dexter/src')

os.environ['LLM_API_OPENAI_KEY'] = 'sk-test-key-placeholder'

import src.astock.agent as agent_module
import src.astock.tools as tools_module

AStockAgent = agent_module.AStockAgent
TOOLS = tools_module.TOOLS

print("=" * 60)
print("A 股投资顾问系统测试")
print("=" * 60)

# 1. 检查工具列表
print("\n📋 可用工具:")
for i, tool in enumerate(TOOLS['astock'], 1):
    print(f"  {i}. {tool.name}: {tool.description}")

# 2. 创建智能体
print("\n🤖 创建智能体...")
agent = AStockAgent(
    max_steps=10,
    max_steps_per_task=3,
    model="openai"
)
print("✓ 智能体创建成功")

# 3. 测试任务规划
print("\n📝 测试任务规划...")
query = "分析贵州茅台的投资价值"
tasks = agent.plan_tasks(query)
print(f"✓ 规划了 {len(tasks)} 个任务:")
for task in tasks:
    print(f"  - {task.description}")

print("\n" + "=" * 60)
print("测试完成！系统运行正常")
print("=" * 60)
