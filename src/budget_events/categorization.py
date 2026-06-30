"""Rule-based transaction categorization for budget_events.

Exports:
    categorize_transactions: Categorize transactions using a pluggable classifier.
    RuleBasedClassifier: Default rule-based classifier.
"""
from typing import List, Optional, Dict, Any
from .types import Transaction, TransactionClassifier

class RuleBasedClassifier:
    """
    Simple rule-based classifier for transactions.

    Args:
        rules: Dict mapping category names to lists of keywords (matched against description/payee).

    Example::
        rules = {
            "Coffee": ["starbucks", "coffee"],
            "Groceries": ["whole foods", "grocery", "supermarket"],
        }
        classifier = RuleBasedClassifier(rules)
        tx.category = classifier.classify(tx)
    """
    def __init__(self, rules: Optional[Dict[str, List[str]]] = None) -> None:
        self.rules = rules or {}

    def classify(self, transaction: Transaction) -> Optional[str]:
        text = f"{transaction.description or ''} {transaction.payee or ''}".lower()
        for category, keywords in self.rules.items():
            for kw in keywords:
                if kw.lower() in text:
                    return category
        return None

def categorize_transactions(
    transactions: List[Transaction],
    classifier: Optional[TransactionClassifier] = None,
) -> List[Transaction]:
    """
    Categorize a list of transactions using the provided classifier.
    If no classifier is given, uses a default RuleBasedClassifier with no rules (no-op).

    Args:
        transactions: List of Transaction objects to categorize.
        classifier: Optional TransactionClassifier. If None, uses RuleBasedClassifier with no rules.

    Returns:
        List[Transaction]: New list of transactions with category field set (if classified).

    Example::
        from budget_events import categorize_transactions, RuleBasedClassifier
        rules = {"Coffee": ["starbucks", "coffee"]}
        classifier = RuleBasedClassifier(rules)
        txs = categorize_transactions(transactions, classifier)
    """
    if classifier is None:
        classifier = RuleBasedClassifier()
    result = []
    for tx in transactions:
        category = classifier.classify(tx)
        tx_new = Transaction(
            id=tx.id,
            date=tx.date,
            amount=tx.amount,
            currency=tx.currency,
            description=tx.description,
            payee=tx.payee,
            category=category if category else tx.category,
            raw=tx.raw,
        )
        result.append(tx_new)
    return result
