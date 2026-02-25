"""
Event Discovery - UI Components
Reusable UI components for event cards, filters, etc.
"""

import streamlit as st
from datetime import datetime
from typing import Optional, Callable, Set
import pandas as pd

import sys
import pathlib
sys.path.insert(0, str(pathlib.Path(__file__).parent.parent))

from app.config import config
from app.utils import format_price, format_date, format_time, format_date_range


def render_event_card(
    row: pd.Series,
    key_prefix: str,
    saved_ids: Set[str],
    on_save: Optional[Callable[[str, str], None]] = None,
    on_details: Optional[Callable[[str], None]] = None,
    on_share: Optional[Callable[[str], None]] = None,
    compact: bool = False
):
    """
    Render an event card.
    
    Args:
        row: Event data as pandas Series
        key_prefix: Unique prefix for button keys
        saved_ids: Set of saved event IDs
        on_save: Callback when save button clicked
        on_details: Callback when details button clicked
        on_share: Callback when share button clicked
        compact: If True, render a more compact card
    """
    event_id = row["id"]
    is_saved = event_id in saved_ids
    
    category = row["category"]
    cat_icon = config.get_category_icon(category)
    cat_color = config.get_category_color(category)
    
    # Card container
    with st.container():
        if compact:
            # Compact layout
            c1, c2 = st.columns([3, 1])
            with c1:
                st.markdown(f"**{cat_icon} {row['title']}**")
                st.caption(f"📍 {row['city']} • {row['venue']}")
                st.caption(f"📅 {format_date(row['date_start'])} • {format_time(row['date_start'])}")
            with c2:
                st.markdown(f"**{format_price(row['price'])}**")
                if st.button("❤️" if is_saved else "🤍", key=f"{key_prefix}_save_{event_id}"):
                    if on_save:
                        on_save(event_id, row["title"])
        else:
            # Full card layout
            cols = st.columns([1, 4, 2])
            
            with cols[0]:
                st.markdown(f"### {cat_icon}")
                st.caption(category)
                st.caption(row["city"])
            
            with cols[1]:
                st.markdown(f"**{row['title']}**")
                
                # Date and venue
                date_str = format_date_range(row["date_start"], row["date_end"])
                st.caption(f"📍 {row['venue']} • {date_str}")
                
                # Description
                description = row.get("description", "")
                if description:
                    st.write(description[:200] + ("..." if len(description) > 200 else ""))
                
                # Price and popularity
                st.caption(f"💰 {format_price(row['price'])} • ⭐ {row['popularity']}% popularity")
                
                # Distance if available
                distance = row.get("distance_km")
                if distance is not None and not pd.isna(distance):
                    st.caption(f"📏 {distance:.1f} km away")
            
            with cols[2]:
                # Action buttons
                btn_cols = st.columns(3)
                
                with btn_cols[0]:
                    if st.button("📄 Details", key=f"{key_prefix}_details_{event_id}"):
                        if on_details:
                            on_details(event_id)
                
                with btn_cols[1]:
                    btn_label = "❤️ Saved" if is_saved else "🤍 Save"
                    if st.button(btn_label, key=f"{key_prefix}_save_{event_id}"):
                        if on_save:
                            on_save(event_id, row["title"])
                
                with btn_cols[2]:
                    if st.button("📤 Share", key=f"{key_prefix}_share_{event_id}"):
                        if on_share:
                            on_share(event_id)
        
        st.divider()


def render_event_details(row: pd.Series, on_close: Optional[Callable] = None):
    """
    Render detailed event view.
    
    Args:
        row: Event data as pandas Series
        on_close: Callback when close button clicked
    """
    category = row["category"]
    cat_icon = config.get_category_icon(category)
    
    with st.container(border=True):
        # Header
        col1, col2 = st.columns([4, 1])
        with col1:
            st.markdown(f"### {cat_icon} {row['title']}")
            st.caption(f"{category} • {row['city']} • {row['venue']}")
        with col2:
            if on_close and st.button("❌ Close", key="close_details"):
                on_close()
                st.rerun()
        
        st.divider()
        
        # Details
        st.write(row.get("description", "No description available."))
        
        col1, col2 = st.columns(2)
        with col1:
            st.markdown("**📅 Date & Time**")
            st.write(format_date_range(row["date_start"], row["date_end"]))
        
        with col2:
            st.markdown("**💰 Price**")
            st.write(format_price(row["price"]))
        
        st.markdown("**⭐ Popularity**")
        st.progress(row["popularity"] / 100, text=f"{row['popularity']}%")
        
        # Actions
        st.divider()
        action_cols = st.columns(3)
        
        with action_cols[0]:
            if st.button("🎫 Get Tickets", key=f"tickets_{row['id']}", use_container_width=True):
                st.info("🎫 Ticket booking coming soon!", icon="🎫")
        
        with action_cols[1]:
            lat, lon = row.get("lat"), row.get("lon")
            if pd.notna(lat) and pd.notna(lon):
                maps_url = f"https://www.google.com/maps/dir/?api=1&destination={lat},{lon}"
                st.link_button("🗺️ Get Directions", maps_url, use_container_width=True)
            else:
                if st.button("🗺️ Directions", key=f"dir_{row['id']}", use_container_width=True, disabled=True):
                    pass
                st.caption("Location not available")
        
        with action_cols[2]:
            if st.button("📤 Share Event", key=f"share_{row['id']}", use_container_width=True):
                st.toast("🔗 Share link copied!", icon="✅")


