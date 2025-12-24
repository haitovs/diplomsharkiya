"""
Sharkiya Event Discovery - Database Management
SQLite database and JSON data handling
"""

import json
import sqlite3
import pathlib
from datetime import datetime
from typing import List, Optional, Dict, Any
import pandas as pd

from .config import config
from .models import Event, EventCreate, EventUpdate, ImportResult


class Database:
    """Database manager for events."""
    
    def __init__(self, db_path: Optional[str] = None):
        self.db_path = db_path or str(pathlib.Path(__file__).parent.parent / "data" / config.DB_FILE)
        self._ensure_tables()
    
    def _get_connection(self) -> sqlite3.Connection:
        """Get database connection."""
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        return conn
    
    def _ensure_tables(self):
        """Create tables if they don't exist."""
        conn = self._get_connection()
        cursor = conn.cursor()
        
        # Events table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS events (
                id TEXT PRIMARY KEY,
                title TEXT NOT NULL,
                category TEXT NOT NULL,
                city TEXT NOT NULL,
                venue TEXT NOT NULL,
                date_start DATETIME NOT NULL,
                date_end DATETIME NOT NULL,
                price REAL DEFAULT 0,
                popularity INTEGER DEFAULT 50,
                lat REAL,
                lon REAL,
                image TEXT,
                description TEXT,
                created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                updated_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                is_active BOOLEAN DEFAULT 1
            )
        """)
        
        # Admins table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS admins (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT UNIQUE NOT NULL,
                password_hash TEXT NOT NULL,
                email TEXT,
                created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                last_login DATETIME
            )
        """)
        
        # Saved events table (per session)
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS saved_events (
                session_id TEXT,
                event_id TEXT,
                saved_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                PRIMARY KEY (session_id, event_id),
                FOREIGN KEY (event_id) REFERENCES events(id)
            )
        """)
        
        # Analytics table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS analytics (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                event_id TEXT,
                action TEXT,
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        """)
        
        conn.commit()
        conn.close()
    
    def get_all_events(self, include_inactive: bool = False) -> pd.DataFrame:
        """Get all events as DataFrame."""
        conn = self._get_connection()
        
        query = "SELECT * FROM events"
        if not include_inactive:
            query += " WHERE is_active = 1"
        query += " ORDER BY date_start ASC"
        
        df = pd.read_sql_query(query, conn)
        conn.close()
        
        # Convert date columns
        for col in ["date_start", "date_end", "created_at", "updated_at"]:
            if col in df.columns:
                df[col] = pd.to_datetime(df[col])
        
        return df
    
    def get_event(self, event_id: str) -> Optional[Dict]:
        """Get a single event by ID."""
        conn = self._get_connection()
        cursor = conn.cursor()
        
        cursor.execute("SELECT * FROM events WHERE id = ?", (event_id,))
        row = cursor.fetchone()
        conn.close()
        
        if row:
            return dict(row)
        return None
    
    def create_event(self, event: EventCreate, event_id: Optional[str] = None) -> str:
        """Create a new event."""
        from .utils import generate_event_id
        
        conn = self._get_connection()
        cursor = conn.cursor()
        
        new_id = event_id or generate_event_id()
        now = datetime.now().isoformat()
        
        cursor.execute("""
            INSERT INTO events (
                id, title, category, city, venue, date_start, date_end,
                price, popularity, lat, lon, image, description,
                created_at, updated_at, is_active
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, 1)
        """, (
            new_id,
            event.title,
            event.category,
            event.city,
            event.venue,
            event.date_start.isoformat(),
            event.date_end.isoformat(),
            event.price,
            event.popularity,
            event.lat,
            event.lon,
            event.image,
            event.description,
            now,
            now,
        ))
        
        conn.commit()
        conn.close()
        
        return new_id
    
    def update_event(self, event_id: str, event: EventUpdate) -> bool:
        """Update an existing event."""
        conn = self._get_connection()
        cursor = conn.cursor()
        
        # Build update query dynamically based on provided fields
        updates = []
        values = []
        
        update_data = event.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            if value is not None:
                if isinstance(value, datetime):
                    value = value.isoformat()
                updates.append(f"{field} = ?")
                values.append(value)
        
        if not updates:
            return False
        
        updates.append("updated_at = ?")
        values.append(datetime.now().isoformat())
        values.append(event_id)
        
        query = f"UPDATE events SET {', '.join(updates)} WHERE id = ?"
        cursor.execute(query, values)
        
        success = cursor.rowcount > 0
        conn.commit()
        conn.close()
        
        return success
    
    def delete_event(self, event_id: str, soft: bool = True) -> bool:
        """Delete an event (soft delete by default)."""
        conn = self._get_connection()
        cursor = conn.cursor()
        
        if soft:
            cursor.execute(
                "UPDATE events SET is_active = 0, updated_at = ? WHERE id = ?",
                (datetime.now().isoformat(), event_id)
            )
        else:
            cursor.execute("DELETE FROM events WHERE id = ?", (event_id,))
        
        success = cursor.rowcount > 0
        conn.commit()
        conn.close()
        
        return success
    
    def restore_event(self, event_id: str) -> bool:
        """Restore a soft-deleted event."""
        conn = self._get_connection()
        cursor = conn.cursor()
        
        cursor.execute(
            "UPDATE events SET is_active = 1, updated_at = ? WHERE id = ?",
            (datetime.now().isoformat(), event_id)
        )
        
        success = cursor.rowcount > 0
        conn.commit()
        conn.close()
        
        return success
    
    def import_from_json(self, json_path: str) -> ImportResult:
        """Import events from JSON file."""
        result = ImportResult()
        
        try:
            with open(json_path, "r", encoding="utf-8") as f:
                events = json.load(f)
        except (json.JSONDecodeError, FileNotFoundError) as e:
            result.errors.append(f"Failed to read JSON file: {e}")
            return result
        
        if not isinstance(events, list):
            result.errors.append("JSON must contain an array of events")
            return result
        
        result.total = len(events)
        
        for event_data in events:
            try:
                # Convert date strings to datetime
                for date_field in ["date_start", "date_end"]:
                    if date_field in event_data and isinstance(event_data[date_field], str):
                        event_data[date_field] = datetime.fromisoformat(event_data[date_field])
                
                event_id = event_data.pop("id", None)
                event = EventCreate(**event_data)
                self.create_event(event, event_id)
                result.success += 1
            except Exception as e:
                result.failed += 1
                result.errors.append(f"Event '{event_data.get('title', 'unknown')}': {e}")
        
        return result
    
    def export_to_json(self) -> str:
        """Export all events to JSON string."""
        df = self.get_all_events(include_inactive=True)
        
        # Convert datetime columns to strings
        for col in ["date_start", "date_end", "created_at", "updated_at"]:
            if col in df.columns:
                df[col] = df[col].dt.strftime("%Y-%m-%dT%H:%M:%S")
        
        return df.to_json(orient="records", indent=2)
    
    def get_event_count(self) -> int:
        """Get total number of active events."""
        conn = self._get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT COUNT(*) FROM events WHERE is_active = 1")
        count = cursor.fetchone()[0]
        conn.close()
        return count
    
    def log_analytics(self, event_id: str, action: str):
        """Log an analytics event."""
        conn = self._get_connection()
        cursor = conn.cursor()
        
        cursor.execute(
            "INSERT INTO analytics (event_id, action) VALUES (?, ?)",
            (event_id, action)
        )
        
        conn.commit()
        conn.close()


