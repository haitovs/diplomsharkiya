import streamlit as st
from utils.data_loader import load_data, get_event_image_base64
from utils.filters import apply_filters
from utils.i18n import t, t_cat, render_language_selector
from state_manager import get_state
from components.styles import (
    inject_custom_css, render_section_header,
    render_event_card_html, get_category_color_hex
)
from components.payment import payment_dialog
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

# --- PURCHASED TICKETS LIST ---
if state.payments.transactions:
    with st.expander(f"🎫 {t('my_tickets')} ({len(state.payments.transactions)})", expanded=False):
        for txn in state.payments.get_history():
            tc1, tc2, tc3, tc4 = st.columns([4, 2, 2, 2])
            with tc1:
                st.markdown(f"**{txn['title']}**")
            with tc2:
                st.caption(f"💰 {int(txn['amount'])} TMT")
            with tc3:
                st.caption(f"🆔 `{txn['txn_id']}`")
            with tc4:
                st.caption(f"📅 {txn['timestamp'][:10]}")

# --- SIDEBAR FILTERS ---
with st.sidebar:
    st.header(f"🔍 {t('filter_by_category')}")

    state.filters.search_query = st.text_input(
        t("search_events"), value=state.filters.search_query, placeholder=t("search_events")
    )

    city_options = [t("all_cities")] + sorted(df["city"].unique().tolist())
    current_city = state.filters.city
    if current_city == "All Cities":
        current_city = t("all_cities")
    state.filters.city = st.selectbox(
        t("event_city"),
        city_options,
        index=city_options.index(current_city) if current_city in city_options else 0
    )
    if state.filters.city == t("all_cities"):
        state.filters.city = "All Cities"

    cat_options = sorted(df["category"].unique().tolist())
    state.filters.categories = st.multiselect(
        t("filter_by_category"), cat_options, default=state.filters.categories
    )

    date_keys = ["All", "Today", "This Week", "This Month"]
    date_labels = [t("all"), t("today"), t("this_week"), t("this_month")]
    current_idx = date_keys.index(state.filters.date_preset) if state.filters.date_preset in date_keys else 0
    selected_date_label = st.selectbox(
        t("event_date"), date_labels, index=current_idx
    )
    state.filters.date_preset = date_keys[date_labels.index(selected_date_label)]

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

        event_id = row.get("id", "")
        img_uri = get_event_image_base64(row.get("image", ""))
        is_saved = state.ui.is_saved(event_id)
        event_price = row.get("price", 0)
        purchase_count = state.payments.get_purchase_count(event_id)

        card_html = render_event_card_html(
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
        )

        # Card + actions in a tight row
        card_col, act_col = st.columns([14, 1])
        with card_col:
            st.markdown(card_html, unsafe_allow_html=True)
        with act_col:
            # Buy ticket button (paid events only)
            if event_price > 0:
                if st.button("🎫", key=f"buy_{event_id}", help=t("buy_ticket")):
                    st.session_state["_payment_event"] = {
                        "id": event_id,
                        "title": row.get("title", ""),
                        "price": event_price,
                    }
                    payment_dialog()
                # Purchased count indicator
                if purchase_count > 0:
                    st.markdown(
                        f"<div style='text-align:center;font-size:0.6rem;color:#10B981;font-weight:600;margin-top:-0.5rem;'>✅×{purchase_count}</div>",
                        unsafe_allow_html=True,
                    )
            # Like/save button
            if st.button(
                "❤️" if is_saved else "🤍",
                key=f"save_{event_id}",
                help=t("save"),
            ):
                state.ui.toggle_save(event_id)
                st.rerun()
