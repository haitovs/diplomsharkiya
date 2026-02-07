# Mähallik Çäreler — Streamlit (statiki)
# Run: streamlit run app.py

import datetime as dt
import json
import math
import pathlib

import folium
import pandas as pd
import streamlit as st
from folium.plugins import Draw
# NEW for draggable circle
from streamlit_folium import st_folium

st.set_page_config(page_title="Mähallik Çäreler", page_icon="🎟️", layout="wide")

# Custom CSS for better UI
st.markdown("""
<style>
div[data-testid="column"] > div > div > div > button {
    width: 100%;
    min-height: 40px;
    white-space: nowrap;
}
/* Improve card visual hierarchy */
.stMarkdown h3 {
    margin-bottom: 0.5rem;
}
/* Better spacing */
.stButton > button {
    font-size: 0.875rem;
}
/* Make tab buttons BIGGER and more prominent */
button[data-baseweb="tab"] {
    font-size: 1.1rem !important;
    font-weight: 600 !important;
    padding: 12px 24px !important;
    min-height: 50px !important;
}
button[data-baseweb="tab"][aria-selected="true"] {
    background-color: rgba(99, 102, 241, 0.1) !important;
    border-bottom: 3px solid #6366f1 !important;
}
/* Map container styling */
.stMap > div {
    border-radius: 8px;
    border: 1px solid #e5e7eb;
}
</style>
""", unsafe_allow_html=True)

# Initialize session state FIRST (before any widgets)
if "filter_date" not in st.session_state:
    st.session_state.filter_date = "Ählisi"
if "saved_ids" not in st.session_state:
    st.session_state.saved_ids = set()
if "details_id" not in st.session_state:
    st.session_state.details_id = None
if "circle_center" not in st.session_state:
    st.session_state.circle_center = (37.9601, 58.3261)  # Ashgabat
if "circle_radius_km" not in st.session_state:
    st.session_state.circle_radius_km = 0.0
if "had_map_drawings" not in st.session_state:
    st.session_state.had_map_drawings = False

# App Header
st.markdown("# 🎟️ Mähallik Çäreler")
st.markdown("*Türkmenistanda geçirilýän çäreleri gözläň we meýilleşdiriň*")
st.divider()

DEFAULT_CENTER = (37.9601, 58.3261)
DEFAULT_RADIUS_KM = 0.0
ALL_CITY_OPTION = "Ählisi"
DEFAULT_DATE_PRESET = "Ählisi"
DEFAULT_SORT_OPTION = "Ýakynda başlaýanlar"
DEFAULT_PRICE_CAP = 200

EXPECTED_COLUMNS = [
    "id",
    "title",
    "category",
    "city",
    "venue",
    "date_start",
    "date_end",
    "price",
    "popularity",
    "lat",
    "lon",
    "image",
    "description",
]
TEXT_COLUMNS = ["id", "title", "category", "city", "venue", "image", "description"]
NUMERIC_COLUMNS = ["price", "popularity"]
FLOAT_COLUMNS = ["lat", "lon"]
DATE_COLUMNS = ["date_start", "date_end"]

# Category color mapping for visual distinction
CATEGORY_COLORS = {
    "Wellness": "#10b981",      # Green
    "Music": "#8b5cf6",         # Purple  
    "Art": "#ec4899",           # Pink
    "Sports": "#3b82f6",        # Blue
    "Tech": "#6366f1",          # Indigo
    "Business": "#f59e0b",      # Amber
    "Food": "#f97316",          # Orange
    "Market": "#14b8a6",        # Teal
    "default": "#6b7280"        # Gray
}

DATA_PATH = pathlib.Path(__file__).parent / "events.json"


