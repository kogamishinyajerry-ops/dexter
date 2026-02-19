"""上下文管理器"""

import json
import os
from pathlib import Path
from typing import Any, Dict, List
from datetime import datetime


class ContextManager:
    """上下文管理器 - 管理大数据量到文件"""

    def __init__(self, model: str = "openai"):
        self.model = model
        self.base_dir = Path(".dexter_context")
        self.base_dir.mkdir(exist_ok=True)
        self.pointers: List[Dict] = []  # 存储上下文指针（轻量级）

    def save_context(self, tool_name: str, args: dict, result: dict, task_id: int) -> str:
        """
        保存工具输出到文件

        Args:
            tool_name: 工具名称
            args: 工具参数
            result: 工具输出
            task_id: 任务ID

        Returns:
            文件路径
        """
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S_%f")
        filename = f"task_{task_id}_{tool_name}_{timestamp}.json"
        filepath = self.base_dir / filename

        # 保存完整数据
        context = {
            "tool_name": tool_name,
            "args": args,
            "result": result,
            "task_id": task_id,
            "timestamp": timestamp
        }

        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(context, f, ensure_ascii=False, indent=2)

        # 生成摘要（轻量级）
        summary = self._generate_summary(result)

        # 保存指针
        pointer = {
            "file_path": str(filepath),
            "tool_name": tool_name,
            "args": args,
            "summary": summary,
            "task_id": task_id,
            "timestamp": timestamp
        }
        self.pointers.append(pointer)

        return str(filepath)

    def _generate_summary(self, result: dict) -> str:
        """生成数据摘要"""
        if 'error' in result:
            return f"错误: {result['error']}"

        if 'data' in result:
            data = result['data']
            if isinstance(data, list) and len(data) > 0:
                return f"包含 {len(data)} 条记录"
            return "数据已获取"

        if 'symbol' in result:
            return f"股票 {result['symbol']} 的数据"

        return "数据已获取"

    def get_all_pointers(self) -> List[Dict]:
        """获取所有上下文指针"""
        return self.pointers

    def select_relevant_contexts(self, query: str, pointers: List[Dict]) -> List[str]:
        """
        选择相关的上下文（简化版，实际应使用 LLM）

        Args:
            query: 用户查询
            pointers: 所有上下文指针

        Returns:
            相关上下文的文件路径列表
        """
        # 简化版：返回所有上下文
        # 实际应该使用 LLM 进行相关性评分和筛选
        return [p['file_path'] for p in pointers]

    def load_contexts(self, filepaths: List[str]) -> List[Dict]:
        """加载上下文数据"""
        contexts = []
        for filepath in filepaths:
            try:
                with open(filepath, 'r', encoding='utf-8') as f:
                    context = json.load(f)
                    contexts.append(context)
            except Exception as e:
                continue
        return contexts

    def cleanup(self):
        """清理旧数据"""
        pass  # 可以添加清理逻辑
