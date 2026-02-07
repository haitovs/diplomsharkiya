import streamlit as st
from state_manager import get_state
import pathlib

# Page Config
st.set_page_config(
    page_title="Sharkiya Event Discovery",
    page_icon="🎟️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Initialize State
state = get_state()

# Landing Page Content
st.markdown("""
<div style="background: linear-gradient(135deg, #6366F1 0%, #10B981 100%); padding: 3rem; border-radius: 12px; margin-bottom: 2rem; text-align: center; color: white;">
    <h1 style="color: white !important; margin-bottom: 0.5rem;">🎟️ Sharkiya Event Discovery</h1>
    <h3 style="color: rgba(255,255,255,0.9) !important; font-weight: 400;">Your Gateway to Local Events in Turkmenistan</h3>
</div>
""", unsafe_allow_html=True)

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
col1, col2, col3 = st.columns(3)
with col1:
    with st.container(border=True):
        st.subheader("📋 Browse")
        st.write("Find concerts, workshops, and more.")
        if st.button("Go to Events", use_container_width=True):
            st.switch_page("pages/1_📋_Events.py")

with col2:
    with st.container(border=True):
        st.subheader("🗺️ Map")
        st.write("Explore events near you interactively.")
        if st.button("Open Map", use_container_width=True):
            st.switch_page("pages/2_🗺️_Map.py")

with col3:
    with st.container(border=True):
        st.subheader("⭐ Saved")
        st.write("Manage your interested events.")
        if st.button("View Saved", use_container_width=True):
            st.switch_page("pages/3_⭐_Saved_Events.py")

# Featured Section
st.markdown("### 🔥 Featured Events")
if not df.empty:
    featured = df.sort_values("popularity", ascending=False).head(3)
    for _, row in featured.iterrows():
        with st.container(border=True):
            fc1, fc2 = st.columns([1, 4])
            with fc1:
                 # Category Icon
                custom_icon = row.get('icon')
                if custom_icon and (pathlib.Path("assets/icons") / f"{custom_icon}.png").exists():
                    st.image(str(pathlib.Path("assets/icons") / f"{custom_icon}.png"), width=40)
                else:
                    st.markdown("## ⭐")
            with fc2:
                st.markdown(f"**{row['title']}** — {row['city']}")
                st.caption(row.get('description', '')[:100] + "...")
else:
    st.info("No events to display.")
