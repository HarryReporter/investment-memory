#!/usr/bin/env python3
"""
多维度估值检查工具
- 历史PE/PB分位数（支持CSV数据源）
- CAPE（周期调整市盈率）
- PEG（含行业调整）
- 综合评分与安全边际
"""

import argparse
import csv
import json
import math
import os
import sys
from pathlib import Path

# 行业PEG调整系数（基于学术研究经验值）
# 低增长行业PEG基准应更高，高增长行业可接受更高PEG
INDUSTRY_PEG_ADJUST = {
    "互联网": 1.0,
    "科技": 1.0,
    "消费": 1.2,
    "医药": 1.1,
    "金融": 1.4,
    "地产": 1.5,
    "能源": 1.3,
    "新能源": 0.9,
    "半导体": 0.9,
    "AI": 0.85,
    "教育": 1.3,
    "游戏": 1.0,
}

# CAPE历史均值参考（美国市场长期均值约17，中国市场约15-20）
CAPE_HISTORICAL_MEAN = 17.0
CAPE_HISTORICAL_STD = 7.0


def load_historical_data(filepath):
    """从CSV加载历史估值数据，格式: date,pe,pb,cape"""
    if not filepath or not os.path.exists(filepath):
        return None
    data = {"pe": [], "pb": [], "cape": []}
    try:
        with open(filepath, "r") as f:
            reader = csv.DictReader(f)
            for row in reader:
                for key in ["pe", "pb", "cape"]:
                    val = row.get(key, "").strip()
                    if val:
                        try:
                            data[key].append(float(val))
                        except ValueError:
                            pass
        return data if any(data[k] for k in data) else None
    except Exception:
        return None


def calculate_percentile(value, historical_values):
    """计算值在历史数据中的真实百分位数"""
    if not historical_values:
        return None
    below = sum(1 for v in historical_values if v <= value)
    return below / len(historical_values)


def get_percentile_assessment(percentile):
    """根据百分位数给出评估"""
    if percentile is None:
        return "未知", None
    if percentile <= 0.2:
        return "低估", "green"
    elif percentile <= 0.4:
        return "合理偏低", "yellow-green"
    elif percentile <= 0.6:
        return "合理", "yellow"
    elif percentile <= 0.8:
        return "合理偏高", "orange"
    else:
        return "高估", "red"


def calculate_pe_relative(pe, industry_pe=None):
    """PE相对行业估值（当无历史数据时的备选方案）"""
    if industry_pe and industry_pe > 0:
        ratio = pe / industry_pe
        if ratio < 0.7:
            return "低估", 0.2
        elif ratio < 0.9:
            return "合理偏低", 0.35
        elif ratio < 1.1:
            return "合理", 0.5
        elif ratio < 1.3:
            return "合理偏高", 0.65
        elif ratio < 1.6:
            return "偏高", 0.8
        else:
            return "高估", 1.0
    return "未知", 0.5


def calculate_cape_ratio(pe, avg_earnings_growth=None, inflation_rate=None):
    """
    计算近似CAPE：
    简化版：CAPE ≈ PE / (1 + 近10年平均盈利增长率)
    完整版需要10年通胀调整后的平均盈利数据
    """
    if pe is None or pe <= 0:
        return None
    if avg_earnings_growth is not None:
        # 简化CAPE：用盈利增长调整当前PE
        cape = pe / (1 + avg_earnings_growth / 100)
        return max(cape, 0)
    return None


def get_cape_assessment(cape):
    """CAPE评估（基于历史统计）"""
    if cape is None:
        return "未知", None
    # 基于Shiller研究的分位
    z_score = (cape - CAPE_HISTORICAL_MEAN) / CAPE_HISTORICAL_STD
    if z_score < -1.0:
        return "显著低估", "green"
    elif z_score < -0.5:
        return "低估", "yellow-green"
    elif z_score < 0.5:
        return "合理", "yellow"
    elif z_score < 1.0:
        return "偏高", "orange"
    else:
        return "高估", "red"


def calculate_peg(pe, growth_rate, industry=None):
    """
    计算PEG，含行业调整
    PEG = PE / (盈利增长率 × 行业调整系数)
    """
    if growth_rate is None or growth_rate <= 0:
        return None
    raw_peg = pe / growth_rate
    adjust = INDUSTRY_PEG_ADJUST.get(industry, 1.0) if industry else 1.0
    adjusted_peg = raw_peg * adjust
    return adjusted_peg


def get_peg_assessment(peg):
    """PEG评估（基于Lynch基准 + Trombley修正）"""
    if peg is None:
        return "无法评估"
    if peg < 0.5:
        return "明显低估"
    elif peg < 0.8:
        return "低估"
    elif peg < 1.2:
        return "合理估值"
    elif peg < 1.5:
        return "合理偏高"
    elif peg < 2.0:
        return "偏高"
    elif peg < 3.0:
        return "高估"
    else:
        return "明显高估"