def load_events(path: pathlib.Path) -> pd.DataFrame:
    """Read and normalize events data from disk, guarding against malformed JSON."""
    if not path.exists():
        st.warning("`data/events.json` tapylmady – görkezmek üçin maglumat ýok.", icon="⚠️")
        return pd.DataFrame(columns=EXPECTED_COLUMNS)

    try:
        raw_text = path.read_text(encoding="utf-8")
    except OSError as exc:
        st.error(f"Çäreler faýlyny okap bolmady: {exc}", icon="🚫")
        return pd.DataFrame(columns=EXPECTED_COLUMNS)

    if not raw_text.strip():
        st.warning("`data/events.json` faýly boş – görkezmek üçin maglumat ýok.", icon="⚠️")
        return pd.DataFrame(columns=EXPECTED_COLUMNS)

    try:
        raw = json.loads(raw_text)
    except json.JSONDecodeError as exc:
        st.error(f"`data/events.json` JSON formatynda näsazlyk bar: {exc}", icon="🚫")
        return pd.DataFrame(columns=EXPECTED_COLUMNS)

    if not isinstance(raw, list):
        st.error("`data/events.json` mazmuny san görnüşinde bolmaly.", icon="🚫")
        return pd.DataFrame(columns=EXPECTED_COLUMNS)

    df = pd.DataFrame(raw)
    for col in EXPECTED_COLUMNS:
        if col not in df.columns:
            df[col] = None
    df = df[EXPECTED_COLUMNS].copy()

    if df.empty:
        return df

    for col in TEXT_COLUMNS:
        df[col] = df[col].fillna("").astype(str)

    for col in NUMERIC_COLUMNS:
        df[col] = pd.to_numeric(df[col], errors="coerce").fillna(0.0)

    for col in FLOAT_COLUMNS:
        df[col] = pd.to_numeric(df[col], errors="coerce")

    for col in DATE_COLUMNS:
        df[col] = pd.to_datetime(df[col], errors="coerce")

    invalid_dates = df[DATE_COLUMNS].isna().any(axis=1)
    if invalid_dates.any():
        st.warning(
            f"{invalid_dates.sum()} çäre senesi nädogry bolandygy üçin görkezilen sanawdan aýyryldy.",
            icon="⚠️",
        )
        df = df.loc[~invalid_dates]

    return df.reset_index(drop=True)

# ---------- Maglumatlar ----------
df = load_events(DATA_PATH)

# ---------- Session state (additional filter states) ----------
# Core states already initialized at top
if not isinstance(st.session_state.saved_ids, set):
    st.session_state.saved_ids = set(st.session_state.saved_ids)

price_ceiling = DEFAULT_PRICE_CAP
if not df.empty and "price" in df.columns:
    price_max = df["price"].max()
    if pd.notna(price_max):
        try:
            price_ceiling = int(math.ceil(float(price_max)))
        except (TypeError, ValueError):
            price_ceiling = DEFAULT_PRICE_CAP
if price_ceiling < 0:
    price_ceiling = DEFAULT_PRICE_CAP

if "filter_city" not in st.session_state:
    st.session_state.filter_city = ALL_CITY_OPTION
if "filter_categories" not in st.session_state:
    st.session_state.filter_categories = []
if "filter_price" not in st.session_state:
    st.session_state.filter_price = price_ceiling
if "filter_search" not in st.session_state:
    st.session_state.filter_search = ""
if "filter_sort" not in st.session_state:
    st.session_state.filter_sort = DEFAULT_SORT_OPTION if not df.empty else "Degişlilik"
if "filter_radius_input" not in st.session_state:
    st.session_state.filter_radius_input = float(st.session_state.circle_radius_km)


# ---------- Kömekçiler ----------
def quick_date_filter(df: pd.DataFrame, preset: str) -> pd.DataFrame:
    if df.empty:
        return df
    if not preset or preset == DEFAULT_DATE_PRESET:
        return df
    today = pd.Timestamp(dt.datetime.now().date())
    if preset == "Şu gün":
        return df[df["date_start"].dt.date == today.date()]
    if preset == "Ertir":
        return df[df["date_start"].dt.date == (today + pd.Timedelta(days=1)).date()]
    if preset == "Şu hepdäniň ahyry":
        weekday = today.weekday()
        sat = today + pd.Timedelta(days=(5 - weekday) % 7)
        sun = sat + pd.Timedelta(days=1)
        return df[(df["date_start"].dt.date >= sat.date()) & (df["date_start"].dt.date <= sun.date())]
    if preset == "7 günüň içinde":
        end = today + pd.Timedelta(days=7)
        return df[(df["date_start"] >= today) & (df["date_start"] < end)]
    return df


def apply_filters(df: pd.DataFrame, city, categories, search, price_max_tmt, date_preset):
    out = df.copy()
    if city and city != ALL_CITY_OPTION:
        out = out[out["city"] == city]
    if categories:
        out = out[out["category"].isin(categories)]
    if search:
        pattern = search.strip()
        if pattern:
            mask = (
                out["title"].str.contains(pattern, case=False, na=False)
                | out["venue"].str.contains(pattern, case=False, na=False)
                | out["description"].str.contains(pattern, case=False, na=False)
            )
            out = out[mask]
    if price_max_tmt is not None:
        out = out[out["price"] <= float(price_max_tmt)]
    out = quick_date_filter(out, date_preset)
    return out


