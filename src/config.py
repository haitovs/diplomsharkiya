# Configuration for Event Discovery
# Core and UI Settings

from dataclasses import dataclass
from typing import Dict, List

@dataclass
class CoreConfig:
    """Core application configuration."""
    
    # App Info
    APP_TITLE = "Local Events"
    APP_SUBTITLE = "Event Discovery"
    APP_ICON = "🎟️"
    VERSION = "4.2"
    
    # Default Location (Ashgabat, Turkmenistan)
    DEFAULT_LAT = 37.9601
    DEFAULT_LON = 58.3261
    DEFAULT_ZOOM = 11
    
    # Cities in Turkmenistan
    CITIES = [
        "Ashgabat",
        "Mary", 
        "Türkmenabat",
        "Dashoguz",
        "Balkanabat",
        "Awaza",
    ]
    
    # Time Zone
    TIMEZONE = "Asia/Ashgabat"  # UTC+5
    
    # Currency
    CURRENCY = "TMT"  # Turkmen Manat
    
    # Data
    DATA_FILE = "events.json"
    CACHE_TTL = 60  # seconds
    
    # Pagination
    EVENTS_PER_PAGE = 20
    
    # Map
    MAP_TILE_PROVIDER = "cartodbpositron"  # Clean, minimal tiles
    MAP_HEIGHT = 600
    ENABLE_MARKER_CLUSTERING = True
    

@dataclass
class UIConfig:
    """UI/UX configuration and styling."""
    
    # Color Palette (Dark Theme)
    COLORS = {
        "bg_primary": "#0A0E27",
        "bg_secondary": "#141B34",
        "bg_card": "#1A2238",
        "accent_primary": "#6366F1",  # Indigo
        "accent_secondary": "#10B981",  # Emerald
        "text_primary": "#F8FAFC",
        "text_secondary": "#94A3B8",
        "text_muted": "#64748B",
        "border_subtle": "#1E293B",
        "success": "#22C55E",
        "warning": "#EAB308",
        "error": "#EF4444",
    }
    
    # Typography
    FONT_FAMILY = "'Inter', sans-serif"
    FONT_URL = "https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap"
    
    # Spacing
    PADDING = {
        "xs": "0.25rem",
        "sm": "0.5rem",
        "md": "1rem",
        "lg": "1.5rem",
        "xl": "2rem",
    }
    
    # Border Radius
    BORDER_RADIUS = {
        "sm": "6px",
        "md": "8px",
        "lg": "12px",
        "xl": "16px",
    }
    
    # Shadows
    SHADOW = "0 4px 6px -1px rgba(0, 0, 0, 0.3)"
    SHADOW_HOVER = "0 8px 16px -2px rgba(99, 102, 241, 0.2)"
    
    # Animation
    TRANSITION = "all 0.2s ease"
    HOVER_TRANSFORM = "translateY(-2px)"


# Category Configuration
CATEGORY_CONFIG = {
    "Music": {
        "icon": "🎵",
        "color": "purple",
        "description": "Concerts, performances, and musical events"
    },
    "Tech": {
        "icon": "💻",
        "color": "blue",
        "description": "Tech talks, workshops, and meetups"
    },
    "Sports": {
        "icon": "⚽",
        "color": "green",
        "description": "Sports events, games, and competitions"
    },
    "Food": {
        "icon": "🍽️",
        "color": "orange",
        "description": "Food festivals, tastings, and culinary events"
    },
    "Art": {
        "icon": "🎨",
        "color": "pink",
        "description": "Art exhibitions, galleries, and workshops"
    },
    "Market": {
        "icon": "🛍️",
        "color": "cadetblue",
        "description": "Markets, fairs, and shopping events"
    },
    "Film": {
        "icon": "🎬",
        "color": "red",
        "description": "Movie screenings and film festivals"
    },
    "Wellness": {
        "icon": "🧘",
        "color": "lightgreen",
        "description": "Yoga, meditation, and wellness activities"
    },
    "Business": {
        "icon": "💼",
        "color": "darkblue",
        "description": "Business conferences and networking"
    },
    "Science": {
        "icon": "🔬",
        "color": "purple",
        "description": "Science fairs, lectures, and exhibitions"
    },
    "Kids": {
        "icon": "👶",
        "color": "beige",
        "description": "Children's activities and family events"
    },
    "Travel": {
        "icon": "✈️",
        "color": "lightblue",
        "description": "Travel expos and tourism events"
    },
    "Community": {
        "icon": "👥",
        "color": "gray",
        "description": "Community gatherings and social events"
    },
}


# Filter Configuration
FILTER_CONFIG = {
    "date_presets": ["All", "Today", "This Week", "This Month"],
    "sort_options": [
        "Date (Soonest)",
        "Price (Low to High)",
        "Price (High to Low)",
        "Popularity"
    ],
    "price_range": {
        "min": 0,
        "max": 200,
        "default_max": 200
    }
}


# Feature Flags
FEATURES = {
    "enable_search": True,
    "enable_save": True,
    "enable_map": True,
    "enable_sorting": True,
    "enable_detail_view": True,
    "enable_toast_notifications": True,
}


# Admin Configuration (for future admin panel)
ADMIN_CONFIG = {
    "session_timeout": 1800,  # 30 minutes
    "password_min_length": 8,
    "require_email": True,
}


# Export all configs
__all__ = [
    'CoreConfig',
    'UIConfig',
    'CATEGORY_CONFIG',
    'FILTER_CONFIG',
    'FEATURES',
    'ADMIN_CONFIG'
]