def calculate_margin_of_safety(current_pe, fair_value_pe):
    """计算安全边际"""
    if fair_value_pe and fair_value_pe > 0:
        return (fair_value_pe - current_pe) / fair_value_pe
    return None


def estimate_fair_value_pe(growth_rate, industry=None, risk_free_rate=3.0):
    """
    基于PEG=1和Gordon模型估算合理PE
    合理PE ≈ min(PEG1对应的PE, Gordon增长模型PE)
    """
    if growth_rate is None or growth_rate <= 0:
        return None

    # 方法1: PEG=1对应的PE
    adjust = INDUSTRY_PEG_ADJUST.get(industry, 1.0) if industry else 1.0
    peg1_pe = growth_rate * adjust

    # 方法2: Gordon增长模型 PE = 1/(r-g)，简化取 r = risk_free + 5% 股权风险溢价
    required_return = risk_free_rate + 5.0
    if growth_rate < required_return:
        gordon_pe = 100 / (required_return - growth_rate)
    else:
        gordon_pe = peg1_pe  # 高增长公司用PEG法

    # 取两者较低值（保守）
    return min(peg1_pe, gordon_pe)


def composite_score(
    pe_percentile=None,
    pe_relative_score=None,
    cape_assessment=None,
    peg_assessment=None,
    margin_of_safety=None,
    growth_rate=None,
):
    """
    综合评分（0-100，越高越有投资价值）
    基于LSEG研究的权重：PE分位数对长期回报解释力最强（R²~0.4-0.78）
    """
    score = 50.0
    factors_used = 0

    # PE历史分位数（权重最高，有最强实证支持）
    if pe_percentile is not None:
        # 分位数越低越好：20%分位 → +25分，80%分位 → -25分
        pe_score = (0.5 - pe_percentile) * 50
        score += pe_score
        factors_used += 1
    elif pe_relative_score is not None:
        pe_score = (0.5 - pe_relative_score) * 40
        score += pe_score
        factors_used += 1

    # CAPE评估
    cape_scores = {
        "显著低估": 20,
        "低估": 12,
        "合理": 0,
        "偏高": -12,
        "高估": -20,
    }
    if cape_assessment and cape_assessment in cape_scores:
        score += cape_scores[cape_assessment]
        factors_used += 1

    # PEG评估
    peg_scores = {
        "明显低估": 20,
        "低估": 12,
        "合理估值": 0,
        "合理偏高": -8,
        "偏高": -15,
        "高估": -20,
        "明显高估": -25,
    }
    if peg_assessment and peg_assessment in peg_scores:
        score += peg_scores[peg_assessment]
        factors_used += 1

    # 安全边际加分
    if margin_of_safety is not None:
        if margin_of_safety > 0.3:
            score += 15
        elif margin_of_safety > 0.15:
            score += 8
        elif margin_of_safety > 0:
            score += 3
        elif margin_of_safety > -0.15:
            score -= 5
        else:
            score -= 12
        factors_used += 1

    # 增长率调整（增长是估值的核心驱动）
    if growth_rate is not None:
        if growth_rate > 30:
            score += 8
        elif growth_rate > 20:
            score += 5
        elif growth_rate > 10:
            score += 2
        elif growth_rate < 5:
            score -= 8
        elif growth_rate < 0:
            score -= 15

    # 归一化到0-100
    score = max(0, min(100, score))

    return score


def get_recommendation(score):
    """根据综合评分给出建议"""
    if score >= 75:
        return "强烈建议买入", "green"
    elif score >= 60:
        return "建议买入", "yellow-green"
    elif score >= 50:
        return "可以持有", "yellow"
    elif score >= 40:
        return "建议观望", "orange"
    elif score >= 25:
        return "建议减仓", "red"
    else:
        return "建议回避", "red"


