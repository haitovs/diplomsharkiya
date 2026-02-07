import streamlit as st
from state_manager import get_state

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
st.title("🎟️ Sharkiya Event Discovery")

st.markdown("""
### Discover the Best Local Events in Turkmenistan
Welcome to the upgraded experience. Browse concerts, workshops, and more.

### 🌟 What's New
- **Modular Design**: Faster and cleaner.
- **Interactive Map**: Find events near you.
- **Saved Events**: Keep track of what you love.

👇 **Get Started**
""")

c1, c2, c3 = st.columns(3)
with c1:
    if st.button("📋 Browse Events", type="primary", use_container_width=True):
        st.switch_page("pages/1_📋_Events.py")
with c2:
    if st.button("🗺️ Open Map", use_container_width=True):
        st.switch_page("pages/2_🗺️_Map.py")
with c3:
    if st.button("⭐ Saved Events", use_container_width=True):
        st.switch_page("pages/3_⭐_Saved_Events.py")

st.divider()
st.caption("Sharkiya Event Discovery v5.0 (Modular Upgrade)")
