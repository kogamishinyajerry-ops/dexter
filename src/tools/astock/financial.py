"""
A股财务数据工具 - 基于 akshare
"""

from typing import List, Optional
from datetime import datetime
import akshare as ak
import pandas as pd
from langchain.tools import tool
from pydantic import BaseModel, Field


class FinancialIndicatorInput(BaseModel):
    """获取财务指标参数"""
    symbol: str = Field(description="股票代码，如 600519")
    period: Optional[str] = Field(default="all", description="周期: all(全部), latest(最新)")


class FinancialStatementInput(BaseModel):
    """获取财务报表参数"""
    symbol: str = Field(description="股票代码，如 600519")
    statement_type: str = Field(description="报表类型: balance(资产负债表), profit(利润表), cash(现金流量表)")
    period: Optional[str] = Field(default="year", description="周期: year(年报), quarter(季报)")


@tool(args_schema=FinancialIndicatorInput)
def astock_get_financial_indicators(symbol: str, period: str = "all") -> dict:
    """
    获取A股财务指标数据

    包括市盈率、市净率、ROE、ROA、毛利率、净利率、负债率等核心财务指标。

    Args:
        symbol: 股票代码，如 600519
        period: 周期: all(全部数据), latest(最新一期)

    Returns:
        包含财务指标的字典，包括：
        - 报告期
        - 市盈率(PE)
        - 市净率(PB)
        - 总市值
        - 流通市值
        - 净资产收益率(ROE)
        - 资产收益率(ROA)
        - 毛利率
        - 净利率
        - 资产负债率
        - 流动比率
        - 速动比率
        - 每股收益(EPS)
        - 每股净资产(BPS)
        - 营业收入增长率
        - 净利润增长率
    """
    try:
        # 标准化股票代码
        symbol = symbol.upper().replace('.SZ', '').replace('.SH', '')

        # 获取财务指标
        df = ak.stock_financial_analysis_indicator(symbol=symbol)

        if df.empty:
            return {
                "error": f"未获取到股票 {symbol} 的财务指标数据",
                "symbol": symbol
            }

        # 转换为字典列表
        records = []
        for _, row in df.iterrows():
            record = {
                "date": str(row.get('date', '')),
                "pe": float(row.get('pe', 0)) if pd.notna(row.get('pe')) else None,
                "pb": float(row.get('pb', 0)) if pd.notna(row.get('pb')) else None,
                "total_mv": float(row.get('total_mv', 0)) if pd.notna(row.get('total_mv')) else None,
                "circ_mv": float(row.get('circ_mv', 0)) if pd.notna(row.get('circ_mv')) else None,
                "roe": float(row.get('roe', 0)) if pd.notna(row.get('roe')) else None,  # ROE
                "roa": float(row.get('roa', 0)) if pd.notna(row.get('roa')) else None,  # ROA
                "gross_margin": float(row.get('gross_margin', 0)) if pd.notna(row.get('gross_margin')) else None,  # 毛利率
                "net_margin": float(row.get('net_margin', 0)) if pd.notna(row.get('net_margin')) else None,  # 净利率
                "debt_to_assets": float(row.get('debt_to_assets', 0)) if pd.notna(row.get('debt_to_assets')) else None,  # 资产负债率
                "current_ratio": float(row.get('current_ratio', 0)) if pd.notna(row.get('current_ratio')) else None,  # 流动比率
                "quick_ratio": float(row.get('quick_ratio', 0)) if pd.notna(row.get('quick_ratio')) else None,  # 速动比率
                "eps": float(row.get('eps', 0)) if pd.notna(row.get('eps')) else None,  # 每股收益
                "bps": float(row.get('bps', 0)) if pd.notna(row.get('bps')) else None,  # 每股净资产
                "revenue_growth_rate": float(row.get('revenue_growth_rate', 0)) if pd.notna(row.get('revenue_growth_rate')) else None,  # 营收增长率
                "profit_growth_rate": float(row.get('profit_growth_rate', 0)) if pd.notna(row.get('profit_growth_rate')) else None,  # 利润增长率
            }
            records.append(record)

        # 如果只要最新一期
        if period == "latest" and records:
            records = [records[0]]

        result = {
            "data_source": "akshare",
            "symbol": symbol,
            "total_count": len(records),
            "data": records
        }

        return result

    except Exception as e:
        return {
            "error": f"获取财务指标失败: {str(e)}",
            "symbol": symbol
        }


