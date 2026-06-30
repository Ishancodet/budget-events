# Minimal import test for budget_events

def test_import_budget_events():
    import budget_events
    assert budget_events is not None
    assert hasattr(budget_events, "normalize_transactions")
    assert hasattr(budget_events, "Transaction")
    assert hasattr(budget_events, "NormalizationResult")
