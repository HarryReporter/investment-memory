#!/usr/bin/env python3
"""
高级仓位管理工具
- 凯利公式（含半凯利/四分之一凯利）
- 波动率目标仓位
- 反马丁格尔（亏损后减仓）
- 最大回撤控制
- 分散化约束
"""

import argparse
import json
import math


# ============================================================
# 1. 凯利公式系列
# ============================================================


def calculate_kelly(win_rate, risk_reward):
    """完整凯利公式: f* = (p*b - q) / b"""
    if risk_reward <= 0 or win_rate <= 0 or win_rate >= 1:
        return 0
    loss_rate = 1 - win_rate
    kelly = (win_rate * risk_reward - loss_rate) / risk_reward
    return max(0, kelly)


def calculate_kelly_fractional(win_rate, risk_reward, fraction=0.5):
    """分数凯利（Half-Kelly, Quarter-Kelly等）"""
    full_kelly = calculate_kelly(win_rate, risk_reward)
    return full_kelly * fraction


def calculate_kelly_multi_asset(returns, win_rates, risk_rewards):
    """
    多资产组合凯利（简化版）
    当无相关性数据时的近似解
    returns: 预期收益率列表
    """
    n = len(returns)
    if n == 0:
        return []

    # 单资产凯利
    individual_kellys = [
        calculate_kelly(wr, rr) for wr, rr in zip(win_rates, risk_rewards)
    ]

    # 简单归一化使总和不超过100%
    total = sum(individual_kellys)
    if total > 1.0:
        individual_kellys = [k / total for k in individual_kellys]

    return individual_kellys


# ============================================================
# 2. 波动率目标仓位
# ============================================================


def calculate_vol_target_position(
    annual_volatility,
    target_volatility=15.0,
    max_position=0.30,
):
    """
    基于波动率的仓位调整
    仓位 = 目标波动率 / 资产波动率
    核心逻辑：波动率越高 → 仓位越低
    """
    if annual_volatility <= 0:
        return max_position
    position = target_volatility / annual_volatility
    return min(position, max_position)


# ============================================================
# 3. 固定分数法（Fixed Fractional）
# ============================================================


def calculate_fixed_fractional(
    total_capital,
    risk_per_trade=2.0,
    entry_price=None,
    stop_loss_price=None,
):
    """
    固定分数法：每笔交易只承担总资金的固定比例风险
    仓位 = (资金 × 风险比例) / 每股风险
    """
    if entry_price and stop_loss_price and entry_price > stop_loss_price:
        risk_per_share = entry_price - stop_loss_price
        position_value = total_capital * (risk_per_trade / 100)
        shares = position_value / risk_per_share
        position_pct = (shares * entry_price) / total_capital
        return {
            "shares": int(shares),
            "position_pct": position_pct,
            "risk_amount": position_value,
        }
    return None


# ============================================================
# 4. 反马丁格尔策略（亏损后减仓）
# ============================================================


def calculate_anti_martingale(
    base_position,
    consecutive_losses=0,
    reduction_factor=0.7,
    min_position=0.02,
):
    """
    反马丁格尔：连续亏损后减小仓位
    连续亏损n次后的仓位 = base_position × reduction_factor^n
    """
    adjusted = base_position * (reduction_factor**consecutive_losses)
    return max(adjusted, min_position)


def calculate_pyramid_position(
    base_position,
    current_profit_pct,
    levels=None,
):
    """
    金字塔加仓：盈利后逐步加仓但递减
    levels: [(盈利阈值%, 加仓比例), ...]
    """
    if levels is None:
        levels = [(5, 0.5), (10, 0.3), (20, 0.2)]

    total_position = base_position
    for threshold, add_pct in levels:
        if current_profit_pct >= threshold:
            total_position += base_position * add_pct
        else:
            break
    return total_position


# ============================================================
# 5. 最大回撤控制
# ============================================================


def calculate_drawdown_adjusted_position(
    base_position,
    current_drawdown_pct,
    max_acceptable_drawdown=20.0,
):
    """
    基于当前回撤调整仓位
    回撤越大 → 仓位越小（保护资本）
    """
    if current_drawdown_pct <= 0:
        return base_position

    # 线性衰减：回撤达到最大可接受回撤时仓位减半
    reduction = min(current_drawdown_pct / max_acceptable_drawdown, 1.0)
    adjusted = base_position * (1 - reduction * 0.5)
    return max(adjusted, 0.01)


# ============================================================
# 6. 综合仓位计算
# ============================================================


