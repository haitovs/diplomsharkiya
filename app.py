\
# Local Events Discovery — Streamlit Template (static, no backend)
# Run: streamlit run app.py

import streamlit as st
import pandas as pd
import json, pathlib, datetime as dt
import pydeck as pdk

st.set_page_config(page_title="Local Events Discovery", page_icon="🎟️", layout="wide")

# ---------- Data loading ----------
DATA_PATH = pathlib.Path(__file__).parent / "data" / "events.json"
if DATA_PATH.exists():
    with open(DATA_PATH, "r", encoding="utf-8") as f:
        raw = json.load(f)
else:
    raw = []  # if missing, empty list

df = pd.DataFrame(raw)

# Ensure datetime types
if not df.empty:
    df["date_start"] = pd.to_datetime(df["date_start"])
    df["date_end"] = pd.to_datetime(df["date_end"])

# ---------- Session state ----------
if "saved_ids" not in st.session_state:
    st.session_state.saved_ids = set()

if "details_id" not in st.session_state:
    st.session_state.details_id = None

# ---------- Helpers ----------
def quick_date_filter(df: pd.DataFrame, preset: str) -> pd.DataFrame:
    if df.empty:
        return df
    today = pd.Timestamp(dt.datetime.now().date())
    if preset == "Today":
        return df[(df["date_start"].dt.date == today.date())]
    if preset == "Tomorrow":
        return df[(df["date_start"].dt.date == (today + pd.Timedelta(days=1)).date())]
    if preset == "This weekend":
        # Assuming weekend = Saturday/Sunday for simplicity
        weekday = today.weekday()  # Monday=0
        # find next Saturday
        days_until_sat = (5 - weekday) % 7
        sat = today + pd.Timedelta(days=days_until_sat)
        sun = sat + pd.Timedelta(days=1)
        return df[(df["date_start"].dt.date >= sat.date()) & (df["date_start"].dt.date <= sun.date())]
    if preset == "Next 7 days":
        end = today + pd.Timedelta(days=7)
        return df[(df["date_start"] >= today) & (df["date_start"] < end)]
    return df  # All dates

def apply_filters(df: pd.DataFrame, city, categories, search, price_max, date_preset):
    out = df.copy()
    if city != "All":
        out = out[out["city"] == city]
    if categories:
        out = out[out["category"].isin(categories)]
    if search:
        s = search.lower()
        out = out[out["title"].str.lower().str.contains(s) | out["venue"].str.lower().str.contains(s) | out["description"].str.lower().str.contains(s)]
    out = out[out["price"] <= price_max]
    out = quick_date_filter(out, date_preset)
    return out

def apply_sort(df: pd.DataFrame, by):
    if df.empty:
        return df
    if by == "Soonest":
        return df.sort_values("date_start", ascending=True)
    if by == "Price (low → high)":
        return df.sort_values("price", ascending=True)
    if by == "Popularity":
        return df.sort_values("popularity", ascending=False)
    return df  # Relevance (no-op)

def event_card(row):
    # Layout: image/emoji (left) + info (right)
    cols = st.columns([1, 3, 2])
    with cols[0]:
        st.markdown("### 🎫")
        st.caption(row["category"])
        st.caption(row["city"])
    with cols[1]:
        st.markdown(f"**{row['title']}**")
        st.caption(f"{row['venue']} • {row['date_start'].strftime('%a, %d %b %H:%M')} — {row['date_end'].strftime('%H:%M')}")
        st.write(row["description"])
        st.caption(f"Popularity: {row['popularity']} • Price: {row['price']} PLN")
    with cols[2]:
        saved = row["id"] in st.session_state.saved_ids
        c1, c2, c3 = st.columns(3)
        with c1:
            if st.button("Details", key=f"details_{row['id']}"):
                st.session_state.details_id = row["id"]
        with c2:
            if st.button("Save" + (" ✓" if saved else ""), key=f"save_{row['id']}"):
                if saved:
                    st.session_state.saved_ids.remove(row["id"])
                else:
                    st.session_state.saved_ids.add(row["id"])
                st.experimental_rerun()
        with c3:
            if st.button("Share", key=f"share_{row['id']}"):
                st.info(f"Share link: https://example.com/event/{row['id']} (simulated)")

