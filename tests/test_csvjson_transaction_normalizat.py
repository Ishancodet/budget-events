"""Tests for budget_events normalization and anomaly detection."""

import pytest
from budget_events import normalize_transactions, Transaction, NormalizationResult, detect_anomalies, AnomalyType

class TestNormalizeTransactions:
    def test_normalize_csv_string(self) -> None:
        csv_data = "date,amount,currency,description\n2024-06-30,-12.34,USD,Coffee shop"
        result = normalize_transactions(csv_data, input_format="csv")
        assert isinstance(result, NormalizationResult)
        assert len(result.transactions) == 1
        tx = result.transactions[0]
        assert tx.amount == -12.34
        assert tx.currency == "USD"
        assert tx.description == "Coffee shop"
        assert tx.date == "2024-06-30"
        assert tx.raw["amount"] == "-12.34" or tx.raw["amount"] == -12.34

    def test_normalize_json_string(self) -> None:
        json_data = '[{"date": "2024-06-30", "amount": -12.34, "currency": "USD", "description": "Coffee shop"}]'
        result = normalize_transactions(json_data, input_format="json")
        assert isinstance(result, NormalizationResult)
        assert len(result.transactions) == 1
        tx = result.transactions[0]
        assert tx.amount == -12.34
        assert tx.currency == "USD"
        assert tx.description == "Coffee shop"
        assert tx.date == "2024-06-30"

    def test_normalize_list_of_dicts(self) -> None:
        data = [{"date": "2024-06-30", "amount": -12.34, "currency": "USD", "description": "Coffee shop"}]
        result = normalize_transactions(data, input_format="json")
        assert isinstance(result, NormalizationResult)
        assert len(result.transactions) == 1
        tx = result.transactions[0]
        assert tx.amount == -12.34
        assert tx.currency == "USD"
        assert tx.description == "Coffee shop"
        assert tx.date == "2024-06-30"

    def test_missing_required_fields(self) -> None:
        data = [{"amount": -12.34, "currency": "USD", "description": "Coffee shop"}]
        result = normalize_transactions(data, input_format="json")
        assert isinstance(result, NormalizationResult)
        assert len(result.transactions) == 0
        assert len(result.errors) == 1
        assert "Missing required field: date" in result.errors[0]

    def test_invalid_amount(self) -> None:
        data = [{"date": "2024-06-30", "amount": "not_a_number", "currency": "USD", "description": "Coffee shop"}]
        result = normalize_transactions(data, input_format="json")
        assert isinstance(result, NormalizationResult)
        assert len(result.transactions) == 0
        assert len(result.errors) == 1
        assert "Invalid amount" in result.errors[0]

    def test_invalid_date(self) -> None:
        data = [{"date": "not_a_date", "amount": -12.34, "currency": "USD", "description": "Coffee shop"}]
        result = normalize_transactions(data, input_format="json")
        assert isinstance(result, NormalizationResult)
        assert len(result.transactions) == 0
        assert len(result.errors) == 1
        assert "Invalid date format" in result.errors[0]

    def test_empty_input(self) -> None:
        data = []
        result = normalize_transactions(data, input_format="json")
        assert isinstance(result, NormalizationResult)
        assert len(result.transactions) == 0
        assert len(result.errors) == 0

class TestAnomalyDetection:
    def test_high_expense_and_duplicate_detection(self) -> None:
        txs = [
            Transaction(id="1", date="2024-06-30", amount=-12.34, currency="USD", description="Coffee shop"),
            Transaction(id="2", date="2024-06-30", amount=-1200.00, currency="USD", description="Laptop purchase"),
            Transaction(id="3", date="2024-06-30", amount=-12.34, currency="USD", description="Coffee shop"),
            Transaction(id="4", date="2024-06-30", amount=1000.00, currency="USD", description="Salary"),
        ]
        anomalies = detect_anomalies(txs, high_expense_threshold=1000)
        high_expenses = [a for a in anomalies if a.type == AnomalyType.HIGH_EXPENSE]
        duplicates = [a for a in anomalies if a.type == AnomalyType.DUPLICATE]
        assert len(high_expenses) == 1
        assert high_expenses[0].transaction.id == "2"
        assert len(duplicates) == 1
        assert duplicates[0].transaction.id == "3"
        assert "duplicate" in duplicates[0].type

    def test_no_anomalies(self) -> None:
        txs = [
            Transaction(id="1", date="2024-06-30", amount=-10.00, currency="USD", description="Lunch"),
            Transaction(id="2", date="2024-06-29", amount=-20.00, currency="USD", description="Groceries"),
        ]
        anomalies = detect_anomalies(txs, high_expense_threshold=1000)
        assert anomalies == []

    def test_empty_transactions(self) -> None:
        anomalies = detect_anomalies([])
        assert anomalies == []
