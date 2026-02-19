"""
A股行情数据工具 - 基于 akshare
"""

from typing import List, Optional
from datetime import datetime
import akshare as ak
import pandas as pd
from langchain.tools import tool
from pydantic import BaseModel, Field


class StockQuoteInput(BaseModel):
    """获取股票实时行情参数"""
    symbol: str = Field(description="股票代码，如 600519 (茅台) 或 000001.SZ (深交所格式)")
    fields: Optional[List[str]] = Field(default=None, description="需要返回的字段列表，默认全部")


class KlineDataInput(BaseModel):
    """获取K线数据参数"""
    symbol: str = Field(description="股票代码，如 600519")
    period: str = Field(description="周期: daily(日线), weekly(周线), monthly(月线)", default="daily")
    start_date: str = Field(description="开始日期，格式 YYYYMMDD")
    end_date: str = Field(description="结束日期，格式 YYYYMMDD，默认为今天")
    adjust: str = Field(description="复权方式: qfq(前复权), hfq(后复权), ''(不复权)", default="qfq")


class SectorPerformanceInput(BaseModel):
    """获取板块表现参数"""
    sector_type: str = Field(description="板块类型: concept(概念), industry(行业), area(地域)")


@tool(args_schema=StockQuoteInput)
def astock_get_quote(symbol: str, fields: Optional[List[str]] = None) -> dict:
    """
    获取A股主板实时行情数据

    使用 akshare 的 stock_zh_a_spot_em() 获取实时行情。
    【重要】本工具仅支持A股主板，不包括科创板和创业板。

    Args:
        symbol: 股票代码，仅支持主板：
                - 沪市主板: 600xxx, 601xxx, 603xxx, 605xxx (如 600519 茅台)
                - 深市主板: 000xxx, 001xxx, 002xxx, 003xxx (如 000001 平安)
                - 不支持: 300xxx (创业板)、688xxx (科创板)
        fields: 需要返回的字段，如 ["代码", "名称", "最新价", "涨跌幅", "成交量", "成交额"]

    Returns:
        包含行情数据的字典，包括：
        - 股票代码
        - 股票名称
        - 最新价
        - 涨跌幅
        - 涨跌额
        - 开盘价
        - 最高价
        - 最低价
        - 昨收价
        - 成交量
        - 成交额
        - 换手率
        - 市盈率
        - 市净率
        - 总市值
        - 流通市值
        - 数据时间
    """
    try:
        # 标准化股票代码
        symbol = symbol.upper().replace('.SZ', '').replace('.SH', '').replace('.SS', '')

        # 检查是否为主板股票
        if symbol.startswith('688'):
            return {
                "error": f"股票代码 {symbol} 属于科创板，本项目仅支持主板股票",
                "symbol": symbol,
                "note": "支持主板：沪市(600/601/603/605)、深市(000/001/002/003)"
            }
        if symbol.startswith('300'):
            return {
                "error": f"股票代码 {symbol} 属于创业板，本项目仅支持主板股票",
                "symbol": symbol,
                "note": "支持主板：沪市(600/601/603/605)、深市(000/001/002/003)"
            }

        # 获取所有A股实时行情
        df = ak.stock_zh_a_spot_em()

        # 查找目标股票
        stock_data = df[df['代码'] == symbol]

        if stock_data.empty:
            return {
                "error": f"未找到股票代码 {symbol}，请检查代码是否正确",
                "symbol": symbol
            }

        # 转为字典
        data = stock_data.iloc[0].to_dict()

        # 字段过滤
        if fields:
            data = {k: v for k, v in data.items() if k in fields}

        # 添加元数据
        result = {
            "data_source": "akshare",
            "symbol": symbol,
            "data": data,
            "timestamp": datetime.now().isoformat()
        }

        return result

    except Exception as e:
        return {
            "error": f"获取行情数据失败: {str(e)}",
            "symbol": symbol
        }


