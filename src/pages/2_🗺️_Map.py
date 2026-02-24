import streamlit as st
import pandas as pd
import folium
from streamlit_folium import st_folium
from utils.data_loader import load_data
from utils.filters import apply_filters
from state_manager import get_state
from components.styles import inject_custom_css, get_category_color_hex
from config import CATEGORY_CONFIG

st.set_page_config(page_title="Map | Sharkiya", page_icon="🗺️", layout="wide")

inject_custom_css()

df = load_data()
state = get_state()

st.title("🗺️ Interactive Map")

# --- SIDEBAR FILTERS (Compact) ---
with st.sidebar:
    st.header("🔍 Filter Map")
    city_options = ["All Cities"] + sorted(df["city"].unique().tolist())
    state.filters.city = st.selectbox(
        "City",
        city_options,
        index=city_options.index(state.filters.city)
        if state.filters.city in city_options else 0
    )

    cat_options = sorted(df["category"].unique().tolist())
    state.filters.categories = st.multiselect(
        "Categories", cat_options, default=state.filters.categories
    )

# --- APPLY FILTERS ---
filtered_df = apply_filters(df, state.filters)

if filtered_df.empty:
    st.warning("No events found to display on map.")
else:
    st.caption(f"Showing {len(filtered_df)} events on map")

    # Center logic
    if state.filters.city != "All Cities" and not filtered_df.empty:
        center = [filtered_df.iloc[0]["lat"], filtered_df.iloc[0]["lon"]]
        zoom = 12
    else:
        center = [37.9601, 58.3261]
        zoom = 6

    import os

    m = folium.Map(location=center, zoom_start=zoom, tiles="cartodbpositron")

    for _, row in filtered_df.iterrows():
        if pd.notna(row.get("lat")) and pd.notna(row.get("lon")):
            cat = row.get("category", "Event")
            cat_cfg = CATEGORY_CONFIG.get(cat, {})
            cat_icon = cat_cfg.get("icon", "📌")
            cat_color = get_category_color_hex(cat)

            custom_icon = row.get("icon")
            icon_obj = None
            if custom_icon and os.path.exists(f"assets/icons/{custom_icon}.png"):
                icon_obj = folium.CustomIcon(
                    icon_image=f"assets/icons/{custom_icon}.png",
                    icon_size=(30, 30),
                )
            else:
                icon_obj = folium.Icon(color="blue", icon="info-sign")

            # Styled popup
            price = row.get("price", 0)
            price_str = "Free" if price == 0 else f"{int(price)} TMT"
            price_color = "#10B981" if price == 0 else "#6366F1"

            date_str = ""
            date_val = row.get("date_start")
            if date_val:
                try:
                    date_str = date_val.strftime("%b %d · %I:%M %p")
                except Exception:
                    raw = str(date_val)
                    date_str = raw.split("T")[0] if "T" in raw else raw

            popup_html = f"""
            <div style="font-family:'Inter',sans-serif; width:220px; padding:4px;">
                <div style="display:flex; align-items:center; gap:6px; margin-bottom:6px;">
                    <span style="font-size:1.2rem;">{cat_icon}</span>
                    <span style="background:rgba(99,102,241,0.12); color:#6366F1;
                        padding:2px 8px; border-radius:12px; font-size:0.7rem;
                        font-weight:600; text-transform:uppercase;">{cat}</span>
                </div>
                <h4 style="margin:0 0 4px 0; font-size:0.95rem; font-weight:600;">{row['title']}</h4>
                <p style="color:#666; font-size:0.8rem; margin:0 0 4px 0;">
                    📍 {row.get('venue', '')} · {row.get('city', '')}
                </p>
                <p style="color:#888; font-size:0.8rem; margin:0 0 6px 0;">
                    📅 {date_str}
                </p>
                <p style="color:#555; font-size:0.78rem; margin:0 0 6px 0;">
                    {row.get('description', '')[:80]}{'...' if len(row.get('description', '')) > 80 else ''}
                </p>
                <div style="background:{price_color}15; color:{price_color};
                    padding:3px 10px; border-radius:6px; display:inline-block;
                    font-weight:700; font-size:0.85rem;">
                    {price_str}
                </div>
            </div>
            """

            folium.Marker(
                [row["lat"], row["lon"]],
                popup=folium.Popup(popup_html, max_width=260),
                tooltip=f"{cat_icon} {row['title']} · {price_str}",
                icon=icon_obj,
            ).add_to(m)

    st_folium(m, width="100%", height=600)
