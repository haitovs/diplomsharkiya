# Mähallik Çäreler — Streamlit (statiki)
# Run: streamlit run app.py

import datetime as dt
import json
import math
import pathlib

import folium
import pandas as pd
import streamlit as st
from folium.plugins import Draw
# NEW for draggable circle
from streamlit_folium import st_folium

st.set_page_config(page_title="Mähallik Çäreler", page_icon="🎟️", layout="wide")

DEFAULT_CENTER = (37.9601, 58.3261)
DEFAULT_RADIUS_KM = 0.0
ALL_CITY_OPTION = "Ähli"
DEFAULT_DATE_PRESET = "Ähli seneler"
DEFAULT_SORT_OPTION = "Iň tiz başlanýan"
DEFAULT_PRICE_CAP = 200

EXPECTED_COLUMNS = [
    "id",
    "title",
    "category",
    "city",
    "venue",
    "date_start",
    "date_end",
    "price",
    "popularity",
    "lat",
    "lon",
    "image",
    "description",
]
TEXT_COLUMNS = ["id", "title", "category", "city", "venue", "image", "description"]
NUMERIC_COLUMNS = ["price", "popularity"]
FLOAT_COLUMNS = ["lat", "lon"]
DATE_COLUMNS = ["date_start", "date_end"]

DATA_PATH = pathlib.Path(__file__).parent / "data" / "events.json"


def load_events(path: pathlib.Path) -> pd.DataFrame:
    """Read and normalize events data from disk, guarding against malformed JSON."""
    if not path.exists():
        st.warning("`data/events.json` tapylmady – görkezmek üçin maglumat ýok.", icon="⚠️")
        return pd.DataFrame(columns=EXPECTED_COLUMNS)

    try:
        raw_text = path.read_text(encoding="utf-8")
    except OSError as exc:
        st.error(f"Çäreler faýlyny okap bolmady: {exc}", icon="🚫")
        return pd.DataFrame(columns=EXPECTED_COLUMNS)

    if not raw_text.strip():
        st.warning("`data/events.json` faýly boş – görkezmek üçin maglumat ýok.", icon="⚠️")
        return pd.DataFrame(columns=EXPECTED_COLUMNS)

    try:
        raw = json.loads(raw_text)
    except json.JSONDecodeError as exc:
        st.error(f"`data/events.json` JSON formatynda näsazlyk bar: {exc}", icon="🚫")
        return pd.DataFrame(columns=EXPECTED_COLUMNS)

    if not isinstance(raw, list):
        st.error("`data/events.json` mazmuny san görnüşinde bolmaly.", icon="🚫")
        return pd.DataFrame(columns=EXPECTED_COLUMNS)

    df = pd.DataFrame(raw)
    for col in EXPECTED_COLUMNS:
        if col not in df.columns:
            df[col] = None
    df = df[EXPECTED_COLUMNS].copy()

    if df.empty:
        return df

    for col in TEXT_COLUMNS:
        df[col] = df[col].fillna("").astype(str)

    for col in NUMERIC_COLUMNS:
        df[col] = pd.to_numeric(df[col], errors="coerce").fillna(0.0)

    for col in FLOAT_COLUMNS:
        df[col] = pd.to_numeric(df[col], errors="coerce")

    for col in DATE_COLUMNS:
        df[col] = pd.to_datetime(df[col], errors="coerce")

    invalid_dates = df[DATE_COLUMNS].isna().any(axis=1)
    if invalid_dates.any():
        st.warning(
            f"{invalid_dates.sum()} çäre senesi nädogry bolandygy üçin görkezilen sanawdan aýyryldy.",
            icon="⚠️",
        )
        df = df.loc[~invalid_dates]

    return df.reset_index(drop=True)

# ---------- Maglumatlar ----------
df = load_events(DATA_PATH)

# ---------- Session state ----------
if "saved_ids" not in st.session_state:
    st.session_state.saved_ids = set()
elif not isinstance(st.session_state.saved_ids, set):
    st.session_state.saved_ids = set(st.session_state.saved_ids)
if "details_id" not in st.session_state:
    st.session_state.details_id = None
# keep circle state between reruns
if "circle_center" not in st.session_state:
    # Aşgabat merkezi hökmünde başla
    st.session_state.circle_center = DEFAULT_CENTER  # (lat, lon)
