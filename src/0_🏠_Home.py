import streamlit as st
from state_manager import get_state
from components.styles import inject_custom_css, render_hero, render_section_header, render_event_card_html, get_category_color_hex
import pathlib

# Page Config
st.set_page_config(
    page_title="Sharkiya Event Discovery",
    page_icon="🎟️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Inject Custom Styles
inject_custom_css()

# Initialize State
state = get_state()

# Hero Banner
render_hero(
    title="Sharkiya Event Discovery",
    subtitle="Your Gateway to Local Events in Turkmenistan",
    icon="🎟️"
)

from utils.data_loader import load_data
df = load_data()

# Stats Row
c1, c2, c3 = st.columns(3)
with c1:
    st.metric("🎉 Upcoming Events", len(df), delta="Live now")
with c2:
    st.metric("🏙️ Cities Covered", df["city"].nunique() if not df.empty else 0)
with c3:
    st.metric("❤️ Community", "Growing")

st.divider()

# Navigation Cards
render_section_header("🧭 Quick Navigation", "Jump to any section")

col1, col2, col3 = st.columns(3)
with col1:
    with st.container(border=True):
        st.markdown("### 📋 Browse Events")
        st.markdown("Find concerts, workshops, and more in your city.")
        if st.button("Go to Events →", use_container_width=True, type="primary"):
            st.switch_page("pages/1_📋_Events.py")

with col2:
    with st.container(border=True):
        st.markdown("### 🗺️ Interactive Map")
        st.markdown("Explore events near you on an interactive map.")
        if st.button("Open Map →", use_container_width=True, type="primary"):
            st.switch_page("pages/2_🗺️_Map.py")

with col3:
    with st.container(border=True):
        st.markdown("### ⭐ Saved Events")
        st.markdown("Manage your bookmarked events.")
        if st.button("View Saved →", use_container_width=True, type="primary"):
            st.switch_page("pages/3_⭐_Saved_Events.py")

st.divider()

# Featured Events — HTML cards
render_section_header("🔥 Featured Events", "Most popular events right now")

if not df.empty:
    from config import CATEGORY_CONFIG
    featured = df.sort_values("popularity", ascending=False).head(5)
    for _, row in featured.iterrows():
        cat = row.get("category", "Event")
        cat_cfg = CATEGORY_CONFIG.get(cat, {})
        cat_icon = cat_cfg.get("icon", "📌")
        cat_color = get_category_color_hex(cat)

        date_str = ""
        start = row.get("date_start")
        if start:
            try:
                date_str = start.strftime("%b %d, %Y · %I:%M %p")
            except Exception:
                date_str = str(start)

        st.markdown(render_event_card_html(
            title=row.get("title", "Untitled"),
            venue=row.get("venue", "TBA"),
            city=row.get("city", "Unknown"),
            date_str=date_str,
            price=row.get("price", 0),
            category=cat,
            cat_icon=cat_icon,
            cat_color=cat_color,
            description=row.get("description", ""),
        ), unsafe_allow_html=True)
else:
    st.info("No events to display.")
