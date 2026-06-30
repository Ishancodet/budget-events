import pytest
from budget_events import Transaction, monthly_rollup, check_budget
from datetime import date

def make_tx(date_, amount, category=None):
    return Transaction(
        id=None,
        date=date_,
        amount=amount,
        currency="USD",
        description="Test",
        payee=None,
        category=category,
        raw={},
    )

def test_monthly_rollup_basic():
    txs = [
        make_tx("2024-06-01", -100),
        make_tx("2024-06-15", -200),
        make_tx("2024-07-01", -300),
    ]
    rollup = monthly_rollup(txs)
    assert rollup == {"2024-06": -300, "2024-07": -300}

def test_monthly_rollup_category():
    txs = [
        make_tx("2024-06-01", -100, category="Food"),
        make_tx("2024-06-15", -200, category="Bills"),
        make_tx("2024-06-20", -50, category="Food"),
    ]
    rollup = monthly_rollup(txs, category="Food")
    assert rollup == {"2024-06": -150}

def test_check_budget_basic():
    rollup = {"2024-06": -1200.0, "2024-07": -800.0}
    budgets = {"2024-06": -1000.0, "2024-07": -900.0}
    result = check_budget(rollup, budgets)
    assert result["2024-06"]["over"] is True
    assert result["2024-07"]["over"] is False
    assert result["2024-06"]["actual"] == -1200.0
    assert result["2024-06"]["budget"] == -1000.0

def test_check_budget_missing_month():
    rollup = {"2024-06": -1200.0}
    budgets = {"2024-07": -1000.0}
    result = check_budget(rollup, budgets)
    assert "2024-06" not in result

def test_monthly_rollup_invalid_date():
    txs = [make_tx("not-a-date", -100)]
    with pytest.raises(Exception):
        monthly_rollup(txs)