if "circle_radius_km" not in st.session_state:
    st.session_state.circle_radius_km = DEFAULT_RADIUS_KM
if "pending_radius_from_map" not in st.session_state:
    st.session_state.pending_radius_from_map = None

price_ceiling = DEFAULT_PRICE_CAP
if not df.empty and "price" in df.columns:
    price_max = df["price"].max()
    if pd.notna(price_max):
        try:
            price_ceiling = int(math.ceil(float(price_max)))
        except (TypeError, ValueError):
            price_ceiling = DEFAULT_PRICE_CAP
if price_ceiling < 0:
    price_ceiling = DEFAULT_PRICE_CAP

if "filter_city" not in st.session_state:
    st.session_state.filter_city = ALL_CITY_OPTION
if "filter_date" not in st.session_state:
    st.session_state.filter_date = DEFAULT_DATE_PRESET
if "filter_categories" not in st.session_state:
    st.session_state.filter_categories = []
if "filter_price" not in st.session_state:
    st.session_state.filter_price = price_ceiling
if "filter_search" not in st.session_state:
    st.session_state.filter_search = ""
if "filter_sort" not in st.session_state:
    st.session_state.filter_sort = DEFAULT_SORT_OPTION if not df.empty else "Degişlilik"
# keep sidebar radius widget state separate from map state
if "filter_radius_input" not in st.session_state:
    st.session_state.filter_radius_input = float(st.session_state.circle_radius_km)


# ---------- Kömekçiler ----------
def quick_date_filter(df: pd.DataFrame, preset: str) -> pd.DataFrame:
    if df.empty:
        return df
    if not preset or preset == DEFAULT_DATE_PRESET:
        return df
    today = pd.Timestamp(dt.datetime.now().date())
    if preset == "Şu gün":
        return df[df["date_start"].dt.date == today.date()]
    if preset == "Ertir":
        return df[df["date_start"].dt.date == (today + pd.Timedelta(days=1)).date()]
    if preset == "Bu hepde aýagy":
        weekday = today.weekday()
        sat = today + pd.Timedelta(days=(5 - weekday) % 7)
        sun = sat + pd.Timedelta(days=1)
        return df[(df["date_start"].dt.date >= sat.date()) & (df["date_start"].dt.date <= sun.date())]
    if preset == "Indiki 7 gün":
        end = today + pd.Timedelta(days=7)
        return df[(df["date_start"] >= today) & (df["date_start"] < end)]
    return df


def apply_filters(df: pd.DataFrame, city, categories, search, price_max_tmt, date_preset):
    out = df.copy()
    if city and city != ALL_CITY_OPTION:
        out = out[out["city"] == city]
    if categories:
        out = out[out["category"].isin(categories)]
    if search:
        pattern = search.strip()
        if pattern:
            mask = (
                out["title"].str.contains(pattern, case=False, na=False)
                | out["venue"].str.contains(pattern, case=False, na=False)
                | out["description"].str.contains(pattern, case=False, na=False)
            )
            out = out[mask]
    if price_max_tmt is not None:
        out = out[out["price"] <= float(price_max_tmt)]
    out = quick_date_filter(out, date_preset)
    return out


def apply_sort(df: pd.DataFrame, by):
    if df.empty:
        return df
    if by == "Iň tiz başlanýan":
        return df.sort_values("date_start", ascending=True)
    if by == "Baha (arzan → gymmat)":
        return df.sort_values("price", ascending=True)
    if by == "Meşhurlylyk":
        return df.sort_values("popularity", ascending=False)
    return df


def haversine_km(lat1, lon1, lat2, lon2):
    R = 6371.0
    dlat = math.radians(lat2 - lat1)
    dlon = math.radians(lon2 - lon1)
    a = (math.sin(dlat / 2)**2 + math.cos(math.radians(lat1)) * math.cos(math.radians(lat2)) * math.sin(dlon / 2)**2)
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    return R * c


def filter_by_circle(df: pd.DataFrame, center_lat, center_lon, radius_km: float):
    if radius_km <= 0 or df.empty:
        return df
    candidates = df[df["lat"].notna() & df["lon"].notna()].copy()
    if candidates.empty:
        return candidates
    distances = candidates.apply(
        lambda r: haversine_km(center_lat, center_lon, float(r["lat"]), float(r["lon"])),
        axis=1,
    )
    keep = distances <= radius_km
    out = candidates.loc[keep].copy()
    out["distance_km"] = distances[keep]
    return out.sort_values("distance_km")


