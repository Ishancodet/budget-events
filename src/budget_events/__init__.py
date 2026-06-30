"""
budget_events - Turn raw expense logs into categorized summaries, budgets, and anomaly flags.
"""

__version__ = "0.1.0"

from .csvjson_transaction_normalizat import normalize_transactions
from .anomaly_detection import detect_anomalies
from .categorization import categorize_transactions, RuleBasedClassifier
from .types import (
    Transaction,
    NormalizationResult,
    Anomaly,
    AnomalyType,
    BudgetEventsOptions,
    BudgetEventsResult,
    TransactionClassifier,
)
from .rollup import monthly_rollup, check_budget
from .exceptions import (
    BudgetEventsError,
    ConfigurationError,
    ValidationError,
)

__all__ = [
    "normalize_transactions",
    "detect_anomalies",
    "categorize_transactions",
    "RuleBasedClassifier",
    "TransactionClassifier",
    "monthly_rollup",
    "check_budget",
    "Transaction",
    "NormalizationResult",
    "Anomaly",
    "AnomalyType",
    "BudgetEventsOptions",
    "BudgetEventsResult",
    "BudgetEventsError",
    "ConfigurationError",
    "ValidationError",
]