def apply_sort(df: pd.DataFrame, by):
    if df.empty:
        return df
    if by == "Ýakynda başlaýanlar":
        return df.sort_values("date_start", ascending=True)
    if by == "Baha (arzan → gymmat)":
        return df.sort_values("price", ascending=True)
    if by == "Meşhurlygy":
        return df.sort_values("popularity", ascending=False)
    return df


def haversine_km(lat1, lon1, lat2, lon2):
    R = 6371.0
    dlat = math.radians(lat2 - lat1)
    dlon = math.radians(lon2 - lon1)
    a = (math.sin(dlat / 2)**2 + math.cos(math.radians(lat1)) * math.cos(math.radians(lat2)) * math.sin(dlon / 2)**2)
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    return R * c


def filter_by_circle(df: pd.DataFrame, center_lat, center_lon, radius_km: float):
    if radius_km <= 0 or df.empty:
        return df
    candidates = df[df["lat"].notna() & df["lon"].notna()].copy()
    if candidates.empty:
        return candidates
    distances = candidates.apply(
        lambda r: haversine_km(center_lat, center_lon, float(r["lat"]), float(r["lon"])),
        axis=1,
    )
    keep = distances <= radius_km
    out = candidates.loc[keep].copy()
    out["distance_km"] = distances[keep]
    return out.sort_values("distance_km")


def reset_filter_state(price_limit: float) -> None:
    st.session_state.filter_city = ALL_CITY_OPTION
    st.session_state.filter_date = DEFAULT_DATE_PRESET
    st.session_state.filter_categories = []
    st.session_state.filter_price = int(price_limit)
    st.session_state.filter_search = ""
    st.session_state.filter_sort = DEFAULT_SORT_OPTION
    st.session_state.circle_center = DEFAULT_CENTER
    st.session_state.circle_radius_km = DEFAULT_RADIUS_KM
    st.session_state.filter_radius_input = DEFAULT_RADIUS_KM
    st.session_state.had_map_drawings = False
    st.session_state.details_id = None


# Namespaced widget keys so tabs never collide
def event_card(row, key_prefix: str):
    # Use container with border for better visual separation
    with st.container(border=True):
        cols = st.columns([1, 4, 2])
        with cols[0]:
            st.markdown("### 🎫")
            # Category badge with color
            category = row['category']
            color = CATEGORY_COLORS.get(category, CATEGORY_COLORS['default'])
            st.markdown(
                f'<span style="background-color: {color}; color: white; padding: 4px 12px; '
                f'border-radius: 12px; font-size: 0.75rem; font-weight: 600; '
                f'display: inline-block; margin: 4px 0;">{category}</span>',
                unsafe_allow_html=True
            )
            st.caption(f"📍 {row['city']}")
        with cols[1]:
            # Improved title hierarchy
            st.markdown(f"### {row['title']}")
            st.caption(f"📍 {row['venue']} • 🕒 {row['date_start'].strftime('%a, %d %b %H:%M')} — {row['date_end'].strftime('%H:%M')}")
            st.write(row["description"][:200] + "..." if len(row["description"]) > 200 else row["description"])
            # Better formatted metadata with visual styling
            col_a, col_b = st.columns(2)
            with col_a:
                st.caption(f"⭐ Meşhurlygy: {row['popularity']}")
            with col_b:
                # Styled price display
                price = row['price']
                if price == 0:
                    st.markdown('💰 Bahasy: <span style="color: #10b981; font-weight: 700;">MUGT</span>', unsafe_allow_html=True)
                else:
                    st.markdown(f'💰 Bahasy: <span style="color: #f59e0b; font-weight: 700;">{price} TMT</span>', unsafe_allow_html=True)
            distance = row.get("distance_km") if hasattr(row, "get") else None
            if distance is not None and not pd.isna(distance):
                st.caption(f"📏 Aralygy: {distance:.1f} km")
        with cols[2]:
            saved = row["id"] in st.session_state.saved_ids
            # Fix: Use wider first column for Details button to prevent wrapping
            c1, c2 = st.columns([1.5, 1])
            with c1:
                if st.button("📄 Jikme-jik", key=f"{key_prefix}_details_{row['id']}", use_container_width=True):
                    show_event_details(row)
            with c2:
                btn_label = "❤️" if saved else "🤍"
                if st.button(btn_label, key=f"{key_prefix}_save_{row['id']}", use_container_width=True):
                    if saved:
                        st.session_state.saved_ids.remove(row["id"])
                        st.toast(f"'{row['title']}' saýlananlardan aýyryldy", icon="💔")
                    else:
                        st.session_state.saved_ids.add(row["id"])
                        st.toast(f"'{row['title']}' saýlananlara goşuldy!", icon="❤️")
                    st.rerun()
            # Share button on new row to prevent cramping
            if st.button("📤 Paýlaş", key=f"{key_prefix}_share_{row['id']}", use_container_width=True):
                # Create shareable Google Maps link
                lat, lon = row.get("lat"), row.get("lon")
                if pd.notna(lat) and pd.notna(lon):
                    share_url = f"https://www.google.com/maps/search/?api=1&query={lat},{lon}"
                    st.toast(f"🔗 Link kopylandy! {share_url}", icon="✅")
                    # Show the link in a text area for easy copying
                    st.markdown(
                        f'<div style="margin-top: 8px; padding: 8px; background: #f3f4f6; border-radius: 4px; '
                        f'font-size: 0.75rem; word-break: break-all;">'
                        f'<a href="{share_url}" target="_blank" style="color: #6366f1;">{share_url}</a>'
                        f'</div>',
                        unsafe_allow_html=True
                    )
                else:
                    st.toast("Koordinatalar ýok, paýlaşyp bolmady", icon="⚠️")


