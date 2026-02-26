"""
Event Discovery - Map Component
Interactive map with event markers and filtering
"""

import streamlit as st
import folium
from folium.plugins import Draw, MarkerCluster
from streamlit_folium import st_folium
import pandas as pd
import math
from typing import Optional, Tuple, Dict, Any

import sys
import pathlib
sys.path.insert(0, str(pathlib.Path(__file__).parent.parent))

from app.config import config
from app.utils import haversine_km, format_price, format_date, format_time


def create_event_map(
    events_df: pd.DataFrame,
    center: Tuple[float, float] = None,
    zoom: int = None,
    radius_km: float = 0.0,
    show_draw_tools: bool = True,
    height: int = 520,
    show_clusters: bool = True,
) -> Tuple[folium.Map, Dict[str, Any]]:
    """
    Create an interactive Folium map with event markers.
    
    Args:
        events_df: DataFrame with events to display
        center: Map center (lat, lon)
        zoom: Zoom level
        radius_km: Radius circle to draw (0 = no circle)
        show_draw_tools: Whether to show drawing tools
        height: Map height in pixels
        show_clusters: Whether to cluster markers
        
    Returns:
        Tuple of (Folium map, map output from st_folium)
    """
    # Default center to Ashgabat
    if center is None:
        center = (config.DEFAULT_LAT, config.DEFAULT_LON)
    
    if zoom is None:
        zoom = config.DEFAULT_ZOOM
    
    # Create map
    m = folium.Map(
        location=list(center),
        zoom_start=zoom,
        control_scale=True,
        tiles="OpenStreetMap"
    )
    
    # Add alternative tile layers
    folium.TileLayer(
        tiles="https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}",
        attr="Esri",
        name="Satellite",
    ).add_to(m)
    
    folium.TileLayer(
        tiles="cartodbpositron",
        name="Light Mode",
    ).add_to(m)
    
    # Add layer control
    folium.LayerControl(position="topright").add_to(m)
    
    # Draw radius circle if specified
    if radius_km > 0:
        folium.Circle(
            location=list(center),
            radius=radius_km * 1000,  # Convert to meters
            color="#6366F1",
            weight=2,
            fill=True,
            fill_opacity=0.1,
            tooltip=f"Search radius: {radius_km:.1f} km",
        ).add_to(m)
    
    # Add event markers
    marker_coords = []
    
    if show_clusters:
        marker_cluster = MarkerCluster(name="Events")
    
    for _, row in events_df.iterrows():
        lat, lon = row.get("lat"), row.get("lon")
        
        if pd.isna(lat) or pd.isna(lon):
            continue
        
        # Get category styling
        category = row.get("category", "")
        cat_color = get_marker_color(category)
        cat_icon = config.get_category_fa_icon(category)
        
        # Create popup content
        popup_html = create_popup_html(row)
        popup = folium.Popup(popup_html, max_width=300)
        
        # Create marker
        marker = folium.Marker(
            location=[float(lat), float(lon)],
            tooltip=row.get("title", "Event"),
            popup=popup,
            icon=folium.Icon(
                color=cat_color,
                icon=cat_icon,
                prefix="fa"
            )
        )
        
        if show_clusters:
            marker.add_to(marker_cluster)
        else:
            marker.add_to(m)
        
        marker_coords.append([float(lat), float(lon)])
    
    if show_clusters:
        marker_cluster.add_to(m)
    
    # Fit bounds to markers if we have any
    if marker_coords and len(marker_coords) > 1:
        m.fit_bounds(marker_coords, padding=(20, 20))
    
    # Add draw tools for radius selection
    if show_draw_tools:
        Draw(
            draw_options={
                "polyline": False,
                "polygon": False,
                "rectangle": False,
                "circle": True,
                "marker": False,
                "circlemarker": False,
            },
            edit_options={
                "edit": True,
                "remove": True
            },
        ).add_to(m)
    
    return m


def render_map(
    events_df: pd.DataFrame,
    center: Tuple[float, float] = None,
    zoom: int = None,
    radius_km: float = 0.0,
    height: int = 520,
    key: str = "events_map"
) -> Dict[str, Any]:
    """
    Render the map and return interaction data.
    
    Args:
        events_df: DataFrame with events
        center: Map center
        zoom: Zoom level
        radius_km: Radius to display
        height: Map height
        key: Unique key for the map widget
        
    Returns:
        Dictionary with map interaction data
    """
    m = create_event_map(
        events_df=events_df,
        center=center,
        zoom=zoom,
        radius_km=radius_km,
        show_draw_tools=True,
        height=height,
    )
    
    # Render map and get output
    map_output = st_folium(
        m,
        height=height,
        use_container_width=True,
        returned_objects=["last_active_drawing", "all_drawings"],
        key=key,
    )
    
    return map_output


