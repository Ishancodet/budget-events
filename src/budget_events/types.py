"""Type definitions for budget_events."""

from dataclasses import dataclass, field
from typing import Any, Optional, List, Dict, Union, Protocol
from datetime import date, datetime
from enum import Enum


class AnomalyType(str, Enum):
    """Types of anomalies detected in transactions."""
    HIGH_EXPENSE = "high_expense"
    DUPLICATE = "duplicate"


@dataclass
class Anomaly:
    """Anomaly detected in a transaction.

    Attributes:
        type: Type of anomaly (e.g., high_expense, duplicate).
        transaction: The Transaction flagged as anomalous.
        details: Optional details about the anomaly.
    """
    type: AnomalyType
    transaction: 'Transaction'
    details: Optional[str] = None


@dataclass
class Transaction:
    """Canonical transaction schema for budget_events.

    Attributes:
        id: Unique transaction identifier (optional, may be generated).
        date: Transaction date (ISO 8601 string or datetime/date).
        amount: Transaction amount (positive for inflow, negative for outflow).
        currency: ISO 4217 currency code (e.g., 'USD').
        description: Description or memo for the transaction.
        payee: Who the transaction was with (optional).
        category: Optional category (may be filled by classifier).
        raw: Original raw record (for traceability).
    Example::
        Transaction(
            id="abc123",
            date="2024-06-30",
            amount=-12.34,
            currency="USD",
            description="Coffee shop",
            payee="Starbucks",
            category=None,
            raw={...},
        )
    """
    id: Optional[str]
    date: Union[str, date, datetime]
    amount: float
    currency: str
    description: str
    payee: Optional[str] = None
    category: Optional[str] = None
    raw: Dict[str, Any] = field(default_factory=dict)


@dataclass
class NormalizationResult:
    """Result of transaction normalization.

    Attributes:
        transactions: List of normalized Transaction objects.
        errors: List of error messages for records that could not be normalized.
    """
    transactions: List[Transaction]
    errors: List[str] = field(default_factory=list)


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


class TransactionClassifier(Protocol):
    """
    Protocol for transaction classifiers.

    Implementations should provide a classify() method that returns a category string or None.

    Example::
        class MyClassifier:
            def classify(self, transaction: Transaction) -> Optional[str]:
                if "coffee" in transaction.description.lower():
                    return "Coffee"
                return None
    """
    def classify(self, transaction: Transaction) -> Optional[str]:
        ...
