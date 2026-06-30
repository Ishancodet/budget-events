# budget_events

Turn raw expense logs into categorized summaries, budgets, and anomaly flags.

## Installation

```bash
pip install budget_events
```

## Quick Start

```python
from budget_events import BudgetEvents

instance = BudgetEvents()
result = instance.run()
print(result)
```

## Features

- CSV/JSON transaction normalization into a canonical schema
- Rule-based categorization with pluggable classifiers
- Monthly rollups, budget checks, and simple anomaly detection

## API Reference

### `BudgetEvents`

#### Constructor

```python
BudgetEvents(options: BudgetEventsOptions | None = None)
```

#### Methods

- `run()` - Execute the main operation. Returns `BudgetEventsResult`.

## Development

```bash
# Install with dev dependencies
make install

# Run tests
make test

# Lint and type-check
make lint

# Format code
make format

# Build
make build
```

## Publishing

1. Update version in `pyproject.toml` and `src/budget_events/__init__.py`
2. Create a GitHub release with tag `v0.x.0`
3. The GitHub Action will automatically publish to PyPI

## License

MIT
