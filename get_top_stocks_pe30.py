#!/usr/bin/env python3
"""A股主板优质股票量化分析（PE<30） - 能源、AI、半导体、电子消费"""

import akshare as ak
import pandas as pd
import numpy as np
from datetime import datetime

# 优质股票池（精选各板块龙头股 - 仅主板）
QUALITY_STOCKS = {
    '能源': [
        '600900',  # 长江电力 - 水电龙头
        '601899',  # 紫金矿业 - 有色金属龙头
        '601615',  # 明阳智能 - 风电龙头
        '600938',  # 中国海油 - 油气龙头
        '600886',  # 国投电力 - 水电
    ],
    'AI': [
        '002405',  # 四维图新 - 自动驾驶
        '002230',  # 科大讯飞 - AI语音
        '002415',  # 海康威视 - AI安防
        '002352',  # 顺丰控股 - 智能物流
        '600570',  # 恒生电子 - 金融科技
    ],
    '半导体': [
        '600584',  # 长电科技 - 封装测试
        '002371',  # 北方华创 - 半导体设备
        '600460',  # 士兰微 - 功率半导体
        '002049',  # 紫光国微 - 安全芯片
        '002156',  # 通富微电 - 封装
    ],
    '电子消费': [
        '000651',  # 格力电器 - 白电龙头
        '600690',  # 海尔智家 - 智能家电
        '000333',  # 美的集团 - 白电龙头
        '603501',  # 韦尔股份 - CIS芯片
        '000100',  # TCL科技 - 面板
    ]
}

def is_mainboard_stock(code):
    """检查是否为主板股票"""
    code = str(code).strip()

    # 沪市主板
    if code.startswith(('600', '601', '603', '605')):
        return True

    # 深市主板
    if code.startswith(('000', '001', '002', '003')):
        return True

    # 排除科创板 (688xxx)
    if code.startswith('688'):
        return False

    # 排除创业板 (300xxx)
    if code.startswith('300'):
        return False

    return False

def get_stock_financial_indicators(stock_code):
    """获取股票财务指标"""
    try:
        indicators = ak.stock_financial_analysis_indicator(symbol=stock_code)
        if not indicators.empty:
            latest = indicators.iloc[0]
            return {
                'roe': float(latest.get('净资产收益率', 0) if pd.notna(latest.get('净资产收益率', 0)) else 0),
                'roa': float(latest.get('总资产净利润率(ROA)', 0) if pd.notna(latest.get('总资产净利润率(ROA)', 0)) else 0),
                'gross_margin': float(latest.get('销售毛利率', 0) if pd.notna(latest.get('销售毛利率', 0)) else 0),
                'net_margin': float(latest.get('销售净利率', 0) if pd.notna(latest.get('销售净利率', 0)) else 0),
                'debt_ratio': float(latest.get('资产负债率', 0) if pd.notna(latest.get('资产负债率', 0)) else 0),
                'current_ratio': float(latest.get('流动比率', 0) if pd.notna(latest.get('流动比率', 0)) else 0),
                'revenue_growth': float(latest.get('营业收入增长率', 0) if pd.notna(latest.get('营业收入增长率', 0)) else 0),
                'profit_growth': float(latest.get('净利润增长率', 0) if pd.notna(latest.get('净利润增长率', 0)) else 0),
                'eps': float(latest.get('基本每股收益', 0) if pd.notna(latest.get('基本每股收益', 0)) else 0),
                'bps': float(latest.get('每股净资产', 0) if pd.notna(latest.get('每股净资产', 0)) else 0)
            }
        return None
    except Exception as e:
        print(f"  获取 {stock_code} 财务指标失败: {e}")
        return None