def load_events_from_json(path: pathlib.Path) -> pd.DataFrame:
    """
    Load events from JSON file (legacy function for compatibility).
    
    Args:
        path: Path to events.json file
        
    Returns:
        DataFrame with events
    """
    expected_columns = [
        "id", "title", "category", "city", "venue",
        "date_start", "date_end", "price", "popularity",
        "lat", "lon", "image", "description"
    ]
    
    if not path.exists():
        return pd.DataFrame(columns=expected_columns)
    
    try:
        with open(path, "r", encoding="utf-8") as f:
            raw = json.load(f)
    except (json.JSONDecodeError, OSError):
        return pd.DataFrame(columns=expected_columns)
    
    if not isinstance(raw, list):
        return pd.DataFrame(columns=expected_columns)
    
    df = pd.DataFrame(raw)
    
    # Ensure all expected columns exist
    for col in expected_columns:
        if col not in df.columns:
            df[col] = None
    
    df = df[expected_columns].copy()
    
    if df.empty:
        return df
    
    # Type conversions
    text_cols = ["id", "title", "category", "city", "venue", "image", "description"]
    for col in text_cols:
        df[col] = df[col].fillna("").astype(str)
    
    numeric_cols = ["price", "popularity"]
    for col in numeric_cols:
        df[col] = pd.to_numeric(df[col], errors="coerce").fillna(0)
    
    float_cols = ["lat", "lon"]
    for col in float_cols:
        df[col] = pd.to_numeric(df[col], errors="coerce")
    
    date_cols = ["date_start", "date_end"]
    for col in date_cols:
        df[col] = pd.to_datetime(df[col], errors="coerce")
    
    # Remove rows with invalid dates
    df = df.dropna(subset=date_cols)
    
    return df.reset_index(drop=True)


# Create default database instance
db = Database()
