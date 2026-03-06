import pandas as pd
import pathlib
import json
import base64
import streamlit as st

DATA_DIR = pathlib.Path(__file__).parent.parent.parent / "data"
DATA_PATH = DATA_DIR / "events.json"


@st.cache_resource
def _get_image_store():
    """Shared image cache across all sessions — encode each image only once."""
    return {}

# Keep module-level reference for admin cache-busting
_image_cache = _get_image_store()


def get_event_image_base64(image_path: str) -> str:
    """Encode an event image as base64 for inline HTML display.
    image_path is relative to the data/ directory (e.g. 'images/event_default.png').
    Returns a data-URI string or empty string if file not found.
    """
    if not image_path:
        return ""

    cache = _get_image_store()
    if image_path in cache:
        return cache[image_path]

    full_path = DATA_DIR / image_path
    if not full_path.exists() or full_path.stat().st_size < 500:
        return ""

    try:
        suffix = full_path.suffix.lower().lstrip(".")
        mime = {"png": "image/png", "jpg": "image/jpeg", "jpeg": "image/jpeg",
                "webp": "image/webp"}.get(suffix, "image/png")
        raw = full_path.read_bytes()
        encoded = base64.b64encode(raw).decode("ascii")
        data_uri = f"data:{mime};base64,{encoded}"
        cache[image_path] = data_uri
        return data_uri
    except Exception:
        return ""


def get_category_image_path(category: str) -> str:
    """Return the category image path for a given category name."""
    if not category:
        return "images/event_default.jpg"
    return f"images/cat_{category.lower()}.jpg"


@st.cache_data(ttl=300)
def load_data():
    """Load events data from JSON. Cached for 5 minutes."""
    if not DATA_PATH.exists():
        return pd.DataFrame()

    try:
        with open(DATA_PATH, "r", encoding="utf-8") as f:
            data = json.load(f)

        if not isinstance(data, list):
            return pd.DataFrame()

        df = pd.DataFrame(data)

        for col in ["date_start", "date_end"]:
            if col in df.columns:
                df[col] = pd.to_datetime(df[col], errors="coerce")

        return df

    except Exception as e:
        print(f"Error loading data: {e}")
        return pd.DataFrame()