def get_stock_info(stock_code):
    """获取股票基本信息和实时行情"""
    try:
        # 获取股票基本信息
        quote = ak.stock_zh_a_spot_em()
        stock_data = quote[quote['代码'] == stock_code]

        if stock_data.empty:
            print(f"  未找到股票 {stock_code}")
            return None

        row = stock_data.iloc[0]
        return {
            'name': row['名称'],
            'code': stock_code,
            'price': float(row.get('最新价', 0) if pd.notna(row.get('最新价', 0)) else 0),
            'pe': float(row.get('市盈率-动态', 0) if pd.notna(row.get('市盈率-动态', 0)) else 0),
            'pb': float(row.get('市净率', 0) if pd.notna(row.get('市净率', 0)) else 0),
            'market_cap': float(row.get('总市值', 0) if pd.notna(row.get('总市值', 0)) else 0),
            'volume': float(row.get('成交量', 0) if pd.notna(row.get('成交量', 0)) else 0),
            'amplitude': float(row.get('振幅', 0) if pd.notna(row.get('振幅', 0)) else 0),
            'turnover': float(row.get('换手率', 0) if pd.notna(row.get('换手率', 0)) else 0),
            'high_52w': float(row.get('52周最高', 0) if pd.notna(row.get('52周最高', 0)) else 0),
            'low_52w': float(row.get('52周最低', 0) if pd.notna(row.get('52周最低', 0)) else 0)
        }
    except Exception as e:
        print(f"  获取 {stock_code} 行情失败: {e}")
        return None

def calculate_quant_score(financial_data, quote_data):
    """计算量化综合评分"""
    score = 0
    reasons = []

    # ROE评分 (20分) - 核心盈利能力指标
    if financial_data['roe'] > 20:
        score += 20
        reasons.append(f"✓ ROE优秀({financial_data['roe']:.2f}%)，盈利能力强")
    elif financial_data['roe'] > 15:
        score += 15
        reasons.append(f"✓ ROE良好({financial_data['roe']:.2f}%)")
    elif financial_data['roe'] > 10:
        score += 10
        reasons.append(f"✓ ROE一般({financial_data['roe']:.2f}%)")

    # 毛利率评分 (15分) - 竞争优势体现
    if financial_data['gross_margin'] > 50:
        score += 15
        reasons.append(f"✓ 毛利率高({financial_data['gross_margin']:.2f}%)，竞争优势明显")
    elif financial_data['gross_margin'] > 30:
        score += 10
        reasons.append(f"✓ 毛利率良好({financial_data['gross_margin']:.2f}%)")

    # 营收增长率评分 (15分) - 成长性指标
    if financial_data['revenue_growth'] > 30:
        score += 15
        reasons.append(f"✓ 营收高速增长({financial_data['revenue_growth']:.2f}%)，成长性好")
    elif financial_data['revenue_growth'] > 20:
        score += 10
        reasons.append(f"✓ 营收稳健增长({financial_data['revenue_growth']:.2f}%)")
    elif financial_data['revenue_growth'] > 10:
        score += 5
        reasons.append(f"✓ 营收稳定({financial_data['revenue_growth']:.2f}%)")

    # 净利润增长率评分 (15分) - 利润成长性
    if financial_data['profit_growth'] > 30:
        score += 15
        reasons.append(f"✓ 利润高速增长({financial_data['profit_growth']:.2f}%)")
    elif financial_data['profit_growth'] > 20:
        score += 10
        reasons.append(f"✓ 利润稳健增长({financial_data['profit_growth']:.2f}%)")
    elif financial_data['profit_growth'] > 10:
        score += 5
        reasons.append(f"✓ 利润稳定增长({financial_data['profit_growth']:.2f}%)")

    # 估值评分 (15分) - PE合理性（PE<30优先）
    if 0 < quote_data['pe'] < 15:
        score += 15
        reasons.append(f"✓ 估值极低(PE={quote_data['pe']:.2f})，安全边际高")
    elif 15 <= quote_data['pe'] < 20:
        score += 13
        reasons.append(f"✓ 估值偏低(PE={quote_data['pe']:.2f})")
    elif 20 <= quote_data['pe'] < 25:
        score += 10
        reasons.append(f"✓ 估值合理(PE={quote_data['pe']:.2f})")
    elif 25 <= quote_data['pe'] < 30:
        score += 7
        reasons.append(f"✓ 估值适中(PE={quote_data['pe']:.2f})")
    elif quote_data['pe'] >= 30:
        score += 0  # PE>=30不加分
        reasons.append(f"⚠ 估值偏高(PE={quote_data['pe']:.2f})，超过30")

    # 负债率评分 (10分) - 财务稳健性
    if financial_data['debt_ratio'] < 40:
        score += 10
        reasons.append(f"✓ 负债率低({financial_data['debt_ratio']:.2f}%)，财务稳健")
    elif financial_data['debt_ratio'] < 60:
        score += 6
        reasons.append(f"✓ 负债率适中({financial_data['debt_ratio']:.2f}%)")

    # 流动性评分 (10分) - 关注度指标
    if 2 < quote_data['turnover'] < 10:
        score += 10
        reasons.append(f"✓ 换手率健康({quote_data['turnover']:.2f}%)，流动性良好")
    elif 1 < quote_data['turnover'] <= 2:
        score += 6
        reasons.append(f"✓ 换手率适中({quote_data['turnover']:.2f}%)")

    return score, reasons

