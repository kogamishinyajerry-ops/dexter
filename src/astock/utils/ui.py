"""UI 工具"""

from functools import wraps
from rich.console import Console
from rich.status import Status


console = Console()


def show_progress(message: str, done_message: str):
    """
    显示进度的装饰器

    Args:
        message: 进行中的消息
        done_message: 完成后的消息
    """
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            with console.status(f"[bold blue]{message}...", spinner="dots"):
                result = func(*args, **kwargs)
            return result
        return wrapper
    return decorator
