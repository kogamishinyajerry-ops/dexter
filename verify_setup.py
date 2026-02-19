"""快速验证 DeepSeek 配置"""

import os
import sys

sys.path.insert(0, '/workspace/dexter/src')

from dotenv import load_dotenv
load_dotenv('/workspace/dexter/.env')

print("=" * 60)
print("配置验证")
print("=" * 60)

# 检查 DeepSeek 配置
api_key = os.getenv("DEEPSEEK_API_KEY")
if api_key:
    print(f"✓ DEEPSEEK_API_KEY: {'*' * 20}{api_key[-4:]}")
else:
    print("✗ DEEPSEEK_API_KEY: 未设置")

base_url = os.getenv("DEEPSEEK_BASE_URL")
if base_url:
    print(f"✓ DEEPSEEK_BASE_URL: {base_url}")
else:
    print("✗ DEEPSEEK_BASE_URL: 未设置")

model = os.getenv("DEEPSEEK_MODEL")
if model:
    print(f"✓ DEEPSEEK_MODEL: {model}")
else:
    print("✗ DEEPSEEK_MODEL: 未设置")

# 测试模块导入
print("\n📦 模块导入测试:")
try:
    from src.astock.model import get_model_config
    print("  ✓ model.py")

    from src.astock.agent import AStockAgent
    print("  ✓ agent.py")

    from src.astock.prompts import PLANNING_SYSTEM_PROMPT
    print("  ✓ prompts.py")

    from src.astock.tools import TOOLS
    print(f"  ✓ tools.py ({len(TOOLS['astock'])} 个工具)")

    from src.astock.utils import Logger
    print("  ✓ utils/")
except Exception as e:
    print(f"  ✗ 导入失败: {e}")

# 测试智能体创建
print("\n🤖 智能体创建测试:")
try:
    agent = AStockAgent(
        max_steps=5,
        max_steps_per_task=2,
        model="deepseek"
    )
    print("  ✓ DeepSeek 智能体创建成功")
except Exception as e:
    print(f"  ✗ 创建失败: {e}")

print("\n" + "=" * 60)
print("配置验证完成！")
print("=" * 60)
print("\n下一步:")
print("  python -m src.astock.cli  # 启动交互式助手")
