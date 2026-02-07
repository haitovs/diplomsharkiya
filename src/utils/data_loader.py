import pandas as pd
import pathlib
import json
import streamlit as st
from datetime import datetime

# Define path relative to this file
# src/utils/data_loader.py -> src/data/events.json (up one level, then across)
# But wait, src/utils/ -> src/ -> data/ is separate?
# Structure is:
# root/
#   data/events.json
#   src/
#     utils/data_loader.py
# So we need to go up two levels from utils to get to root, then into data.

DATA_PATH = pathlib.Path(__file__).parent.parent.parent / "data" / "events.json"

@st.cache_data(ttl=60)
def load_data():
    """
    Load events data from the JSON file.
    Returns a pandas DataFrame with processed dates.
    """
    if not DATA_PATH.exists():
        return pd.DataFrame()
    
    try:
        with open(DATA_PATH, "r", encoding="utf-8") as f:
            data = json.load(f)
        
        if not isinstance(data, list):
            return pd.DataFrame()
        
        df = pd.DataFrame(data)
        
        # Ensure date columns are datetime objects
        for col in ["date_start", "date_end"]:
            if col in df.columns:
                df[col] = pd.to_datetime(df[col], errors="coerce")
        
        return df
    
    except Exception as e:
        print(f"Error loading data: {e}")
        return pd.DataFrame()
