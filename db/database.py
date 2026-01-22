import sqlite3
from pathlib import Path

DB_PATH = Path(__file__).resolve().parent / "bookings.db"

def get_connection():
    return sqlite3.connect(DB_PATH, check_same_thread=False)

def create_table():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS bookings (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            phone TEXT,
            email TEXT,
            test TEXT,
            test_center TEXT,
            date TEXT,
            time TEXT
        )
    """)

    conn.commit()
    conn.close()

def insert_booking(data):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO bookings (name, phone, email, test, test_center, date, time)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    """, (
        data["name"],
        data["phone"],
        data["email"],
        data["test"],
        data["test_center"],
        data["date"],
        data["time"]
    ))

    conn.commit()
    conn.close()

def fetch_all_bookings():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT id, name, phone, email, test, test_center, date, time
        FROM bookings
    """)
    rows = cursor.fetchall()

    conn.close()
    return rows

def count_bookings_for_slot(test, test_center, date, time):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT COUNT(*)
        FROM bookings
        WHERE test = ?
          AND test_center = ?
          AND date = ?
          AND time = ?
    """, (test, test_center, date, time))

    count = cursor.fetchone()[0]
    conn.close()
    return count
