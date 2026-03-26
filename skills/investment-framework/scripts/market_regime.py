#!/usr/bin/env python3
"""
市场状态检测工具
- 趋势判断（均线系统）
- 波动率环境（低波/正常/高波/恐慌）
- 恐慌指数（VIX-like）
- 仓位调整建议
"""

import argparse
import json
import math


# ============================================================
# 1. 趋势判断
# ============================================================


def assess_trend(
    price,
    ma20=None,
    ma60=None,
    ma200=None,
):
    """
    多均线趋势判断
    返回趋势方向和强度
    """
    signals = []

    if ma20 and price:
        if price > ma20:
            signals.append(1)
        else:
            signals.append(-1)

    if ma60 and price:
        if price > ma60:
            signals.append(1)
        else:
            signals.append(-1)

    if ma200 and price:
        if price > ma200:
            signals.append(1)
        else:
            signals.append(-1)

    if ma20 and ma60:
        if ma20 > ma60:
            signals.append(1)
        else:
            signals.append(-1)

    if ma60 and ma200:
        if ma60 > ma200:
            signals.append(1)
        else:
            signals.append(-1)

    if not signals:
        return "未知", 0

    total = sum(signals)
    n = len(signals)
    strength = total / n  # -1 到 1

    if strength >= 0.6:
        return "强势上涨", strength
    elif strength >= 0.2:
        return "温和上涨", strength
    elif strength > -0.2:
        return "震荡", strength
    elif strength > -0.6:
        return "温和下跌", strength
    else:
        return "强势下跌", strength


# ============================================================
# 2. 波动率环境
# ============================================================


def assess_volatility_regime(
    current_volatility,
    historical_avg_volatility=None,
    vix=None,
):
    """
    波动率环境判断
    current_volatility: 当前年化波动率（%）
    historical_avg_volatility: 历史平均波动率（%）
    vix: 恐慌指数
    """
    result = {}

    # 基于绝对水平
    if current_volatility:
        if current_volatility < 12:
            result["absolute_regime"] = "极低波动"
        elif current_volatility < 18:
            result["absolute_regime"] = "低波动"
        elif current_volatility < 28:
            result["absolute_regime"] = "正常波动"
        elif current_volatility < 40:
            result["absolute_regime"] = "高波动"
        else:
            result["absolute_regime"] = "恐慌波动"
        result["current_volatility"] = current_volatility

    # 基于相对水平（vs历史）
    if (
        current_volatility
        and historical_avg_volatility
        and historical_avg_volatility > 0
    ):
        ratio = current_volatility / historical_avg_volatility
        result["vol_ratio"] = round(ratio, 2)
        if ratio > 2.0:
            result["relative_regime"] = "极端偏高"
        elif ratio > 1.5:
            result["relative_regime"] = "显著偏高"
        elif ratio > 1.2:
            result["relative_regime"] = "偏高"
        elif ratio > 0.8:
            result["relative_regime"] = "正常"
        else:
            result["relative_regime"] = "偏低"

    # VIX恐慌判断
    if vix is not None:
        if vix > 40:
            result["fear_level"] = "极度恐慌"
        elif vix > 30:
            result["fear_level"] = "恐慌"
        elif vix > 20:
            result["fear_level"] = "谨慎"
        elif vix > 12:
            result["fear_level"] = "正常"
        else:
            result["fear_level"] = "贪婪"
        result["vix"] = vix

    return result


# ============================================================
# 3. 综合市场状态
# ============================================================


def determine_market_regime(
    trend_direction,
    trend_strength,
    vol_regime,
):
    """
    综合市场状态判断
    """
    # 基于趋势和波动率的组合
    if "上涨" in trend_direction and vol_regime in ["低波动", "极低波动"]:
        return "牛市（低波上涨）", "green"
    elif "上涨" in trend_direction and vol_regime in ["正常波动"]:
        return "牛市", "yellow-green"
    elif "上涨" in trend_direction and vol_regime in ["高波动", "恐慌波动"]:
        return "牛市末期（注意风险）", "orange"
    elif trend_direction == "震荡" and vol_regime in ["低波动", "极低波动"]:
        return "低波震荡（等待方向）", "yellow"
    elif trend_direction == "震荡" and vol_regime in ["正常波动"]:
        return "震荡", "yellow"
    elif trend_direction == "震荡" and vol_regime in ["高波动", "恐慌波动"]:
        return "高波震荡（谨慎）", "orange"
    elif "下跌" in trend_direction and vol_regime in ["低波动", "极低波动"]:
        return "阴跌", "orange"
    elif "下跌" in trend_direction and vol_regime in ["正常波动"]:
        return "熊市", "red"
    elif "下跌" in trend_direction and vol_regime in ["高波动", "恐慌波动"]:
        return "恐慌性下跌", "red"
    else:
        return "状态不明", "gray"


# ============================================================
# 4. 仓位调整建议
# ============================================================


