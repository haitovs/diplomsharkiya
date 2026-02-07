# 🎟️ Local Events - Sharkiya Event Discovery  
# v5.0 - Advanced State Management

import streamlit as st
import pandas as pd
import pathlib
import json
from datetime import datetime, timedelta
import folium
from streamlit_folium import st_folium
from state_manager import get_state

# ============ PAGE CONFIG ============
st.set_page_config(
    page_title="Local Events • Sharkiya",
    page_icon="🎟️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ============ PROFESSIONAL CSS ============
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');

* { font-family: 'Inter', sans-serif !important; }

:root {
    --bg-primary: #0A0E27;
    --bg-secondary: #141B34;
    --bg-card: #1A2238;
    --accent-primary: #6366F1;
    --accent-secondary: #10B981;
    --text-primary: #F8FAFC;
    --text-secondary: #94A3B8;
    --text-muted: #64748B;
    --border-subtle: #1E293B;
    --shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.3);
}

.main > div { padding: 2rem; }
[data-testid="stAppViewContainer"], [data-testid="stApp"] { 
    background: var(--bg-primary) !important; 
}

/* === COMPLETELY HIDE SIDEBAR COLLAPSE === */
button[kind="header"] { display: none !important; }
[data-testid="collapsedControl"] { display: none !important; }
[data-testid="stSidebarCollapsedControl"] { display: none !important; }
section[data-testid="stSidebar"] button[aria-label*="collapse"] { display: none !important; }

/* === SIDEBAR === */
section[data-testid="stSidebar"] {
    background: var(--bg-secondary) !important;
    border-right: 1px solid var(--border-subtle);
    min-width: 320px !important;
    max-width: 320px !important;
}

section[data-testid="stSidebar"] > div { padding: 1.5rem 1rem !important; }

section[data-testid="stSidebar"] h3 {
    font-size: 0.75rem;
    font-weight: 600;
    color: var(--text-muted) !important;
    text-transform: uppercase;
    letter-spacing: 0.05em;
    margin-top: 1rem !important;
    margin-bottom: 0.5rem !important;
}

section[data-testid="stSidebar"] [data-testid="stVerticalBlock"] { gap: 0.5rem !important; }
section[data-testid="stSidebar"] [data-testid="stMarkdownContainer"] { margin-bottom: 0.25rem !important; }

/* Full width inputs */
section[data-testid="stSidebar"] [data-testid="stSelectbox"],
section[data-testid="stSidebar"] [data-testid="stMultiSelect"],
section[data-testid="stSidebar"] [data-testid="stTextInput"],
section[data-testid="stSidebar"] [data-testid="stSlider"] { width: 100% !important; }

section[data-testid="stSidebar"] [data-testid="stSelectbox"] > div,
section[data-testid="stSidebar"] [data-testid="stMultiSelect"] > div,
section[data-testid="stSidebar"] [data-testid="stTextInput"] > div input { width: 100% !important; }

section[data-testid="stSidebar"] h1 {
    font-size: 1.25rem;
    font-weight: 700;
    color: var(--text-primary) !important;
    margin-bottom: 0.5rem;
}

/* === STATS === */
[data-testid="stMetric"] {
    background: linear-gradient(135deg, var(--bg-card) 0%, var(--bg-secondary) 100%);
    border: 1px solid var(--border-subtle);
    border-radius: 12px;
    padding: 1.25rem;
    box-shadow: var(--shadow);
}

[data-testid="stMetricLabel"] {
    color: var(--text-secondary) !important;
    font-size: 0.75rem;
    font-weight: 500;
    text-transform: uppercase;
}

[data-testid="stMetricValue"] {
    color: var(--accent-primary) !important;
    font-size: 2rem;
    font-weight: 700;
}

/* === EVENT CARDS === */
[data-testid="stVerticalBlockBorderWrapper"] {
    background: var(--bg-card) !important;
    border: 1px solid var(--border-subtle) !important;
    border-radius: 12px !important;
    padding: 1.25rem !important;
    margin: 0.75rem 0 !important;
    transition: all 0.2s ease;
    box-shadow: var(--shadow);
}

[data-testid="stVerticalBlockBorderWrapper"]:hover {
    border-color: var(--accent-primary) !important;
    box-shadow: 0 8px 16px -2px rgba(99, 102, 241, 0.2);
    transform: translateY(-2px);
}

/* === TABS === */
[data-testid="stTabs"] { margin-top: 1.5rem; }
[data-testid="stTabs"] button {
    background: transparent !important;
    border-bottom: 2px solid transparent;
    color: var(--text-secondary) !important;
    padding: 0.75rem 1.5rem;
    font-weight: 500;
}