def reset_filter_state(price_limit: float) -> None:
    st.session_state.filter_city = ALL_CITY_OPTION
    st.session_state.filter_date = DEFAULT_DATE_PRESET
    st.session_state.filter_categories = []
    st.session_state.filter_price = int(price_limit)
    st.session_state.filter_search = ""
    st.session_state.filter_sort = DEFAULT_SORT_OPTION
    st.session_state.circle_center = DEFAULT_CENTER
    st.session_state.circle_radius_km = DEFAULT_RADIUS_KM
    st.session_state.filter_radius_input = DEFAULT_RADIUS_KM
    st.session_state.details_id = None


# Namespaced widget keys so tabs never collide
def event_card(row, key_prefix: str):
    cols = st.columns([1, 3, 2])
    with cols[0]:
        st.markdown("### 🎫")
        st.caption(row["category"])
        st.caption(row["city"])
    with cols[1]:
        st.markdown(f"**{row['title']}**")
        st.caption(f"{row['venue']} • {row['date_start'].strftime('%a, %d %b %H:%M')} — {row['date_end'].strftime('%H:%M')}")
        st.write(row["description"])
        st.caption(f"Meşhurlylyk: {row['popularity']} • Bahasy: {row['price']} TMT")
        distance = row.get("distance_km") if hasattr(row, "get") else None
        if distance is not None and not pd.isna(distance):
            st.caption(f"Uzaklygy: {distance:.1f} km")
    with cols[2]:
        saved = row["id"] in st.session_state.saved_ids
        c1, c2, c3 = st.columns(3)
        with c1:
            if st.button("Doly maglumat", key=f"{key_prefix}_details_{row['id']}"):
                st.session_state.details_id = row["id"]
        with c2:
            if st.button(("Halanlara gos ✓" if saved else "Halanlara gos"), key=f"{key_prefix}_save_{row['id']}"):
                if saved:
                    st.session_state.saved_ids.remove(row["id"])
                else:
                    st.session_state.saved_ids.add(row["id"])
                st.rerun()
        with c3:
            st.button("Paýlaş", key=f"{key_prefix}_share_{row['id']}")


def details_panel(df: pd.DataFrame, event_id: str):
    row = df[df["id"] == event_id]
    if row.empty:
        return
    row = row.iloc[0]
    with st.container(border=True):
        st.markdown(f"### {row['title']}")
        st.caption(f"{row['category']} • {row['city']} • {row['venue']}")
        st.write(row["description"])
        st.write(f"**Haçan:** {row['date_start'].strftime('%Y-%m-%d %H:%M')} — {row['date_end'].strftime('%H:%M')}")
        st.write(f"**Bahasy:** {row['price']} TMT")
        st.write(f"**Meşhurlylyk:** {row['popularity']}")
        c1, c2, c3 = st.columns(3)
        with c1:
            st.button("Biletler (stub)", key=f"tickets_{row['id']}")
        with c2:
            st.button("Ýol görkezme (stub)", key=f"dir_{row['id']}")
        with c3:
            if st.button("Ýap", key="close_details"):
                st.session_state.details_id = None
                st.rerun()


