"""Core module for budget_events."""

from .types import BudgetEventsOptions, BudgetEventsResult


class BudgetEvents:
    """Turn raw expense logs into categorized summaries, budgets, and anomaly flags.

    Example::

        from budget_events import BudgetEvents

        instance = BudgetEvents()
        result = instance.run()
        print(result)
    """

    def __init__(self, options: BudgetEventsOptions | None = None) -> None:
        self.options = options or BudgetEventsOptions()

    def run(self) -> BudgetEventsResult:
        """Execute the main operation.

        Returns:
            BudgetEventsResult with the operation outcome.
        """
        # TODO: Implement core functionality
        # Key features to implement:
        #   - CSV/JSON transaction normalization into a canonical schema
        #   - Rule-based categorization with pluggable classifiers
        #   - Monthly rollups, budget checks, and simple anomaly detection

        return BudgetEventsResult(
            success=True,
            data={"message": "BudgetEvents is working!"},
        )
