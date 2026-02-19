#!/usr/bin/env python3
"""测试主板股票代码验证功能"""

def is_mainboard_stock(code: str) -> bool:
    """检查是否为主板股票"""
    code = str(code).strip()

    # 沪市主板
    if code.startswith(('600', '601', '603', '605')):
        return True

    # 深市主板
    if code.startswith(('000', '001', '002', '003')):
        return True

    return False

# 测试用例
test_cases = [
    # 沪市主板（应为True）
    ('600519', '贵州茅台', True),
    ('601899', '紫金矿业', True),
    ('603501', '韦尔股份', True),
    ('605088', '宏华数科', True),

    # 深市主板（应为True）
    ('000001', '平安银行', True),
    ('000651', '格力电器', True),
    ('002371', '北方华创', True),
    ('002405', '四维图新', True),
    ('002230', '科大讯飞', True),

    # 创业板（应为False）
    ('300750', '宁德时代', False),
    ('300033', '同花顺', False),
    ('300474', '景嘉微', False),

    # 科创板（应为False）
    ('688981', '中芯国际', False),
    ('688111', '金山办公', False),
    ('688008', '澜起科技', False),

    # 其他（应为False）
    ('301001', '北交所', False),
]

print("="*80)
print("主板股票代码验证测试")
print("="*80)

passed = 0
failed = 0

for code, name, expected in test_cases:
    result = is_mainboard_stock(code)
    status = "✓ 通过" if result == expected else "✗ 失败"

    if result == expected:
        passed += 1
    else:
        failed += 1

    print(f"{status} | {code} | {name:20s} | 期望: {expected:5} | 实际: {result:5}")

print("="*80)
print(f"测试结果: 通过 {passed}/{len(test_cases)}，失败 {failed}/{len(test_cases)}")
print("="*80)

# 测试工具函数返回格式
print("\n工具函数返回格式示例:")
print("-" * 80)

def mock_get_quote(symbol: str):
    """模拟 astock_get_quote 函数"""
    if not is_mainboard_stock(symbol):
        return {
            "error": f"股票代码 {symbol} 不属于主板，本项目仅支持主板股票",
            "symbol": symbol,
            "note": "支持主板：沪市(600/601/603/605)、深市(000/001/002/003)，不支持科创板(688)和创业板(300)"
        }
    return {
        "symbol": symbol,
        "status": "success",
        "data": {"price": 100.0}
    }

print("\n测试1: 主板股票 (600519)")
result1 = mock_get_quote("600519")
print(f"  结果: {result1}")

print("\n测试2: 科创板股票 (688981)")
result2 = mock_get_quote("688981")
print(f"  结果: {result2}")

print("\n测试3: 创业板股票 (300750)")
result3 = mock_get_quote("300750")
print(f"  结果: {result3}")

print("="*80)
print("测试完成！")
print("="*80)
