#!/usr/bin/env python3
"""
多维度风险评估工具
- 市场风险：估值水平 + 行业动量
- 公司风险：市值 + 盈利稳定性 + 竞争力
- 流动性风险：换手率 + 自由流通比例
- 政策风险：行业政策敏感度
- 波动率风险：历史波动率 + Beta
- 综合风险评分与建议
"""

import argparse
import json
import math


# ============================================================
# 1. 市场风险（估值 + 动量）
# ============================================================


def assess_market_risk(
    valuation_score=None,
    price_vs_ma200=None,
    industry_relative_strength=None,
):
    """
    市场风险评估
    valuation_score: 来自check_valuation的评分（0-100，越高越好）
    price_vs_ma200: 当前价/200日均线，>1表示在均线上方
    industry_relative_strength: 行业相对强度（0-100）
    """
    score = 50.0

    # 估值调整（来自估值检查的评分，需反转：高估值分=低风险）
    if valuation_score is not None:
        # 估值分75以上 → 低风险（-15），估值分25以下 → 高风险（+15）
        val_adj = (50 - valuation_score) * 0.3
        score += val_adj

    # 趋势调整
    if price_vs_ma200 is not None:
        if price_vs_ma200 > 1.10:  # 远高于均线，可能过热
            score += 10
        elif price_vs_ma200 > 1.0:  # 在均线上方
            score -= 5
        elif price_vs_ma200 > 0.90:  # 略低于均线
            score += 5
        else:  # 显著低于均线，趋势弱
            score += 15

    # 行业相对强度
    if industry_relative_strength is not None:
        if industry_relative_strength > 70:
            score -= 8  # 强势行业风险较低
        elif industry_relative_strength < 30:
            score += 10  # 弱势行业风险较高

    return min(max(score, 0), 100)


# ============================================================
# 2. 公司风险（基本面）
# ============================================================


def assess_company_risk(
    market_cap,
    is_profitable=True,
    profit_growth_stability=None,
    has_competitive_advantage=True,
    debt_to_equity=None,
):
    """
    公司风险评估
    profit_growth_stability: 近5年盈利增长的标准差/均值（变异系数），越小越稳定
    debt_to_equity: 负债/股东权益
    """
    score = 50.0

    # 市值风险
    if market_cap:
        if market_cap > 5000:
            score -= 15
        elif market_cap > 1000:
            score -= 8
        elif market_cap > 100:
            score += 5
        elif market_cap > 30:
            score += 12
        else:
            score += 20

    # 盈利能力
    if not is_profitable:
        score += 20

    # 盈利稳定性
    if profit_growth_stability is not None:
        if profit_growth_stability < 0.2:
            score -= 10  # 盈利非常稳定
        elif profit_growth_stability < 0.5:
            score -= 3
        elif profit_growth_stability > 1.0:
            score += 10  # 盈利波动大

    # 竞争优势（护城河）
    if not has_competitive_advantage:
        score += 15

    # 负债风险
    if debt_to_equity is not None:
        if debt_to_equity > 2.0:
            score += 15
        elif debt_to_equity > 1.0:
            score += 8
        elif debt_to_equity < 0.3:
            score -= 5

    return min(max(score, 0), 100)


# ============================================================
# 3. 流动性风险
# ============================================================


def assess_liquidity_risk(
    daily_volume=None,
    market_cap=None,
    bid_ask_spread_pct=None,
):
    """
    流动性风险评估
    bid_ask_spread_pct: 买卖价差占价格百分比
    """
    score = 50.0

    # 换手率
    if daily_volume and market_cap and market_cap > 0:
        turnover_rate = daily_volume / market_cap * 100
        if turnover_rate > 2.0:
            score -= 15  # 高流动性
        elif turnover_rate > 1.0:
            score -= 10
        elif turnover_rate > 0.5:
            score -= 5
        elif turnover_rate > 0.1:
            score += 5
        else:
            score += 18  # 极低流动性

    # 买卖价差
    if bid_ask_spread_pct is not None:
        if bid_ask_spread_pct < 0.1:
            score -= 5
        elif bid_ask_spread_pct > 0.5:
            score += 10
        elif bid_ask_spread_pct > 1.0:
            score += 18

    return min(max(score, 0), 100)


