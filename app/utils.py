"""
Sharkiya Event Discovery - Utility Functions
Helper functions for distance calculation, date filtering, etc.
"""

import math
from datetime import datetime, timedelta
from typing import Optional, Tuple, List
import pandas as pd


def haversine_km(lat1: float, lon1: float, lat2: float, lon2: float) -> float:
    """
    Calculate the great-circle distance between two points on Earth.
    
    Args:
        lat1, lon1: Coordinates of point 1
        lat2, lon2: Coordinates of point 2
        
    Returns:
        Distance in kilometers
    """
    R = 6371.0  # Earth's radius in km
    
    dlat = math.radians(lat2 - lat1)
    dlon = math.radians(lon2 - lon1)
    
    a = (math.sin(dlat / 2) ** 2 + 
         math.cos(math.radians(lat1)) * 
         math.cos(math.radians(lat2)) * 
         math.sin(dlon / 2) ** 2)
    
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    
    return R * c


def filter_by_distance(
    df: pd.DataFrame,
    center_lat: float,
    center_lon: float,
    radius_km: float
) -> pd.DataFrame:
    """
    Filter events by distance from a center point.
    
    Args:
        df: DataFrame with events
        center_lat, center_lon: Center point coordinates
        radius_km: Maximum distance in km (0 means no filtering)
        
    Returns:
        Filtered DataFrame with distance_km column added
    """
    if radius_km <= 0 or df.empty:
        return df
    
    # Only consider events with valid coordinates
    has_coords = df["lat"].notna() & df["lon"].notna()
    candidates = df[has_coords].copy()
    
    if candidates.empty:
        return candidates
    
    # Calculate distances
    distances = candidates.apply(
        lambda r: haversine_km(center_lat, center_lon, float(r["lat"]), float(r["lon"])),
        axis=1
    )
    
    # Filter by radius
    within_radius = distances <= radius_km
    result = candidates[within_radius].copy()
    result["distance_km"] = distances[within_radius]
    
    return result.sort_values("distance_km")


def get_date_range(preset: str) -> Tuple[Optional[datetime], Optional[datetime]]:
    """
    Get date range from a preset string.
    
    Args:
        preset: One of "All", "Today", "Tomorrow", "This Weekend", "This Week", "This Month"
        
    Returns:
        Tuple of (start_date, end_date) or (None, None) for "All"
    """
    if not preset or preset == "All":
        return None, None
    
    today = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
    
    if preset == "Today":
        return today, today + timedelta(days=1)
    
    if preset == "Tomorrow":
        tomorrow = today + timedelta(days=1)
        return tomorrow, tomorrow + timedelta(days=1)
    
    if preset == "This Weekend":
        weekday = today.weekday()
        # Find next Saturday (5) and Sunday (6)
        days_until_saturday = (5 - weekday) % 7
        if days_until_saturday == 0 and weekday != 5:
            days_until_saturday = 7
        saturday = today + timedelta(days=days_until_saturday)
        sunday = saturday + timedelta(days=1)
        return saturday, sunday + timedelta(days=1)
    
    if preset == "This Week":
        # Current week (Monday to Sunday)
        start_of_week = today - timedelta(days=today.weekday())
        end_of_week = start_of_week + timedelta(days=7)
        return start_of_week, end_of_week
    
    if preset == "This Month":
        start_of_month = today.replace(day=1)
        # Get first day of next month
        if today.month == 12:
            end_of_month = today.replace(year=today.year + 1, month=1, day=1)
        else:
            end_of_month = today.replace(month=today.month + 1, day=1)
        return start_of_month, end_of_month
    
    return None, None


def filter_by_date_preset(df: pd.DataFrame, preset: str) -> pd.DataFrame:
    """
    Filter events by date preset.
    
    Args:
        df: DataFrame with events (must have date_start column)
        preset: Date preset string
        
    Returns:
        Filtered DataFrame
    """
    if df.empty or not preset or preset == "All":
        return df
    
    start_date, end_date = get_date_range(preset)
    
    if start_date is None:
        return df
    
    # Ensure date_start is datetime
    if not pd.api.types.is_datetime64_any_dtype(df["date_start"]):
        df = df.copy()
        df["date_start"] = pd.to_datetime(df["date_start"])
    
    mask = (df["date_start"] >= start_date)
    if end_date:
        mask &= (df["date_start"] < end_date)
    
    return df[mask]