def check_valuation(
    code,
    pe,
    industry_pe=None,
    growth_rate=None,
    pb=None,
    industry=None,
    historical_data_path=None,
    avg_earnings_growth=None,
    risk_free_rate=3.0,
    output_json=False,
):
    """多维度估值检查"""
    result = {
        "code": code,
        "pe": pe,
        "industry_pe": industry_pe,
        "growth_rate": growth_rate,
        "pb": pb,
        "industry": industry,
    }

    # 加载历史数据
    hist_data = load_historical_data(historical_data_path)

    # === PE分析 ===
    pe_percentile = None
    pe_relative_score = None

    if hist_data and hist_data["pe"]:
        pe_percentile = calculate_percentile(pe, hist_data["pe"])
        pe_assessment, pe_color = get_percentile_assessment(pe_percentile)
        result["pe_percentile"] = round(pe_percentile, 4)
        result["pe_assessment_method"] = "historical_percentile"
    else:
        pe_assessment, pe_relative_score = calculate_pe_relative(pe, industry_pe)
        pe_color = None
        result["pe_assessment_method"] = "industry_relative"

    result["pe_assessment"] = pe_assessment

    # === CAPE分析 ===
    cape = calculate_cape_ratio(pe, avg_earnings_growth)
    result["cape"] = cape
    if cape is not None:
        cape_assessment, cape_color = get_cape_assessment(cape)
        result["cape_assessment"] = cape_assessment

        # 也检查历史CAPE分位
        if hist_data and hist_data["cape"]:
            cape_percentile = calculate_percentile(cape, hist_data["cape"])
            result["cape_percentile"] = (
                round(cape_percentile, 4) if cape_percentile else None
            )
    else:
        cape_assessment = None

    # === PB分析 ===
    if pb is not None:
        if hist_data and hist_data["pb"]:
            pb_percentile = calculate_percentile(pb, hist_data["pb"])
            result["pb_percentile"] = round(pb_percentile, 4) if pb_percentile else None
            pb_assessment, _ = get_percentile_assessment(pb_percentile)
        else:
            # 简单阈值（银行<1, 科技<5等仅为粗略参考）
            pb_assessment = "需行业对比"
        result["pb"] = pb
        result["pb_assessment"] = pb_assessment

    # === PEG分析 ===
    peg = calculate_peg(pe, growth_rate, industry)
    result["peg"] = round(peg, 2) if peg else None
    peg_assessment = get_peg_assessment(peg)
    result["peg_assessment"] = peg_assessment

    # === 合理估值估算与安全边际 ===
    fair_pe = estimate_fair_value_pe(growth_rate, industry, risk_free_rate)
    result["estimated_fair_pe"] = round(fair_pe, 1) if fair_pe else None

    margin_of_safety = calculate_margin_of_safety(pe, fair_pe)
    result["margin_of_safety"] = (
        round(margin_of_safety, 3) if margin_of_safety is not None else None
    )

    # === 综合评分 ===
    score = composite_score(
        pe_percentile=pe_percentile,
        pe_relative_score=pe_relative_score,
        cape_assessment=cape_assessment,
        peg_assessment=peg_assessment,
        margin_of_safety=margin_of_safety,
        growth_rate=growth_rate,
    )
    result["score"] = round(score, 1)

    recommendation, rec_color = get_recommendation(score)
    result["recommendation"] = recommendation

    if output_json:
        print(json.dumps(result, ensure_ascii=False, indent=2))
    else:
        print(f"估值检查: {code}")
        print("=" * 60)

        print(f"\nPE分析:")
        print(f"  当前PE: {pe}")
        if industry_pe:
            print(f"  行业PE: {industry_pe}")
        print(f"  评估: {pe_assessment}")
        print(
            f"  方法: {'历史分位数' if pe_percentile is not None else '行业相对估值'}"
        )
        if pe_percentile is not None:
            print(f"  历史分位: {pe_percentile:.1%}")

        if cape is not None:
            print(f"\nCAPE分析:")
            print(f"  近似CAPE: {cape:.1f}")
            print(f"  评估: {cape_assessment}")
            if result.get("cape_percentile") is not None:
                print(f"  历史分位: {result['cape_percentile']:.1%}")

        print(f"\nPEG分析:")
        if peg is not None:
            print(f"  PEG: {peg:.2f} (行业调整后)")
            print(f"  评估: {peg_assessment}")
            print(f"  增长率: {growth_rate}%")
        else:
            print(f"  无法计算（需要增长率）")

        if fair_pe:
            print(f"\n安全边际:")
            print(f"  估算合理PE: {fair_pe:.1f}")
            if margin_of_safety is not None:
                mos_pct = margin_of_safety * 100
                sign = "+" if mos_pct > 0 else ""
                print(f"  安全边际: {sign}{mos_pct:.1f}%")

        print(f"\n综合评分: {score:.0f}/100")
        print(f"建议: {recommendation}")
        print("=" * 60)

    return result


def main():
    parser = argparse.ArgumentParser(description="多维度估值检查")
    parser.add_argument("--code", required=True, help="股票代码")
    parser.add_argument("--pe", type=float, required=True, help="当前市盈率")
    parser.add_argument("--industry-pe", type=float, help="行业平均市盈率")
    parser.add_argument("--growth-rate", type=float, help="预期盈利增长率（%%）")
    parser.add_argument("--pb", type=float, help="市净率")
    parser.add_argument("--industry", help="所属行业")
    parser.add_argument("--historical-data", help="历史估值CSV文件路径")
    parser.add_argument(
        "--avg-earnings-growth",
        type=float,
        help="近10年平均盈利增长率（%%），用于计算CAPE",
    )
    parser.add_argument(
        "--risk-free-rate", type=float, default=3.0, help="无风险利率（%%），默认3%%"
    )
    parser.add_argument(
        "--json", action="store_true", dest="output_json", help="输出JSON格式"
    )
    args = parser.parse_args()

    result = check_valuation(
        code=args.code,
        pe=args.pe,
        industry_pe=args.industry_pe,
        growth_rate=args.growth_rate,
        pb=args.pb,
        industry=args.industry,
        historical_data_path=args.historical_data,
        avg_earnings_growth=args.avg_earnings_growth,
        risk_free_rate=args.risk_free_rate,
        output_json=args.output_json,
    )

    return 0


if __name__ == "__main__":
    exit(main())