# ---------- Sidebar ----------
with st.sidebar:
    st.markdown("## Filtrler")
    city_options = [ALL_CITY_OPTION] + (sorted(df["city"].unique().tolist()) if not df.empty else [])
    if st.session_state.filter_city not in city_options:
        st.session_state.filter_city = ALL_CITY_OPTION
    city = st.selectbox("Şäherler", options=city_options, key="filter_city")

    date_options = ["Şu gün", "Ertir", "Bu hepde aýagy", "Indiki 7 gün", DEFAULT_DATE_PRESET]
    date_preset = st.radio("Sene aralygy", options=date_options, index=date_options.index(DEFAULT_DATE_PRESET), key="filter_date")

    category_options = sorted(df["category"].unique().tolist()) if not df.empty else []
    if st.session_state.filter_categories:
        st.session_state.filter_categories = [c for c in st.session_state.filter_categories if c in category_options]
    categories = st.multiselect("Kategoriýa", options=category_options, key="filter_categories")

    if st.session_state.filter_price > price_ceiling:
        st.session_state.filter_price = price_ceiling
    if st.session_state.filter_price < 0:
        st.session_state.filter_price = 0
    price_step = 5 if price_ceiling >= 5 else 1
    price_max = st.slider(
        "Iň köp baha (TMT)",
        min_value=0,
        max_value=price_ceiling,
        step=price_step,
        key="filter_price",
    )

    search = st.text_input("Gözleg", placeholder="Ady, ýerini ýa-da düşündirişi boýunça...", key="filter_search")

    sort_options = ["Degişlilik", DEFAULT_SORT_OPTION, "Baha (arzan → gymmat)", "Meşhurlylyk"]
    if st.session_state.filter_sort not in sort_options:
        st.session_state.filter_sort = DEFAULT_SORT_OPTION
    sort_by = st.selectbox("Tertiplemek", options=sort_options, key="filter_sort")

    st.markdown("---")
    st.markdown("### Radius boýunça Filtr (kartada)")
    # apply any pending radius from map BEFORE rendering widget to avoid rewrite errors
    if st.session_state.pending_radius_from_map is not None:
        st.session_state.circle_radius_km = float(st.session_state.pending_radius_from_map)
        st.session_state.filter_radius_input = float(st.session_state.pending_radius_from_map)
        st.session_state.pending_radius_from_map = None
    # also let users tweak radius numerically
    radius_km_number = float(
        st.number_input(
            "Radius (km)",
            min_value=0.0,
            step=0.5,
            format="%.1f",
            key="filter_radius_input",
        )
    )
    # sync widget value into map state
    if not math.isclose(radius_km_number, st.session_state.circle_radius_km, rel_tol=1e-9, abs_tol=1e-4):
        st.session_state.circle_radius_km = radius_km_number

    c_reset_center, c_reset_radius = st.columns(2)
    with c_reset_center:
        if st.button("Karta: Aşgabada getir", key="btn_reset_center"):
            st.session_state.circle_center = DEFAULT_CENTER
            st.session_state.circle_radius_km = DEFAULT_RADIUS_KM
            st.session_state.pending_radius_from_map = DEFAULT_RADIUS_KM
            st.rerun()
    with c_reset_radius:
        if st.button("Radiusy 0 km", key="btn_reset_radius"):
            st.session_state.circle_radius_km = 0.0
            st.session_state.pending_radius_from_map = 0.0
            st.rerun()

    if st.button("Filtrleri täzeden aç", type="secondary"):
        reset_filter_state(price_ceiling)
        st.rerun()

# ---------- Tabs ----------
tabs = st.tabs(["📋 Sanaw", "🗺️ Kartada", "⭐ Halananlar"])

# Optional details header
if st.session_state.details_id:
    details_panel(df, st.session_state.details_id)
    st.divider()

base_filtered = apply_filters(df, city, categories, search, price_max, date_preset)