def calculate_position_sizing(
    risk_level,
    total_capital=None,
    win_rate=None,
    risk_reward=None,
    annual_volatility=None,
    consecutive_losses=0,
    current_drawdown_pct=0.0,
    entry_price=None,
    stop_loss_price=None,
    kelly_fraction=0.5,
    target_volatility=15.0,
    output_json=False,
):
    """综合仓位计算"""
    result = {
        "risk_level": risk_level,
        "total_capital": total_capital,
        "win_rate": win_rate,
        "risk_reward": risk_reward,
        "annual_volatility": annual_volatility,
    }

    # --- 风险等级上限 ---
    risk_limits = {
        "very_high": 0.05,
        "high": 0.10,
        "medium": 0.20,
        "low": 0.30,
    }
    risk_names = {
        "very_high": "极高风险",
        "high": "高风险",
        "medium": "中等风险",
        "low": "低风险",
    }
    max_position = risk_limits.get(risk_level, 0.15)
    result["risk_level_name"] = risk_names.get(risk_level, "未知")
    result["max_position_by_risk"] = max_position

    # --- 凯利公式 ---
    kelly_full = None
    kelly_adjusted = None
    if win_rate and risk_reward:
        kelly_full = calculate_kelly(win_rate, risk_reward)
        kelly_adjusted = calculate_kelly_fractional(
            win_rate, risk_reward, kelly_fraction
        )
        result["kelly_full"] = round(kelly_full, 4)
        result["kelly_fraction"] = kelly_fraction
        result["kelly_adjusted"] = round(kelly_adjusted, 4)

    # --- 波动率目标仓位 ---
    vol_target_pos = None
    if annual_volatility and annual_volatility > 0:
        vol_target_pos = calculate_vol_target_position(
            annual_volatility, target_volatility, max_position
        )
        result["vol_target_position"] = round(vol_target_pos, 4)
        result["target_volatility"] = target_volatility

    # --- 确定基础仓位（取最保守的）---
    candidates = [max_position]
    if kelly_adjusted is not None:
        candidates.append(kelly_adjusted)
    if vol_target_pos is not None:
        candidates.append(vol_target_pos)
    base_position = min(candidates)

    # --- 反马丁格尔调整 ---
    if consecutive_losses > 0:
        base_position = calculate_anti_martingale(base_position, consecutive_losses)
        result["consecutive_losses"] = consecutive_losses
        result["anti_martingale_applied"] = True

    # --- 回撤控制调整 ---
    if current_drawdown_pct > 0:
        base_position = calculate_drawdown_adjusted_position(
            base_position, current_drawdown_pct
        )
        result["current_drawdown_pct"] = current_drawdown_pct
        result["drawdown_adjusted"] = True

    # --- 最终仓位 ---
    final_position = base_position
    result["suggested_position"] = round(final_position, 4)

    # --- 具体金额 ---
    if total_capital:
        result["suggested_amount"] = round(total_capital * final_position, 2)

    # --- 固定分数法（如果有止损价）---
    if entry_price and stop_loss_price and total_capital:
        ff_result = calculate_fixed_fractional(
            total_capital, 2.0, entry_price, stop_loss_price
        )
        if ff_result:
            result["fixed_fractional"] = ff_result

    # --- 分散化约束 ---
    diversification = {
        "single_stock_max": 0.20,
        "single_industry_max": 0.30,
        "correlated_group_max": 0.40,
        "cash_reserve_min": 0.10,
        "notes": "同行业/同概念相关性高，视为相关组",
    }
    result["diversification"] = diversification

    if output_json:
        print(json.dumps(result, ensure_ascii=False, indent=2))
    else:
        print(f"仓位计算")
        print("=" * 60)
        print(f"\n风险等级: {result['risk_level_name']}")

        print(f"\n仓位来源:")
        print(f"  风险等级上限: {max_position:.0%}")
        if kelly_full is not None:
            print(f"  完整凯利: {kelly_full:.1%}")
            print(f"  {kelly_fraction:.0%}凯利: {kelly_adjusted:.1%}")
        if vol_target_pos is not None:
            print(
                f"  波动率目标: {vol_target_pos:.1%} (目标波动率{target_volatility}%)"
            )

        if consecutive_losses > 0:
            print(f"\n反马丁格尔: 连续亏损{consecutive_losses}次，仓位已缩减")

        if current_drawdown_pct > 0:
            print(f"\n回撤控制: 当前回撤{current_drawdown_pct:.1f}%，仓位已缩减")

        print(f"\n建议仓位: {final_position:.1%}")
        if total_capital:
            print(f"建议金额: {total_capital * final_position:,.0f}元")

        if result.get("fixed_fractional"):
            ff = result["fixed_fractional"]
            print(f"\n固定分数法参考:")
            print(f"  建议股数: {ff['shares']}")
            print(f"  仓位占比: {ff['position_pct']:.1%}")

        print(f"\n分散化约束:")
        for k, v in diversification.items():
            if k != "notes":
                print(f"  {k}: {v:.0%}")

        print("=" * 60)

    return result


def main():
    parser = argparse.ArgumentParser(description="综合仓位计算")
    parser.add_argument(
        "--risk-level",
        choices=["very_high", "high", "medium", "low"],
        required=True,
        help="风险等级",
    )
    parser.add_argument("--total-capital", type=float, help="总资金")
    parser.add_argument("--win-rate", type=float, help="预期胜率（0-1）")
    parser.add_argument("--risk-reward", type=float, help="风险回报比")
    parser.add_argument("--annual-volatility", type=float, help="年化波动率（%%）")
    parser.add_argument(
        "--consecutive-losses", type=int, default=0, help="连续亏损次数"
    )
    parser.add_argument(
        "--current-drawdown", type=float, default=0.0, help="当前回撤（%%）"
    )
    parser.add_argument("--entry-price", type=float, help="买入价格")
    parser.add_argument("--stop-loss-price", type=float, help="止损价格")
    parser.add_argument(
        "--kelly-fraction", type=float, default=0.5, help="凯利分数（默认0.5即半凯利）"
    )
    parser.add_argument(
        "--target-volatility", type=float, default=15.0, help="目标年化波动率（%%）"
    )
    parser.add_argument(
        "--json", action="store_true", dest="output_json", help="输出JSON格式"
    )
    args = parser.parse_args()

    result = calculate_position_sizing(
        risk_level=args.risk_level,
        total_capital=args.total_capital,
        win_rate=args.win_rate,
        risk_reward=args.risk_reward,
        annual_volatility=args.annual_volatility,
        consecutive_losses=args.consecutive_losses,
        current_drawdown_pct=args.current_drawdown,
        entry_price=args.entry_price,
        stop_loss_price=args.stop_loss_price,
        kelly_fraction=args.kelly_fraction,
        target_volatility=args.target_volatility,
        output_json=args.output_json,
    )

    return 0


if __name__ == "__main__":
    exit(main())