def analyze_stocks():
    """分析股票池"""
    print("开始A股主板量化分析（PE<30筛选）...")
    print(f"分析日期: {datetime.now().strftime('%Y-%m-%d')}")
    print("="*80)
    print("【重要】仅分析A股主板股票（沪市600/601/603/605、深市000/001/002/003）")
    print("        不包括科创板(688)和创业板(300)")
    print("【筛选条件】市盈率 PE < 30")
    print("="*80)

    all_results = []

    for sector, codes in QUALITY_STOCKS.items():
        print(f"\n【{sector}板块】分析中...")

        for code in codes:
            # 检查是否为主板股票
            if not is_mainboard_stock(code):
                print(f"  跳过 {code} (非主板股票)")
                continue

            print(f"  正在分析 {code}...", end=' ')

            # 获取基本信息
            info = get_stock_info(code)
            if info is None:
                print("失败")
                continue

            print(f"找到: {info['name']}", end=' ')

            # 检查PE是否满足条件
            if info['pe'] >= 30:
                print(f"(PE={info['pe']:.1f}，不符合PE<30条件，跳过)")
                continue

            print(f"(PE={info['pe']:.1f})", end=' ')

            # 获取财务指标
            financial = get_stock_financial_indicators(code)
            if financial is None:
                print("(无财务数据)")
                continue

            # 计算评分
            score, reasons = calculate_quant_score(financial, info)

            all_results.append({
                'code': code,
                'name': info['name'],
                'sector': sector,
                'score': score,
                'reasons': reasons,
                'price': info['price'],
                'pe': info['pe'],
                'pb': info['pb'],
                'market_cap': info['market_cap'],
                'turnover': info['turnover'],
                'roe': financial['roe'],
                'gross_margin': financial['gross_margin'],
                'revenue_growth': financial['revenue_growth'],
                'profit_growth': financial['profit_growth'],
                'debt_ratio': financial['debt_ratio'],
                'net_margin': financial['net_margin']
            })

            print(f"(评分: {score})")

    return all_results