@tool(args_schema=FinancialStatementInput)
def astock_get_financial_statement(symbol: str, statement_type: str = "profit", period: str = "year") -> dict:
    """
    获取A股财务报表数据

    支持资产负债表、利润表、现金流量表的年报和季报数据。

    Args:
        symbol: 股票代码，如 600519
        statement_type: 报表类型
                        - balance: 资产负债表
                        - profit: 利润表
                        - cash: 现金流量表
        period: 周期: year(年报), quarter(季报)

    Returns:
        包含财务报表数据的字典
    """
    try:
        symbol = symbol.upper().replace('.SZ', '').replace('.SH', '')

        # 根据报表类型获取数据
        if statement_type == "balance":
            # 资产负债表
            df = ak.stock_balance_sheet_by_yearly_em(symbol=symbol) if period == "year" else \
                 ak.stock_balance_sheet_by_quarterly_em(symbol=symbol)
            statement_name = "资产负债表"
        elif statement_type == "profit":
            # 利润表
            df = ak.stock_profit_sheet_by_yearly_em(symbol=symbol) if period == "year" else \
                 ak.stock_profit_sheet_by_quarterly_em(symbol=symbol)
            statement_name = "利润表"
        elif statement_type == "cash":
            # 现金流量表
            df = ak.stock_cash_flow_sheet_by_yearly_em(symbol=symbol) if period == "year" else \
                 ak.stock_cash_flow_sheet_by_quarterly_em(symbol=symbol)
            statement_name = "现金流量表"
        else:
            return {
                "error": f"不支持的报表类型: {statement_type}，支持: balance, profit, cash",
                "symbol": symbol
            }

        if df.empty:
            return {
                "error": f"未获取到{statement_name}数据",
                "symbol": symbol,
                "statement_type": statement_type
            }

        # 转换为字典
        records = []
        for _, row in df.iterrows():
            records.append({
                "date": str(row.get('date', '')),
                "data": row.to_dict()
            })

        result = {
            "data_source": "akshare",
            "symbol": symbol,
            "statement_type": statement_type,
            "statement_name": statement_name,
            "period": period,
            "total_count": len(records),
            "data": records
        }

        return result

    except Exception as e:
        return {
            "error": f"获取财务报表失败: {str(e)}",
            "symbol": symbol,
            "statement_type": statement_type
        }


@tool
def astock_compare_with_peers(symbol: str, industry: str = None) -> dict:
    """
    同行业财务指标对比

    将指定股票与同行业公司的财务指标进行对比分析。

    Args:
        symbol: 股票代码，如 600519
        industry: 行业名称，如 白酒，如果为空则自动获取

    Returns:
        包含同行业对比数据的字典
    """
    try:
        symbol = symbol.upper().replace('.SZ', '').replace('.SH', '')

        # 如果没有指定行业，先获取股票的行业
        if not industry:
            stock_info = ak.stock_individual_info_em(symbol=symbol)
            industry = stock_info[stock_info['item'] == '行业']['value'].values[0] if not stock_info.empty else ""

        if not industry:
            return {
                "error": f"无法获取股票 {symbol} 的行业信息",
                "symbol": symbol
            }

        # 获取行业股票列表（这里简化处理，实际需要更复杂的逻辑）
        # 实际项目中可以从行业分类数据源获取

        # 这里返回示例数据，实际应该从行业数据源获取
        result = {
            "data_source": "akshare",
            "symbol": symbol,
            "industry": industry,
            "message": "同行业对比功能需要行业股票列表，当前返回示例数据",
            "peer_data": []
        }

        return result

    except Exception as e:
        return {
            "error": f"获取同行业对比失败: {str(e)}",
            "symbol": symbol
        }
