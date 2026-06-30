"""Custom exceptions for budget_events."""

from __future__ import annotations

class BudgetEventsError(Exception):
    """Base exception for all BudgetEvents errors.

    Attributes:
        message: Human-readable error description.
        code: Optional machine-readable error code.
    """
    def __init__(self, message: str, code: str | None = None) -> None:
        super().__init__(message)
        self.code = code

class ConfigurationError(BudgetEventsError):
    """Raised when the SDK is misconfigured."""

class ValidationError(BudgetEventsError):
    """Raised when input validation fails."""

class TimeoutError(BudgetEventsError):
    """Raised when an operation exceeds its time limit."""