def position_adjustment(
    trend_direction,
    vol_regime,
    base_position=0.20,
):
    """
    根据市场状态给出仓位调整建议
    """
    adjustments = {
        "multiplier": 1.0,
        "suggestion": "",
        "details": [],
    }

    # 趋势调整
    if "强势上涨" in trend_direction:
        adjustments["multiplier"] *= 1.2
        adjustments["details"].append("趋势强势，可适当增加仓位")
    elif "温和上涨" in trend_direction:
        adjustments["multiplier"] *= 1.0
        adjustments["details"].append("趋势温和上涨，维持仓位")
    elif trend_direction == "震荡":
        adjustments["multiplier"] *= 0.7
        adjustments["details"].append("震荡市，减少仓位至70%")
    elif "温和下跌" in trend_direction:
        adjustments["multiplier"] *= 0.5
        adjustments["details"].append("下跌趋势，仓位减半")
    elif "强势下跌" in trend_direction:
        adjustments["multiplier"] *= 0.3
        adjustments["details"].append("强势下跌，仓位降至30%或空仓")

    # 波动率调整
    if "恐慌" in vol_regime:
        adjustments["multiplier"] *= 0.5
        adjustments["details"].append("恐慌波动，再减半")
    elif "高波动" in vol_regime:
        adjustments["multiplier"] *= 0.7
        adjustments["details"].append("高波动，减仓30%")
    elif "极低波动" in vol_regime:
        adjustments["multiplier"] *= 1.1
        adjustments["details"].append("低波动环境，可略微加仓")

    # 确保不超限
    adjustments["multiplier"] = min(adjustments["multiplier"], 1.5)
    adjustments["multiplier"] = max(adjustments["multiplier"], 0.1)

    adjusted = base_position * adjustments["multiplier"]
    adjustments["base_position"] = base_position
    adjustments["adjusted_position"] = round(adjusted, 4)

    if adjusted > base_position:
        adjustments["suggestion"] = f"建议加仓至{adjusted:.0%}"
    elif adjusted < base_position * 0.8:
        adjustments["suggestion"] = f"建议减仓至{adjusted:.0%}"
    else:
        adjustments["suggestion"] = f"维持仓位{adjusted:.0%}附近"

    return adjustments


# ============================================================
# 综合入口
# ============================================================


def detect_market_regime(
    price=None,
    ma20=None,
    ma60=None,
    ma200=None,
    current_volatility=None,
    historical_avg_volatility=None,
    vix=None,
    base_position=0.20,
    output_json=False,
):
    """市场状态检测"""
    result = {}

    # 趋势
    trend_dir, trend_str = assess_trend(price, ma20, ma60, ma200)
    result["trend"] = {
        "direction": trend_dir,
        "strength": round(trend_str, 2),
    }

    # 波动率
    vol_info = assess_volatility_regime(
        current_volatility, historical_avg_volatility, vix
    )
    result["volatility"] = vol_info

    # 综合状态
    vol_regime = vol_info.get("absolute_regime", "正常波动")
    regime, color = determine_market_regime(trend_dir, trend_str, vol_regime)
    result["regime"] = regime
    result["regime_color"] = color

    # 仓位调整
    adj = position_adjustment(trend_dir, vol_regime, base_position)
    result["position_adjustment"] = adj

    if output_json:
        print(json.dumps(result, ensure_ascii=False, indent=2))
    else:
        print(f"市场状态检测")
        print("=" * 60)

        print(f"\n趋势判断:")
        print(f"  方向: {trend_dir}")
        print(f"  强度: {trend_str:.2f}")
        if price and ma200:
            premium = (price / ma200 - 1) * 100
            print(f"  相对200日均线: {'+' if premium > 0 else ''}{premium:.1f}%")

        print(f"\n波动率环境:")
        for k, v in vol_info.items():
            label = {
                "current_volatility": "当前波动率",
                "absolute_regime": "绝对水平",
                "relative_regime": "相对水平",
                "vol_ratio": "波动率比率",
                "fear_level": "恐慌程度",
                "vix": "VIX",
            }.get(k, k)
            print(f"  {label}: {v}")

        print(f"\n综合市场状态: {regime}")

        print(f"\n仓位调整:")
        print(f"  基准仓位: {adj['base_position']:.0%}")
        print(f"  调整倍数: {adj['multiplier']:.2f}x")
        print(f"  调整后仓位: {adj['adjusted_position']:.0%}")
        for d in adj["details"]:
            print(f"  → {d}")
        print(f"  建议: {adj['suggestion']}")

        print("=" * 60)

    return result


def main():
    parser = argparse.ArgumentParser(description="市场状态检测")
    parser.add_argument("--price", type=float, help="当前价格/指数点位")
    parser.add_argument("--ma20", type=float, help="20日均线")
    parser.add_argument("--ma60", type=float, help="60日均线")
    parser.add_argument("--ma200", type=float, help="200日均线")
    parser.add_argument(
        "--volatility",
        type=float,
        dest="current_volatility",
        help="当前年化波动率（%%）",
    )
    parser.add_argument(
        "--hist-volatility",
        type=float,
        dest="historical_avg_volatility",
        help="历史平均波动率（%%）",
    )
    parser.add_argument("--vix", type=float, help="恐慌指数VIX")
    parser.add_argument(
        "--base-position", type=float, default=0.20, help="基准仓位（默认20%%）"
    )
    parser.add_argument(
        "--json", action="store_true", dest="output_json", help="输出JSON格式"
    )
    args = parser.parse_args()

    result = detect_market_regime(
        price=args.price,
        ma20=args.ma20,
        ma60=args.ma60,
        ma200=args.ma200,
        current_volatility=args.current_volatility,
        historical_avg_volatility=args.historical_avg_volatility,
        vix=args.vix,
        base_position=args.base_position,
        output_json=args.output_json,
    )

    return 0


if __name__ == "__main__":
    exit(main())
