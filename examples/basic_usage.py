#!/usr/bin/env python3
"""Basic usage example for budget_events."""

from budget_events import BudgetEvents, BudgetEventsOptions


def main() -> None:
    # Create with default options
    instance = BudgetEvents()
    result = instance.run()
    print(f"Default run: success={result.success}, data={result.data}")

    # Create with custom options
    options = BudgetEventsOptions(verbose=True)
    instance = BudgetEvents(options)
    result = instance.run()
    print(f"Verbose run: success={result.success}, data={result.data}")


if __name__ == "__main__":
    main()
