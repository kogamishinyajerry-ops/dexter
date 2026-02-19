"""
风险提示模块

生成投资风险警告和教育内容
"""

RISK_WARNINGS = {
    "市场风险": {
        "系统性风险": [
            "宏观经济下行可能导致市场整体下跌",
            "货币政策变化可能影响流动性",
            "地缘政治事件可能引发市场波动",
            "黑天鹅事件无法预测和规避"
        ],
        "周期性风险": [
            "行业有周期性，需要判断所处阶段",
            "经济周期会影响企业盈利",
            "牛市和熊市轮换是常态"
        ]
    },
    
    "个股风险": {
        "基本面风险": [
            "公司业绩可能不及预期",
            "财务数据可能存在造假风险",
            "管理层变动可能影响经营",
            "核心技术人员离职可能削弱竞争力"
        ],
        "估值风险": [
            "PE/PB 过高可能存在泡沫",
            "概念炒作推高估值",
            "市场情绪可能导致价格偏离价值"
        ],
        "流动性风险": [
            "小盘股可能成交低迷",
            "停牌可能导致无法交易",
            "大股东减持可能造成冲击"
        ]
    },
    
    "投资误区": {
        "常见错误": [
            "追涨杀跌：大涨追买，大跌恐慌卖出",
            "频繁交易：增加交易成本，容易踏空",
            "满仓操作：无现金应对机会和风险",
            "听信消息：小道消息往往不可靠",
            "忽视基本面：只看图形不看公司",
            "过度自信：认为自己能战胜市场"
        ],
        "正确做法": [
            "逆向思维：人弃我取，人取我予",
            "长期持有：减少交易，享受复利",
            "控制仓位：保留现金，灵活应对",
            "独立判断：基于公开信息决策",
            "研究公司：基本面是投资基础",
            "保持谦逊：承认市场不确定性"
        ]
    },
    
    "风险控制": {
        "仓位管理": [
            "单只股票不超过总资金 20%",
            "同一行业不超过总资金 30%",
            "根据市场情况调整总体仓位",
            "保留 10-20% 现金应对机会"
        ],
        "止损原则": [
            "技术止损：跌破关键支撑位",
            "财务止损：基本面恶化",
            "时间止损：长期不涨且理由不充分",
            "绝对止损：亏损超过 10-15%"
        ],
        "分散投资": [
            "跨行业：至少 3-5 个行业",
            "跨规模：大盘、中盘、小盘搭配",
            "跨主题：成长、价值、红利组合"
        ]
    }
}

def get_risk_warning_html() -> str:
    """生成风险提示 HTML"""
    html = """
    <div style="background: #fff3cd; border: 2px solid #ffc107; border-radius: 8px; padding: 20px; margin: 20px 0;">
        <h2 style="color: #856404; margin-top: 0;">⚠️ 重要风险提示</h2>
        
        <h3 style="color: #856404;">市场风险</h3>
        <ul style="color: #856404;">
            <li>股票市场存在系统性风险，可能出现整体下跌</li>
            <li>宏观经济、政策变化可能影响市场表现</li>
            <li>地缘政治等黑天鹅事件无法预测</li>
        </ul>
        
        <h3 style="color: #856404;">个股风险</h3>
        <ul style="color: #856404;">
            <li>公司业绩可能不及预期或下滑</li>
            <li>估值过高可能存在泡沫风险</li>
            <li>小盘股可能存在流动性不足</li>
            <li>大股东减持可能造成股价冲击</li>
        </ul>
        
        <h3 style="color: #856404;">投资误区</h3>
        <ul style="color: #856404;">
            <li>追涨杀跌：容易高位接盘、低位割肉</li>
            <li>频繁交易：增加成本、容易踏空</li>
            <li>满仓操作：无法应对市场变化</li>
            <li>听信消息：小道消息往往不可靠</li>
        </ul>
        
        <h3 style="color: #856404;">风险控制建议</h3>
        <ul style="color: #856404;">
            <li>分散投资，控制单股仓位不超过 20%</li>
            <li>设置止损纪律，及时止损</li>
            <li>长期持有，减少频繁交易</li>
            <li>深入研究公司基本面</li>
        </ul>
        
        <div style="background: #f8d7da; border: 1px solid #f5c6cb; border-radius: 4px; padding: 15px; margin-top: 20px;">
            <strong style="color: #721c24;">免责声明：</strong><br>
            <span style="color: #721c24;">
            本工具提供的所有分析和建议仅供参考，不构成任何投资建议。
            投资者应根据自身情况独立判断并承担投资风险。<br><br>
            <strong>市场有风险，投资需谨慎！</strong>
            </span>
        </div>
    </div>
    """
    return html

