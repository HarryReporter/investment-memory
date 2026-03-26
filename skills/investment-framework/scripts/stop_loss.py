#!/usr/bin/env python3
"""
止损止盈计算工具
- ATR止损法（基于波动率）
- 百分比止损法
- 支撑位止损法
- 分批止盈策略
- 移动止损（Trailing Stop）
"""

import argparse
import json


# ============================================================
# 1. ATR止损法
# ============================================================


def calculate_atr_stop(entry_price, atr, multiplier=2.0, direction="long"):
    """
    基于ATR（平均真实波幅）的止损
    止损价 = 入场价 ± ATR × 倍数
    """
    if direction == "long":
        stop_loss = entry_price - atr * multiplier
    else:
        stop_loss = entry_price + atr * multiplier
    return round(stop_loss, 2)


def calculate_atr_targets(entry_price, atr, direction="long"):
    """
    基于ATR的分级止盈
    T1: 1.5倍ATR, T2: 3倍ATR, T3: 5倍ATR
    """
    if direction == "long":
        return {
            "T1保守": round(entry_price + atr * 1.5, 2),
            "T2标准": round(entry_price + atr * 3.0, 2),
            "T3激进": round(entry_price + atr * 5.0, 2),
        }
    else:
        return {
            "T1保守": round(entry_price - atr * 1.5, 2),
            "T2标准": round(entry_price - atr * 3.0, 2),
            "T3激进": round(entry_price - atr * 5.0, 2),
        }


# ============================================================
# 2. 百分比止损法
# ============================================================


def calculate_percentage_stop(entry_price, stop_pct, direction="long"):
    """固定百分比止损"""
    if direction == "long":
        return round(entry_price * (1 - stop_pct / 100), 2)
    else:
        return round(entry_price * (1 + stop_pct / 100), 2)


# ============================================================
# 3. 移动止损（Trailing Stop）
# ============================================================


def calculate_trailing_stop(
    highest_price,
    current_price,
    trail_pct=8.0,
    trail_atr=None,
    atr_multiplier=2.5,
):
    """
    移动止损
    两种模式：百分比移动 / ATR移动
    """
    stops = {}

    # 百分比移动止损
    pct_stop = highest_price * (1 - trail_pct / 100)
    stops["pct_trailing"] = round(pct_stop, 2)

    # ATR移动止损
    if trail_atr:
        atr_stop = highest_price - trail_atr * atr_multiplier
        stops["atr_trailing"] = round(atr_stop, 2)

    return stops


# ============================================================
# 4. 分批止盈策略
# ============================================================


def calculate_batch_take_profit(
    entry_price,
    position_size,
    risk_reward_target=3.0,
    atr=None,
    stop_loss_price=None,
    direction="long",
):
    """
    分批止盈策略
    根据风险回报比和ATR确定止盈价位和分批比例
    """
    # 确定止损距离
    if stop_loss_price:
        stop_distance = abs(entry_price - stop_loss_price)
    elif atr:
        stop_distance = atr * 2.0
    else:
        stop_distance = entry_price * 0.08  # 默认8%

    # 计算各批次止盈价
    batches = []

    # 第一批（50%仓位）：1.5倍风险回报比
    t1_distance = stop_distance * 1.5
    if direction == "long":
        t1_price = entry_price + t1_distance
    else:
        t1_price = entry_price - t1_distance
    batches.append(
        {
            "batch": 1,
            "pct_of_position": 50,
            "target_price": round(t1_price, 2),
            "risk_reward": 1.5,
        }
    )

    # 第二批（30%仓位）：3倍风险回报比
    t2_distance = stop_distance * 3.0
    if direction == "long":
        t2_price = entry_price + t2_distance
    else:
        t2_price = entry_price - t2_distance
    batches.append(
        {
            "batch": 2,
            "pct_of_position": 30,
            "target_price": round(t2_price, 2),
            "risk_reward": 3.0,
        }
    )

    # 第三批（20%仓位）：5倍风险回报比或移动止损
    t3_distance = stop_distance * 5.0
    if direction == "long":
        t3_price = entry_price + t3_distance
    else:
        t3_price = entry_price - t3_distance
    batches.append(
        {
            "batch": 3,
            "pct_of_position": 20,
            "target_price": round(t3_price, 2),
            "risk_reward": 5.0,
            "note": "或使用移动止损跟踪",
        }
    )

    return batches


# ============================================================
# 5. 综合止损止盈计算
# ============================================================


