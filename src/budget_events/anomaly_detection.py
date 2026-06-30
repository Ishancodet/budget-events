"""Anomaly detection for budget_events transactions.

Exports:
    detect_anomalies: Scan transactions for high expenses and duplicates.
"""
from __future__ import annotations
from typing import List, Optional, Dict, Tuple
from .types import Transaction, Anomaly, AnomalyType


def detect_anomalies(
    transactions: List[Transaction],
    high_expense_threshold: Optional[float] = None,
    duplicate_window_days: int = 2,
) -> List[Anomaly]:
    """
    Scan normalized transactions for anomalies: unusually high expenses and potential duplicates.

    Args:
        transactions: List of normalized Transaction objects.
        high_expense_threshold: Flag expenses above this absolute value (negative for outflow). If None, uses 99th percentile.
        duplicate_window_days: Number of days within which to consider duplicates (default: 2).

    Returns:
        List[Anomaly]: List of detected anomalies.

    Example::
        anomalies = detect_anomalies(transactions)
        for anomaly in anomalies:
            print(anomaly.type, anomaly.details)
    """
    anomalies: List[Anomaly] = []
    if not transactions:
        return anomalies

    # --- High Expense Detection ---
    expenses = [abs(tx.amount) for tx in transactions if tx.amount < 0]
    threshold = high_expense_threshold
    if threshold is None and expenses:
        # Use 99th percentile as default threshold
        sorted_exp = sorted(expenses)
        idx = int(0.99 * len(sorted_exp))
        threshold = sorted_exp[min(idx, len(sorted_exp)-1)]
    if threshold:
        for tx in transactions:
            if tx.amount < 0 and abs(tx.amount) >= threshold:
                anomalies.append(Anomaly(
                    type=AnomalyType.HIGH_EXPENSE,
                    transaction=tx,
                    details=f"Expense {tx.amount} >= threshold {threshold}",
                ))

    # --- Duplicate Detection ---
    # Consider duplicates as same amount, date, and description/payee within window
    seen: Dict[Tuple[str, float, str], List[Transaction]] = {}
    for tx in transactions:
        key = (
            str(tx.date),
            float(tx.amount),
            (tx.description or "")[:32].lower(),
        )
        if key in seen:
            for prev in seen[key]:
                anomalies.append(Anomaly(
                    type=AnomalyType.DUPLICATE,
                    transaction=tx,
                    details=f"Possible duplicate of transaction ID {prev.id}",
                ))
            seen[key].append(tx)
        else:
            seen[key] = [tx]
    return anomalies
