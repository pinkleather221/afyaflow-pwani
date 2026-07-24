"""Deterministic stock-risk and redistribution logic for AfyaFlow Pwani."""

from __future__ import annotations

import math

from .schemas import FacilityInventory, StockReport, StockRisk, TransferOption


RED_THRESHOLD_DAYS = 3
AMBER_THRESHOLD_DAYS = 7
SURPLUS_THRESHOLD_DAYS = 14
TRANSFER_BUFFER_DAYS = 7


def estimate_adjusted_daily_use(report: StockReport) -> int:
    """Adjust demand conservatively when patient footfall is unusually high.

    The prototype uses patient footfall only as a demand signal. If footfall is
    provided and is more than twice the normal daily use proxy, demand is raised
    by 25%. These thresholds are prototype assumptions and not official policy.
    """

    if report.patient_footfall_today is None:
        return report.average_daily_use
    if report.patient_footfall_today > report.average_daily_use * 2:
        return max(1, math.ceil(report.average_daily_use * 1.25))
    return report.average_daily_use


def calculate_stock_risk(report: StockReport) -> StockRisk:
    """Compute an explainable stock-risk classification."""

    adjusted_daily_use = estimate_adjusted_daily_use(report)
    days_of_stock = report.balance_units / adjusted_daily_use
    if days_of_stock < RED_THRESHOLD_DAYS:
        level = "red"
        reason = "Less than 3 days of stock remaining; immediate action is needed."
    elif days_of_stock < AMBER_THRESHOLD_DAYS:
        level = "amber"
        reason = "Between 3 and 7 days of stock remaining; plan replenishment now."
    else:
        level = "green"
        reason = "At least 7 days of stock remaining; continue routine monitoring."
    return StockRisk(
        days_of_stock=round(days_of_stock, 2),
        adjusted_daily_use=adjusted_daily_use,
        level=level,
        reason=reason,
    )


def rank_transfer_options(
    report: StockReport,
    inventory: list[FacilityInventory],
    max_options: int = 3,
) -> list[TransferOption]:
    """Rank nearby synthetic facilities that can safely donate stock."""

    matches: list[TransferOption] = []
    for candidate in inventory:
        if candidate.item.lower() != report.item.lower():
            continue
        candidate_days = candidate.balance_units / candidate.average_daily_use
        if candidate_days <= SURPLUS_THRESHOLD_DAYS:
            continue
        surplus_units = math.floor(
            candidate.balance_units - (candidate.average_daily_use * TRANSFER_BUFFER_DAYS)
        )
        if surplus_units <= 0:
            continue
        matches.append(
            TransferOption(
                facility=candidate.facility,
                item=candidate.item,
                surplus_units=surplus_units,
                days_of_stock_after_transfer=round(
                    (candidate.balance_units - surplus_units) / candidate.average_daily_use,
                    2,
                ),
                distance_km=candidate.distance_km,
                reason=(
                    f"{candidate.facility} has more than {SURPLUS_THRESHOLD_DAYS} days "
                    f"of {candidate.item} and is {candidate.distance_km:g} km away."
                ),
            )
        )
    return sorted(matches, key=lambda option: (option.distance_km, -option.surplus_units))[
        :max_options
    ]


def calculate_stock_risk_with_transfers(
    report: StockReport,
    inventory: list[FacilityInventory],
) -> StockRisk:
    """Calculate risk and attach ranked redistribution candidates."""

    base = calculate_stock_risk(report)
    transfers = rank_transfer_options(report, inventory)
    return StockRisk(
        days_of_stock=base.days_of_stock,
        adjusted_daily_use=base.adjusted_daily_use,
        level=base.level,
        reason=base.reason,
        transfer_rank=transfers,
    )