with tabs[1]:
    st.subheader("Karta — tegelek zony ")
    # Build Leaflet map
    center_lat, center_lon = st.session_state.circle_center
    m = folium.Map(location=[center_lat, center_lon], zoom_start=12, control_scale=True)

    # Apply circle filter to the map view so pins match radius selection
    filtered_for_map = filter_by_circle(base_filtered, center_lat, center_lon, radius_km_number)

    # If no events satisfy filters, keep map but notify user
    if filtered_for_map.empty:
        st.info("Saýlanan radius/filtr boýunça kartada görkezmäge ýolbaşylar ýok.")

    # Pre-add our circle so user can edit/drag it
    if radius_km_number > 0:
        folium.Circle(
            location=[center_lat, center_lon],
            radius=float(radius_km_number) * 1000.0,  # km → m
            color="#003366",
            weight=2,
            fill=True,
            fill_opacity=0.15,
            tooltip="Radius zona (sürükläp ýerini üýtgedip bilersiňiz)",
    ).add_to(m)

    # Add event markers (already radius-filtered for the map view)
    marker_coords = []
    for _, r in filtered_for_map.iterrows():
        if pd.isna(r["lat"]) or pd.isna(r["lon"]):
            continue
        start_label = r["date_start"].strftime("%Y-%m-%d %H:%M")
        popup = folium.Popup(
            "<br/>".join(
                [
                    f"<b>{r['title']}</b>",
                    r["venue"],
                    start_label,
                    f"Baha: {r['price']} TMT",
                ]
            ),
            max_width=300,
        )
        folium.Marker(
            location=[float(r["lat"]), float(r["lon"])],
            tooltip=r["title"],
            popup=popup,
        ).add_to(m)
        marker_coords.append([float(r["lat"]), float(r["lon"])])

    if marker_coords:
        # Fit to visible markers so users see the relevant area immediately
        m.fit_bounds(marker_coords, padding=(20, 20))

    # Add Draw control (user can draw/edit/move the circle)
    Draw(
        draw_options={
            "polyline": False,
            "polygon": False,
            "rectangle": False,
            "circle": True,
            "marker": False,
            "circlemarker": False,
        },
        edit_options={
            "edit": True,
            "remove": True
        },
    ).add_to(m)

    out = st_folium(
        m,
        height=520,
        use_container_width=True,
        returned_objects=["last_active_drawing", "all_drawings"],
        key="events-map",
    )

    # Read back the circle the user edited/drew (draggable via Draw→Edit)
    new_center = None
    new_radius_km = None

    # Prefer the last active drawing if available
    feature = (out or {}).get("last_active_drawing")
    drawings = (out or {}).get("all_drawings", [])
    if not feature and drawings:
        # Or fall back to the latest drawing (if any)
        feature = drawings[-1]
    # If user removed everything, clear radius filter to avoid stale values
    if not drawings and feature is None and radius_km_number > 0:
        new_radius_km = 0.0
        radius_km_number = 0.0

    if feature and isinstance(feature, dict):
        geom = feature.get("geometry", {})
        props = feature.get("properties", {})
        # Leaflet Draw encodes a circle as type 'Point' with radius in properties (meters)
        # Sometimes it may send as Polygon approximation; handle both.
        if geom.get("type") == "Point" and "radius" in props:
            lat = geom["coordinates"][1]
            lon = geom["coordinates"][0]
            rad_m = float(props["radius"])
            new_center = (lat, lon)
            new_radius_km = rad_m / 1000.0
        elif geom.get("type") == "Polygon":
            # Approximate center from first coordinate ring
            ring = geom.get("coordinates", [[]])[0]
            if ring:
                # simple centroid of vertices
                lats = [pt[1] for pt in ring]
                lons = [pt[0] for pt in ring]
                lat = sum(lats) / len(lats)
                lon = sum(lons) / len(lons)
                new_center = (lat, lon)
                # radius rough guess from first point
                lat0, lon0 = lats[0], lons[0]
                new_radius_km = haversine_km(lat, lon, lat0, lon0)

    # Update session state from either map or numeric field
    if new_center:
        st.session_state.circle_center = new_center
    if new_radius_km is not None:
        updated_radius = float(new_radius_km)
        if not math.isclose(updated_radius, st.session_state.circle_radius_km, rel_tol=1e-9, abs_tol=1e-4):
            st.session_state.circle_radius_km = updated_radius
        # Defer syncing to widget (handled before widget render next rerun)
        st.session_state.pending_radius_from_map = updated_radius
        radius_km_number = updated_radius

    # Show current circle info
    st.caption(f"Merkez LAT/LON: {st.session_state.circle_center[0]:.6f}, {st.session_state.circle_center[1]:.6f} • "
               f"Radius: {st.session_state.circle_radius_km:.1f} km")

# Now apply circle filter after map interactions (for list view)
filtered = filter_by_circle(
    base_filtered,
    st.session_state.circle_center[0],
    st.session_state.circle_center[1],
    st.session_state.circle_radius_km,
)
filtered = apply_sort(filtered, sort_by)

with tabs[0]:
    st.subheader("Çäreleriň sanawy")
    if filtered.empty:
        st.info("Saýlanan Filtrlere laýyk çäre tapylmady.")
    else:
        for _, row in filtered.iterrows():
            event_card(row, key_prefix="list")
            st.divider()

with tabs[2]:
    st.subheader("Halanan çäreler")
    if not st.session_state.saved_ids:
        st.info("Häzirlikçe halananlar ýok. Islendik kartda **Halanlara gos** düwmesine basyp goşuň.")
    else:
        fav_df = df[df["id"].isin(st.session_state.saved_ids)]
        fav_df = apply_sort(fav_df, sort_by)
        for _, row in fav_df.iterrows():
            event_card(row, key_prefix="fav")
            st.divider()
