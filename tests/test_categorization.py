import pytest
from budget_events import Transaction, categorize_transactions, RuleBasedClassifier


def test_rule_based_classifier_basic():
    rules = {
        "Coffee": ["starbucks", "coffee"],
        "Groceries": ["whole foods", "grocery", "supermarket"],
    }
    classifier = RuleBasedClassifier(rules)
    tx1 = Transaction(id="1", date="2024-06-30", amount=-4.5, currency="USD", description="Starbucks", payee=None, raw={})
    tx2 = Transaction(id="2", date="2024-06-30", amount=-50, currency="USD", description="Whole Foods Market", payee=None, raw={})
    tx3 = Transaction(id="3", date="2024-06-30", amount=-20, currency="USD", description="Lunch", payee=None, raw={})
    txs = [tx1, tx2, tx3]
    result = categorize_transactions(txs, classifier)
    assert result[0].category == "Coffee"
    assert result[1].category == "Groceries"
    assert result[2].category is None

def test_categorize_transactions_no_classifier():
    tx = Transaction(id="1", date="2024-06-30", amount=-10, currency="USD", description="Misc", payee=None, raw={})
    result = categorize_transactions([tx])
    assert result[0].category is None

def test_rule_based_classifier_case_insensitive():
    rules = {"Coffee": ["starbucks"]}
    classifier = RuleBasedClassifier(rules)
    tx = Transaction(id="1", date="2024-06-30", amount=-4.5, currency="USD", description="STARBUCKS", payee=None, raw={})
    result = categorize_transactions([tx], classifier)
    assert result[0].category == "Coffee"

def test_rule_based_classifier_payee():
    rules = {"Coffee": ["starbucks"]}
    classifier = RuleBasedClassifier(rules)
    tx = Transaction(id="1", date="2024-06-30", amount=-4.5, currency="USD", description="", payee="Starbucks", raw={})
    result = categorize_transactions([tx], classifier)
    assert result[0].category == "Coffee"
