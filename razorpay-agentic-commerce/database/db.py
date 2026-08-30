"""
SQLite connection + initialization helpers for the Agentic Commerce Platform.
"""
import sqlite3
import os
from pathlib import Path

DB_DIR = Path(__file__).resolve().parent
SCHEMA_PATH = DB_DIR / "schema.sql"


_env_path = os.environ.get("RZP_DB_PATH")
DB_PATH = Path(_env_path).resolve() if _env_path else DB_DIR / "agentic_commerce.db"


def get_connection() -> sqlite3.Connection:
    try:
        # Make sure the target directory actually exists before connecting.
        DB_PATH.parent.mkdir(parents=True, exist_ok=True)
        conn = sqlite3.connect(str(DB_PATH), check_same_thread=False)
    except sqlite3.OperationalError as e:
        raise sqlite3.OperationalError(
            f"Could not open/create the database file at: {DB_PATH}\n"
            "This usually happens when the project folder is inside a OneDrive-synced "
            "or permission-restricted Windows path. Fix it by either:\n"
            "  1) Moving the whole project folder to a plain local path, e.g. C:\\dev\\razorpay-agentic-commerce, or\n"
            "  2) Setting an environment variable to store the DB elsewhere, e.g.:\n"
            '     $env:RZP_DB_PATH="C:\\rzp-data\\agentic_commerce.db"\n'
            f"Original error: {e}"
        ) from e
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON")
    return conn


def init_db(reset: bool = False):
    """Create tables (and optionally wipe the DB first)."""
    if reset and DB_PATH.exists():
        os.remove(DB_PATH)

    conn = get_connection()
    with open(SCHEMA_PATH, "r") as f:
        conn.executescript(f.read())
    conn.commit()

    # Seed only if empty
    cur = conn.execute("SELECT COUNT(*) AS c FROM users")
    if cur.fetchone()["c"] == 0:
        _seed(conn)

    conn.close()


def _seed(conn: sqlite3.Connection):
    conn.execute(
        "INSERT INTO users (name, upi_id, bank_account, spend_limit, passkey_verified) "
        "VALUES (?, ?, ?, ?, ?)",
        ("Aditi Rao", "aditi.rao@upi", "HDFC-XXXX-4521", 50000, 0),
    )

    merchants = [
        # name, category, rating, location, base_price(per-unit), syndicate_partner_of
        ("PaperMart Wholesale", "stationery", 4.6, "Bengaluru", 480, None),
        ("OfficeDepot India", "stationery", 4.3, "Bengaluru", 510, None),
        ("PrintSource Traders", "stationery", 4.8, "Bengaluru", 495, None),
        ("Bulk Papers Co.", "stationery", 4.1, "Bengaluru", 470, None),
        ("QuickShip Logistics", "logistics", 4.7, "Bengaluru", 3000, "stationery"),
        ("GreenDesk Furnishing", "furniture", 4.5, "Bengaluru", 450, None),
        ("ErgoWorks Interiors", "furniture", 4.4, "Bengaluru", 520, None),
        ("UrbanLeaf Plants", "decor", 4.6, "Bengaluru", 5000, "furniture"),
    ]
    conn.executemany(
        "INSERT INTO merchants (name, category, rating, location, base_price, syndicate_partner_of) "
        "VALUES (?, ?, ?, ?, ?, ?)",
        merchants,
    )
    conn.commit()


if __name__ == "__main__":
    init_db(reset=True)
    print(f"Initialized database at {DB_PATH}")