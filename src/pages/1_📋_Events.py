import streamlit as st
import pathlib
from utils.data_loader import load_data
from utils.filters import apply_filters
from state_manager import get_state
from components.styles import (
    inject_custom_css, render_section_header,
    render_event_card_html, get_category_color_hex
)
from config import CATEGORY_CONFIG

# Page Config
st.set_page_config(page_title="Events | Sharkiya", page_icon="📋", layout="wide")

inject_custom_css()

# Load Data & State
df = load_data()
state = get_state()

# Title
st.title("📋 Events List")

if df.empty:
    st.error("No data found. Please check data/events.json.")
    st.stop()

# --- SIDEBAR FILTERS ---
with st.sidebar:
    st.header("🔍 Filter Events")

    # Search
    state.filters.search_query = st.text_input(
        "Search", value=state.filters.search_query, placeholder="Title, venue..."
    )

    # City
    city_options = ["All Cities"] + sorted(df["city"].unique().tolist())
    state.filters.city = st.selectbox(
        "City",
        city_options,
        index=city_options.index(state.filters.city) if state.filters.city in city_options else 0
    )

    # Categories
    cat_options = sorted(df["category"].unique().tolist())
    state.filters.categories = st.multiselect(
        "Categories", cat_options, default=state.filters.categories
    )

    # Date
    date_options = ["All", "Today", "This Week", "This Month"]
    state.filters.date_preset = st.selectbox(
        "Date",
        date_options,
        index=date_options.index(state.filters.date_preset)
        if state.filters.date_preset in date_options else 0
    )

    # Price
    if "price" in df.columns:
        max_p = int(df["price"].max())
        state.filters.max_price = st.slider(
            "Max Price", 0, max_p, state.filters.max_price
        )

    if st.button("🗑️ Reset Filters", type="primary", use_container_width=True):
        state.reset_filters()
        st.rerun()

# --- APPLY FILTERS ---
filtered_df = apply_filters(df, state.filters)

# --- DISPLAY ---
render_section_header(
    f"Found {len(filtered_df)} events",
    "Showing results matching your filters"
)

if filtered_df.empty:
    st.info("No events match your filters. Try adjusting the sidebar filters.")
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

        # Save button (Streamlit button for interactivity)
        col_spacer, col_save = st.columns([5, 1])
        with col_save:
            is_saved = state.ui.is_saved(row.get("id"))
            if st.button(
                "❤️" if is_saved else "🤍",
                key=f"save_{row.get('id')}",
                help="Save this event"
            ):
                state.ui.toggle_save(row.get("id"))
                st.rerun()
