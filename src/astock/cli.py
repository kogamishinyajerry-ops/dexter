"""CLI 入口点"""

import sys
from rich.console import Console
from rich.panel import Panel
from rich.text import Text

from .agent import AStockAgent
from .utils import Logger

console = Console()


def show_intro():
    """显示欢迎信息"""
    intro_text = """
╔═════════════════════════════════════════════════════════╗
║                                                           ║
║   📊 A股投资专业助手 (A-Share AI Advisor) v1.0.0         ║
║                                                           ║
║   基于 Dexter 架构的 A 股市场智能投资分析系统             ║
║                                                           ║
╚═════════════════════════════════════════════════════════╝

💡 支持的分析类型：
   • 个股分析 - 全面分析基本面、技术面、资金面、消息面
   • 行业研究 - 行业对比、龙头分析、产业链分析
   • 市场研判 - 大盘趋势、热点题材、资金流向
   • 选股策略 - 基本面选股、技术面选股、事件驱动

⚠️  免责声明：
   本工具提供的所有分析和建议仅供参考，不构成任何投资建议。
   投资有风险，入市需谨慎。

输入问题开始分析，输入 'exit' 或 'quit' 退出
"""
    panel = Panel(intro_text, border_style="cyan")
    console.print(panel)
    console.print()


def main():
    """主函数"""
    # 检查环境变量
    import os
    api_keys = {
        "deepseek": os.getenv("DEEPSEEK_API_KEY"),
        "openai": os.getenv("LLM_API_OPENAI_KEY"),
        "anthropic": os.getenv("LLM_API_ANTHROPIC_KEY"),
    }

    available_providers = [k for k, v in api_keys.items() if v]

    if not available_providers:
        console.print("[red]错误: 未设置任何 LLM API 密钥[/red]")
        console.print("请在 .env 文件中设置以下任意一个:")
        console.print("  - DEEPSEEK_API_KEY (推荐，国内可用)")
        console.print("  - LLM_API_OPENAI_KEY")
        console.print("  - LLM_API_ANTHROPIC_KEY")
        sys.exit(1)

    # 显示欢迎信息
    show_intro()

    # 选择模型提供者（优先使用 DeepSeek）
    if "deepseek" in available_providers:
        model_provider = "deepseek"
        console.print("[green]✓ 使用 DeepSeek 模型[/green]")
    elif "anthropic" in available_providers:
        model_provider = "anthropic"
        console.print("[green]✓ 使用 Anthropic 模型[/green]")
    else:
        model_provider = "openai"
        console.print("[green]✓ 使用 OpenAI 模型[/green]")

    # 创建智能体
    agent = AStockAgent(
        max_steps=20,
        max_steps_per_task=5,
        model=model_provider
    )

    # 交互循环
    while True:
        try:
            # 获取用户输入
            query = console.input("\n[bold cyan]请输入您的问题: [/bold cyan]")

            if not query.strip():
                continue

            if query.lower() in ['exit', 'quit', 'q']:
                console.print("\n[bold green]感谢使用 A股投资专业助手！[/bold green]")
                break

            # 执行分析
            console.print()
            result = agent.run(query)

            # 显示结果
            if result:
                result_panel = Panel(
                    result,
                    title="📈 分析结果",
                    title_align="left",
                    border_style="green"
                )
                console.print(result_panel)

        except KeyboardInterrupt:
            console.print("\n\n[yellow]分析被中断[/yellow]")
            continue
        except Exception as e:
            console.print(f"\n[red]发生错误: {str(e)}[/red]")
            continue


if __name__ == "__main__":
    main()
