import os
from datetime import date
from typing import List, Dict

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from models import Base, Transaction, Goal


DB_FILE = os.path.join(os.path.dirname(__file__), "dados.db")
# Allow overriding the database URL for tests or advanced usage via STORAGE_URL env var.
DB_URL = os.environ.get("STORAGE_URL")
if DB_URL:
    ENGINE = create_engine(DB_URL, connect_args={"check_same_thread": False})
else:
    ENGINE = create_engine(f"sqlite:///{DB_FILE}", connect_args={"check_same_thread": False})
Session = sessionmaker(bind=ENGINE)


def init_db():
    """Create SQLite database and tables if they don't exist."""
    Base.metadata.create_all(ENGINE)


def add_transaction(tx_date: date, tx_type: str, category: str, amount: float, note: str = "") -> int:
    session = Session()
    tx = Transaction(date=tx_date, type=tx_type, category=category, amount=amount, note=note)
    session.add(tx)
    session.commit()
    tx_id = tx.id
    session.close()
    return tx_id


def list_transactions() -> List[Dict]:
    session = Session()
    rows = session.query(Transaction).order_by(Transaction.date.desc()).all()
    result = []
    for r in rows:
        result.append({
            "id": r.id,
            "date": r.date,
            "type": r.type,
            "category": r.category,
            "amount": r.amount,
            "note": r.note,
        })
    session.close()
    return result


def add_goal(name: str, target_amount: float, due_date: date = None) -> int:
    session = Session()
    g = Goal(name=name, target_amount=target_amount, current_amount=0.0, due_date=due_date)
    session.add(g)
    session.commit()
    gid = g.id
    session.close()
    return gid


def get_summary() -> Dict[str, float]:
    session = Session()
    income = session.query(Transaction).filter(Transaction.type == "income").all()
    expense = session.query(Transaction).filter(Transaction.type == "expense").all()
    total_income = sum([i.amount for i in income])
    total_expense = sum([e.amount for e in expense])
    session.close()
    return {"income": total_income, "expense": total_expense, "balance": total_income - total_expense}
