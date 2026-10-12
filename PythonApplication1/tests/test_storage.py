import os
import sys
from datetime import date
import importlib

# Ensure the package directory is on sys.path so 'import storage' finds PythonApplication1/storage.py
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))


def setup_module(module):
    # Point storage to an in-memory SQLite for tests
    os.environ["STORAGE_URL"] = "sqlite:///:memory:"


def test_transactions_and_summary():
    # Import storage after setting env var
    import storage
    importlib.reload(storage)

    storage.init_db()

    # Add income and expense
    today = date.today()
    storage.add_transaction(today, "income", "Salário", 2000.0, "Recebimento")
    storage.add_transaction(today, "expense", "Alimentação", 150.5, "Supermercado")

    txs = storage.list_transactions()
    assert len(txs) == 2

    summary = storage.get_summary()
    assert summary["income"] == 2000.0
    assert summary["expense"] == 150.5
    assert abs(summary["balance"] - 1849.5) < 1e-6


def test_goals():
    import storage
    importlib.reload(storage)
    storage.init_db()

    gid = storage.add_goal("Viagem", 3000.0, None)
    assert isinstance(gid, int)
