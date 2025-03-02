from fastapi import FastAPI
import sqlite3
import time

app = FastAPI()

# Lokale SQLite-Datenbank einrichten
DB_FILE = "test.db"

def get_db_connection():
    conn = sqlite3.connect(DB_FILE)
    conn.row_factory = sqlite3.Row
    return conn

# Initialisierung der Test-Datenbank
def init_db():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS test_table (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            value TEXT
        )
    """)
    conn.commit()
    conn.close()

init_db()  # Datenbank beim Start initialisieren

# API-Endpunkte

@app.get("/get_data")
def get_data():
    """Simuliert eine Datenbankabfrage."""
    start_time = time.time()
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM test_table LIMIT 10")
    data = cursor.fetchall()
    conn.close()
    return {"response_time": time.time() - start_time, "data": [dict(row) for row in data]}

@app.post("/update_data")
def update_data():
    """Simuliert eine Schreiboperation in der Datenbank."""
    start_time = time.time()
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO test_table (name, value) VALUES (?, ?)", ("TestName", "TestValue"))
    conn.commit()
    conn.close()
    return {"response_time": time.time() - start_time, "status": "inserted"}
