"""
核心智能体模块 - 基于 Dexter 架构改造
"""

from typing import List, Optional
from datetime import datetime

from langchain_core.messages import AIMessage
from langsmith import traceable, trace

from .model import call_llm, call_llm_stream, DEFAULT_MODEL_PROVIDER
from .prompts import (
    ACTION_SYSTEM_PROMPT,
    get_answer_system_prompt,
    PLANNING_SYSTEM_PROMPT,
    VALIDATION_SYSTEM_PROMPT,
    META_VALIDATION_SYSTEM_PROMPT,
)
from .schemas import IsDone, Task, TaskList
from src.tools import TOOLS
from .utils import Logger
from .utils.ui import show_progress
from .utils import ContextManager


class AStockAgent:
    """A股投资分析智能体"""

    def __init__(
        self,
        max_steps: int = 20,
        max_steps_per_task: int = 5,
        model: str = DEFAULT_MODEL_PROVIDER,
    ):
        """
        初始化智能体

        Args:
            max_steps: 全局最大步骤限制（安全机制）
            max_steps_per_task: 每个任务的最大步骤限制
            model: 使用的 LLM 模型
        """
        self.logger = Logger()
        self.max_steps = max_steps
        self.max_steps_per_task = max_steps_per_task
        self.model = model
        self.context_manager = ContextManager(model=model)

    def plan_tasks(self, query: str) -> List[Task]:
        """
        将用户查询分解为任务列表

        Args:
            query: 用户的自然语言查询

        Returns:
            任务列表
        """
        with trace(name="task_planning"):
            # 获取可用工具描述
            tool_descriptions = "\n".join(
                [f"- {t.name}: {t.description}" for t in TOOLS["astock"]]
            )

            prompt = f"""
            针对用户的投资研究问题: "{query}"

            请创建一个任务列表来完成分析。
            A股投资分析通常包括以下几个方面：
            - 基本面分析（财务数据、估值、行业地位）
            - 技术面分析（价格走势、技术指标）
            - 资金面分析（资金流向、北向资金）
            - 消息面分析（新闻资讯、公告、政策）

            请根据问题类型，合理规划任务顺序。
            示例格式: {{"tasks": [{{"id": 1, "description": "获取茅台的财务指标", "done": false}}]}}

            可用工具列表:
            {tool_descriptions}
            """
            system_prompt = PLANNING_SYSTEM_PROMPT.format(tools=tool_descriptions)

            try:
                response = call_llm(
                    prompt, system_prompt=system_prompt, output_schema=TaskList
                )
                tasks = response.tasks
            except Exception as e:
                self.logger._log(f"任务规划失败: {e}")
                # 降级处理：直接创建一个任务
                tasks = [Task(id=1, description=query, done=False)]

            # 记录任务列表
            task_dicts = [task.model_dump() for task in tasks]
            self.logger.log_task_list(task_dicts)
            return tasks

    def ask_for_actions(self, task_desc: str, last_outputs: str = "") -> AIMessage:
        """
        询问 LLM 下一步应该采取什么行动

        Args:
            task_desc: 当前任务描述
            last_outputs: 之前的工具输出摘要

        Returns:
            AI 消息，可能包含工具调用
        """
        with trace(name="ask_for_further_actions"):
            prompt = f"""
            当前任务: "{task_desc}"

            之前的工具输出历史:
            {last_outputs}

            对于 akshare 相关工具（astock_ 前缀），如果工具调用已经返回空结果或错误，不要重复调用相同的工具。

            基于当前任务和已有的输出，下一步应该做什么？

            如果没有更多工具需要调用，可以直接返回最终答案。
            如果任务说明之前的任务已经收集了数据，或者只是综合之前的信息，也可以直接返回答案。

            不要询问确认问题，自主做出判断。

            A股投资注意事项:
            - 优先使用复权价格进行技术分析
            - 波动率应年化（sqrt(252)因子）
            - 关注北向资金流向作为外资风向标
            - 注意A股特有的涨跌停限制
            - 关注融资融券余额变化
            """
            try:
                return call_llm(
                    prompt,
                    system_prompt=ACTION_SYSTEM_PROMPT,
                    tools=TOOLS["astock"],
                    model=self.model,
                )
            except Exception as e:
                self.logger._log(f"获取行动失败: {e}")
                return AIMessage(content="获取行动失败")

    def ask_if_done(self, task_desc: str, recent_results: str) -> bool:
        """
        检查当前任务是否完成

        Args:
            task_desc: 任务描述
            recent_results: 最近的工具输出

        Returns:
            任务是否完成
        """
        with trace(name="ask_if_done"):
            prompt = f"""
            我们正在完成任务: "{task_desc}"

            最近的工具输出摘要:
            {recent_results}

            根据以上信息，任务是否已完成？
            """
            try:
                resp = call_llm(
                    prompt,
                    system_prompt=VALIDATION_SYSTEM_PROMPT,
                    output_schema=IsDone,
                    model=self.model,
                )
                return resp.done
            except Exception:
                return False

    def is_goal_achieved(
        self, query: str, task_outputs: list, tasks: List[Task]
    ) -> bool:
        """
        检查整体目标是否达成

        Args:
            query: 原始用户查询
            task_outputs: 所有任务输出
            tasks: 任务列表

        Returns:
            目标是否达成
        """
        with trace(name="is_goal_achieved"):
            all_results = "\n\n".join(task_outputs) if task_outputs else "尚未收集数据"

            # 格式化任务状态
            tasks_info = []
            for task in tasks:
                status = "✓ 完成" if task.done else "✗ 未完成"
                tasks_info.append(f"- [{status}] {task.description}")
            tasks_summary = "\n".join(tasks_info) if tasks_info else "未规划任务"

            prompt = f"""
            原始用户问题: "{query}"

            计划的任务（仅供参考，不是硬性要求）:
            {tasks_summary}

            已收集的数据和结果:
            {all_results}

            基于以上数据，用户的原始问题是否得到了充分回答？
            请以任务列表作为参考，但重点是问题本身是否得到回答。
            """
            try:
                resp = call_llm(
                    prompt,
                    system_prompt=META_VALIDATION_SYSTEM_PROMPT,
                    output_schema=IsDone,
                    model=self.model,
                )
                return resp.done
            except Exception as e:
                self.logger._log(f"目标检查失败: {e}")
                return False

    def _execute_tool(self, tool, tool_name: str, inp_args):
        """执行工具并显示进度"""
        @show_progress(f"正在执行 {tool_name}...", "")
        def run_tool():
            return tool.run(inp_args)
        return run_tool()

    def confirm_action(self, tool: str, input_str: str) -> bool:
        """确认是否执行工具（这里自动确认）"""
        return True

    @traceable
    def run(self, query: str) -> str:
        """
        执行主循环，处理用户查询

        Args:
            query: 用户的自然语言查询

        Returns:
            综合分析结果
        """
        # 显示用户查询
        self.logger.log_user_query(query)

        # 初始化状态
        step_count = 0
        last_actions = []
        task_output_summaries = []
        tasks: List[Task] = []

        try:
            # 1. 分解任务
            tasks = self.plan_tasks(query)

            if not tasks or len(tasks) == 0:
                # 无任务，直接生成答案
                answer = self._generate_answer(query, tasks)
                return answer

            # 2. 循环执行任务
            task_id = 0
            while any(not t.done for t in tasks):
                # 全局安全检查
                if step_count >= self.max_steps:
                    self.logger._log("达到全局最大步骤限制，停止执行")
                    break

                # 选择下一个未完成任务
                task = next(t for t in tasks if not t.done)
                task_id += 1

                with trace(
                    name=f"task_{task_id}: {task.description}",
                    metadata={"task_description": task.description},
                ):
                    self.logger.log_task_start(task.description)

                    per_task_steps = 0
                    task_step_summaries = []

                    # 执行任务直到完成或达到限制
                    while per_task_steps < self.max_steps_per_task:
                        if step_count >= self.max_steps:
                            self.logger._log("达到全局最大步骤限制")
                            return

                        # 询问下一步行动
                        ai_message = self.ask_for_actions(
                            task.description,
                            last_outputs="\n".join(task_step_summaries),
                        )

                        # 无工具调用，任务完成
                        if not ai_message.tool_calls:
                            task.done = True
                            self.logger.log_task_done(task.description)
                            break

                        # 处理每个工具调用
                        for tool_call in ai_message.tool_calls:
                            if step_count >= self.max_steps:
                                break

                            tool_name = tool_call["name"]
                            tool_args = tool_call["args"]

                            # 循环检测
                            action_sig = f"{tool_name}:{tool_args}"
                            last_actions.append(action_sig)
                            if len(last_actions) > 4:
                                last_actions = last_actions[-4:]
                            if len(set(last_actions)) == 1 and len(last_actions) == 4:
                                self.logger._log("检测到重复动作，停止执行")
                                task.done = True
                                self.logger.log_task_done(task.description)
                                break

                            # 执行工具
                            tool_to_run = next(
                                (t for t in TOOLS["astock"] if t.name == tool_name),
                                None,
                            )
                            if tool_to_run and self.confirm_action(tool_name, str(tool_args)):
                                try:
                                    result = self._execute_tool(
                                        tool_to_run, tool_name, tool_args
                                    )
                                    self.logger.log_tool_run(tool_args, result)

                                    # 保存上下文到文件
                                    context_path = self.context_manager.save_context(
                                        tool_name=tool_name,
                                        args=tool_args,
                                        result=result,
                                        task_id=task.id,
                                    )

                                    # 记录摘要
                                    pointer = self.context_manager.pointers[-1]
                                    summary = f"{tool_name}({tool_args}): {pointer['summary']}"
                                    task_output_summaries.append(summary)
                                    task_step_summaries.append(summary)

                                except Exception as e:
                                    self.logger._log(f"工具执行失败: {e}")
                                    error_summary = f"{tool_name}({tool_args}) 错误: {e}"
                                    task_output_summaries.append(error_summary)
                                    task_step_summaries.append(error_summary)

                            step_count += 1
                            per_task_steps += 1

                        # 检查任务是否完成
                        if self.ask_if_done(
                            task.description, "\n".join(task_step_summaries)
                        ):
                            task.done = True
                            self.logger.log_task_done(task.description)
                            break

                # 检查整体目标是否达成
                if task.done and self.is_goal_achieved(
                    query, task_output_summaries, tasks
                ):
                    self.logger._log("主目标已达成，生成最终答案")
                    break

        except KeyboardInterrupt:
            self.logger._log("执行被用户中断")
            return

        # 生成最终答案
        answer = self._generate_answer(query, tasks)
        return answer

    def _generate_answer(self, query: str, execution_plan: List[Task]) -> str:
        """生成最终答案"""
        with trace(name="answer_generation"):
            # 获取所有上下文指针
            all_pointers = self.context_manager.get_all_pointers()

            if not all_pointers:
                answer_prompt = f"""
                原始用户问题: "{query}"

                未收集到任何工具数据。
                """
            else:
                # 选择相关上下文
                selected_filepaths = self.context_manager.select_relevant_contexts(
                    query, all_pointers
                )

                # 加载上下文
                selected_contexts = self.context_manager.load_contexts(selected_filepaths)

                # 格式化上下文
                formatted_results = []
                for ctx in selected_contexts:
                    tool_name = ctx.get("tool_name", "unknown")
                    args = ctx.get("args", {})
                    result = ctx.get("result", {})
                    formatted_results.append(
                        f"{tool_name}({args}) 的输出:\n{result}"
                    )

                all_results = "\n\n".join(formatted_results)

                answer_prompt = f"""
                原始用户问题: "{query}"

                执行计划:
                {execution_plan}

                工具收集的数据和结果:
                {all_results}

                基于以上数据，为用户提供专业的投资分析。
                请包含具体的数据、计算和洞察，并给出合理的投资建议。

                注意事项:
                - 明确说明数据的来源和时间范围
                - 对关键指标进行解释
                - 指出潜在的风险因素
                - 给出客观的投资建议（不做买卖建议，只做分析判断）
                """

            # 流式生成答案
            text_chunks = call_llm_stream(
                answer_prompt,
                system_prompt=get_answer_system_prompt(),
                model_type="strong",
                model=self.model,
            )
            accumulated_answer = self.logger.ui.stream_answer(text_chunks)

            return accumulated_answer
