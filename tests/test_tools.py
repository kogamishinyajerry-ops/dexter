"""测试工具"""

import sys
import os

# 添加 src 到路径
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from astock.tools.astock import (
    astock_get_quote,
    astock_get_kline,
    astock_get_financial_indicators,
)


def test_get_quote():
    """测试获取行情"""
    print("\n测试: astock_get_quote")
    print("=" * 50)

    result = astock_get_quote.invoke({"symbol": "600519"})  # 贵州茅台

    if "error" in result:
        print(f"❌ 失败: {result['error']}")
    else:
        print(f"✅ 成功")
        print(f"   股票: {result['data'].get('名称', 'N/A')}")
        print(f"   最新价: {result['data'].get('最新价', 'N/A')}")
        print(f"   涨跌幅: {result['data'].get('涨跌幅', 'N/A')}%")
        print(f"   成交额: {result['data'].get('成交额', 'N/A')}")


def test_get_kline():
    """测试获取K线"""
    print("\n测试: astock_get_kline")
    print("=" * 50)

    result = astock_get_kline.invoke({
        "symbol": "600519",
        "period": "daily",
        "start_date": "20240101",
        "end_date": "20241231"
    })

    if "error" in result:
        print(f"❌ 失败: {result['error']}")
    else:
        print(f"✅ 成功")
        print(f"   数据条数: {result['total_count']}")
        if result['total_count'] > 0:
            latest = result['data'][0]
            print(f"   最新数据: {latest['date']} 收盘价 {latest['close']}")


def test_get_financial_indicators():
    """测试获取财务指标"""
    print("\n测试: astock_get_financial_indicators")
    print("=" * 50)

    result = astock_get_financial_indicators.invoke({"symbol": "600519", "period": "latest"})

    if "error" in result:
        print(f"❌ 失败: {result['error']}")
    else:
        print(f"✅ 成功")
        if result['total_count'] > 0:
            data = result['data'][0]
            print(f"   报告期: {data.get('date', 'N/A')}")
            print(f"   市盈率: {data.get('pe', 'N/A')}")
            print(f"   市净率: {data.get('pb', 'N/A')}")
            print(f"   ROE: {data.get('roe', 'N/A')}")
            print(f"   净利率: {data.get('net_margin', 'N/A')}")


if __name__ == "__main__":
    print("\n" + "=" * 60)
    print("A股投资助手 - 工具测试")
    print("=" * 60)

    try:
        test_get_quote()
        test_get_kline()
        test_get_financial_indicators()

        print("\n" + "=" * 60)
        print("✅ 所有测试完成！")
        print("=" * 60)

    except Exception as e:
        print(f"\n❌ 测试失败: {str(e)}")
        import traceback
        traceback.print_exc()
