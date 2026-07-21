"""SQLite 데이터베이스 관리"""
import sqlite3
import json
from .config import DATABASE_PATH


def get_db():
    conn = sqlite3.connect(str(DATABASE_PATH))
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    """테이블 생성 (앱 시작 시 1회)"""
    conn = get_db()
    conn.executescript("""
        CREATE TABLE IF NOT EXISTS stores (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            address TEXT NOT NULL,
            lat REAL NOT NULL,
            lng REAL NOT NULL,
            category TEXT NOT NULL,
            menus TEXT DEFAULT '[]',
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );

        CREATE TABLE IF NOT EXISTS contents (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            store_id INTEGER,
            user_input TEXT NOT NULL,
            instagram TEXT,
            banner TEXT,
            hashtags TEXT,
            market_info TEXT,
            festival_info TEXT,
            model_used TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (store_id) REFERENCES stores(id)
        );
    """)
    conn.commit()
    conn.close()
