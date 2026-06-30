"""Type definitions for budget_events."""

from dataclasses import dataclass, field
from typing import Any, Optional


@dataclass
class BudgetEventsOptions:
    """Configuration options for BudgetEvents.

    Attributes:
        verbose: Enable verbose logging for debugging.
        feature_1: Configuration for: CSV/JSON transaction normalization into a canonical schema
        feature_2: Configuration for: Rule-based categorization with pluggable classifiers
        feature_3: Configuration for: Monthly rollups, budget checks, and simple anomaly detection
    """

    verbose: bool = False
    feature_1: Optional[dict[str, Any]] = None
    feature_2: Optional[dict[str, Any]] = None
    feature_3: Optional[dict[str, Any]] = None


@dataclass
class BudgetEventsResult:
    """Result returned by BudgetEvents operations.

    Attributes:
        success: Whether the operation succeeded.
        data: The result data, if successful.
        error: Error message, if the operation failed.
    """

    success: bool
    data: Any = field(default=None)
    error: Optional[str] = None
