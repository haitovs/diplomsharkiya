import streamlit as st
from utils.data_loader import load_data, get_event_image_base64
from utils.i18n import t, t_cat, render_language_selector
from state_manager import get_state
from components.styles import (
    inject_custom_css, render_section_header,
    render_event_card_html, get_category_color_hex
)
from config import CATEGORY_CONFIG

st.set_page_config(page_title="Saved | Event Discovery", page_icon="⭐", layout="wide")

inject_custom_css()
render_language_selector()

df = load_data()
state = get_state()

st.title(f"⭐ {t('saved_page_title')}")

if not state.ui.saved_events:
    st.markdown(f"""
    <div style="
        text-align: center; padding: 3rem 2rem;
        background: #141B34; border: 1px dashed rgba(99,102,241,0.3);
        border-radius: 16px; margin: 2rem 0;
    ">
        <p style="font-size: 3rem; margin-bottom: 0.5rem;">🤍</p>
        <h3 style="color: #F8FAFC; margin-bottom: 0.5rem;">{t('no_saved_events')}</h3>
        <p style="color: #94A3B8;">{t('saved_events_desc')}</p>
    </div>
    """, unsafe_allow_html=True)
else:
    saved_df = df[df["id"].isin(state.ui.saved_events)]

    if saved_df.empty:
        st.warning(t("no_events"))
    else:
        render_section_header(
            f"{len(saved_df)} {t('saved_page_title')}",
            t("saved_page_subtitle")
        )

        for _, row in saved_df.iterrows():
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

            col_spacer, col_remove = st.columns([5, 1])
            with col_remove:
                if st.button(f"💔 {t('remove')}", key=f"remove_{row['id']}"):
                    state.ui.toggle_save(row["id"])
                    st.rerun()