@st.dialog("Çäre barada jikme-jik maglumat")
def show_event_details(row):
    """Modern modal dialog for event details using @st.dialog decorator."""
    # Category badge
    category = row['category']
    color = CATEGORY_COLORS.get(category, CATEGORY_COLORS['default'])
    st.markdown(
        f'<span style="background-color: {color}; color: white; padding: 6px 16px; '
        f'border-radius: 16px; font-size: 0.875rem; font-weight: 700; '
        f'display: inline-block; margin-bottom: 1rem;">{category}</span>',
        unsafe_allow_html=True
    )
    
    st.markdown(f"# {row['title']}")
    st.caption(f"📍 {row['city']} • {row['venue']}")
    st.divider()
    
    # Event details in organized sections
    st.markdown("### 📝 Düşündiriş")
    st.write(row["description"])
    
    st.markdown("### ⏰ Wagt we ýer")
    col1, col2 = st.columns(2)
    with col1:
        st.write(f"**Başlangyç:** {row['date_start'].strftime('%Y-%m-%d %H:%M')}")
        st.write(f"**Soňy:** {row['date_end'].strftime('%Y-%m-%d %H:%M')}")
    with col2:
        st.write(f"**Ýer:** {row['venue']}")
        st.write(f"**Şäher:** {row['city']}")
    
    st.markdown("### 💰 Baha we meşhurlygy")
    col1, col2 = st.columns(2)
    with col1:
        price = row['price']
        if price == 0:
            st.markdown('<p style="font-size: 1.5rem; color: #10b981; font-weight: 700;">MUGT</p>', unsafe_allow_html=True)
        else:
            st.markdown(f'<p style="font-size: 1.5rem; color: #f59e0b; font-weight: 700;">{price} TMT</p>', unsafe_allow_html=True)
    with col2:
        st.write(f"**Meşhurlygy:** ⭐ {row['popularity']}")
    
    st.divider()
    
    # Action buttons
    col1, col2 = st.columns(2)
    with col1:
        if st.button("🎫 Biletler satyn al", use_container_width=True, type="primary"):
            st.info("Bilet satyn almak funksiýasy ýakynda elýeterli bolar!", icon="🎫")
    with col2:
        lat, lon = row.get("lat"), row.get("lon")
        if pd.notna(lat) and pd.notna(lon):
            maps_url = f"https://www.google.com/maps/dir/?api=1&destination={lat},{lon}"
            st.link_button("🗺️ Ýol görkezme", maps_url, use_container_width=True)


