"""CSV/JSON transaction normalization for budget_events.

Exports:
    normalize_transactions: Normalize CSV/JSON data into canonical Transaction objects.
"""
from __future__ import annotations
from typing import Any, List, Dict, Union, IO
import csv
import json
from datetime import datetime, date

from .types import Transaction, NormalizationResult
from .exceptions import ValidationError, BudgetEventsError
from ._utils import validate_not_empty

def normalize_transactions(
    data: Union[str, List[Dict[str, Any]], IO[str]],
    input_format: str = "auto",
    encoding: str = "utf-8",
) -> NormalizationResult:
    print("[budget_events.csvjson_transaction_normalizat] Entered normalize_transactions")
    """
    Normalize CSV or JSON transaction data into canonical Transaction objects.

    Args:
        data: CSV string, JSON string, list of dicts, or file-like object.
        input_format: 'csv', 'json', or 'auto' (default: auto-detect).
        encoding: Encoding for file-like objects (default: 'utf-8').

    Returns:
        NormalizationResult: Contains normalized transactions and errors.

    Raises:
        ValidationError: If input is invalid or cannot be parsed.

    Example::
        csv_data = "date,amount,currency,description\n2024-06-30,-12.34,USD,Coffee shop"
        result = normalize_transactions(csv_data, input_format="csv")
        print(result.transactions)
    """
    try:
        print(f"[budget_events.csvjson_transaction_normalizat] input_format: {input_format}, type(data): {type(data)}")
        if input_format == "auto":
            if isinstance(data, str):
                print("[budget_events.csvjson_transaction_normalizat] auto: data is str")
                if data.strip().startswith("[") or data.strip().startswith("{"):
                    input_format = "json"
                else:
                    input_format = "csv"
            elif hasattr(data, "read"):
                print("[budget_events.csvjson_transaction_normalizat] auto: data is file-like")
                # Peek at first few bytes
                pos = data.tell()
                head = data.read(2048)
                data.seek(pos)
                if head.strip().startswith("[") or head.strip().startswith("{"):
                    input_format = "json"
                else:
                    input_format = "csv"
            elif isinstance(data, list):
                print("[budget_events.csvjson_transaction_normalizat] auto: data is list")
                input_format = "json"
            else:
                print("[budget_events.csvjson_transaction_normalizat] auto: unsupported type")
                raise ValidationError("Unsupported input type for normalization.")

        records: List[Dict[str, Any]] = []
        print(f"[budget_events.csvjson_transaction_normalizat] resolved input_format: {input_format}")
        if input_format == "csv":
            if hasattr(data, "read"):
                print("[budget_events.csvjson_transaction_normalizat] reading CSV from file-like")
                reader = csv.DictReader(data)
                records = list(reader)
            elif isinstance(data, str):
                print("[budget_events.csvjson_transaction_normalizat] reading CSV from string")
                reader = csv.DictReader(data.splitlines())
                records = list(reader)
            else:
                print("[budget_events.csvjson_transaction_normalizat] CSV input invalid type")
                raise ValidationError("CSV input must be a string or file-like object.")
        elif input_format == "json":
            if hasattr(data, "read"):
                print("[budget_events.csvjson_transaction_normalizat] reading JSON from file-like")
                records = json.load(data)
            elif isinstance(data, str):
                print("[budget_events.csvjson_transaction_normalizat] reading JSON from string")
                records = json.loads(data)
            elif isinstance(data, list):
                print("[budget_events.csvjson_transaction_normalizat] using JSON list directly")
                records = data
            else:
                print("[budget_events.csvjson_transaction_normalizat] JSON input invalid type")
                raise ValidationError("JSON input must be a string, list, or file-like object.")
            if isinstance(records, dict):
                print("[budget_events.csvjson_transaction_normalizat] wrapping JSON dict in list")
                records = [records]
        else:
            print(f"[budget_events.csvjson_transaction_normalizat] unknown input_format: {input_format}")
            raise ValidationError(f"Unknown input_format: {input_format}")

        transactions: List[Transaction] = []
        errors: List[str] = []
        print(f"[budget_events.csvjson_transaction_normalizat] records count: {len(records)}")
        for idx, rec in enumerate(records):
            try:
                print(f"[budget_events.csvjson_transaction_normalizat] normalizing record {idx}")
                tx = _normalize_record(rec)
                transactions.append(tx)
            except BudgetEventsError as e:
                print(f"[budget_events.csvjson_transaction_normalizat] error in record {idx}: {e}")
                errors.append(f"Record {idx}: {e}")
        print(f"[budget_events.csvjson_transaction_normalizat] returning NormalizationResult with {len(transactions)} transactions, {len(errors)} errors")
        return NormalizationResult(transactions=transactions, errors=errors)
    except BudgetEventsError as e:
        print(f"[budget_events.csvjson_transaction_normalizat] BudgetEventsError: {e}")
        raise
    except Exception as e:
        print(f"[budget_events.csvjson_transaction_normalizat] Exception: {e}")
        raise ValidationError(f"Failed to normalize transactions: {e}")


def _normalize_record(rec: Dict[str, Any]) -> Transaction:
    print(f"[budget_events.csvjson_transaction_normalizat] _normalize_record called with: {rec}")
    """Normalize a single record to Transaction schema. Raises ValidationError on error."""
    # Required fields: date, amount, currency, description
    try:
        date_val = rec.get("date") or rec.get("transaction_date")
        if not date_val:
            print("[budget_events.csvjson_transaction_normalizat] Missing required field: date")
            raise ValidationError("Missing required field: date")
        # Accept ISO string, date, or datetime
        if isinstance(date_val, (date, datetime)):
            date_str = date_val.isoformat()
        else:
            date_str = str(date_val)
            # Validate ISO format
            try:
                datetime.fromisoformat(date_str)
            except Exception:
                print(f"[budget_events.csvjson_transaction_normalizat] Invalid date format: {date_str}")
                raise ValidationError(f"Invalid date format: {date_str}")

        amount_val = rec.get("amount")
        if amount_val is None:
            print("[budget_events.csvjson_transaction_normalizat] Missing required field: amount")
            raise ValidationError("Missing required field: amount")
        try:
            amount = float(amount_val)
        except Exception:
            print(f"[budget_events.csvjson_transaction_normalizat] Invalid amount: {amount_val}")
            raise ValidationError(f"Invalid amount: {amount_val}")

        currency = validate_not_empty(str(rec.get("currency", "")).upper(), "currency")
        description = validate_not_empty(str(rec.get("description", "")), "description")
        payee = rec.get("payee") or rec.get("merchant")
        category = rec.get("category")
        tx_id = rec.get("id") or rec.get("transaction_id")
        print(f"[budget_events.csvjson_transaction_normalizat] Creating Transaction object")
        return Transaction(
            id=tx_id,
            date=date_str,
            amount=amount,
            currency=currency,
            description=description,
            payee=payee,
            category=category,
            raw=rec,
        )
    except BudgetEventsError:
        print("[budget_events.csvjson_transaction_normalizat] BudgetEventsError in _normalize_record")
        raise
    except Exception as e:
        print(f"[budget_events.csvjson_transaction_normalizat] Exception in _normalize_record: {e}")
        raise ValidationError(f"Failed to normalize record: {e}")
