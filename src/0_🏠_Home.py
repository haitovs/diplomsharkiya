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
    icon="🎟️",
    badge=t("event_discovery_platform"),
)

from utils.data_loader import load_data
df = load_data()

# Stats Row — rendered as HTML for guaranteed equal height
_ev_count = len(df)
_city_count = df["city"].nunique() if not df.empty else 0
st.markdown(f"""
<div style="display: flex; gap: 1rem; margin-bottom: 0.5rem;">
    <div style="flex:1; background: linear-gradient(135deg,#141B34,#1A2238);
        border:1px solid rgba(99,102,241,0.15); border-radius:12px;
        padding:1rem 1.25rem;">
        <p style="color:#94A3B8; font-weight:500; font-size:0.85rem;
            text-transform:uppercase; letter-spacing:0.05em; margin:0;">
            🎉 {t('upcoming_events')}</p>
        <p style="color:#F8FAFC; font-weight:700; font-size:1.75rem; margin:0.25rem 0 0 0;">
            {_ev_count}</p>
        <p style="color:#10B981; font-size:0.85rem; margin:0.15rem 0 0 0;">↑ {t('live_now')}</p>
    </div>
    <div style="flex:1; background: linear-gradient(135deg,#141B34,#1A2238);
        border:1px solid rgba(99,102,241,0.15); border-radius:12px;
        padding:1rem 1.25rem;">
        <p style="color:#94A3B8; font-weight:500; font-size:0.85rem;
            text-transform:uppercase; letter-spacing:0.05em; margin:0;">
            🏙️ {t('cities_covered')}</p>
        <p style="color:#F8FAFC; font-weight:700; font-size:1.75rem; margin:0.25rem 0 0 0;">
            {_city_count}</p>
        <p style="color:transparent; font-size:0.85rem; margin:0.15rem 0 0 0;">.</p>
    </div>
    <div style="flex:1; background: linear-gradient(135deg,#141B34,#1A2238);
        border:1px solid rgba(99,102,241,0.15); border-radius:12px;
        padding:1rem 1.25rem;">
        <p style="color:#94A3B8; font-weight:500; font-size:0.85rem;
            text-transform:uppercase; letter-spacing:0.05em; margin:0;">
            ❤️ {t('community')}</p>
        <p style="color:#F8FAFC; font-weight:700; font-size:1.75rem; margin:0.25rem 0 0 0;">
            {t('growing')}</p>
        <p style="color:transparent; font-size:0.85rem; margin:0.15rem 0 0 0;">.</p>
    </div>
</div>
""", unsafe_allow_html=True)

st.divider()

# Navigation Cards
render_section_header(t("quick_navigation"), t("jump_to_section"))

NAV_CARDS = [
    {"title": t("browse_events"), "desc": t("browse_events_desc"), "btn": t("go_to_events"), "page": "pages/1_📋_Events.py"},
    {"title": t("interactive_map"), "desc": t("interactive_map_desc"), "btn": t("open_map"), "page": "pages/2_🗺️_Map.py"},
    {"title": t("saved_events"), "desc": t("saved_events_desc"), "btn": t("view_saved"), "page": "pages/3_⭐_Saved_Events.py"},
]

st.markdown("""
<div style="display: flex; gap: 1rem; margin-bottom: 1rem;">
""" + "".join(f"""
<div style="
    flex: 1; padding: 1.5rem;
    background: #141B34; border: 1px solid rgba(99,102,241,0.15);
    border-radius: 12px; display: flex; flex-direction: column;
    min-height: 200px;
">
    <h3 style="margin: 0 0 0.5rem 0; font-size: 1.2rem; font-weight: 600; color: #F8FAFC;">{c['title']}</h3>
    <p style="color: #94A3B8; font-size: 0.9rem; flex: 1;">{c['desc']}</p>
</div>
""" for c in NAV_CARDS) + "</div>", unsafe_allow_html=True)

nav_cols = st.columns(3)
for i, card in enumerate(NAV_CARDS):
    with nav_cols[i]:
        if st.button(card["btn"], use_container_width=True, type="primary", key=f"nav_{i}"):
            st.switch_page(card["page"])

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
