"""
Sharkiya Event Discovery - Configuration
Default location: Ashgabat, Turkmenistan
"""

from dataclasses import dataclass, field
from typing import Dict, List, Tuple, Optional
from datetime import timedelta


@dataclass
class MapConfig:
    """Map configuration settings."""
    default_lat: float = 37.9601
    default_lon: float = 58.3261
    default_zoom: int = 12
    min_zoom: int = 8
    max_zoom: int = 18
    tile_layer: str = "OpenStreetMap"


@dataclass
class Config:
    """Application configuration."""
    
    # App Info
    APP_TITLE: str = "Local Events"
    APP_SUBTITLE: str = "Discover and plan events in Turkmenistan"
    APP_ICON: str = "🎟️"
    APP_VERSION: str = "2.0.0"
    
    # Default Location: Ashgabat, Turkmenistan
    DEFAULT_LAT: float = 37.9601
    DEFAULT_LON: float = 58.3261
    DEFAULT_ZOOM: int = 12
    DEFAULT_RADIUS_KM: float = 0.0
    
    # Map Settings
    map: MapConfig = field(default_factory=MapConfig)
    
    # Cities in Turkmenistan
    CITIES: List[str] = field(default_factory=lambda: [
        "Ashgabat",
        "Mary",
        "Türkmenabat",
        "Dashoguz",
        "Balkanabat",
        "Awaza",
    ])
    
    # City Coordinates
    CITY_COORDS: Dict[str, Tuple[float, float]] = field(default_factory=lambda: {
        "Ashgabat": (37.9601, 58.3261),
        "Mary": (37.6005, 61.8302),
        "Türkmenabat": (39.0733, 63.5786),
        "Dashoguz": (41.8387, 59.9650),
        "Balkanabat": (39.5104, 54.3672),
        "Awaza": (40.0224, 52.9693),
    })
    
    # Event Categories with icons and colors
    CATEGORIES: Dict[str, Dict[str, str]] = field(default_factory=lambda: {
        "Music": {"icon": "🎵", "color": "#8B5CF6", "fa_icon": "music"},
        "Tech": {"icon": "💻", "color": "#3B82F6", "fa_icon": "laptop"},
        "Sports": {"icon": "⚽", "color": "#22C55E", "fa_icon": "futbol"},
        "Food": {"icon": "🍽️", "color": "#F97316", "fa_icon": "utensils"},
        "Art": {"icon": "🎨", "color": "#EC4899", "fa_icon": "palette"},
        "Market": {"icon": "🛍️", "color": "#14B8A6", "fa_icon": "shopping-bag"},
        "Film": {"icon": "🎬", "color": "#DC2626", "fa_icon": "film"},
        "Wellness": {"icon": "🧘", "color": "#84CC16", "fa_icon": "spa"},
        "Business": {"icon": "💼", "color": "#1E40AF", "fa_icon": "briefcase"},
        "Science": {"icon": "🔬", "color": "#6366F1", "fa_icon": "flask"},
        "Kids": {"icon": "👶", "color": "#FBBF24", "fa_icon": "child"},
        "Travel": {"icon": "✈️", "color": "#06B6D4", "fa_icon": "plane"},
        "Community": {"icon": "👥", "color": "#6B7280", "fa_icon": "users"},
    })
    
    # Date Filter Presets
    DATE_PRESETS: List[str] = field(default_factory=lambda: [
        "All",
        "Today",
        "Tomorrow",
        "This Weekend",
        "This Week",
        "This Month",
    ])
    
    # Sort Options
    SORT_OPTIONS: List[str] = field(default_factory=lambda: [
        "Relevance",
        "Date (Soonest)",
        "Price (Low to High)",
        "Price (High to Low)",
        "Popularity",
    ])
    
    # Price Ranges (min, max) - None means no limit
    PRICE_RANGES: List[Tuple[str, Optional[int], Optional[int]]] = field(default_factory=lambda: [
        ("All Prices", None, None),
        ("Free", 0, 0),
        ("Under 50 TMT", 1, 50),
        ("50-100 TMT", 50, 100),
        ("100-200 TMT", 100, 200),
        ("200+ TMT", 200, None),
    ])
    
    # Time of Day Filters
    TIME_OF_DAY: Dict[str, Tuple[int, int]] = field(default_factory=lambda: {
        "Morning (6-12)": (6, 12),
        "Afternoon (12-17)": (12, 17),
        "Evening (17-22)": (17, 22),
        "Night (22-6)": (22, 6),
    })
    
    # Admin Settings
    ADMIN_SESSION_TIMEOUT: int = 1800  # 30 minutes in seconds
    ADMIN_USERNAME: str = "admin"
    ADMIN_PASSWORD_HASH: str = ""  # Will be set during setup
    
    # Pagination
    EVENTS_PER_PAGE: int = 20
    
    # Data Paths
    DATA_DIR: str = "data"
    EVENTS_FILE: str = "events.json"
    DB_FILE: str = "events.db"
    
    # UI Theme Colors
    THEME: Dict[str, str] = field(default_factory=lambda: {
        "primary": "#6366F1",
        "primary_dark": "#4F46E5",
        "secondary": "#10B981",
        "accent": "#F59E0B",
        "background": "#F8FAFC",
        "surface": "#FFFFFF",
        "text_primary": "#1E293B",
        "text_secondary": "#64748B",
        "border": "#E2E8F0",
        "success": "#22C55E",
        "warning": "#EAB308",
        "error": "#EF4444",
    })
    
    def get_category_color(self, category: str) -> str:
        """Get color for a category."""
        return self.CATEGORIES.get(category, {}).get("color", "#6B7280")
    
    def get_category_icon(self, category: str) -> str:
        """Get emoji icon for a category."""
        return self.CATEGORIES.get(category, {}).get("icon", "📌")
    
    def get_category_fa_icon(self, category: str) -> str:
        """Get Font Awesome icon for a category."""
        return self.CATEGORIES.get(category, {}).get("fa_icon", "calendar")


# Global config instance
config = Config()
