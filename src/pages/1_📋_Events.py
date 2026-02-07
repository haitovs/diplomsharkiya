import streamlit as st
import pathlib
from utils.data_loader import load_data
from utils.filters import apply_filters
from state_manager import get_state

# Page Config
st.set_page_config(page_title="Events | Sharkiya", page_icon="📋", layout="wide")

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
    state.filters.search_query = st.text_input("Search", value=state.filters.search_query, placeholder="Title, venue...")
    
    # City
    city_options = ["All Cities"] + sorted(df["city"].unique().tolist())
    state.filters.city = st.selectbox(
        "City", 
        city_options, 
        index=city_options.index(state.filters.city) if state.filters.city in city_options else 0
    )
    
    # Categories
    cat_options = sorted(df["category"].unique().tolist())
    state.filters.categories = st.multiselect("Categories", cat_options, default=state.filters.categories)
    
    # Date
    date_options = ["All", "Today", "This Week", "This Month"]
    state.filters.date_preset = st.selectbox(
        "Date", 
        date_options, 
        index=date_options.index(state.filters.date_preset) if state.filters.date_preset in date_options else 0
    )
    
    # Price
    if "price" in df.columns:
        max_p = int(df["price"].max())
        state.filters.max_price = st.slider("Max Price", 0, max_p, state.filters.max_price)

    if st.button("Reset Filters", type="primary"):
        state.reset_filters()
        st.rerun()

# --- APPLY FILTERS ---
filtered_df = apply_filters(df, state.filters)

# --- DISPLAY ---
st.markdown(f"**Found {len(filtered_df)} events**")

if filtered_df.empty:
    st.info("No events match your filters.")
else:
    for _, row in filtered_df.iterrows():
        with st.container(border=True):
            c1, c2, c3 = st.columns([1, 4, 1])
            
            with c1:
                # Category Icon/Badge
                custom_icon = row.get('icon')
                # CWD is src/
                if custom_icon and (pathlib.Path("assets/icons") / f"{custom_icon}.png").exists():
                    st.image(str(pathlib.Path("assets/icons") / f"{custom_icon}.png"), width=50)
                else:
                    st.markdown(f"### 📌") 
                
                st.caption(row.get('category', 'Event'))
            
            with c2:
                st.subheader(row.get('title', 'Untitled'))
                st.markdown(f"📍 **{row.get('venue', 'Unknown')}** in {row.get('city', 'Unknown')}")
                
                # Date Formatting
                start = row.get('date_start')
                if start:
                    st.caption(f"📅 {start.strftime('%b %d, %Y • %I:%M %p')}")
                
                # Description truncated
                desc = row.get('description', '')
                if len(desc) > 150:
                    st.text(desc[:150] + "...")
                else:
                    st.text(desc)
                    
            with c3:
                price = row.get('price', 0)
                price_str = "Free" if price == 0 else f"{price} TMT"
                st.markdown(f"### {price_str}")
                
                is_saved = state.ui.is_saved(row.get('id'))
                if st.button("❤️ Saved" if is_saved else "🤍 Save", key=f"save_{row.get('id')}"):
                    state.ui.toggle_save(row.get('id'))
                    st.rerun()