def calculate_stop_loss_take_profit(
    entry_price,
    atr=None,
    atr_multiplier=2.0,
    stop_pct=None,
    support_price=None,
    highest_price=None,
    position_size=None,
    direction="long",
    output_json=False,
):
    """综合止损止盈计算"""
    result = {
        "entry_price": entry_price,
        "direction": direction,
    }

    # --- 止损价计算（多种方法）---
    stops = {}

    # ATR止损
    if atr:
        atr_stop = calculate_atr_stop(entry_price, atr, atr_multiplier, direction)
        stops["atr_stop"] = atr_stop
        result["atr"] = atr
        result["atr_multiplier"] = atr_multiplier

    # 百分比止损
    if stop_pct:
        pct_stop = calculate_percentage_stop(entry_price, stop_pct, direction)
        stops["pct_stop"] = pct_stop
        result["stop_pct"] = stop_pct

    # 支撑位止损
    if support_price:
        if direction == "long" and support_price < entry_price:
            stops["support_stop"] = support_price
        elif direction == "short" and support_price > entry_price:
            stops["support_stop"] = support_price

    result["stop_loss_options"] = stops

    # 推荐止损（ATR优先，其次支撑位，最后百分比）
    if "atr_stop" in stops:
        result["recommended_stop"] = stops["atr_stop"]
        result["stop_method"] = "ATR"
    elif "support_stop" in stops:
        result["recommended_stop"] = stops["support_stop"]
        result["stop_method"] = "支撑位"
    elif "pct_stop" in stops:
        result["recommended_stop"] = stops["pct_stop"]
        result["stop_method"] = "百分比"

    # --- 止盈价计算 ---
    targets = {}
    if atr:
        targets["atr_targets"] = calculate_atr_targets(entry_price, atr, direction)

    # 分批止盈
    stop_for_batch = result.get("recommended_stop")
    batches = calculate_batch_take_profit(
        entry_price, position_size, 3.0, atr, stop_for_batch, direction
    )
    targets["batch_strategy"] = batches
    result["take_profit"] = targets

    # --- 移动止损 ---
    if highest_price:
        trail_stops = calculate_trailing_stop(highest_price, entry_price, 8.0, atr, 2.5)
        result["trailing_stop"] = trail_stops

    # --- 风险回报比 ---
    if result.get("recommended_stop"):
        stop = result["recommended_stop"]
        risk = abs(entry_price - stop)
        if risk > 0 and batches:
            t1 = batches[0]["target_price"]
            reward = abs(t1 - entry_price)
            result["risk_reward_ratio"] = round(reward / risk, 2)

    if output_json:
        print(json.dumps(result, ensure_ascii=False, indent=2))
    else:
        print(f"止损止盈分析")
        print("=" * 60)
        print(f"入场价: {entry_price}")
        print(f"方向: {'做多' if direction == 'long' else '做空'}")
        if atr:
            print(f"ATR: {atr}")

        print(f"\n止损方案:")
        for method, price in stops.items():
            risk_pct = abs(entry_price - price) / entry_price * 100
            label = {
                "atr_stop": "ATR止损",
                "pct_stop": "百分比止损",
                "support_stop": "支撑位止损",
            }.get(method, method)
            marker = (
                " ← 推荐"
                if method.replace("_stop", "") == result.get("stop_method", "").lower()
                else ""
            )
            print(f"  {label}: {price}  (风险{risk_pct:.1f}%){marker}")

        print(f"\n分批止盈策略:")
        for b in batches:
            profit_pct = abs(b["target_price"] - entry_price) / entry_price * 100
            rr = b["risk_reward"]
            note = f"  ({b['note']})" if b.get("note") else ""
            print(
                f"  第{b['batch']}批({b['pct_of_position']}%仓位): {b['target_price']}  盈利{profit_pct:.1f}%  R:R={rr}{note}"
            )

        if result.get("risk_reward_ratio"):
            print(f"\n首目标风险回报比: {result['risk_reward_ratio']}")

        if highest_price:
            print(f"\n移动止损参考:")
            print(f"  最高价: {highest_price}")
            for method, price in trail_stops.items():
                label = "百分比移动止损" if "pct" in method else "ATR移动止损"
                print(f"  {label}: {price}")

        print("=" * 60)

    return result


def main():
    parser = argparse.ArgumentParser(description="止损止盈计算")
    parser.add_argument("--entry-price", type=float, required=True, help="入场价格")
    parser.add_argument("--atr", type=float, help="ATR（平均真实波幅）")
    parser.add_argument(
        "--atr-multiplier", type=float, default=2.0, help="ATR止损倍数（默认2.0）"
    )
    parser.add_argument("--stop-pct", type=float, help="止损百分比（如5表示5%%）")
    parser.add_argument("--support-price", type=float, help="支撑位价格")
    parser.add_argument(
        "--highest-price", type=float, help="持仓以来最高价（用于移动止损）"
    )
    parser.add_argument("--position-size", type=float, help="持仓数量")
    parser.add_argument(
        "--direction", choices=["long", "short"], default="long", help="方向"
    )
    parser.add_argument(
        "--json", action="store_true", dest="output_json", help="输出JSON格式"
    )
    args = parser.parse_args()

    result = calculate_stop_loss_take_profit(
        entry_price=args.entry_price,
        atr=args.atr,
        atr_multiplier=args.atr_multiplier,
        stop_pct=args.stop_pct,
        support_price=args.support_price,
        highest_price=args.highest_price,
        position_size=args.position_size,
        direction=args.direction,
        output_json=args.output_json,
    )

    return 0


if __name__ == "__main__":
    exit(main())