# ---------- Sidebar ----------
with st.sidebar:
    st.markdown("## Süzgüçler")
    
    # Move search to top for better UX
    search = st.text_input("🔍 Gözleg", placeholder="Ady, ýeri ýa-da düşündiriş...", key="filter_search")
    
    st.markdown("---")
    
    # Group filters logically
    category_options = sorted(df["category"].unique().tolist()) if not df.empty else []
    if st.session_state.filter_categories:
        st.session_state.filter_categories = [c for c in st.session_state.filter_categories if c in category_options]
    categories = st.multiselect("Görnüşi", options=category_options, key="filter_categories")
    
    st.markdown("")
    date_options = ["Şu gün", "Ertir", "Şu hepdäniň ahyry", "7 günüň içinde", DEFAULT_DATE_PRESET]
    date_preset = st.radio("Sene", options=date_options, index=date_options.index(st.session_state.filter_date), key="filter_date")
    
    st.markdown("")
    city_options = [ALL_CITY_OPTION] + (sorted(df["city"].unique().tolist()) if not df.empty else [])
    if st.session_state.filter_city not in city_options:
        st.session_state.filter_city = ALL_CITY_OPTION
    city = st.selectbox("Şäher", options=city_options, key="filter_city")
    
    st.markdown("")
    if st.session_state.filter_price > price_ceiling:
        st.session_state.filter_price = price_ceiling
    if st.session_state.filter_price < 0:
        st.session_state.filter_price = 0
    price_step = 5 if price_ceiling >= 5 else 1
    price_max = st.slider(
        "Iň ýokary baha (TMT)",
        min_value=0,
        max_value=price_ceiling,
        step=price_step,
        key="filter_price",
    )

    sort_options = ["Degişlilik", DEFAULT_SORT_OPTION, "Baha (arzan → gymmat)", "Meşhurlygy"]
    if st.session_state.filter_sort not in sort_options:
        st.session_state.filter_sort = DEFAULT_SORT_OPTION
    sort_by = st.selectbox("Tertip", options=sort_options, key="filter_sort")

    st.markdown("---")
    st.markdown("### Aralyk boýunça süzgüç")
    # Sync filter_radius_input with circle_radius_km on load
    if "filter_radius_input" not in st.session_state:
        st.session_state.filter_radius_input = st.session_state.circle_radius_km
    
    # Radius input widget
    radius_km_number = float(
        st.number_input(
            "Aralyk (km)",
            min_value=0.0,
            step=0.5,
            format="%.1f",
            key="filter_radius_input",
        )
    )
    # Sync widget value into map state
    if not math.isclose(radius_km_number, st.session_state.circle_radius_km, rel_tol=1e-9, abs_tol=1e-4):
        st.session_state.circle_radius_km = radius_km_number

    c_reset_center, c_reset_radius = st.columns(2)
    with c_reset_center:
        if st.button("Aşgabada git", key="btn_reset_center"):
            st.session_state.circle_center = DEFAULT_CENTER
            st.session_state.circle_radius_km = DEFAULT_RADIUS_KM
            st.session_state.filter_radius_input = DEFAULT_RADIUS_KM
            st.session_state.had_map_drawings = False
            st.rerun()
    with c_reset_radius:
        if st.button("Aralygy aýyr", key="btn_reset_radius"):
            st.session_state.circle_radius_km = 0.0
            st.session_state.filter_radius_input = 0.0
            st.session_state.had_map_drawings = False
            st.rerun()

    if st.button("Süzgüçleri arassala", type="secondary"):
        reset_filter_state(price_ceiling)
        st.rerun()

# ---------- Tabs ----------
tabs = st.tabs(["📋 Sanaw", "🗺️ Karta", "⭐ Saýlananlar"])

# Apply filters
base_filtered = apply_filters(df, city, categories, search, price_max, date_preset)

with tabs[1]:
    st.subheader("🗺️ Karta — Tegelek zony")
    
    # Show loading message while map initializes

# Now apply circle filter after map interactions (for list view)
filtered = filter_by_circle(
    base_filtered,
    st.session_state.circle_center[0],
    st.session_state.circle_center[1],
    st.session_state.circle_radius_km,
)
filtered = apply_sort(filtered, sort_by)

with tabs[0]:
    st.subheader("Çäreleriň sanawy")
    if filtered.empty:
        st.info("Saýlanan Filtrlere laýyk çäre tapylmady.")
    else:
        for _, row in filtered.iterrows():
            event_card(row, key_prefix="list")
            st.divider()

with tabs[2]:
    st.subheader("Halanan çäreler")
    if not st.session_state.saved_ids:
        st.info("Häzirlikçe halananlar ýok. Islendik kartda **Halanlara goş** düwmesine basyp goşuň.")
    else:
        fav_df = df[df["id"].isin(st.session_state.saved_ids)]
        fav_df = apply_sort(fav_df, sort_by)
        for _, row in fav_df.iterrows():
            event_card(row, key_prefix="fav")
            st.divider()
