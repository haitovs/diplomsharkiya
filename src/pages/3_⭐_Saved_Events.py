import streamlit as st
from utils.data_loader import load_data
from state_manager import get_state

st.set_page_config(page_title="Saved | Sharkiya", page_icon="⭐", layout="wide")

df = load_data()
state = get_state()

st.title("⭐ Saved Events")

if not state.ui.saved_events:
    st.info("You haven't saved any events yet. Go to the Events List to add some!")
else:
    # Filter df for saved IDs
    saved_df = df[df["id"].isin(state.ui.saved_events)]
    
    if saved_df.empty:
        st.warning("Saved events not found in database (maybe IDs changed?).")
    else:
        for _, row in saved_df.iterrows():
            with st.container(border=True):
                c1, c2 = st.columns([4, 1])
                with c1:
                    st.subheader(row['title'])
                    st.caption(f"{row['venue']} • {row['city']}")
                with c2:
                    if st.button("💔 Remove", key=f"remove_{row['id']}"):
                        state.ui.toggle_save(row['id'])
                        st.rerun()
