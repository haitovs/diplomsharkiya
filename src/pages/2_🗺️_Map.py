import streamlit as st
import pandas as pd
import folium
from streamlit_folium import st_folium
from utils.data_loader import load_data, get_event_image_base64, get_category_image_path
from utils.filters import apply_filters
from utils.i18n import t, t_cat, render_language_selector
from state_manager import get_state
from components.styles import inject_custom_css, get_category_color_hex
from config import CATEGORY_CONFIG

st.set_page_config(page_title="Map | Event Discovery", page_icon="🗺️", layout="wide")

inject_custom_css()
render_language_selector()

df = load_data()
state = get_state()

st.title(f"🗺️ {t('map_page_title')}")

# --- SIDEBAR FILTERS (Compact) ---
with st.sidebar:
    st.header(f"🔍 {t('filter_by_city')}")
    city_options = [t("all_cities")] + sorted(df["city"].unique().tolist())
    current_city = state.filters.city
    if current_city == "All Cities":
        current_city = t("all_cities")
    state.filters.city = st.selectbox(
        t("event_city"),
        city_options,
        index=city_options.index(current_city)
        if current_city in city_options else 0
    )
    if state.filters.city == t("all_cities"):
        state.filters.city = "All Cities"

    cat_options = sorted(df["category"].unique().tolist())
    state.filters.categories = st.multiselect(
        t("filter_by_category"), cat_options, default=state.filters.categories
    )

    st.markdown("---")
    st.caption(f"ℹ️ {t('map_note')}")

# --- APPLY FILTERS ---
filtered_df = apply_filters(df, state.filters)

if filtered_df.empty:
    st.warning(t("no_events"))
else:
    st.caption(f"{t('showing_events')}: {len(filtered_df)}")

    # Center logic — default zoomed on Ashgabat
    if state.filters.city != "All Cities" and not filtered_df.empty:
        center = [filtered_df.iloc[0]["lat"], filtered_df.iloc[0]["lon"]]
        zoom = 13
    else:
        center = [37.9601, 58.3261]
        zoom = 12

    # OpenStreetMap as the selected default tile layer
    m = folium.Map(location=center, zoom_start=zoom, tiles="OpenStreetMap")

    folium.TileLayer(
        tiles="https://{s}.basemaps.cartocdn.com/light_all/{z}/{x}/{y}{r}.png",
        attr='&copy; <a href="https://carto.com/">CARTO</a>',
        name="CartoDB Positron",
        overlay=False,
        control=True,
    ).add_to(m)

    folium.LayerControl().add_to(m)

    # Pre-cache all category images once
    _img_cache = {}

    def _get_popup_image(cat, img_path):
        key = img_path or cat
        if key in _img_cache:
            return _img_cache[key]
        path = img_path
        if not path or path == "images/event_default.jpg":
            path = get_category_image_path(cat)
        uri = get_event_image_base64(path)
        if not uri:
            uri = get_event_image_base64("images/event_default.jpg")
        _img_cache[key] = uri
        return uri

    for _, row in filtered_df.iterrows():
        if pd.notna(row.get("lat")) and pd.notna(row.get("lon")):
            cat = row.get("category", "Event")
            cat_cfg = CATEGORY_CONFIG.get(cat, {})
            cat_icon = cat_cfg.get("icon", "📌")
            cat_color = get_category_color_hex(cat)
            cat_display = t_cat(cat)

            icon_obj = folium.DivIcon(
                html=f'<div style="font-size:1.6rem;text-align:center;'
                     f'line-height:1;text-shadow:0 1px 3px rgba(0,0,0,0.4);">'
                     f'{cat_icon}</div>',
                icon_size=(32, 32),
                icon_anchor=(16, 16),
            )

            price = row.get("price", 0)
            price_str = t("free") if price == 0 else f"{int(price)} TMT"
            price_color = "#10B981" if price == 0 else "#6366F1"

            date_str = ""
            date_val = row.get("date_start")
            if date_val:
                try:
                    date_str = date_val.strftime("%b %d · %I:%M %p")
                except Exception:
                    raw = str(date_val)
                    date_str = raw.split("T")[0] if "T" in raw else raw

            img_data_uri = _get_popup_image(cat, row.get("image", ""))

            # Photo button inline next to price using <details>
            photo_details_html = ""
            if img_data_uri:
                photo_details_html = (
                    '<details style="display:inline-block;margin:0;vertical-align:middle;">'
                    '<summary style="cursor:pointer;display:inline-block;'
                    'background:rgba(99,102,241,0.15);color:#6366F1;'
                    'border-radius:6px;padding:2px 8px;font-size:0.72rem;'
                    'font-weight:600;list-style:none;user-select:none;'
                    'line-height:1.4;">'
                    '\U0001f4f7</summary>'
                    f'<img src="{img_data_uri}" style="max-height:60px;max-width:100%;'
                    f'object-fit:cover;border-radius:4px;margin-top:4px;display:block;" />'
                    '</details>'
                )

            popup_html = f"""
            <div style="font-family:'Inter',sans-serif; width:220px; padding:4px;">
                <div style="display:flex; align-items:center; gap:6px; margin-bottom:6px;">
                    <span style="font-size:1.2rem;">{cat_icon}</span>
                    <span style="background:rgba(99,102,241,0.12); color:#6366F1;
                        padding:2px 8px; border-radius:12px; font-size:0.7rem;
                        font-weight:600; text-transform:uppercase;">{cat_display}</span>
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
                <div style="display:flex; align-items:center; gap:6px;">
                    <span style="background:{price_color}15; color:{price_color};
                        padding:3px 10px; border-radius:6px; display:inline-block;
                        font-weight:700; font-size:0.85rem;">
                        {price_str}
                    </span>
                    {photo_details_html}
                </div>
            </div>
            """

            folium.Marker(
                [row["lat"], row["lon"]],
                popup=folium.Popup(popup_html, max_width=260),
                tooltip=f"{cat_icon} {row['title']} · {price_str}",
                icon=icon_obj,
            ).add_to(m)

    try:
        st_folium(m, width="100%", height=600)
    except Exception as e:
        st.error(f"Map rendering error: {e}")
        st.info("Try refreshing the page.")