def details_panel(df: pd.DataFrame, event_id: str):
    if not event_id:
        return
    row = df[df["id"] == event_id]
    if row.empty:
        return
    row = row.iloc[0]
    with st.container(border=True):
        st.markdown(f"### {row['title']}")
        st.caption(f"{row['category']} • {row['city']} • {row['venue']}")
        st.write(row["description"])
        st.write(f"**When:** {row['date_start'].strftime('%Y-%m-%d %H:%M')} — {row['date_end'].strftime('%H:%M')}")
        st.write(f"**Price:** {row['price']} PLN")
        st.write(f"**Popularity:** {row['popularity']}")
        c1, c2, c3 = st.columns(3)
        with c1:
            st.button("Get Tickets (stub)", key=f"tickets_{row['id']}")
        with c2:
            st.button("Directions (stub)", key=f"dir_{row['id']}")
        with c3:
            if st.button("Close", key="close_details"):
                st.session_state.details_id = None
                st.experimental_rerun()

# ---------- Sidebar (global filters) ----------
with st.sidebar:
    st.markdown("## Filters")
    city = st.selectbox("City", options=["All"] + sorted(df["city"].unique().tolist() if not df.empty else []), index= (["All"] + sorted(df["city"].unique().tolist() if not df.empty else [])).index("All") if not df.empty else 0)
    date_preset = st.radio("Dates", options=["Today", "Tomorrow", "This weekend", "Next 7 days", "All dates"], index=4, horizontal=False)
    categories = st.multiselect("Categories", options=sorted(df["category"].unique().tolist() if not df.empty else []))
    price_max = st.slider("Max price (PLN)", min_value=0, max_value=int(df["price"].max()) if not df.empty else 200, value=int(df["price"].max()) if not df.empty else 200, step=5)
    search = st.text_input("Search", placeholder="Search by title, venue...")
    sort_by = st.selectbox("Sort by", options=["Relevance", "Soonest", "Price (low → high)", "Popularity"], index=1 if not df.empty else 0)
    if st.button("Reset filters"):
        # Reset by re-running; minimalistic approach
        st.experimental_rerun()

# ---------- Main Tabs ----------
tabs = st.tabs(["📋 List", "🗺️ Map", "⭐ Favorites"])

# Optional details panel at top
if st.session_state.details_id:
    details_panel(df, st.session_state.details_id)
    st.divider()

filtered = apply_filters(df, city, categories, search, price_max, date_preset)
filtered = apply_sort(filtered, sort_by)

with tabs[0]:
    st.subheader("Events")
    if filtered.empty:
        st.info("No events match your filters.")
    else:
        for _, row in filtered.iterrows():
            event_card(row)
            st.divider()

with tabs[1]:
    st.subheader("Map view")
    if filtered.empty:
        st.info("No events to display on the map for current filters.")
    else:
        layer = pdk.Layer(
            "ScatterplotLayer",
            data=filtered,
            get_position="[lon, lat]",
            get_radius=60,
            pickable=True,
        )
        tooltip = {"text": "{title}\n{venue}\n{date_start}"}
        view_state = pdk.ViewState(latitude=filtered["lat"].mean(), longitude=filtered["lon"].mean(), zoom=12)
        r = pdk.Deck(map_style=None, initial_view_state=view_state, layers=[layer], tooltip=tooltip)
        st.pydeck_chart(r)

with tabs[2]:
    st.subheader("Favorites")
    if not st.session_state.saved_ids:
        st.info("No saved events yet. Click **Save** on any event to add it here.")
    else:
        fav_df = df[df["id"].isin(st.session_state.saved_ids)]
        fav_df = apply_sort(fav_df, sort_by)
        for _, row in fav_df.iterrows():
            event_card(row)
            st.divider()
