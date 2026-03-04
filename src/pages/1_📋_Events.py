import streamlit as st
from utils.data_loader import load_data, get_event_image_base64
from utils.filters import apply_filters
from utils.i18n import t, t_cat, render_language_selector
from state_manager import get_state
from components.styles import (
    inject_custom_css, render_section_header,
    render_event_card_html, get_category_color_hex
)
from components.ui_components import payment_dialog
from config import CATEGORY_CONFIG

# Page Config
st.set_page_config(page_title="Events | Event Discovery", page_icon="📋", layout="wide")

inject_custom_css()
render_language_selector()

# Load Data & State
df = load_data()
state = get_state()

# Title
st.title(f"📋 {t('events_page_title')}")

if df.empty:
    st.error(t("no_events"))
    st.stop()

# --- SIDEBAR FILTERS ---
with st.sidebar:
    st.header(f"🔍 {t('filter_by_category')}")

    # Search
    state.filters.search_query = st.text_input(
        t("search_events"), value=state.filters.search_query, placeholder=t("search_events")
    )

    # City
    city_options = [t("all_cities")] + sorted(df["city"].unique().tolist())
    current_city = state.filters.city
    if current_city == "All Cities":
        current_city = t("all_cities")
    state.filters.city = st.selectbox(
        t("event_city"),
        city_options,
        index=city_options.index(current_city) if current_city in city_options else 0
    )
    # Map translated "All Cities" back to internal value
    if state.filters.city == t("all_cities"):
        state.filters.city = "All Cities"

    # Categories
    cat_options = sorted(df["category"].unique().tolist())
    state.filters.categories = st.multiselect(
        t("filter_by_category"), cat_options, default=state.filters.categories
    )

    # Date — translate labels but map back to internal English values
    date_keys = ["All", "Today", "This Week", "This Month"]
    date_labels = [t("all"), t("today"), t("this_week"), t("this_month")]
    current_idx = date_keys.index(state.filters.date_preset) if state.filters.date_preset in date_keys else 0
    selected_date_label = st.selectbox(
        t("event_date"), date_labels, index=current_idx
    )
    state.filters.date_preset = date_keys[date_labels.index(selected_date_label)]

    # Price
    if "price" in df.columns:
        max_p = int(df["price"].max())
        state.filters.max_price = st.slider(
            t("event_price"), 0, max_p, state.filters.max_price
        )

    if st.button(f"🗑️ {t('reset_filters')}", type="primary", use_container_width=True):
        state.reset_filters()
        st.rerun()

# --- APPLY FILTERS ---
filtered_df = apply_filters(df, state.filters)

# --- DISPLAY ---
render_section_header(
    f"{len(filtered_df)} {t('events_found')}",
    t("events_page_subtitle")
)

if filtered_df.empty:
    st.info(t("no_events"))
else:
    for _, row in filtered_df.iterrows():
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
        is_saved = state.ui.is_saved(row.get("id"))
        event_price = row.get("price", 0)
        event_id = row.get("id")

        card_col, buy_col, like_col = st.columns([12, 2, 1])
        with card_col:
            st.markdown(render_event_card_html(
                title=row.get("title", "Untitled"),
                venue=row.get("venue", "TBA"),
                city=row.get("city", "Unknown"),
                date_str=date_str,
                price=event_price,
                category=t_cat(cat),
                cat_icon=cat_icon,
                cat_color=cat_color,
                description=row.get("description", ""),
                free_text=t("free"),
                image_data_uri=img_uri,
            ), unsafe_allow_html=True)
        with buy_col:
            st.markdown("<div style='height:0.5rem'></div>", unsafe_allow_html=True)
            if event_price > 0:
                if state.payments.has_purchased(event_id):
                    st.markdown(
                        f"<span style='color:#10B981;font-weight:600;font-size:0.85rem;'>{t('already_purchased')}</span>",
                        unsafe_allow_html=True,
                    )
                else:
                    if st.button(
                        t("buy_ticket"),
                        key=f"buy_{event_id}",
                        type="primary",
                    ):
                        st.session_state["_payment_event"] = {
                            "id": event_id,
                            "title": row.get("title", ""),
                            "price": event_price,
                        }
                        payment_dialog()
        with like_col:
            st.markdown("<div style='height:0.5rem'></div>", unsafe_allow_html=True)
            if st.button(
                "❤️" if is_saved else "🤍",
                key=f"save_{event_id}",
                help=t("save"),
            ):
                state.ui.toggle_save(event_id)
                st.rerun()
