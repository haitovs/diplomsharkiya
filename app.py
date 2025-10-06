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

# ---------- Maglumatlar ----------
DATA_PATH = pathlib.Path(__file__).parent / "data" / "events.json"
raw = json.loads(DATA_PATH.read_text(encoding="utf-8")) if DATA_PATH.exists() else []
df = pd.DataFrame(raw)

if not df.empty:
    df["date_start"] = pd.to_datetime(df["date_start"])
    df["date_end"] = pd.to_datetime(df["date_end"])

# ---------- Session state ----------
if "saved_ids" not in st.session_state:
    st.session_state.saved_ids = set()
if "details_id" not in st.session_state:
    st.session_state.details_id = None
# keep circle state between reruns
if "circle_center" not in st.session_state:
    # Aşgabat merkezi hökmünde başla
    st.session_state.circle_center = (37.9601, 58.3261)  # (lat, lon)
if "circle_radius_km" not in st.session_state:
    st.session_state.circle_radius_km = 0.0


# ---------- Kömekçiler ----------
def quick_date_filter(df: pd.DataFrame, preset: str) -> pd.DataFrame:
    if df.empty:
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
    if city != "Ähli":
        out = out[out["city"] == city]
    if categories:
        out = out[out["category"].isin(categories)]
    if search:
        s = search.lower()
        out = out[out["title"].str.lower().str.contains(s) | out["venue"].str.lower().str.contains(s) | out["description"].str.lower().str.contains(s)]
    out = out[out["price"] <= price_max_tmt]
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
    distances = df.apply(lambda r: haversine_km(center_lat, center_lon, float(r["lat"]), float(r["lon"])), axis=1)
    keep = distances <= radius_km
    out = df.loc[keep].copy()
    out["distance_km"] = distances[keep]
    return out


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
    sehir_options = ["Ähli"] + (sorted(df["city"].unique().tolist()) if not df.empty else [])
    city = st.selectbox("Şäherler", options=sehir_options, index=0)

    date_preset = st.radio(
        "Sene aralygy",
        options=["Şu gün", "Ertir", "Bu hepde aýagy", "Indiki 7 gün", "Ähli seneler"],
        index=4,
    )

    categories = st.multiselect("Kategoriýa", options=(sorted(df["category"].unique().tolist()) if not df.empty else []))

    price_max = st.slider(
        "Iň köp baha (TMT)",
        min_value=0,
        max_value=int(df["price"].max()) if not df.empty else 200,
        value=int(df["price"].max()) if not df.empty else 200,
        step=5,
    )

    search = st.text_input("Gözleg", placeholder="Ady, ýerini ýa-da düşündirişi boýunça...")

    sort_by = st.selectbox(
        "Tertiplemek",
        options=["Degişlilik", "Iň tiz başlanýan", "Baha (arzan → gymmat)", "Meşhurlylyk"],
        index=1 if not df.empty else 0,
    )

    st.markdown("---")
    st.markdown("### Radius boýunça Filtr (kartada)")
    # also let users tweak radius numerically
    radius_km_number = st.number_input("Radius (km)", value=float(st.session_state.circle_radius_km), min_value=0.0, step=0.5, format="%.1f")
    if st.button("Filtrleri täzeden aç"):
        st.rerun()

# ---------- Tabs ----------
tabs = st.tabs(["📋 Sanaw", "🗺️ Kartada", "⭐ Halananlar"])

# Optional details header
if st.session_state.details_id:
    details_panel(df, st.session_state.details_id)
    st.divider()

# Apply filters before map
filtered = apply_filters(df, city, categories, search, price_max, date_preset)

with tabs[1]:
    st.subheader("Karta — tegelek zony ")
    # Build Leaflet map
    center_lat, center_lon = st.session_state.circle_center
    m = folium.Map(location=[center_lat, center_lon], zoom_start=12, control_scale=True)

    # Pre-add our circle so user can edit/drag it
    if radius_km_number > 0:
        folium.Circle(
            location=[center_lat, center_lon],
            radius=radius_km_number * 1000.0,  # km → m
            color="#003366",
            weight=2,
            fill=True,
            fill_opacity=0.15,
            tooltip="Radius zona (sürükläp ýerini üýtgedip bilersiňiz)",
        ).add_to(m)

    # Add event markers
    for _, r in filtered.iterrows():
        popup = folium.Popup(
            f"<b>{r['title']}</b><br/>{r['venue']}<br/>{r['date_start']}<br/>Baha: {r['price']} TMT",
            max_width=300,
        )
        folium.Marker(
            location=[float(r["lat"]), float(r["lon"])],
            tooltip=r["title"],
            popup=popup,
        ).add_to(m)

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

    out = st_folium(m, height=520, use_container_width=True, returned_objects=["last_active_drawing", "all_drawings"])

    # Read back the circle the user edited/drew (draggable via Draw→Edit)
    new_center = None
    new_radius_km = None

    # Prefer the last active drawing if available
    feature = (out or {}).get("last_active_drawing")
    if not feature:
        # Or fall back to all drawings (if any)
        drawings = (out or {}).get("all_drawings", [])
        if drawings:
            feature = drawings[-1]

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
    # numeric field overrides only if changed
    st.session_state.circle_radius_km = float(radius_km_number if radius_km_number is not None else st.session_state.circle_radius_km)
    if new_radius_km is not None:
        st.session_state.circle_radius_km = float(new_radius_km)

    # Show current circle info
    st.caption(f"Merkez LAT/LON: {st.session_state.circle_center[0]:.6f}, {st.session_state.circle_center[1]:.6f} • "
               f"Radius: {st.session_state.circle_radius_km:.1f} km")

# Now apply circle filter after map interactions
filtered = filter_by_circle(filtered, st.session_state.circle_center[0], st.session_state.circle_center[1], st.session_state.circle_radius_km)
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