# ============================================================
# 4. 政策/监管风险
# ============================================================

# 基础政策敏感度（正值=政策风险高，负值=政策支持）
_POLICY_BASE_RISK = {
    "互联网": 12,  # 反垄断监管
    "教育": 25,  # 双减政策
    "游戏": 15,  # 版号限制
    "地产": 22,  # 三道红线
    "医药": 8,  # 集采压力
    "金融": 6,  # 强监管行业
    "新能源": -12,  # 政策大力支持
    "半导体": -10,  # 国产替代
    "AI": -8,  # 政策支持
    "科技": 3,
    "消费": 0,
    "能源": 10,
}


def assess_policy_risk(industry, recent_policy_events=None):
    """
    政策风险评估
    recent_policy_events: 近期政策事件列表 [(事件描述, 影响程度-10~10), ...]
    """
    score = 50.0

    # 基础行业政策风险
    base = _POLICY_BASE_RISK.get(industry, 5)
    score += base

    # 近期事件调整
    if recent_policy_events:
        for _, impact in recent_policy_events:
            score += impact

    return min(max(score, 0), 100)


# ============================================================
# 5. 波动率风险
# ============================================================


def assess_volatility_risk(
    annual_volatility=None,
    beta=None,
    max_drawdown_1y=None,
):
    """
    波动率风险评估
    annual_volatility: 年化波动率（%）
    beta: 相对大盘的Beta
    max_drawdown_1y: 近1年最大回撤（%）
    """
    score = 50.0

    # 波动率
    if annual_volatility is not None:
        # A股平均约25%，美股约15%
        if annual_volatility > 50:
            score += 20
        elif annual_volatility > 35:
            score += 12
        elif annual_volatility > 25:
            score += 5
        elif annual_volatility > 15:
            score -= 5
        else:
            score -= 10

    # Beta
    if beta is not None:
        if beta > 1.5:
            score += 12
        elif beta > 1.2:
            score += 5
        elif beta < 0.8:
            score -= 8
        elif beta < 0.5:
            score -= 12

    # 最大回撤
    if max_drawdown_1y is not None:
        if max_drawdown_1y > 50:
            score += 15
        elif max_drawdown_1y > 30:
            score += 8
        elif max_drawdown_1y < 15:
            score -= 8

    return min(max(score, 0), 100)


# ============================================================
# 综合评估
# ============================================================


def get_risk_level(score):
    """获取风险等级"""
    if score <= 30:
        return "低风险", "green"
    elif score <= 42:
        return "中低风险", "yellow-green"
    elif score <= 55:
        return "中等风险", "yellow"
    elif score <= 70:
        return "中高风险", "orange"
    else:
        return "高风险", "red"


def get_recommendation(total_score, risk_level):
    """获取投资建议"""
    if total_score <= 32:
        return "可以积极配置"
    elif total_score <= 42:
        return "可以适当配置"
    elif total_score <= 55:
        return "谨慎配置，控制仓位"
    elif total_score <= 68:
        return "建议观望或小仓位试探"
    else:
        return "建议回避"


