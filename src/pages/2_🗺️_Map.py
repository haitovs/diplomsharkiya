import streamlit as st
import pandas as pd
import folium
from branca.element import Element
from streamlit_folium import st_folium
from utils.data_loader import load_data, get_event_image_base64, get_category_image_path
from utils.filters import apply_filters
from utils.i18n import t, t_cat, render_language_selector
from state_manager import get_state
from components.styles import inject_custom_css, get_category_color_hex
from components.payment import payment_dialog
from config import CATEGORY_CONFIG

st.set_page_config(page_title="Map | Event Discovery", page_icon="🗺️", layout="wide")

inject_custom_css()
render_language_selector()

df = load_data()
state = get_state()

# --- PAYMENT DIALOG TRIGGER (from map popup link) ---
_buy_id = st.query_params.get("buy")
if _buy_id:
    st.query_params.clear()
    _buy_row = df[df["id"] == _buy_id]
    if not _buy_row.empty:
        _r = _buy_row.iloc[0]
        st.session_state["_payment_event"] = {
            "id": _r["id"],
            "title": _r["title"],
            "price": _r["price"],
        }
        payment_dialog()

st.title(f"🗺️ {t('map_page_title')}")

st.markdown(
    """
    <style>
    /* Keep map visible during Streamlit reruns (avoid blue/dim stale overlay). */
    .st-key-mapcanvas [data-testid="stElementContainer"][data-stale="true"] {
        opacity: 1 !important;
        transition: none !important;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

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

@st.cache_data(ttl=300, show_spinner=False)
def _build_map_html(events_json: str, lang: str, city_filter: str, cat_filter: tuple):
    """Build the folium map and return its HTML. Cached for 5 minutes."""
    import json as _json
    rows = _json.loads(events_json)

    # Center logic
    if city_filter != "All Cities" and rows:
        center = [rows[0]["lat"], rows[0]["lon"]]
        zoom = 13
    else:
        center = [37.9601, 58.3261]
        zoom = 12

    m = folium.Map(
        location=center, zoom_start=zoom, tiles=None,
        control_scale=True, prefer_canvas=True, fade_animation=False,
    )

    folium.TileLayer(
        tiles="OpenStreetMap",
        attr='&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors',
        name="OpenStreetMap", overlay=False, control=True, show=True,
    ).add_to(m)

    folium.TileLayer(
        tiles="https://{s}.basemaps.cartocdn.com/light_all/{z}/{x}/{y}{r}.png",
        attr='&copy; <a href="https://carto.com/">CARTO</a>',
        name="CartoDB Positron", overlay=False, control=True, show=False,
    ).add_to(m)

    m.get_root().html.add_child(Element(
        "<style>.leaflet-container{background:#f8fafc !important;}</style>"
    ))

    folium.LayerControl().add_to(m)

    # Image cache for this build
    _img_cache = {}

    def _get_img(cat, img_path):
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

    free_text = t("free")
    buy_label = t("buy_ticket").replace("🎫 ", "")

    for row in rows:
        if row.get("lat") is None or row.get("lon") is None:
            continue

        cat = row.get("category", "Event")
        cat_cfg = CATEGORY_CONFIG.get(cat, {})
        cat_icon = cat_cfg.get("icon", "📌")
        cat_color = get_category_color_hex(cat)
        cat_display = t_cat(cat)

        icon_obj = folium.DivIcon(
            html=f'<div style="font-size:1.6rem;text-align:center;'
                 f'line-height:1;text-shadow:0 1px 3px rgba(0,0,0,0.4);">'
                 f'{cat_icon}</div>',
            icon_size=(32, 32), icon_anchor=(16, 16),
        )

        price = row.get("price", 0)
        price_str = free_text if price == 0 else f"{int(price)} TMT"
        price_color = "#10B981" if price == 0 else "#6366F1"

        date_str = ""
        ds = row.get("date_start", "")
        if ds:
            try:
                from datetime import datetime as _dt
                date_str = _dt.fromisoformat(ds).strftime("%b %d · %I:%M %p")
            except Exception:
                date_str = str(ds).split("T")[0] if "T" in str(ds) else str(ds)

        img_data_uri = _get_img(cat, row.get("image", ""))
        photo_html = ""
        if img_data_uri:
            photo_html = (
                '<details style="display:inline-block;margin:0;vertical-align:middle;">'
                '<summary style="cursor:pointer;display:inline-block;'
                'background:rgba(99,102,241,0.15);color:#6366F1;'
                'border-radius:6px;padding:2px 8px;font-size:0.72rem;'
                'font-weight:600;list-style:none;user-select:none;'
                'line-height:1.4;">📷</summary>'
                f'<img src="{img_data_uri}" style="max-height:60px;max-width:100%;'
                f'object-fit:cover;border-radius:4px;margin-top:4px;display:block;" />'
                '</details>'
            )

        desc = row.get("description", "")[:80]
        if len(row.get("description", "")) > 80:
            desc += "..."

        ticket_badge = "<span style='background:rgba(99,102,241,0.15);color:#6366F1;padding:3px 8px;border-radius:6px;font-size:0.72rem;font-weight:600;'>🎫 Ticket</span>" if price > 0 else ""
        buy_btn = f"<a href='?buy={row['id']}' target='_top' style='display:inline-block;margin-top:6px;padding:5px 14px;background:linear-gradient(135deg,#6366F1,#8B5CF6);color:white;border-radius:8px;font-size:0.78rem;font-weight:600;text-decoration:none;text-align:center;'>🎫 {buy_label}</a>" if price > 0 else ""

        popup_html = f"""
        <div style="font-family:'Inter',sans-serif;width:220px;padding:4px;">
            <div style="display:flex;align-items:center;gap:6px;margin-bottom:6px;">
                <span style="font-size:1.2rem;">{cat_icon}</span>
                <span style="background:rgba(99,102,241,0.12);color:#6366F1;
                    padding:2px 8px;border-radius:12px;font-size:0.7rem;
                    font-weight:600;text-transform:uppercase;">{cat_display}</span>
            </div>
            <h4 style="margin:0 0 4px 0;font-size:0.95rem;font-weight:600;">{row['title']}</h4>
            <p style="color:#666;font-size:0.8rem;margin:0 0 4px 0;">📍 {row.get('venue','')} · {row.get('city','')}</p>
            <p style="color:#888;font-size:0.8rem;margin:0 0 6px 0;">📅 {date_str}</p>
            <p style="color:#555;font-size:0.78rem;margin:0 0 6px 0;">{desc}</p>
            <div style="display:flex;align-items:center;gap:6px;flex-wrap:wrap;">
                <span style="background:{price_color}15;color:{price_color};
                    padding:3px 10px;border-radius:6px;display:inline-block;
                    font-weight:700;font-size:0.85rem;">{price_str}</span>
                {ticket_badge}
                {photo_html}
            </div>
            {buy_btn}
        </div>"""

        folium.Marker(
            [row["lat"], row["lon"]],
            popup=folium.Popup(popup_html, max_width=260),
            tooltip=f"{cat_icon} {row['title']} · {price_str}",
            icon=icon_obj,
        ).add_to(m)

    return m


if filtered_df.empty:
    st.warning(t("no_events"))
else:
    st.caption(f"{t('showing_events')}: {len(filtered_df)}")

    # Serialize filtered data for caching (hashable key)
    from utils.i18n import get_lang
    _events_json = filtered_df.to_json(orient="records", date_format="iso")
    _cache_key_cats = tuple(sorted(state.filters.categories))

    m = _build_map_html(_events_json, get_lang(), state.filters.city, _cache_key_cats)

    try:
        with st.container(key="mapcanvas"):
            st_folium(
                m,
                key="main_events_map",
                height=600,
                use_container_width=True,
                returned_objects=[],
            )
    except Exception as e:
        st.error(f"Map rendering error: {e}")
        st.info("Try refreshing the page.")

