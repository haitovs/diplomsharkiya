import streamlit as st
from components.styles import inject_custom_css, render_hero

st.set_page_config(page_title="About | Sharkiya", page_icon="ℹ️")

inject_custom_css()

render_hero(
    title="About Sharkiya",
    subtitle="Your premier platform for local events in Turkmenistan",
    icon="ℹ️"
)

st.markdown("""
### 🎯 What is Sharkiya?

Sharkiya Event Discovery is a modern platform that connects people with local events
across Turkmenistan. From concerts and tech meetups to food festivals and art exhibitions
— discover what's happening in your city.

### ✨ Key Features
""")

col1, col2, col3 = st.columns(3)
with col1:
    with st.container(border=True):
        st.markdown("### 📋 Smart Browsing")
        st.markdown("Filter events by city, category, date, and price. Full-text search included.")
with col2:
    with st.container(border=True):
        st.markdown("### 🗺️ Interactive Map")
        st.markdown("Explore events geographically with rich popups showing all event details.")
with col3:
    with st.container(border=True):
        st.markdown("### ⭐ Save & Plan")
        st.markdown("Bookmark your favorite events to build your personal event calendar.")

st.markdown("""
### 🏙️ Cities Covered

| City | Region | Status |
|------|--------|--------|
| Ashgabat | Ahal | ✅ Active |
| Mary | Mary | ✅ Active |
| Türkmenabat | Lebap | ✅ Active |
| Dashoguz | Dashoguz | ✅ Active |
| Balkanabat | Balkan | ✅ Active |
| Awaza | Turkmenbashi | ✅ Active |

### 📬 For Event Organizers

Want to list your event on Sharkiya? Contact our admin team through the admin panel
to add your events to the platform.

---
*Version 5.0 • Built with Streamlit • Sharkiya Event Discovery*
""")