def process_map_drawing(map_output: Dict[str, Any]) -> Tuple[Optional[Tuple[float, float]], Optional[float]]:
    """
    Process map drawing output to extract circle center and radius.
    
    Args:
        map_output: Output from st_folium
        
    Returns:
        Tuple of (center, radius_km) or (None, None)
    """
    if not map_output:
        return None, None
    
    feature = map_output.get("last_active_drawing")
    drawings = map_output.get("all_drawings", [])
    
    if not feature and drawings:
        feature = drawings[-1]
    
    if not feature or not isinstance(feature, dict):
        return None, None
    
    geom = feature.get("geometry", {})
    props = feature.get("properties", {})
    
    # Handle circle (Point with radius)
    if geom.get("type") == "Point" and "radius" in props:
        lat = geom["coordinates"][1]
        lon = geom["coordinates"][0]
        radius_m = float(props["radius"])
        return (lat, lon), radius_m / 1000.0
    
    # Handle polygon approximation of circle
    if geom.get("type") == "Polygon":
        ring = geom.get("coordinates", [[]])[0]
        if ring:
            lats = [pt[1] for pt in ring]
            lons = [pt[0] for pt in ring]
            lat = sum(lats) / len(lats)
            lon = sum(lons) / len(lons)
            radius_km = haversine_km(lat, lon, lats[0], lons[0])
            return (lat, lon), radius_km
    
    return None, None


def get_marker_color(category: str) -> str:
    """
    Get Folium marker color for a category.
    
    Args:
        category: Event category
        
    Returns:
        Folium color name
    """
    color_map = {
        "Music": "purple",
        "Tech": "blue",
        "Sports": "green",
        "Food": "orange",
        "Art": "pink",
        "Market": "cadetblue",
        "Film": "darkred",
        "Wellness": "lightgreen",
        "Business": "darkblue",
        "Science": "darkpurple",
        "Kids": "beige",
        "Travel": "lightblue",
        "Community": "gray",
    }
    return color_map.get(category, "red")


def create_popup_html(row: pd.Series, image_data_uri: str = "") -> str:
    """
    Create HTML content for marker popup.

    Args:
        row: Event data
        image_data_uri: Optional base64 data URI for the event image

    Returns:
        HTML string
    """
    title = row.get("title", "Event")
    venue = row.get("venue", "")
    category = row.get("category", "")
    price = row.get("price", 0)
    date_start = row.get("date_start")

    if pd.notna(date_start):
        date_str = format_date(date_start) + " " + format_time(date_start)
    else:
        date_str = "TBD"

    price_str = "Free" if price == 0 else f"{int(price)} TMT"

    photo_details_html = ""
    if image_data_uri:
        photo_details_html = (
            '<details style="display:inline-block;margin:0;vertical-align:middle;">'
            '<summary style="cursor:pointer;display:inline-block;'
            'background:rgba(99,102,241,0.15);color:#6366F1;'
            'border-radius:6px;padding:2px 8px;font-size:0.72rem;'
            'font-weight:600;list-style:none;user-select:none;'
            'line-height:1.4;">'
            '\U0001f4f7</summary>'
            f'<img src="{image_data_uri}" style="max-height:60px;max-width:100%;'
            f'object-fit:cover;border-radius:4px;margin-top:4px;display:block;" />'
            '</details>'
        )

    html = f"""
    <div style="font-family: Arial, sans-serif; min-width: 200px;">
        <h4 style="margin: 0 0 8px 0; color: #1E293B;">{title}</h4>
        <p style="margin: 4px 0; color: #64748B; font-size: 12px;">
            📍 {venue}
        </p>
        <p style="margin: 4px 0; color: #64748B; font-size: 12px;">
            📅 {date_str}
        </p>
        <div style="display:flex; align-items:center; gap:6px; margin: 4px 0; font-size: 12px;">
            <span style="background: #E2E8F0; padding: 2px 8px; border-radius: 4px;">{category}</span>
            <span style="font-weight: bold; color: #6366F1;">{price_str}</span>
            {photo_details_html}
        </div>
    </div>
    """

    return html


def render_mini_map(lat: float, lon: float, height: int = 200, zoom: int = 15) -> None:
    """
    Render a small map for event details.
    
    Args:
        lat: Latitude
        lon: Longitude
        height: Map height
        zoom: Zoom level
    """
    m = folium.Map(
        location=[lat, lon],
        zoom_start=zoom,
        scrollWheelZoom=False,
        dragging=False,
    )
    
    folium.Marker(
        location=[lat, lon],
        icon=folium.Icon(color="red", icon="location-dot", prefix="fa")
    ).add_to(m)
    
    st_folium(
        m,
        height=height,
        use_container_width=True,
        key=f"mini_map_{lat}_{lon}"
    )