def generate_report(results):
    """生成分析报告"""
    # 转换为DataFrame
    df = pd.DataFrame(results)

    if df.empty:
        print("\n未能获取到符合PE<30条件的有效数据")
        return

    # 按评分排序
    df = df.sort_values('score', ascending=False).reset_index(drop=True)
    top15 = df.head(15)

    print("\n" + "="*100)
    print(" "*25 + "A股主板量化指标TOP15股票推荐（PE<30）")
    print("="*100)
    print(f"分析时间: {datetime.now().strftime('%Y年%m月%d日 %H:%M:%S')}")
    print(f"数据来源: 东方财富、AkShare")
    print("="*100)

    print("\n【风险提示】")
    print("  ★ 本推荐基于历史量化指标分析，仅供参考，不构成任何投资建议")
    print("  ★ 股市有风险，投资需谨慎，请您独立判断并承担投资风险")
    print("  ★ 建议结合自身风险承受能力、投资目标综合决策")
    print("  ★ 请持续关注公司基本面变化和市场风险因素")
    print("  ★ 本报告仅涵盖A股主板，不包括科创板和创业板")
    print("  ★ PE<30筛选标准可能排除部分高成长优质公司")
    print("="*100)

    for idx, (_, row) in enumerate(top15.iterrows()):
        print(f"\n{'='*100}")
        print(f"【排名 #{idx+1}】{row['name']} ({row['code']})")
        print(f"所属板块: {row['sector']}")
        print(f"{'='*100}")
        print(f"量化评分: {row['score']}/100")

        # 基本面数据
        print(f"\n【估值与交易】")
        print(f"  当前价格: ¥{row['price']:.2f}")
        print(f"  市盈率PE: {row['pe']:.2f}  |  市净率PB: {row['pb']:.2f}")
        print(f"  总市值: {row['market_cap']/100000000:.2f}亿元  |  换手率: {row['turnover']:.2f}%")

        # 盈利能力
        print(f"\n【盈利能力】")
        print(f"  ROE: {row['roe']:.2f}%  |  净利率: {row['net_margin']:.2f}%")
        print(f"  毛利率: {row['gross_margin']:.2f}%")

        # 成长性
        print(f"\n【成长性】")
        print(f"  营收增长率: {row['revenue_growth']:.2f}%")
        print(f"  净利润增长率: {row['profit_growth']:.2f}%")

        # 财务健康
        print(f"\n【财务健康】")
        print(f"  资产负债率: {row['debt_ratio']:.2f}%")

        # 推荐理由
        print(f"\n【推荐理由】")
        for i, reason in enumerate(row['reasons'], 1):
            print(f"  {reason}")

        # 风险提示
        risks = []
        if row['pe'] > 25:
            risks.append(f"估值接近上限(PE={row['pe']:.2f})，需谨慎")
        if row['turnover'] > 15:
            risks.append(f"换手率过高({row['turnover']:.2f}%)，可能存在短期炒作")
        if row['debt_ratio'] > 70:
            risks.append(f"负债率偏高({row['debt_ratio']:.2f}%)，关注财务压力")
        if row['revenue_growth'] < 0:
            risks.append(f"营收下滑({row['revenue_growth']:.2f}%)，需关注经营状况")
        if row['profit_growth'] < 0:
            risks.append(f"利润下滑({row['profit_growth']:.2f}%)，盈利能力减弱")

        if risks:
            print(f"\n【风险提示】")
            for risk in risks:
                print(f"  ⚠ {risk}")

    # 板块分布统计
    print(f"\n{'='*100}")
    print(f"【板块分布统计】")
    sector_count = top15['sector'].value_counts()
    for sector, count in sector_count.items():
        print(f"  {sector}: {count}只")

    # PE分布统计
    print(f"\n【市盈率(PE)分布统计】")
    pe_ranges = [
        (0, 15, "PE < 15"),
        (15, 20, "15 ≤ PE < 20"),
        (20, 25, "20 ≤ PE < 25"),
        (25, 30, "25 ≤ PE < 30")
    ]
    for low, high, label in pe_ranges:
        count = len(top15[(top15['pe'] >= low) & (top15['pe'] < high)])
        if count > 0:
            print(f"  {label}: {count}只")

    # 低估值精选
    print(f"\n【低估值精选（PE < 15）】")
    low_pe = top15[top15['pe'] < 15].sort_values('pe')
    if not low_pe.empty:
        for _, row in low_pe.iterrows():
            print(f"  {row['name']} ({row['code']}) - PE: {row['pe']:.1f}")
    else:
        print("  无PE < 15的股票")

    print(f"\n{'='*100}")
    print(f"【A股主板说明】")
    print(f"  沪市主板: 600xxx, 601xxx, 603xxx, 605xxx")
    print(f"  深市主板: 000xxx, 001xxx, 002xxx, 003xxx")
    print(f"  不包括: 创业板(300xxx)、科创板(688xxx)")
    print(f"{'='*100}")
    print(f"报告结束 | 共推荐 {len(top15)} 只股票")
    print("="*100)

    # 保存详细数据
    output_file = f"/workspace/dexter/top_stocks_pe30_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
    top15.to_csv(output_file, index=False, encoding='utf-8-sig')
    print(f"\n详细数据已保存至: {output_file}")

def main():
    # 分析股票
    results = analyze_stocks()

    if results:
        # 生成报告
        generate_report(results)
    else:
        print("\n未能获取到任何股票数据，请检查网络连接")

if __name__ == "__main__":
    main()
