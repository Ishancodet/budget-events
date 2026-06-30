"""Tests for budget_events."""

from budget_events import BudgetEvents, BudgetEventsOptions


class TestBudgetEvents:
    def test_create_instance_with_defaults(self) -> None:
        instance = BudgetEvents()
        assert instance is not None

    def test_create_instance_with_options(self) -> None:
        options = BudgetEventsOptions(verbose=True)
        instance = BudgetEvents(options)
        assert instance.options.verbose is True

    def test_run_successfully(self) -> None:
        instance = BudgetEvents()
        result = instance.run()
        assert result.success is True
        assert result.data is not None

    def test_run_returns_result_type(self) -> None:
        instance = BudgetEvents()
        result = instance.run()
        assert result.error is None