def filter_by_time_of_day(df: pd.DataFrame, time_range: Tuple[int, int]) -> pd.DataFrame:
    """
    Filter events by time of day.
    
    Args:
        df: DataFrame with events
        time_range: Tuple of (start_hour, end_hour)
        
    Returns:
        Filtered DataFrame
    """
    if df.empty:
        return df
    
    start_hour, end_hour = time_range
    
    # Handle overnight ranges (e.g., 22-6)
    if start_hour > end_hour:
        mask = (df["date_start"].dt.hour >= start_hour) | (df["date_start"].dt.hour < end_hour)
    else:
        mask = (df["date_start"].dt.hour >= start_hour) & (df["date_start"].dt.hour < end_hour)
    
    return df[mask]


def apply_sort(df: pd.DataFrame, sort_by: str) -> pd.DataFrame:
    """
    Sort events by specified criteria.
    
    Args:
        df: DataFrame with events
        sort_by: Sort option string
        
    Returns:
        Sorted DataFrame
    """
    if df.empty:
        return df
    
    if sort_by == "Date (Soonest)":
        return df.sort_values("date_start", ascending=True)
    
    if sort_by == "Price (Low to High)":
        return df.sort_values("price", ascending=True)
    
    if sort_by == "Price (High to Low)":
        return df.sort_values("price", ascending=False)
    
    if sort_by == "Popularity":
        return df.sort_values("popularity", ascending=False)
    
    # Default: Relevance (by popularity then date)
    return df.sort_values(["popularity", "date_start"], ascending=[False, True])


def format_price(price: float) -> str:
    """Format price for display."""
    if price == 0:
        return "Free"
    return f"{int(price)} TMT"


def format_date(dt: datetime) -> str:
    """Format datetime for display."""
    return dt.strftime("%b %d, %Y")


def format_time(dt: datetime) -> str:
    """Format time for display."""
    return dt.strftime("%I:%M %p")


def format_datetime(dt: datetime) -> str:
    """Format full datetime for display."""
    return dt.strftime("%b %d, %Y • %I:%M %p")


def format_date_range(start: datetime, end: datetime) -> str:
    """Format date range for display."""
    if start.date() == end.date():
        return f"{format_date(start)} • {format_time(start)} - {format_time(end)}"
    return f"{format_datetime(start)} - {format_datetime(end)}"


def generate_event_id() -> str:
    """Generate a unique event ID."""
    import uuid
    return f"evt_{uuid.uuid4().hex[:12]}"


def search_events(df: pd.DataFrame, query: str) -> pd.DataFrame:
    """
    Search events by title, venue, or description.
    
    Args:
        df: DataFrame with events
        query: Search query string
        
    Returns:
        Filtered DataFrame matching the query
    """
    if df.empty or not query or not query.strip():
        return df
    
    pattern = query.strip().lower()
    
    mask = (
        df["title"].str.lower().str.contains(pattern, na=False) |
        df["venue"].str.lower().str.contains(pattern, na=False) |
        df["description"].str.lower().str.contains(pattern, na=False)
    )
    
    return df[mask]


def get_events_stats(df: pd.DataFrame) -> dict:
    """
    Get statistics about events.
    
    Args:
        df: DataFrame with events
        
    Returns:
        Dictionary with statistics
    """
    if df.empty:
        return {
            "total": 0,
            "cities": 0,
            "categories": 0,
            "free_events": 0,
            "avg_price": 0,
            "upcoming_this_week": 0,
        }
    
    today = datetime.now()
    week_from_now = today + timedelta(days=7)
    
    upcoming_mask = (df["date_start"] >= today) & (df["date_start"] < week_from_now)
    
    return {
        "total": len(df),
        "cities": df["city"].nunique(),
        "categories": df["category"].nunique(),
        "free_events": len(df[df["price"] == 0]),
        "avg_price": round(df["price"].mean(), 2) if len(df) > 0 else 0,
        "upcoming_this_week": len(df[upcoming_mask]),
    }
