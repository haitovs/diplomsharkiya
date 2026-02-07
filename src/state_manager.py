"""
State Management Module for Sharkiya Event Discovery
Senior Developer Best Practices Implementation
"""

from dataclasses import dataclass, field
from typing import Set, List, Optional, Dict, Any
from datetime import datetime
import streamlit as st


@dataclass
class FilterState:
    """Manages all filter-related state."""
    city: str = "All Cities"
    date_preset: str = "All"
    categories: List[str] = field(default_factory=list)
    max_price: int = 200
    search_query: str = ""
    sort_by: str = "Date (Soonest)"
    
    def reset(self):
        """Reset all filters to default values."""
        self.city = "All Cities"
        self.date_preset = "All"
        self.categories = []
        self.max_price = 200
        self.search_query = ""
        self.sort_by = "Date (Soonest)"


@dataclass
class MapState:
    """Manages map-specific state."""
    center: List[float] = field(default_factory=lambda: [37.9601, 58.3261])
    zoom: int = 11
    last_clicked: Optional[Dict[str, Any]] = None
    
    def update_from_interaction(self, map_data: Optional[Dict[str, Any]]):
        """Update map state from st_folium interaction."""
        if not map_data:
            return
            
        if map_data.get("center"):
            self.center = [
                map_data["center"]["lat"],
                map_data["center"]["lng"]
            ]
        
        if map_data.get("zoom"):
            self.zoom = map_data["zoom"]
        
        if map_data.get("last_clicked"):
            self.last_clicked = map_data["last_clicked"]


@dataclass
class UIState:
    """Manages UI-specific state."""
    active_tab: int = 0  # 0=Events, 1=Map, 2=Saved
    saved_events: Set[str] = field(default_factory=set)
    detail_event_id: Optional[str] = None
    
    def toggle_save(self, event_id: str) -> bool:
        """Toggle save state for an event. Returns True if now saved."""
        if event_id in self.saved_events:
            self.saved_events.discard(event_id)
            return False
        else:
            self.saved_events.add(event_id)
            return True
    
    def is_saved(self, event_id: str) -> bool:
        """Check if event is saved."""
        return event_id in self.saved_events


class AppStateManager:
    """
    Centralized state management for the application.
    Implements singleton pattern for consistency across reruns.
    """
    
    _instance = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._initialized = False
        return cls._instance
    
    def __init__(self):
        if self._initialized:
            return
        
        self.filters = FilterState()
        self.map = MapState()
        self.ui = UIState()
        self._initialized = True
    
    @classmethod
    def get_instance(cls) -> 'AppStateManager':
        """Get or create the singleton instance."""
        return cls()
    
    def sync_to_session_state(self):
        """Sync state to Streamlit session_state for persistence."""
        if "app_state" not in st.session_state:
            st.session_state.app_state = {
                "filters": self.filters,
                "map": self.map,
                "ui": self.ui
            }
        else:
            st.session_state.app_state["filters"] = self.filters
            st.session_state.app_state["map"] = self.map
            st.session_state.app_state["ui"] = self.ui
    
    def load_from_session_state(self):
        """Load state from Streamlit session_state."""
        if "app_state" in st.session_state:
            self.filters = st.session_state.app_state.get("filters", FilterState())
            self.map = st.session_state.app_state.get("map", MapState())
            self.ui = st.session_state.app_state.get("ui", UIState())
    
    def reset_filters(self):
        """Reset all filters to default."""
        self.filters.reset()
        self.sync_to_session_state()


# Convenience function for accessing state
def get_state() -> AppStateManager:
    """Get the global state manager instance."""
    if "state_manager" not in st.session_state:
        st.session_state.state_manager = AppStateManager.get_instance()
        st.session_state.state_manager.load_from_session_state()
    return st.session_state.state_manager
