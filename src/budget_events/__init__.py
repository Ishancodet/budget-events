"""
budget_events - Turn raw expense logs into categorized summaries, budgets, and anomaly flags.
"""

__version__ = "0.1.0"

from .csvjson_transaction_normalizat import BudgetEvents
from .types import BudgetEventsOptions, BudgetEventsResult
from .exceptions import BudgetEventsError, ConfigurationError, ValidationError

__all__ = [
    "BudgetEvents",
    "BudgetEventsOptions",
    "BudgetEventsResult",
    "BudgetEventsError",
    "ConfigurationError",
    "ValidationError",
]
