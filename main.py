# 🎟️ Local Events - Sharkiya Event Discovery
# Simplified User Application

import streamlit as st
import pandas as pd
import pathlib
import math
import json
from datetime import datetime, timedelta

import folium
from streamlit_folium import st_folium

# Page config
st.set_page_config(
    page_title="Local Events",
    page_icon="🎟️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ============ Config ============
DEFAULT_LAT = 37.9601
DEFAULT_LON = 58.3261

CITIES = {
    "Ashgabat": (37.9601, 58.3261),
    "Mary": (37.6005, 61.8302),
    "Türkmenabat": (39.0733, 63.5786),
    "Dashoguz": (41.8387, 59.9650),
    "Balkanabat": (39.5104, 54.3672),
    "Awaza": (40.0224, 52.9693),
}

CATEGORIES = {
    "Music": {"icon": "🎵", "color": "purple"},
    "Tech": {"icon": "💻", "color": "blue"},
    "Sports": {"icon": "⚽", "color": "green"},
    "Food": {"icon": "🍽️", "color": "orange"},
    "Art": {"icon": "🎨", "color": "pink"},
    "Market": {"icon": "🛍️", "color": "cadetblue"},
    "Film": {"icon": "🎬", "color": "darkred"},
    "Wellness": {"icon": "🧘", "color": "lightgreen"},
    "Business": {"icon": "💼", "color": "darkblue"},
    "Science": {"icon": "🔬", "color": "darkpurple"},
    "Kids": {"icon": "👶", "color": "beige"},
    "Travel": {"icon": "✈️", "color": "lightblue"},
    "Community": {"icon": "👥", "color": "gray"},
}

# CSS
st.markdown("""
<style>
[data-testid="stAppViewContainer"] { background: linear-gradient(135deg, #0F172A 0%, #1E293B 100%); }
[data-testid="stAppViewContainer"] p, [data-testid="stAppViewContainer"] span, 
[data-testid="stAppViewContainer"] label { color: #E2E8F0 !important; }
[data-testid="stMetric"] { background: rgba(30,41,59,0.8); border-radius: 12px; border: 1px solid rgba(99,102,241,0.3); }
[data-testid="stMetric"] [data-testid="stMetricValue"] { color: #10B981 !important; }
h1 { background: linear-gradient(135deg, #6366F1 0%, #A855F7 100%); -webkit-background-clip: text; -webkit-text-fill-color: transparent; }
h2, h3 { color: #F1F5F9 !important; }
[data-testid="stSidebar"] { background: #0F172A !important; }
[data-testid="stSidebar"] * { color: #E2E8F0 !important; }
</style>
""", unsafe_allow_html=True)

# ============ Data ============
DATA_PATH = pathlib.Path(__file__).parent / "events.json"

@st.cache_data(ttl=60)
def load_data():
    if not DATA_PATH.exists():
        return pd.DataFrame()
    try:
        with open(DATA_PATH, "r", encoding="utf-8") as f:
            data = json.load(f)
        df = pd.DataFrame(data)
        for col in ["date_start", "date_end"]:
            if col in df.columns:
                df[col] = pd.to_datetime(df[col])
        return df
    except:
        return pd.DataFrame()

df = load_data()

# ============ Helpers ============
def haversine_km(lat1, lon1, lat2, lon2):
    R = 6371.0
    dlat, dlon = math.radians(lat2 - lat1), math.radians(lon2 - lon1)
    a = math.sin(dlat/2)**2 + math.cos(math.radians(lat1)) * math.cos(math.radians(lat2)) * math.sin(dlon/2)**2
    return R * 2 * math.atan2(math.sqrt(a), math.sqrt(1-a))

def filter_by_distance(df, lat, lon, radius):
    if radius <= 0 or df.empty:
        return df
    result = df[df["lat"].notna() & df["lon"].notna()].copy()
    if result.empty:
        return result
    result["distance_km"] = result.apply(lambda r: haversine_km(lat, lon, float(r["lat"]), float(r["lon"])), axis=1)
    return result[result["distance_km"] <= radius].sort_values("distance_km")

def filter_by_date(df, preset):
    if df.empty or preset == "All":
        return df
    today = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
    if preset == "Today":
        return df[df["date_start"].dt.date == today.date()]
    elif preset == "This Week":
        return df[(df["date_start"] >= today) & (df["date_start"] < today + timedelta(days=7))]
    elif preset == "This Month":
        next_month = (today.replace(day=28) + timedelta(days=4)).replace(day=1)
        return df[(df["date_start"] >= today) & (df["date_start"] < next_month)]
    return df

def format_price(p):
    return "Free" if p == 0 else f"{int(p)} TMT"

def format_dt(dt):
    return dt.strftime("%b %d • %I:%M %p")

# ============ Session State ============
if "saved" not in st.session_state:
    st.session_state.saved = set()
if "center" not in st.session_state:
    st.session_state.center = [DEFAULT_LAT, DEFAULT_LON]
if "radius" not in st.session_state:
    st.session_state.radius = 0.0
if "detail" not in st.session_state:
    st.session_state.detail = None

# ============ Header ============
st.markdown("# 🎟️ Local Events")

if not df.empty:
    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Events", len(df))
    c2.metric("Cities", df["city"].nunique())
    c3.metric("Free", len(df[df["price"] == 0]))
    c4.metric("Upcoming", len(df[df["date_start"] >= datetime.now()]))

st.divider()

# ============ Sidebar ============
with st.sidebar:
    st.markdown("## 🔍 Filters")
    
    f_city = st.selectbox("City", ["All"] + list(CITIES.keys()))
    f_date = st.radio("Date", ["All", "Today", "This Week", "This Month"])
    f_cats = st.multiselect("Categories", list(CATEGORIES.keys()))
    max_p = int(df["price"].max()) if not df.empty else 200
    f_price = st.slider("Max Price", 0, max_p, max_p)
    f_search = st.text_input("Search")
    
    st.divider()
    st.markdown("## 🗺️ Location")
    
    # Radius slider - THE MAIN CONTROL
    st.session_state.radius = st.slider(
        "Search Radius (km)", 
        min_value=0.0, 
        max_value=50.0, 
        value=st.session_state.radius,
        step=1.0,
        help="0 = show all events"
    )
    
    # Quick city buttons
    st.markdown("**Jump to:**")
    cols = st.columns(2)
    for i, (city, coords) in enumerate(CITIES.items()):
        with cols[i % 2]:
            if st.button(city, key=f"c_{city}", use_container_width=True):
                st.session_state.center = list(coords)
                st.rerun()
    
    if st.button("🔄 Reset", use_container_width=True):
        st.session_state.center = [DEFAULT_LAT, DEFAULT_LON]
        st.session_state.radius = 0.0
        st.rerun()

# ============ Apply Filters ============
filtered = df.copy() if not df.empty else pd.DataFrame()

if not filtered.empty:
    if f_city != "All":
        filtered = filtered[filtered["city"] == f_city]
    if f_cats:
        filtered = filtered[filtered["category"].isin(f_cats)]
    filtered = filtered[filtered["price"] <= f_price]
    filtered = filter_by_date(filtered, f_date)
    if f_search:
        q = f_search.lower()
        filtered = filtered[
            filtered["title"].str.lower().str.contains(q, na=False) |
            filtered["venue"].str.lower().str.contains(q, na=False)
        ]
    if st.session_state.radius > 0:
        filtered = filter_by_distance(
            filtered,
            st.session_state.center[0],
            st.session_state.center[1],
            st.session_state.radius
        )

# ============ Detail View ============
if st.session_state.detail and not df.empty:
    evt = df[df["id"] == st.session_state.detail]
    if not evt.empty:
        r = evt.iloc[0]
        with st.container(border=True):
            col1, col2 = st.columns([5, 1])
            col1.markdown(f"### {CATEGORIES.get(r['category'], {}).get('icon', '📌')} {r['title']}")
            if col2.button("❌"):
                st.session_state.detail = None
                st.rerun()
            st.caption(f"{r['category']} • {r['city']} • {r['venue']}")
            st.write(r.get("description", ""))
            st.markdown(f"**📅** {format_dt(r['date_start'])} | **💰** {format_price(r['price'])}")
            if pd.notna(r.get("lat")):
                st.link_button("🗺️ Directions", f"https://www.google.com/maps/dir/?api=1&destination={r['lat']},{r['lon']}")
        st.divider()

# ============ Tabs ============
tabs = st.tabs(["📋 Events", "🗺️ Map", "⭐ Saved"])

# Tab 1: Events
with tabs[0]:
    st.subheader(f"📋 {len(filtered)} Events")
    
    if filtered.empty:
        st.info("No events found")
    else:
        for _, r in filtered.iterrows():
            with st.container(border=True):
                c1, c2, c3 = st.columns([1, 5, 1])
                c1.markdown(f"### {CATEGORIES.get(r['category'], {}).get('icon', '📌')}")
                with c2:
                    st.markdown(f"**{r['title']}**")
                    st.caption(f"📍 {r['venue']} • {r['city']} • {format_dt(r['date_start'])} • {format_price(r['price'])}")
                    if "distance_km" in filtered.columns and pd.notna(r.get("distance_km")):
                        st.caption(f"📏 {r['distance_km']:.1f} km")
                with c3:
                    if st.button("📄", key=f"d_{r['id']}", help="Details"):
                        st.session_state.detail = r["id"]
                        st.rerun()
                    is_saved = r["id"] in st.session_state.saved
                    if st.button("❤️" if is_saved else "🤍", key=f"s_{r['id']}", help="Save"):
                        if is_saved:
                            st.session_state.saved.discard(r["id"])
                        else:
                            st.session_state.saved.add(r["id"])
                        st.rerun()

# Tab 2: Map - SIMPLE CLICK TO SET CENTER
with tabs[1]:
    st.subheader("🗺️ Map")
    
    # Info
    if st.session_state.radius > 0:
        st.success(f"📍 Showing events within **{st.session_state.radius:.0f} km** of center. **Click map to move center.**", icon="✅")
    else:
        st.info("ℹ️ Set a radius in the sidebar, then **click anywhere on the map** to set center.", icon="🗺️")
    
    # Build map
    m = folium.Map(location=st.session_state.center, zoom_start=12, tiles="cartodbpositron")
    
    # Center marker
    folium.Marker(
        st.session_state.center,
        tooltip="📍 Search Center (click elsewhere to move)",
        icon=folium.Icon(color="red", icon="crosshairs", prefix="fa")
    ).add_to(m)
    
    # Radius circle
    if st.session_state.radius > 0:
        folium.Circle(
            st.session_state.center,
            radius=st.session_state.radius * 1000,
            color="#6366F1",
            weight=2,
            fill=True,
            fill_opacity=0.15,
            tooltip=f"{st.session_state.radius:.0f} km radius"
        ).add_to(m)
    
    # Event markers
    for _, r in filtered.iterrows():
        if pd.notna(r.get("lat")) and pd.notna(r.get("lon")):
            color = CATEGORIES.get(r["category"], {}).get("color", "blue")
            icon_emoji = CATEGORIES.get(r["category"], {}).get("icon", "📌")
            folium.Marker(
                [r["lat"], r["lon"]],
                tooltip=f"{icon_emoji} {r['title']}",
                popup=f"<b>{r['title']}</b><br>{r['venue']}<br>{format_price(r['price'])}",
                icon=folium.Icon(color=color, icon="info-sign")
            ).add_to(m)
    
    # Render map - ONLY capture clicks
    out = st_folium(m, height=500, use_container_width=True, returned_objects=["last_clicked"], key="map")
    
    # Handle click - SET NEW CENTER
    if out and out.get("last_clicked"):
        click = out["last_clicked"]
        new_lat, new_lon = click["lat"], click["lng"]
        # Only update if significantly different (avoid micro-movements)
        if abs(new_lat - st.session_state.center[0]) > 0.001 or abs(new_lon - st.session_state.center[1]) > 0.001:
            st.session_state.center = [new_lat, new_lon]
            st.toast(f"📍 Center moved to {new_lat:.4f}, {new_lon:.4f}")
            st.rerun()
    
    # Quick info
    st.caption(f"Center: {st.session_state.center[0]:.4f}, {st.session_state.center[1]:.4f} | Radius: {st.session_state.radius:.0f} km | Events: {len(filtered)}")

# Tab 3: Saved
with tabs[2]:
    st.subheader("⭐ Saved")
    if not st.session_state.saved:
        st.info("Click ❤️ on events to save them")
    else:
        saved_df = df[df["id"].isin(st.session_state.saved)]
        for _, r in saved_df.iterrows():
            with st.container(border=True):
                c1, c2 = st.columns([5, 1])
                c1.markdown(f"**{r['title']}** • {r['city']} • {format_price(r['price'])}")
                if c2.button("❌", key=f"rm_{r['id']}"):
                    st.session_state.saved.discard(r["id"])
                    st.rerun()

st.divider()
st.caption("🎟️ Local Events v2.0")