@tool(args_schema=KlineDataInput)
def astock_get_kline(
    symbol: str,
    period: str = "daily",
    start_date: str = None,
    end_date: str = None,
    adjust: str = "qfq"
) -> dict:
    """
    获取A股主板历史K线数据

    使用 akshare 的 stock_zh_a_hist() 获取历史K线。
    【重要】本工具仅支持A股主板，不包括科创板和创业板。

    Args:
        symbol: 股票代码，仅支持主板：
                - 沪市主板: 600xxx, 601xxx, 603xxx, 605xxx
                - 深市主板: 000xxx, 001xxx, 002xxx, 003xxx
                - 不支持: 300xxx (创业板)、688xxx (科创板)
        period: 周期: daily(日线), weekly(周线), monthly(月线)
        start_date: 开始日期，格式 YYYYMMDD，如 20240101
        end_date: 结束日期，格式 YYYYMMDD，如 20241231，默认为今天
        adjust: 复权方式: qfq(前复权), hfq(后复权), ''(不复权)

    Returns:
        包含K线数据的字典，包括：
        - 日期
        - 开盘价
        - 收盘价
        - 最高价
        - 最低价
        - 成交量
        - 成交额
        - 振幅
        - 涨跌幅
        - 涨跌额
        - 换手率
    """
    try:
        # 标准化参数
        symbol = symbol.upper().replace('.SZ', '').replace('.SH', '')

        # 检查是否为主板股票
        if symbol.startswith('688'):
            return {
                "error": f"股票代码 {symbol} 属于科创板，本项目仅支持主板股票",
                "symbol": symbol,
                "note": "支持主板：沪市(600/601/603/605)、深市(000/001/002/003)"
            }
        if symbol.startswith('300'):
            return {
                "error": f"股票代码 {symbol} 属于创业板，本项目仅支持主板股票",
                "symbol": symbol,
                "note": "支持主板：沪市(600/601/603/605)、深市(000/001/002/003)"
            }

        # 设置默认结束日期
        if not end_date:
            end_date = datetime.now().strftime("%Y%m%d")

        # 设置默认开始日期（默认1年）
        if not start_date:
            from datetime import timedelta
            start_date = (datetime.now() - timedelta(days=365)).strftime("%Y%m%d")

        # 映射周期参数
        period_map = {
            "daily": "日k",
            "weekly": "周k",
            "monthly": "月k"
        }
        period_cn = period_map.get(period, "日k")

        # 获取K线数据
        df = ak.stock_zh_a_hist(
            symbol=symbol,
            period=period_cn,
            start_date=start_date,
            end_date=end_date,
            adjust=adjust
        )

        if df.empty:
            return {
                "error": f"未获取到K线数据，请检查日期范围是否正确",
                "symbol": symbol,
                "period": period
            }

        # 转换为记录列表
        records = []
        for _, row in df.iterrows():
            records.append({
                "date": row['日期'].strftime("%Y-%m-%d") if hasattr(row['日期'], 'strftime') else str(row['日期']),
                "open": float(row['开盘']) if pd.notna(row['开盘']) else None,
                "close": float(row['收盘']) if pd.notna(row['收盘']) else None,
                "high": float(row['最高']) if pd.notna(row['最高']) else None,
                "low": float(row['最低']) if pd.notna(row['最低']) else None,
                "volume": float(row['成交量']) if pd.notna(row['成交量']) else None,
                "amount": float(row['成交额']) if pd.notna(row['成交额']) else None,
                "amplitude": float(row['振幅']) if pd.notna(row['振幅']) else None,
                "change_percent": float(row['涨跌幅']) if pd.notna(row['涨跌幅']) else None,
                "change_amount": float(row['涨跌额']) if pd.notna(row['涨跌额']) else None,
                "turnover": float(row['换手率']) if pd.notna(row['换手率']) else None,
            })

        result = {
            "data_source": "akshare",
            "symbol": symbol,
            "period": period,
            "adjust": adjust,
            "start_date": start_date,
            "end_date": end_date,
            "total_count": len(records),
            "data": records
        }

        return result

    except Exception as e:
        return {
            "error": f"获取K线数据失败: {str(e)}",
            "symbol": symbol,
            "period": period
        }


