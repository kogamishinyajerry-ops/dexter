"""A股工具集"""

from .quote import (
    astock_get_quote,
    astock_get_kline,
    astock_get_sector_performance,
    astock_get_index_data,
)
from .financial import (
    astock_get_financial_indicators,
    astock_get_financial_statement,
    astock_compare_with_peers,
)

# 导出工具列表
ASTOCK_TOOLS = [
    # 行情工具
    astock_get_quote,
    astock_get_kline,
    astock_get_sector_performance,
    astock_get_index_data,
    # 财务工具
    astock_get_financial_indicators,
    astock_get_financial_statement,
    astock_compare_with_peers,
]

__all__ = [
    'astock_get_quote',
    'astock_get_kline',
    'astock_get_sector_performance',
    'astock_get_index_data',
    'astock_get_financial_indicators',
    'astock_get_financial_statement',
    'astock_compare_with_peers',
    'ASTOCK_TOOLS',
]