def format_risk_warning_for_llm() -> str:
    """格式化风险警告供 LLM 使用"""
    text = "【重要风险警告】\n\n"
    
    for category, subcategories in RISK_WARNINGS.items():
        text += f"\n## {category}\n"
        
        if isinstance(subcategories, dict):
            for subcategory, items in subcategories.items():
                text += f"\n### {subcategory}\n"
                for item in items:
                    text += f"- {item}\n"
        elif isinstance(subcategories, list):
            for item in subcategories:
                text += f"- {item}\n"
    
    text += "\n\n【免责声明】\n"
    text += "以上风险提示仅供参考，投资者应根据自身情况独立判断并承担投资风险。\n"
    text += "市场有风险，投资需谨慎！\n"
    
    return text

def check_risk_level(analysis_result: dict) -> str:
    """
    根据分析结果评估风险级别
    
    Args:
        analysis_result: 分析结果字典
    
    Returns:
        风险级别: "低"、"中"、"高"
    """
    risk_score = 0
    
    # 估值风险
    if "估值" in analysis_result:
        pe = analysis_result["估值"].get("pe", 0)
        pb = analysis_result["估值"].get("pb", 0)
        
        if pe > 50 or pb > 10:
            risk_score += 2
        elif pe > 30 or pb > 5:
            risk_score += 1
    
    # 成长风险
    if "成长性" in analysis_result:
        revenue_growth = analysis_result["成长性"].get("revenue_growth", 0)
        
        if revenue_growth < 0:
            risk_score += 2
        elif revenue_growth < 10:
            risk_score += 1
    
    # 财务风险
    if "财务" in analysis_result:
        debt_ratio = analysis_result["财务"].get("debt_ratio", 0)
        
        if debt_ratio > 0.7:
            risk_score += 2
        elif debt_ratio > 0.5:
            risk_score += 1
    
    # 技术风险
    if "技术面" in analysis_result:
        trend = analysis_result["技术面"].get("trend", "")
        
        if trend == "下降":
            risk_score += 2
        elif trend == "横盘":
            risk_score += 1
    
    # 判断风险级别
    if risk_score >= 6:
        return "高"
    elif risk_score >= 3:
        return "中"
    else:
        return "低"

def generate_risk_report(analysis_result: dict) -> str:
    """
    生成风险报告
    
    Args:
        analysis_result: 分析结果字典
    
    Returns:
        风险报告文本
    """
    risk_level = check_risk_level(analysis_result)
    
    report = f"""
    【风险分析报告】
    
    风险级别: {risk_level}风险
    
    """
    
    if risk_level == "高":
        report += """
        风险提示:
        - 当前投资风险较高，建议谨慎
        - 不建议重仓持有
        - 建议设置止损位
        - 密切关注基本面变化
        """
    elif risk_level == "中":
        report += """
        风险提示:
        - 当前投资风险适中
        - 建议控制仓位
        - 关注风险因素变化
        - 可考虑分批布局
        """
    else:
        report += """
        风险提示:
        - 当前投资风险较低
        - 仍需关注市场变化
        - 建议长期持有
        - 定期跟踪基本面
        """
    
    report += f"""
    
    【免责声明】
    以上风险分析仅供参考，投资者应根据自身情况独立判断并承担投资风险。
    市场有风险，投资需谨慎！
    """
    
    return report
