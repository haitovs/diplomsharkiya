import streamlit as st
from state_manager import get_state
from components.styles import inject_custom_css, render_hero, render_section_header, render_event_card_html, get_category_color_hex
from utils.i18n import t, t_cat, render_language_selector
from utils.data_loader import get_event_image_base64

# Page Config
st.set_page_config(
    page_title="Event Discovery",
    page_icon="🎟️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Inject Custom Styles
inject_custom_css()

# Language Selector
render_language_selector()

# Initialize State
state = get_state()

# Hero Banner
render_hero(
    title=t("app_title"),
    subtitle=t("app_subtitle"),
    icon="🎟️"
)

from utils.data_loader import load_data
df = load_data()

# Stats Row
c1, c2, c3 = st.columns(3)
with c1:
    st.metric(f"🎉 {t('upcoming_events')}", len(df), delta=t("live_now"))
with c2:
    st.metric(f"🏙️ {t('cities_covered')}", df["city"].nunique() if not df.empty else 0)
with c3:
    st.metric(f"❤️ {t('community')}", t("growing"))

st.divider()

# Navigation Cards
render_section_header(t("quick_navigation"), t("jump_to_section"))

col1, col2, col3 = st.columns(3)
with col1:
    with st.container(border=True):
        st.markdown(f"### {t('browse_events')}")
        st.markdown(t("browse_events_desc"))
        if st.button(t("go_to_events"), use_container_width=True, type="primary"):
            st.switch_page("pages/1_📋_Events.py")

with col2:
    with st.container(border=True):
        st.markdown(f"### {t('interactive_map')}")
        st.markdown(t("interactive_map_desc"))
        if st.button(t("open_map"), use_container_width=True, type="primary"):
            st.switch_page("pages/2_🗺️_Map.py")

with col3:
    with st.container(border=True):
        st.markdown(f"### {t('saved_events')}")
        st.markdown(t("saved_events_desc"))
        if st.button(t("view_saved"), use_container_width=True, type="primary"):
            st.switch_page("pages/3_⭐_Saved_Events.py")

st.divider()

# Featured Events — HTML cards
render_section_header(t("featured_events"), t("featured_events_desc"))

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

        img_uri = get_event_image_base64(row.get("image", ""))

        st.markdown(render_event_card_html(
            title=row.get("title", "Untitled"),
            venue=row.get("venue", "TBA"),
            city=row.get("city", "Unknown"),
            date_str=date_str,
            price=row.get("price", 0),
            category=t_cat(cat),
            cat_icon=cat_icon,
            cat_color=cat_color,
            description=row.get("description", ""),
            free_text=t("free"),
            image_data_uri=img_uri,
        ), unsafe_allow_html=True)
else:
    st.info(t("no_events"))
