import streamlit as st
from utils.data_loader import load_data
from state_manager import get_state
from components.styles import (
    inject_custom_css, render_section_header,
    render_event_card_html, get_category_color_hex
)
from config import CATEGORY_CONFIG

st.set_page_config(page_title="Saved | Event Discovery", page_icon="⭐", layout="wide")

inject_custom_css()

df = load_data()
state = get_state()

st.title("⭐ Saved Events")

if not state.ui.saved_events:
    st.markdown("""
    <div style="
        text-align: center; padding: 3rem 2rem;
        background: #141B34; border: 1px dashed rgba(99,102,241,0.3);
        border-radius: 16px; margin: 2rem 0;
    ">
        <p style="font-size: 3rem; margin-bottom: 0.5rem;">🤍</p>
        <h3 style="color: #F8FAFC; margin-bottom: 0.5rem;">No saved events yet</h3>
        <p style="color: #94A3B8;">Browse the Events List and tap the heart icon to save events here.</p>
    </div>
    """, unsafe_allow_html=True)
else:
    saved_df = df[df["id"].isin(state.ui.saved_events)]

    if saved_df.empty:
        st.warning("Saved events not found in database (IDs may have changed).")
    else:
        render_section_header(
            f"You have {len(saved_df)} saved event{'s' if len(saved_df) != 1 else ''}",
            "Your bookmarked events"
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

            col_spacer, col_remove = st.columns([5, 1])
            with col_remove:
                if st.button("💔 Remove", key=f"remove_{row['id']}"):
                    state.ui.toggle_save(row["id"])
                    st.rerun()
