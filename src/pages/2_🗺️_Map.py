import streamlit as st
import pandas as pd
import folium
from streamlit_folium import st_folium
from utils.data_loader import load_data
from utils.filters import apply_filters
from state_manager import get_state

st.set_page_config(page_title="Map | Sharkiya", page_icon="🗺️", layout="wide")

df = load_data()
state = get_state()

st.title("🗺️ Interactive Map")

# --- SIDEBAR FILTERS (Compact) ---
with st.sidebar:
    st.header("Filter Map")
    city_options = ["All Cities"] + sorted(df["city"].unique().tolist())
    state.filters.city = st.selectbox(
        "City", 
        city_options, 
        index=city_options.index(state.filters.city) if state.filters.city in city_options else 0
    )

# --- APPLY FILTERS ---
filtered_df = apply_filters(df, state.filters)

if filtered_df.empty:
    st.warning("No events found to display on map.")
else:
    # Default center (Ashgabat or average)
    if state.filters.city != "All Cities" and not filtered_df.empty:
        # Center on first event of city
        center = [filtered_df.iloc[0]['lat'], filtered_df.iloc[0]['lon']]
        zoom = 12
    else:
        # Default Ashgabat
        center = [37.9601, 58.3261]
        zoom = 6

    # Offline Map Configuration
    import os
    
    # Path to local tiles (CWD is src/)
    tiles_dir = "assets/tiles"
    
    # Check if we have local tiles (simple check)
    has_local_tiles = os.path.exists(tiles_dir) and len(os.listdir(tiles_dir)) > 0
    
    if has_local_tiles:
        pass

    m = folium.Map(location=center, zoom_start=zoom)
    
    for _, row in filtered_df.iterrows():
        if pd.notna(row.get('lat')) and pd.notna(row.get('lon')):
             # Determine Icon
             custom_icon = row.get('icon')
             
             # Default settings
             icon_obj = None
             
             if custom_icon and os.path.exists(f"assets/icons/{custom_icon}.png"):
                 # Use Custom Image Marker
                 icon_obj = folium.CustomIcon(
                     icon_image=f"assets/icons/{custom_icon}.png",
                     icon_size=(30, 30),
                 )
             else:
                 # Default Marker
                 # Fix 404s by pointing to local assets if needed, but Folium default is usually fine if not 404ing.
                 # The previous 404s were likely due to some CDN issue or pathing.
                 # If we want to use local default markers:
                 # icon_obj = folium.Icon(color='blue', icon='info-sign')
                 # For now, let's stick to default style unless custom icon is set.
                 icon_obj = folium.Icon(color='blue', icon='info-sign')

             folium.Marker(
                [row['lat'], row['lon']],
                popup=row['title'],
                tooltip=f"{row['title']} ({row['price']} TMT)",
                icon=icon_obj
            ).add_to(m)

    st_folium(m, width="100%", height=600)
