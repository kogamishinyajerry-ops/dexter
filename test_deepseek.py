"""测试 DeepSeek API 连接"""

import os
import sys

# 添加 src 到路径
sys.path.insert(0, '/workspace/dexter/src')

from dotenv import load_dotenv
load_dotenv('/workspace/dexter/.env')

from src.astock.model import call_llm, get_model_config

print("=" * 60)
print("DeepSeek API 连接测试")
print("=" * 60)

# 1. 检查环境变量
api_key = os.getenv("DEEPSEEK_API_KEY")
print(f"\n📋 API Key: {'*' * 20}{api_key[-4:] if api_key else 'None'}")

base_url = os.getenv("DEEPSEEK_BASE_URL")
print(f"📋 Base URL: {base_url}")

# 2. 获取模型配置
print("\n🔧 模型配置:")
config = get_model_config("deepseek")
print(f"  - 模型: {config['model']}")
print(f"  - 强模型: {config['strong_model']}")
print(f"  - 温度: {config['temperature']}")
print(f"  - 最大 tokens: {config['max_tokens']}")

# 3. 测试简单调用
print("\n🚀 测试 API 调用...")
try:
    response = call_llm(
        prompt="你好，请用一句话介绍一下贵州茅台。",
        system_prompt="你是一个专业的投资分析师。",
        model="deepseek"
    )
    print(f"✓ 调用成功！")
    print(f"\n回答: {response.content if hasattr(response, 'content') else response}")
except Exception as e:
    print(f"✗ 调用失败: {e}")
    import traceback
    traceback.print_exc()

print("\n" + "=" * 60)
print("测试完成")
print("=" * 60)