[data-testid="stTabs"] button[aria-selected="true"] {
    border-bottom-color: var(--accent-primary) !important;
    color: var(--text-primary) !important;
}

/* === BUTTONS === */
button {
    background: var(--bg-card) !important;
    border: 1px solid var(--border-subtle) !important;
    border-radius: 8px !important;
    padding: 0.6rem 1.2rem !important;
    color: var(--text-primary) !important;
    font-weight: 500;
    font-size: 0.875rem !important;
    transition: all 0.2s ease;
    min-height: 38px !important;
}

button:hover {
    border-color: var(--accent-primary) !important;
    background: rgba(99, 102, 241, 0.1) !important;
}

button[kind="primary"] {
    background: var(--accent-primary) !important;
    border-color: var(--accent-primary) !important;
}

/* === INPUTS === */
input, [data-baseweb="select"], textarea {
    background: var(--bg-card) !important;
    border: 1px solid var(--border-subtle) !important;
    border-radius: 8px !important;
    color: var(--text-primary) !important;
}

/* === ALERTS === */
[data-testid="stAlert"] {
    background: var(--bg-card) !important;
    border: 1px solid var(--border-subtle) !important;
    border-radius: 12px;
    padding: 1rem;
}

/* === DROPDOWNS === */
[data-baseweb="menu"] li {
    background: var(--bg-card) !important;
    color: var(--text-primary) !important;
}

[data-baseweb="menu"] li:hover {
    background: rgba(99, 102, 241, 0.2) !important;
}

h1, h2, h3 { color: var(--text-primary) !important; }
p, span { color: var(--text-secondary) !important; }
hr { border-color: var(--border-subtle); margin: 1.5rem 0; }
#MainMenu, footer, header { visibility: hidden; }

.category-badge {
    display: inline-block;
    padding: 0.25rem 0.75rem;
    border-radius: 6px;
    font-size: 0.75rem;
    font-weight: 600;
    background: rgba(99, 102, 241, 0.15);
    color: var(--accent-primary);
    border: 1px solid rgba(99, 102, 241, 0.3);
}

.price-tag {
    display: inline-block;
    padding: 0.25rem 0.75rem;
    border-radius: 6px;
    font-size: 0.875rem;
    font-weight: 600;
    background: rgba(16, 185, 129, 0.15);
    color: var(--accent-secondary);
}

