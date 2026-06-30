"""
Monthly rollups and budget checks for budget_events.

Provides functions to summarize transactions by month and check against budgets.
"""
from typing import List, Dict, Optional, Any
from datetime import date, datetime
from collections import defaultdict
from .types import Transaction
from .exceptions import ValidationError


def _parse_month(dt: str | date | datetime) -> str:
    """Convert a date/datetime/ISO string to 'YYYY-MM' format."""
    if isinstance(dt, str):
        try:
            d = datetime.fromisoformat(dt)
        except Exception:
            raise ValidationError(f"Invalid date string: {dt}")
    elif isinstance(dt, datetime):
        d = dt
    elif isinstance(dt, date):
        d = datetime(dt.year, dt.month, dt.day)
    else:
        raise ValidationError(f"Invalid date type: {type(dt)}")
    return f"{d.year:04d}-{d.month:02d}"


def monthly_rollup(transactions: List[Transaction], category: Optional[str] = None) -> Dict[str, float]:
    """
    Summarize total transaction amounts by month.

    Args:
        transactions: List of Transaction objects.
        category: If provided, only include transactions in this category.

    Returns:
        Dict mapping 'YYYY-MM' to total amount for that month.

    Example::
        rollup = monthly_rollup(transactions)
        # {'2024-06': -1200.0, '2024-07': -800.0}
    """
    rollup: Dict[str, float] = defaultdict(float)
    for tx in transactions:
        if category and tx.category != category:
            continue
        month = _parse_month(tx.date)
        rollup[month] += tx.amount
    return dict(rollup)


def check_budget(
    rollup: Dict[str, float],
    budgets: Dict[str, float],
) -> Dict[str, Dict[str, Any]]:
    """
    Check monthly rollups against budgets.

    Args:
        rollup: Dict mapping 'YYYY-MM' to total amount (from monthly_rollup).
        budgets: Dict mapping 'YYYY-MM' to budget limit (negative for outflow).

    Returns:
        Dict mapping 'YYYY-MM' to dict with 'actual', 'budget', and 'over' (bool).

    Example::
        result = check_budget({'2024-06': -1200.0}, {'2024-06': -1000.0})
        # {'2024-06': {'actual': -1200.0, 'budget': -1000.0, 'over': True}}
    """
    result: Dict[str, Dict[str, Any]] = {}
    for month, actual in rollup.items():
        budget = budgets.get(month)
        if budget is None:
            continue
        result[month] = {
            'actual': actual,
            'budget': budget,
            'over': actual < budget if budget < 0 else actual > budget,
        }
    return result