def risk_assessment(
    code,
    industry,
    market_cap=None,
    daily_volume=None,
    valuation_score=None,
    is_profitable=True,
    has_competitive_advantage=True,
    annual_volatility=None,
    beta=None,
    max_drawdown_1y=None,
    price_vs_ma200=None,
    debt_to_equity=None,
    profit_growth_stability=None,
    bid_ask_spread_pct=None,
    recent_policy_events=None,
    weights=None,
    output_json=False,
):
    """综合风险评估"""
    result = {
        "code": code,
        "industry": industry,
    }

    # 各维度评估
    market_risk = assess_market_risk(
        valuation_score=valuation_score,
        price_vs_ma200=price_vs_ma200,
    )

    company_risk = assess_company_risk(
        market_cap=market_cap,
        is_profitable=is_profitable,
        profit_growth_stability=profit_growth_stability,
        has_competitive_advantage=has_competitive_advantage,
        debt_to_equity=debt_to_equity,
    )

    liquidity_risk = assess_liquidity_risk(
        daily_volume=daily_volume,
        market_cap=market_cap,
        bid_ask_spread_pct=bid_ask_spread_pct,
    )

    policy_risk = assess_policy_risk(industry, recent_policy_events)

    volatility_risk = assess_volatility_risk(
        annual_volatility=annual_volatility,
        beta=beta,
        max_drawdown_1y=max_drawdown_1y,
    )

    risk_scores = {
        "market_risk": market_risk,
        "company_risk": company_risk,
        "liquidity_risk": liquidity_risk,
        "policy_risk": policy_risk,
        "volatility_risk": volatility_risk,
    }
    result["risk_scores"] = {k: round(v, 1) for k, v in risk_scores.items()}

    # 加权总分（默认权重，可覆盖）
    default_weights = {
        "market_risk": 0.25,
        "company_risk": 0.25,
        "liquidity_risk": 0.15,
        "policy_risk": 0.15,
        "volatility_risk": 0.20,
    }
    w = weights if weights else default_weights
    result["weights"] = w

    total_score = sum(risk_scores[k] * w[k] for k in w)
    result["total_score"] = round(total_score, 1)

    risk_level, color = get_risk_level(total_score)
    result["risk_level"] = risk_level
    result["risk_color"] = color

    recommendation = get_recommendation(total_score, risk_level)
    result["recommendation"] = recommendation

    if output_json:
        print(json.dumps(result, ensure_ascii=False, indent=2))
    else:
        print(f"风险评估: {code}")
        print("=" * 60)
        print(f"行业: {industry}")

        print(f"\n各维度风险评分（0-100，越高风险越大）:")
        labels = {
            "market_risk": "市场风险",
            "company_risk": "公司风险",
            "liquidity_risk": "流动性风险",
            "policy_risk": "政策风险",
            "volatility_risk": "波动率风险",
        }
        for key, label in labels.items():
            bar_len = int(risk_scores[key] / 5)
            bar = "█" * bar_len + "░" * (20 - bar_len)
            print(f"  {label:8s}: {risk_scores[key]:5.0f}  [{bar}]  权重{w[key]:.0%}")

        print(f"\n综合评估:")
        print(f"  总分: {total_score:.0f}/100")
        print(f"  风险等级: {risk_level}")
        print(f"  建议: {recommendation}")
        print("=" * 60)

    return result


def main():
    parser = argparse.ArgumentParser(description="多维度风险评估")
    parser.add_argument("--code", required=True, help="股票代码")
    parser.add_argument("--industry", required=True, help="所属行业")
    parser.add_argument("--market-cap", type=float, help="市值（亿元）")
    parser.add_argument("--daily-volume", type=float, help="日均成交额（亿元）")
    parser.add_argument(
        "--valuation-score", type=float, help="估值评分（0-100，来自check_valuation）"
    )
    parser.add_argument("--not-profitable", action="store_true", help="未盈利")
    parser.add_argument(
        "--no-competitive-advantage", action="store_true", help="无竞争优势"
    )
    parser.add_argument("--annual-volatility", type=float, help="年化波动率（%%）")
    parser.add_argument("--beta", type=float, help="Beta系数")
    parser.add_argument("--max-drawdown", type=float, help="近1年最大回撤（%%）")
    parser.add_argument("--price-vs-ma200", type=float, help="当前价/200日均线")
    parser.add_argument("--debt-to-equity", type=float, help="负债/股东权益")
    parser.add_argument("--profit-stability", type=float, help="盈利增长变异系数")
    parser.add_argument("--bid-ask-spread", type=float, help="买卖价差（%%）")
    parser.add_argument(
        "--json", action="store_true", dest="output_json", help="输出JSON格式"
    )
    args = parser.parse_args()

    result = risk_assessment(
        code=args.code,
        industry=args.industry,
        market_cap=args.market_cap,
        daily_volume=args.daily_volume,
        valuation_score=args.valuation_score,
        is_profitable=not args.not_profitable,
        has_competitive_advantage=not args.no_competitive_advantage,
        annual_volatility=args.annual_volatility,
        beta=args.beta,
        max_drawdown_1y=args.max_drawdown,
        price_vs_ma200=args.price_vs_ma200,
        debt_to_equity=args.debt_to_equity,
        profit_growth_stability=args.profit_stability,
        bid_ask_spread_pct=args.bid_ask_spread,
        output_json=args.output_json,
    )

    return 0


if __name__ == "__main__":
    exit(main())
