"""模型接口 - LLM 调用"""

from typing import List, Optional, Literal, TypedDict, Union
from langchain_openai import ChatOpenAI
from langchain_anthropic import ChatAnthropic
from langchain_core.messages import AIMessage, BaseMessage
from langchain_core.runnables import RunnableConfig
import os


# 模型提供者
MODEL_PROVIDER = Literal["openai", "anthropic", "deepseek"]

# 默认模型
DEFAULT_MODEL_PROVIDER: MODEL_PROVIDER = "deepseek"  # 默认使用 DeepSeek


class ModelConfig(TypedDict):
    """模型配置"""
    provider: MODEL_PROVIDER
    model: str
    strong_model: Optional[str]
    temperature: float
    max_tokens: int


def get_model_config(provider: MODEL_PROVIDER = "deepseek") -> ModelConfig:
    """
    获取模型配置

    Args:
        provider: 模型提供者

    Returns:
        模型配置字典
    """
    if provider == "openai":
        return ModelConfig(
            provider="openai",
            model=os.getenv("LLM_API_OPENAI_MODEL", "gpt-4o"),
            strong_model=os.getenv("LLM_API_OPENAI_STRONG_MODEL", "gpt-4o"),
            temperature=0.1,
            max_tokens=4096
        )
    elif provider == "anthropic":
        return ModelConfig(
            provider="anthropic",
            model=os.getenv("LLM_API_ANTHROPIC_MODEL", "claude-3-5-sonnet-20241022"),
            strong_model=os.getenv("LLM_API_ANTHROPIC_STRONG_MODEL", "claude-3-5-sonnet-20241022"),
            temperature=0.1,
            max_tokens=4096
        )
    elif provider == "deepseek":
        return ModelConfig(
            provider="deepseek",
            model=os.getenv("DEEPSEEK_MODEL", "deepseek-chat"),
            strong_model=os.getenv("DEEPSEEK_STRONG_MODEL", "deepseek-reasoner"),
            temperature=0.1,
            max_tokens=4096
        )
    else:
        raise ValueError(f"不支持的模型提供者: {provider}")


def _get_llm(
    provider: MODEL_PROVIDER = "deepseek",
    model_type: Literal["normal", "strong"] = "normal",
    temperature: float = 0.1
) -> Union[ChatOpenAI, ChatAnthropic]:
    """
    获取 LLM 实例

    Args:
        provider: 模型提供者
        model_type: 模型类型
        temperature: 温度

    Returns:
        LLM 实例
    """
    config = get_model_config(provider)

    # 选择模型
    model_name = config["strong_model"] if model_type == "strong" else config["model"]
    temp = temperature if model_type == "normal" else 0.3  # 强模型用稍高温度

    if provider == "openai":
        api_key = os.getenv("LLM_API_OPENAI_KEY")
        if not api_key:
            raise ValueError("未设置 LLM_API_OPENAI_KEY")

        return ChatOpenAI(
            model=model_name,
            temperature=temp,
            max_tokens=config["max_tokens"],
            api_key=api_key
        )

    elif provider == "anthropic":
        api_key = os.getenv("LLM_API_ANTHROPIC_KEY")
        if not api_key:
            raise ValueError("未设置 LLM_API_ANTHROPIC_KEY")

        return ChatAnthropic(
            model=model_name,
            temperature=temp,
            max_tokens=config["max_tokens"],
            api_key=api_key
        )

    elif provider == "deepseek":
        api_key = os.getenv("DEEPSEEK_API_KEY")
        if not api_key:
            raise ValueError("未设置 DEEPSEEK_API_KEY")

        base_url = os.getenv("DEEPSEEK_BASE_URL", "https://api.deepseek.com/v1")

        return ChatOpenAI(
            model=model_name,
            temperature=temp,
            max_tokens=config["max_tokens"],
            api_key=api_key,
            base_url=base_url
        )


def call_llm(
    prompt: str,
    system_prompt: str = "",
    tools: Optional[List] = None,
    output_schema: Optional[type] = None,
    model_type: Literal["normal", "strong"] = "normal",
    model: MODEL_PROVIDER = DEFAULT_MODEL_PROVIDER
) -> AIMessage | dict:
    """
    调用 LLM

    Args:
        prompt: 用户提示
        system_prompt: 系统提示
        tools: 工具列表
        output_schema: 输出 schema (用于结构化输出)
        model_type: 模型类型
        model: 模型提供者

    Returns:
        LLM 响应
    """
    llm = _get_llm(provider=model, model_type=model_type)

    # 构建消息
    messages: List[BaseMessage] = []

    if system_prompt:
        messages.append(("system", system_prompt))

    messages.append(("user", prompt))

    # 配置
    config: RunnableConfig = {}

    # 工具调用
    if tools:
        llm = llm.bind_tools(tools)

    # 结构化输出
    if output_schema:
        llm = llm.with_structured_output(output_schema)

    # 调用
    response = llm.invoke(messages, config)

    return response


def call_llm_stream(
    prompt: str,
    system_prompt: str = "",
    model_type: Literal["normal", "strong"] = "strong",
    model: MODEL_PROVIDER = DEFAULT_MODEL_PROVIDER
):
    """
    流式调用 LLM

    Args:
        prompt: 用户提示
        system_prompt: 系统提示
        model_type: 模型类型（答案生成默认用强模型）
        model: 模型提供者

    Yields:
        文本块
    """
    llm = _get_llm(provider=model, model_type=model_type)

    # 构建消息
    messages: List[BaseMessage] = []

    if system_prompt:
        messages.append(("system", system_prompt))

    messages.append(("user", prompt))

    # 流式调用
    for chunk in llm.stream(messages):
        if hasattr(chunk, 'content') and chunk.content:
            yield chunk.content
