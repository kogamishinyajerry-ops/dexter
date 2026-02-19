"""日志工具"""

from typing import Any, Dict, List
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.text import Text


class Logger:
    """日志记录器"""

    def __init__(self):
        self.console = Console()
        self.ui = UI(self.console)

    def _log(self, message: str, style: str = "dim"):
        """内部日志"""
        self.console.print(f"  {message}", style=style)

    def log_user_query(self, query: str):
        """记录用户查询"""
        panel = Panel(
            Text(query, style="bold cyan"),
            title="📊 用户问题",
            title_align="left",
            border_style="cyan"
        )
        self.console.print(panel)
        self.console.print()

    def log_task_list(self, tasks: List[Dict]):
        """记录任务列表"""
        if not tasks:
            return

        table = Table(title="📋 执行计划", show_header=True, header_style="bold magenta")
        table.add_column("ID", style="dim", width=6)
        table.add_column("任务描述", style="cyan")
        table.add_column("状态", justify="center", width=10)

        for task in tasks:
            status = "✓ 完成" if task.get('done') else "○ 待办"
            style = "green" if task.get('done') else "yellow"
            table.add_row(str(task['id']), task['description'], Text(status, style=style))

        self.console.print(table)
        self.console.print()

    def log_task_start(self, task_desc: str):
        """记录任务开始"""
        self._log(f"▶ 开始任务: {task_desc}", style="blue bold")

    def log_task_done(self, task_desc: str):
        """记录任务完成"""
        self._log(f"✓ 任务完成: {task_desc}", style="green bold")
        self.console.print()

    def log_tool_run(self, args: Any, result: Any):
        """记录工具执行"""
        # 结果可能很大，只记录摘要
        if isinstance(result, dict):
            if 'error' in result:
                self._log(f"  ⚠ {result['error']}", style="red")
            elif 'data' in result:
                self._log(f"  ✓ 获取到数据", style="green")
            else:
                self._log(f"  ✓ 工具执行成功", style="green")
        else:
            self._log(f"  ✓ 工具执行成功", style="green")


class UI:
    """用户界面"""

    def __init__(self, console: Console):
        self.console = console

    def stream_answer(self, text_chunks):
        """流式显示答案"""
        answer = ""
        self.console.print("\n")
        with self.console.status("[bold green]生成分析报告...", spinner="dots"):
            for chunk in text_chunks:
                answer += chunk
        return answer

    def display_progress(self, message: str, done_message: str):
        """显示进度"""
        pass  # 可以使用 @show_progress 装饰器实现