.event-icon {
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 3rem;
    padding: 0.5rem;
}
</style>
""", unsafe_allow_html=True)

# ============ CONFIG ============
CITIES = {
    "Ashgabat": {"lat": 37.9601, "lon": 58.3261},
    "Mary": {"lat": 37.6005, "lon": 61.8302},
    "Türkmenabat": {"lat": 39.0733, "lon": 63.5786},
    "Dashoguz": {"lat": 41.8387, "lon": 59.9650},
    "Balkanabat": {"lat": 39.5104, "lon": 54.3672},
    "Awaza": {"lat": 40.0224, "lon": 52.9693},
}

CATEGORIES = {
    "Music": {"icon": "🎵", "color": "purple"},
    "Tech": {"icon": "💻", "color": "blue"},
    "Sports": {"icon": "⚽", "color": "green"},
    "Food": {"icon": "🍽️", "color": "orange"},
    "Art": {"icon": "🎨", "color": "pink"},
    "Market": {"icon": "🛍️", "color": "cadetblue"},
    "Film": {"icon": "🎬", "color": "red"},
    "Wellness": {"icon": "🧘", "color": "lightgreen"},
    "Business": {"icon": "💼", "color": "darkblue"},
    "Science": {"icon": "🔬", "color": "purple"},
    "Kids": {"icon": "👶", "color": "beige"},
    "Travel": {"icon": "✈️", "color": "lightblue"},
    "Community": {"icon": "👥", "color": "gray"},
}

DATA_PATH = pathlib.Path(__file__).parent / "events.json"

# ============ DATA LOADING ============
@st.cache_data(ttl=60)
def load_data():
    if not DATA_PATH.exists():
        return pd.DataFrame()
    try:
        with open(DATA_PATH, "r", encoding="utf-8") as f:
            data = json.load(f)
        if not isinstance(data, list):
            return pd.DataFrame()
        df = pd.DataFrame(data)
        for col in ["date_start", "date_end"]:
            if col in df.columns:
                df[col] = pd.to_datetime(df[col], errors="coerce")
        return df
    except Exception:
        return pd.DataFrame()

df = load_data()

# ============ STATE MANAGEMENT ============
state = get_state()

# ============ HELPERS ============
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

def format_dt(dt_val):
    if pd.isna(dt_val):
        return "TBD"
    return dt_val.strftime("%b %d, %Y • %I:%M %p")

# ============ TRACK ACTIVE TAB ============
# Use query params to track which tab is active
if "tab" in st.query_params:
    tab_name = st.query_params["tab"]
    if tab_name == "events":
        state.ui.active_tab = 0
    elif tab_name == "map":
        state.ui.active_tab = 1
    elif tab_name == "saved":
        state.ui.active_tab = 2

# ============ SIDEBAR WITH CONDITIONAL FILTERS ============
with st.sidebar:
    st.markdown("# 🎟️ Sharkiya Events")
    st.markdown("Discover local events in Turkmenistan")
    
    # COMMON FILTERS (all tabs)
    st.markdown("### 🔍 FILTERS")
    city_options = ["All Cities"] + sorted([c for c in CITIES.keys()])
    state.filters.city = st.selectbox(
        "Select City",
        city_options,
        index=city_options.index(state.filters.city) if state.filters.city in city_options else 0,
        key="city_filter",
        label_visibility="hidden"
    )
    
    st.markdown("### 📅 DATE")
    date_options = ["All", "Today", "This Week", "This Month"]
    state.filters.date_preset = st.radio(
        "Select Date",
        date_options,
        index=date_options.index(state.filters.date_preset) if state.filters.date_preset in date_options else 0,
        key="date_filter",
        label_visibility="hidden"
    )
    
    st.markdown("### 🏷️ CATEGORY")
    cat_options = sorted(list(CATEGORIES.keys()))
    state.filters.categories = st.multiselect(
        "Select Categories",
        cat_options,
        default=state.filters.categories,
        key="cat_filter",
        label_visibility="hidden"
    )
    
    # CONDITIONAL FILTERS BASED ON ACTIVE TAB
    if state.ui.active_tab == 0:  # Events List only
        st.markdown("### 💰 PRICE RANGE")
        max_p = 200
        if not df.empty and "price" in df.columns:
            max_price = df["price"].max()
            if pd.notna(max_price):
                max_p = int(max_price)
        state.filters.max_price = st.slider(
            "Select Price Range",
            0,
            max_p,
            state.filters.max_price if state.filters.max_price <= max_p else max_p,
            key="price_filter",
            label_visibility="hidden"
        )
        
        st.markdown("### 🔎 SEARCH")
        state.filters.search_query = st.text_input(
            "Search Events",
            value=state.filters.search_query,
            placeholder="Search events...",
            key="search_filter",
            label_visibility="hidden"
        )
        
        st.divider()
        
        st.markdown("### ⚡ SORT BY")
        sort_options = ["Date (Soonest)", "Price (Low to High)", "Price (High to Low)", "Popularity"]
        state.filters.sort_by = st.selectbox(
            "Sort By",
            sort_options,
            index=sort_options.index(state.filters.sort_by) if state.filters.sort_by in sort_options else 0,
            key="sort_filter",
            label_visibility="hidden"
        )
    
    elif state.ui.active_tab == 1:  # Map only
        st.markdown("### 🗺️ MAP SETTINGS")
        st.caption("Use the map controls to navigate")
        st.caption(f"Current zoom: {state.map.zoom}")
    
    st.divider()
    
    if st.button("🔄 Reset All Filters", use_container_width=True, type="primary"):
        state.reset_filters()
        st.rerun()

# ============ STATS BAR ============
if not df.empty:
    c1, c2, c3, c4 = st.columns(4)
    with c1:
        st.metric("📅 Total Events", len(df))
    with c2:
        st.metric("🏙️ Cities", df["city"].nunique() if "city" in df.columns else 0)
    with c3:
        st.metric("🆓 Free Events", len(df[df["price"] == 0]) if "price" in df.columns else 0)
    with c4:
        upcoming = len(df[df["date_start"] >= datetime.now()]) if "date_start" in df.columns else 0
        st.metric("⏰ Upcoming", upcoming)

st.divider()

# ============ APPLY FILTERS ============
filtered = df.copy() if not df.empty else pd.DataFrame()

if not filtered.empty:
    # Common filters
    if state.filters.city != "All Cities":
        filtered = filtered[filtered["city"] == state.filters.city]
    if state.filters.categories:
        filtered = filtered[filtered["category"].isin(state.filters.categories)]
    filtered = filter_by_date(filtered, state.filters.date_preset)
    
    # List-specific filters
    if state.ui.active_tab == 0:
        if "price" in filtered.columns:
            filtered = filtered[filtered["price"] <= state.filters.max_price]
        
        if state.filters.search_query:
            q = state.filters.search_query.lower()
            mask = pd.Series([False] * len(filtered), index=filtered.index)
            if "title" in filtered.columns:
                mask |= filtered["title"].str.lower().str.contains(q, na=False)
            if "venue" in filtered.columns:
                mask |= filtered["venue"].str.lower().str.contains(q, na=False)
            filtered = filtered[mask]
        
        # Sorting
        if not filtered.empty:
            if state.filters.sort_by == "Date (Soonest)" and "date_start" in filtered.columns:
                filtered = filtered.sort_values("date_start")
            elif state.filters.sort_by == "Price (Low to High)" and "price" in filtered.columns:
                filtered = filtered.sort_values("price")
            elif state.filters.sort_by == "Price (High to Low)" and "price" in filtered.columns:
                filtered = filtered.sort_values("price", ascending=False)
            elif state.filters.sort_by == "Popularity" and "popularity" in filtered.columns:
                filtered = filtered.sort_values("popularity", ascending=False)

# ============ DETAIL VIEW ============
if state.ui.detail_event_id and not df.empty:
    evt = df[df["id"] == state.ui.detail_event_id]
    if not evt.empty:
        r = evt.iloc[0]
        with st.container(border=True):
            col1, col2 = st.columns([8, 1])
            cat_icon = CATEGORIES.get(r.get("category", ""), {}).get("icon", "📌")
            
            with col1:
                st.markdown(f"## {cat_icon} {r.get('title', 'Event')}")
                st.markdown(f"<span class='category-badge'>{r.get('category', 'N/A')}</span>", 
                           unsafe_allow_html=True)
            
            with col2:
                if st.button("✕", key="close_detail", help="Close"):
                    state.ui.detail_event_id = None
                    st.rerun()
            
            st.markdown(f"**📍 Venue:** {r.get('venue', 'N/A')} • {r.get('city', 'N/A')}")
            st.markdown(f"**📅 When:** {format_dt(r.get('date_start'))}")
            
            desc = r.get("description", "")
            if desc:
                st.markdown(f"**📝 Description:**")
                st.markdown(f"_{desc}_")
            
            col_a, col_b, col_c = st.columns(3)
            with col_a:
                st.markdown(f"<div class='price-tag'>{format_price(r.get('price', 0))}</div>", 
                           unsafe_allow_html=True)
            with col_b:
                st.markdown(f"**⭐ Popularity:** {r.get('popularity', 0)}%")
            with col_c:
                lat, lon = r.get("lat"), r.get("lon")
                if pd.notna(lat) and pd.notna(lon):
                    st.link_button("🗺️ Directions", 
                                  f"https://www.google.com/maps/dir/?api=1&destination={lat},{lon}")
        st.divider()

# ============ TABS WITH QUERY PARAM TRACKING ============
def on_tab_change():
    """Callback to update active tab in state."""
    pass

tab_list = st.tabs(["📋 Events List", "🗺️ Interactive Map", "⭐ Saved Events"])

# Tab 1: Events List
with tab_list[0]:
    st.query_params.update({"tab": "events"})
    state.ui.active_tab = 0
    
    if filtered.empty:
        st.info("🔍 No events found", icon ="ℹ️")
    else:
        st.markdown(f"### Found {len(filtered)} Events")
        
        for _, r in filtered.iterrows():
            with st.container(border=True):
                cols = st.columns([1, 7, 1.5])
                
                cat_icon = CATEGORIES.get(r.get("category", ""), {}).get("icon", "📌")
                
                with cols[0]:
                    st.markdown(f"<div class='event-icon'>{cat_icon}</div>", unsafe_allow_html=True)
                
                with cols[1]:
                    st.markdown(f"**{r.get('title', 'Event')}**")
                    st.caption(f"📍 {r.get('venue', '')} • {r.get('city', '')}")
                    st.caption(f"📅 {format_dt(r.get('date_start'))}")
                    st.markdown(f"<span class='price-tag'>{format_price(r.get('price', 0))}</span>", 
                               unsafe_allow_html=True)
                
                with cols[2]:
                    if st.button("📄 Info", key=f"d_{r.get('id', '')}", use_container_width=True):
                        state.ui.detail_event_id = r.get("id")
                        st.rerun()
                    
                    is_saved = state.ui.is_saved(r.get("id"))
                    if st.button("❤️" if is_saved else "🤍 Save", 
                                key=f"s_{r.get('id', '')}", 
                                use_container_width=True):
                        was_saved = state.ui.toggle_save(r.get("id"))
                        st.toast("Saved!" if was_saved else "Removed", icon="❤️" if was_saved else "💔")

# Tab 2: Interactive Map
with tab_list[1]:
    st.query_params.update({"tab": "map"})
    state.ui.active_tab = 1
    
    if filtered.empty:
        st.info("🗺️ No events to display", icon="ℹ️")
    else:
        st.markdown(f"### Interactive Map - {len(filtered)} Events")
        
        try:
            m = folium.Map(
                location=state.map.center,
                zoom_start=state.map.zoom,
                tiles='OpenStreetMap'
            )
            
            for _, row in filtered.iterrows():
                if pd.notna(row.get("lat")) and pd.notna(row.get("lon")):
                    category = row.get("category", "")
                    color = CATEGORIES.get(category, {}).get("color", "blue")
                    icon = CATEGORIES.get(category, {}).get("icon", "📌")
                    
                    popup_html = f"""
                    <div style="font-family: Inter, sans-serif; min-width: 280px; padding: 16px;
                                background: #1A2238; border-radius: 12px; color: #F8FAFC;">
                        <div style="font-size: 18px; font-weight: 700; margin-bottom: 12px; color: #F8FAFC;
                                    border-bottom: 2px solid #6366F1; padding-bottom: 8px;">
                            {icon} {row.get('title', 'Event')}
                        </div>
                        <div style="margin: 8px 0; font-size: 14px; color: #94A3B8;">
                            <strong style="color: #6366F1;">📍</strong> {row.get('venue', '')}, {row.get('city', '')}
                        </div>
                        <div style="margin: 8px 0; font-size: 14px; color: #94A3B8;">
                            <strong style="color: #6366F1;">📅</strong> {format_dt(row.get('date_start'))}
                        </div>
                        <div style="margin-top: 12px; padding-top: 8px; border-top: 1px solid #334155;">
                            <span style="background: rgba(16, 185, 129, 0.2); color: #10B981;
                                        padding: 6px 12px; border-radius: 6px; font-weight: 600; font-size: 15px;">
                                💰 {format_price(row.get('price', 0))}
                            </span>
                        </div>
                    </div>
                    """
                    
                    folium.Marker(
                        location=[float(row["lat"]), float(row["lon"])],
                        popup=folium.Popup(popup_html, max_width=320),
                        tooltip=f"{icon} {row.get('title', 'Event')}",
                        icon=folium.Icon(color=color, icon="info-sign")
                    ).add_to(m)
            
            map_data = st_folium(m, width=None, height=600, returned_objects=["last_clicked"], key="event_map_v3")
            state.map.update_from_interaction(map_data)
            
            st.caption("💡 Click markers for details • Map remembers your position")
            
        except Exception as e:
            st.error(f"⚠️ Map error: {str(e)}")

# Tab 3: Saved Events
with tab_list[2]:
    st.query_params.update({"tab": "saved"})
    state.ui.active_tab = 2
    
    if not state.ui.saved_events:
        st.info("⭐ No saved events yet", icon="ℹ️")
    else:
        saved_df = df[df["id"].isin(state.ui.saved_events)] if not df.empty else pd.DataFrame()
        
        if saved_df.empty:
            st.warning("❌ Saved events not found", icon="⚠️")
        else:
            st.markdown(f"### Your {len(saved_df)} Saved Events")
            
            for _, r in saved_df.iterrows():
                with st.container(border=True):
                    cols = st.columns([1, 7, 1.5])
                    
                    cat_icon = CATEGORIES.get(r.get("category", ""), {}).get("icon", "📌")
                    
                    with cols[0]:
                        st.markdown(f"<div class='event-icon'>{cat_icon}</div>", unsafe_allow_html=True)
                    
                    with cols[1]:
                        st.markdown(f"**{r.get('title', 'Event')}**")
                        st.caption(f"📍 {r.get('city', '')} • {format_price(r.get('price', 0))}")
                    
                    with cols[2]:
                        if st.button("📄 Info", key=f"sd_{r.get('id', '')}", use_container_width=True):
                            state.ui.detail_event_id = r.get("id")
                            st.rerun()
                        if st.button("✕ Remove", key=f"rm_{r.get('id', '')}", use_container_width=True):
                            state.ui.toggle_save(r.get("id"))
                            st.toast("Removed from saved", icon="🗑️")

# Sync state at the end
state.sync_to_session_state()