def render_filters_sidebar(
    df: pd.DataFrame,
    current_filters: dict,
    on_reset: Optional[Callable] = None
) -> dict:
    """
    Render the filters sidebar.
    
    Args:
        df: DataFrame with all events (for extracting filter options)
        current_filters: Current filter state
        on_reset: Callback when reset button clicked
        
    Returns:
        Updated filter dictionary
    """
    st.markdown("## 🔍 Filters")
    
    filters = current_filters.copy()
    
    # City filter
    city_options = ["All"] + config.CITIES
    filters["city"] = st.selectbox(
        "City",
        options=city_options,
        index=city_options.index(current_filters.get("city", "All")) if current_filters.get("city", "All") in city_options else 0,
        key="filter_city"
    )
    
    # Date filter
    filters["date_preset"] = st.radio(
        "Date",
        options=config.DATE_PRESETS,
        index=config.DATE_PRESETS.index(current_filters.get("date_preset", "All")),
        key="filter_date"
    )
    
    # Category filter
    category_options = list(config.CATEGORIES.keys())
    filters["categories"] = st.multiselect(
        "Categories",
        options=category_options,
        default=current_filters.get("categories", []),
        key="filter_categories"
    )
    
    # Price filter
    max_price = int(df["price"].max()) if not df.empty else 200
    filters["price_max"] = st.slider(
        "Max Price (TMT)",
        min_value=0,
        max_value=max_price,
        value=current_filters.get("price_max", max_price),
        step=5 if max_price >= 50 else 1,
        key="filter_price"
    )
    
    # Search
    filters["search"] = st.text_input(
        "Search",
        value=current_filters.get("search", ""),
        placeholder="Search events...",
        key="filter_search"
    )
    
    # Sort
    filters["sort_by"] = st.selectbox(
        "Sort by",
        options=config.SORT_OPTIONS,
        index=config.SORT_OPTIONS.index(current_filters.get("sort_by", "Date (Soonest)")),
        key="filter_sort"
    )
    
    st.divider()
    
    # Radius filter
    st.markdown("### 📍 Location Filter")
    filters["radius_km"] = st.number_input(
        "Radius (km)",
        min_value=0.0,
        value=current_filters.get("radius_km", 0.0),
        step=0.5,
        format="%.1f",
        key="filter_radius"
    )
    
    # Quick location buttons
    col1, col2 = st.columns(2)
    with col1:
        if st.button("📍 Ashgabat", key="btn_ashgabat", use_container_width=True):
            filters["center"] = config.CITY_COORDS["Ashgabat"]
            st.rerun()
    with col2:
        if st.button("🔄 Clear Radius", key="btn_clear_radius", use_container_width=True):
            filters["radius_km"] = 0.0
            st.rerun()
    
    st.divider()
    
    # Reset button
    if st.button("🗑️ Clear All Filters", type="secondary", use_container_width=True):
        if on_reset:
            on_reset()
        st.rerun()
    
    return filters


def render_stats_cards(stats: dict):
    """
    Render statistics cards.
    
    Args:
        stats: Dictionary with statistics
    """
    cols = st.columns(4)
    
    with cols[0]:
        st.metric(
            label="Total Events",
            value=stats.get("total", 0),
            delta=f"{stats.get('upcoming_this_week', 0)} this week"
        )
    
    with cols[1]:
        st.metric(
            label="Cities",
            value=stats.get("cities", 0)
        )
    
    with cols[2]:
        st.metric(
            label="Free Events",
            value=stats.get("free_events", 0)
        )
    
    with cols[3]:
        st.metric(
            label="Avg. Price",
            value=f"{stats.get('avg_price', 0):.0f} TMT"
        )


def render_category_chips(categories: list, selected: list, on_select: Optional[Callable] = None):
    """
    Render category filter chips.
    
    Args:
        categories: List of available categories
        selected: List of currently selected categories
        on_select: Callback when category selected
    """
    cols = st.columns(len(categories) if len(categories) <= 6 else 6)
    
    for i, cat in enumerate(categories[:12]):
        with cols[i % 6]:
            icon = config.get_category_icon(cat)
            is_selected = cat in selected
            
            if st.button(
                f"{icon} {cat}",
                key=f"cat_chip_{cat}",
                type="primary" if is_selected else "secondary",
                use_container_width=True
            ):
                if on_select:
                    on_select(cat)