@tool(args_schema=SectorPerformanceInput)
def astock_get_sector_performance(sector_type: str = "industry") -> dict:
    """
    获取A股板块表现数据

    支持概念板块、行业板块、地域板块的实时表现排行。

    Args:
        sector_type: 板块类型
                    - concept: 概念板块（如 AI、新能源汽车等）
                    - industry: 行业板块（如 银行、医药等）
                    - area: 地域板块（如 上海、广东等）

    Returns:
        包含板块排行的字典，每个板块包括：
        - 板块名称
        - 最新价
        - 涨跌幅
        - 涨跌额
        - 领涨股
        - 成交量
        - 领涨股票代码
    """
    try:
        # 获取板块数据
        if sector_type == "concept":
            df = ak.stock_board_concept_name_em()
            type_name = "概念板块"
        elif sector_type == "industry":
            df = ak.stock_board_industry_name_em()
            type_name = "行业板块"
        elif sector_type == "area":
            df = ak.stock_board_area_name_em()
            type_name = "地域板块"
        else:
            return {
                "error": f"不支持的板块类型: {sector_type}，支持: concept, industry, area"
            }

        if df.empty:
            return {
                "error": f"未获取到{type_name}数据",
                "sector_type": sector_type
            }

        # 转换为列表
        records = []
        for _, row in df.head(100).iterrows():  # 只取前100
            records.append({
                "board_name": row.get('板块名称', ''),
                "price": float(row.get('最新价', 0)) if pd.notna(row.get('最新价')) else None,
                "change_percent": float(row.get('涨跌幅', 0)) if pd.notna(row.get('涨跌幅')) else None,
                "change_amount": float(row.get('涨跌额', 0)) if pd.notna(row.get('涨跌额')) else None,
                "leader": row.get('领涨股', ''),
                "volume": float(row.get('成交量', 0)) if pd.notna(row.get('成交量')) else None,
                "leader_code": row.get('领涨股票代码', ''),
                "timestamp": datetime.now().isoformat()
            })

        result = {
            "data_source": "akshare",
            "sector_type": sector_type,
            "type_name": type_name,
            "total_count": len(records),
            "data": records
        }

        return result

    except Exception as e:
        return {
            "error": f"获取板块数据失败: {str(e)}",
            "sector_type": sector_type
        }


@tool
def astock_get_index_data(index_code: str = "000001") -> dict:
    """
    获取A股主要指数数据

    支持上证指数(000001)、深证成指(399001)、创业板指(399006)、科创50(000688)等。

    Args:
        index_code: 指数代码，默认 000001 (上证指数)

    Returns:
        包含指数实时数据的字典
    """
    try:
        # 获取指数实时数据
        df = ak.stock_zh_index_spot_em()

        # 查找目标指数
        index_data = df[df['代码'] == index_code]

        if index_data.empty:
            return {
                "error": f"未找到指数代码 {index_code}",
                "index_code": index_code
            }

        data = index_data.iloc[0].to_dict()

        result = {
            "data_source": "akshare",
            "index_code": index_code,
            "index_name": data.get('名称', ''),
            "data": {
                "latest_price": float(data.get('最新价', 0)) if pd.notna(data.get('最新价')) else None,
                "change_percent": float(data.get('涨跌幅', 0)) if pd.notna(data.get('涨跌幅')) else None,
                "change_amount": float(data.get('涨跌额', 0)) if pd.notna(data.get('涨跌额')) else None,
                "volume": float(data.get('成交量', 0)) if pd.notna(data.get('成交量')) else None,
                "high": float(data.get('最高', 0)) if pd.notna(data.get('最高')) else None,
                "low": float(data.get('最低', 0)) if pd.notna(data.get('最低')) else None,
            },
            "timestamp": datetime.now().isoformat()
        }

        return result

    except Exception as e:
        return {
            "error": f"获取指数数据失败: {str(e)}",
            "index_code": index_code
        }
