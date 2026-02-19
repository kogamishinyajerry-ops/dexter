"""数据模型定义"""

from typing import List
from pydantic import BaseModel, Field


class Task(BaseModel):
    """任务模型"""
    id: int = Field(description="任务ID")
    description: str = Field(description="任务描述")
    done: bool = Field(default=False, description="是否完成")


class TaskList(BaseModel):
    """任务列表"""
    tasks: List[Task] = Field(description="任务列表")


class IsDone(BaseModel):
    """任务完成状态"""
    done: bool = Field(description="是否完成")


class OptimizedToolArgs(BaseModel):
    """优化后的工具参数"""
    arguments: dict = Field(description="优化后的参数")
