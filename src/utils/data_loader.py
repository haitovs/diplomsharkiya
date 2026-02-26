import pandas as pd
import pathlib
import json
import base64
import streamlit as st
from datetime import datetime

DATA_DIR = pathlib.Path(__file__).parent.parent.parent / "data"
DATA_PATH = DATA_DIR / "events.json"

# Cache for base64-encoded images to avoid re-encoding on every rerun
_image_cache: dict[str, str] = {}


def get_event_image_base64(image_path: str) -> str:
    """Encode an event image as base64 for inline HTML display.
    image_path is relative to the data/ directory (e.g. 'images/event_default.png').
    Returns a data-URI string or empty string if file not found.
    """
    if not image_path:
        return ""

    if image_path in _image_cache:
        return _image_cache[image_path]

    full_path = DATA_DIR / image_path
    if not full_path.exists():
        return ""

    try:
        suffix = full_path.suffix.lower().lstrip(".")
        mime = {"png": "image/png", "jpg": "image/jpeg", "jpeg": "image/jpeg",
                "webp": "image/webp"}.get(suffix, "image/png")
        raw = full_path.read_bytes()
        encoded = base64.b64encode(raw).decode("ascii")
        data_uri = f"data:{mime};base64,{encoded}"
        _image_cache[image_path] = data_uri
        return data_uri
    except Exception:
        return ""

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
