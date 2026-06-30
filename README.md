# budget_events

Turn raw expense logs into categorized summaries, budgets, and anomaly flags.

## Installation

```bash
pip install budget_events
```

## Quick Start

```python
from budget_events import normalize_transactions, detect_anomalies

csv_data = "date,amount,currency,description\n2024-06-30,-12.34,USD,Coffee shop\n2024-06-30,-1200.00,USD,Laptop purchase\n2024-06-30,-12.34,USD,Coffee shop"
result = normalize_transactions(csv_data, input_format="csv")
print(result.transactions)

# Anomaly detection
anomalies = detect_anomalies(result.transactions)
for anomaly in anomalies:
    print(anomaly.type, anomaly.details)
```

## Features

- CSV/JSON transaction normalization into a canonical schema
- Rule-based categorization with pluggable classifiers
- Monthly rollups, budget checks, and simple anomaly detection

## Advanced: Custom and Rule-Based Categorization

You can categorize transactions using either the built-in rule-based classifier or your own custom logic.

### Rule-Based Categorization Example

```python
from budget_events import categorize_transactions, RuleBasedClassifier, Transaction

# Define rules: category name -> list of keywords
rules = {
    "Coffee": ["starbucks", "coffee"],
    "Groceries": ["whole foods", "grocery", "supermarket"],
    "Tech": ["laptop", "apple store", "best buy"],
}
classifier = RuleBasedClassifier(rules)

transactions = [
    Transaction(id="1", date="2024-06-30", amount=-12.34, currency="USD", description="Coffee shop", payee="Starbucks"),
    Transaction(id="2", date="2024-06-30", amount=-1200.00, currency="USD", description="Laptop purchase", payee="Apple Store"),
    Transaction(id="3", date="2024-06-30", amount=-80.00, currency="USD", description="Groceries", payee="Whole Foods"),
]

categorized = categorize_transactions(transactions, classifier)
for tx in categorized:
    print(tx.description, "=>", tx.category)
# Output:
# Coffee shop => Coffee
# Laptop purchase => Tech
# Groceries => Groceries
```

### Custom Classifier Example

You can implement your own classifier by creating a class with a `classify(transaction)` method:

```python
from budget_events import categorize_transactions, Transaction, TransactionClassifier
from typing import Optional

class MyCustomClassifier:
    def classify(self, transaction: Transaction) -> Optional[str]:
        if transaction.amount < -1000:
            return "Large Purchase"
        if "coffee" in (transaction.description or "").lower():
            return "Coffee"
        return None

transactions = [
    Transaction(id="1", date="2024-06-30", amount=-1500.00, currency="USD", description="Laptop"),
    Transaction(id="2", date="2024-06-30", amount=-12.34, currency="USD", description="Coffee shop"),
]

custom_classifier = MyCustomClassifier()
categorized = categorize_transactions(transactions, custom_classifier)
for tx in categorized:
    print(tx.description, "=>", tx.category)
# Output:
# Laptop => Large Purchase
# Coffee shop => Coffee
```

_Tip: You can chain or combine classifiers by writing a wrapper that tries multiple strategies!_

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
