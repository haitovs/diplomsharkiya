# 🔧 Super Admin — Event Management System

import streamlit as st
import pathlib
import json
from datetime import datetime, timedelta
import uuid

st.set_page_config(
    page_title="Super Admin — Event Management",
    page_icon="🔧",
    layout="wide"
)

from components.styles import inject_custom_css
from utils.i18n import t, t_cat, render_language_selector
inject_custom_css()
render_language_selector()

# ============ Config ============
DATA_PATH = pathlib.Path(__file__).parent.parent.parent / "data" / "events.json"
IMG_DIR = pathlib.Path(__file__).parent.parent.parent / "data" / "images"
ADMIN_PASSWORD = "admin"

CITIES = ["Ashgabat", "Mary", "Türkmenabat", "Dashoguz", "Balkanabat", "Awaza"]
CATEGORIES = ["Music", "Tech", "Sports", "Food", "Art", "Market", "Film",
              "Wellness", "Business", "Science", "Kids", "Travel", "Community"]

CITY_COORDS = {
    "Ashgabat": (37.9601, 58.3261),
    "Mary": (37.6005, 61.8302),
    "Türkmenabat": (39.0733, 63.5786),
    "Dashoguz": (41.8387, 59.9650),
    "Balkanabat": (39.5104, 54.3672),
    "Awaza": (40.0224, 52.9693),
}

# ============ Data helpers ============
def load_events():
    if not DATA_PATH.exists():
        return []
    try:
        with open(DATA_PATH, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return []

def save_events(events):
    with open(DATA_PATH, "w", encoding="utf-8") as f:
        json.dump(events, f, indent=2, ensure_ascii=False)

def generate_id():
    return f"evt{uuid.uuid4().hex[:6]}"

# ============ Auth ============
def check_auth():
    if "admin_auth" not in st.session_state:
        st.session_state.admin_auth = False

    if st.session_state.admin_auth:
        return True

    # ─── Super Admin Login Screen ─────────────────
    st.markdown("""
    <div style="
        max-width: 420px; margin: 4rem auto; padding: 2.5rem;
        background: linear-gradient(135deg, #141B34 0%, #1A2238 100%);
        border: 1px solid rgba(99, 102, 241, 0.2);
        border-radius: 16px;
        box-shadow: 0 20px 40px -12px rgba(0, 0, 0, 0.5);
        text-align: center;
    ">
        <p style="font-size: 2.5rem; margin-bottom: 0.25rem;">🔐</p>
        <h2 style="color: #F8FAFC; margin: 0 0 0.25rem 0; font-weight: 700;">""" + t("super_admin") + """</h2>
        <p style="color: #94A3B8; font-size: 0.9rem; margin-bottom: 1.5rem;">""" + t("admin_access_desc") + """</p>
    </div>
    """, unsafe_allow_html=True)

    with st.form("login"):
        username = st.text_input(t("username"), placeholder="admin")
        password = st.text_input(t("password"), type="password")
        submit = st.form_submit_button(f"🔑 {t('login')}", use_container_width=True)

    if submit:
        if username == "admin" and password == ADMIN_PASSWORD:
            st.session_state.admin_auth = True
            st.session_state.admin_user = username
            st.rerun()
        else:
            st.error(f"❌ {t('invalid_credentials')}")

    return False

# ============ Main ============
if not check_auth():
    st.stop()

events = load_events()

# ─── Header ───────────────────────────────────────
hdr_l, hdr_r = st.columns([5, 1])
with hdr_l:
    st.markdown(f"### 🛡️ {t('super_admin')} — {t('event_management_system')}")
with hdr_r:
    if st.button(f"🚪 {t('logout')}", use_container_width=True):
        st.session_state.admin_auth = False
        st.rerun()

# ─── Two Tabs: Events | Settings ──────────────────
tab_events, tab_settings = st.tabs([
    f"📋 {t('manage_events_tab')}",
    f"⚙️ {t('settings_tab')}",
])

# ═════════════════ TAB 1: Events ═════════════════
with tab_events:
    # --- Dashboard stats ---
    total = len(events)
    cities = len(set(e.get("city", "") for e in events)) if events else 0
    free_count = len([e for e in events if e.get("price", 0) == 0])
    cat_count = len(set(e.get("category", "") for e in events)) if events else 0

    c1, c2, c3, c4 = st.columns(4)
    with c1:
        st.metric(f"📊 {t('total_events')}", total)
    with c2:
        st.metric(f"🏙️ {t('cities_covered')}", cities)
    with c3:
        st.metric(f"🆓 {t('free_events')}", free_count)
    with c4:
        st.metric(f"🏷️ {t('categories_count')}", cat_count)

    st.divider()

    # --- Filters ---
    col_f1, col_f2, col_f3 = st.columns(3)
    with col_f1:
        admin_city = st.selectbox(
            t("filter_city"),
            [t("all")] + CITIES,
            key="admin_filter_city"
        )
    with col_f2:
        admin_cat = st.selectbox(
            t("filter_category"),
            [t("all")] + [t_cat(c) for c in CATEGORIES],
            key="admin_filter_cat"
        )
    with col_f3:
        admin_search = st.text_input(t("search"), key="admin_search")

    # Map translated category back to internal name
    cat_label_to_key = {t_cat(c): c for c in CATEGORIES}

    display_events = events[::-1]
    if admin_city != t("all"):
        display_events = [e for e in display_events if e.get("city") == admin_city]
    if admin_cat != t("all"):
        internal_cat = cat_label_to_key.get(admin_cat, admin_cat)
        display_events = [e for e in display_events if e.get("category") == internal_cat]
    if admin_search:
        display_events = [e for e in display_events
                          if admin_search.lower() in e.get("title", "").lower()]

    st.caption(t("showing_of", count=len(display_events), total=len(events)))

    # --- Event list ---
    if not display_events:
        st.info(t("no_events_found"))
    else:
        for event in display_events:
            price = event.get("price", 0)
            price_str = t("free") if price == 0 else f"{int(price)} TMT"
            cat_display = t_cat(event.get("category", ""))
            eid = event["id"]

            with st.expander(
                f"{cat_display} · **{event.get('title', 'Untitled')}** — "
                f"{event.get('city', '')} · {price_str}"
            ):
                # ── Compact overview: image + info + inline actions ──
                ov_img, ov_info = st.columns([1, 5])
                with ov_img:
                    cur_img_path = pathlib.Path(__file__).parent.parent.parent / "data" / event.get("image", "")
                    if event.get("image") and cur_img_path.exists():
                        st.image(str(cur_img_path), width=90)
                    else:
                        st.markdown("🖼️", help="No image")
                with ov_info:
                    st.markdown(
                        f"📍 {event.get('venue', 'N/A')} · {event.get('city', 'N/A')} &nbsp;|&nbsp; "
                        f"📅 {str(event.get('date_start', 'N/A'))[:16]} &nbsp;|&nbsp; "
                        f"💰 {price_str}"
                    )
                    if event.get("description"):
                        st.caption(event["description"][:120])

                # Inline action buttons
                act1, act2, act3 = st.columns([1, 1, 4])
                with act1:
                    if st.button(f"📋 {t('duplicate')}", key=f"dup_{eid}", use_container_width=True):
                        new_event = event.copy()
                        new_event["id"] = generate_id()
                        new_event["title"] = f"{event['title']} (Copy)"
                        events.append(new_event)
                        save_events(events)
                        st.rerun()
                with act2:
                    if st.button(f"🗑️ {t('delete')}", key=f"del_{eid}", use_container_width=True):
                        events = [e for e in events if e.get("id") != eid]
                        save_events(events)
                        st.rerun()

                # ── Compact edit form ──
                with st.form(key=f"edit_{eid}"):
                    r1c1, r1c2, r1c3, r1c4 = st.columns([3, 3, 2, 2])
                    with r1c1:
                        e_title = st.text_input(t("title_field"), value=event.get("title", ""), key=f"ti_{eid}")
                    with r1c2:
                        e_venue = st.text_input(t("venue_label"), value=event.get("venue", ""), key=f"ve_{eid}")
                    with r1c3:
                        e_city = st.selectbox(t("event_city"), CITIES,
                                              index=CITIES.index(event.get("city", "Ashgabat"))
                                              if event.get("city") in CITIES else 0, key=f"ci_{eid}")
                    with r1c4:
                        e_cat = st.selectbox(t("event_category"), CATEGORIES,
                                             index=CATEGORIES.index(event.get("category", "Music"))
                                             if event.get("category") in CATEGORIES else 0, key=f"ca_{eid}")

                    r2c1, r2c2, r2c3, r2c4 = st.columns(4)
                    with r2c1:
                        e_price = st.number_input(t("price_label"), value=float(event.get("price", 0)),
                                                  min_value=0.0, step=5.0, key=f"pr_{eid}")
                    with r2c2:
                        e_pop = st.slider(t("popularity"), 1, 100,
                                          int(event.get("popularity", 50)), key=f"po_{eid}")
                    default_lat, default_lon = CITY_COORDS.get(event.get("city", "Ashgabat"), (37.9601, 58.3261))
                    with r2c3:
                        e_lat = st.number_input("Lat", value=float(event.get("lat", default_lat)),
                                                format="%.6f", step=0.001, key=f"lat_{eid}")
                    with r2c4:
                        e_lon = st.number_input("Lon", value=float(event.get("lon", default_lon)),
                                                format="%.6f", step=0.001, key=f"lon_{eid}")

                    dc1, dc2 = st.columns([4, 1])
                    with dc1:
                        e_desc = st.text_area(t("event_description"),
                                              value=event.get("description", ""), height=68, key=f"de_{eid}")
                    with dc2:
                        use_center = st.checkbox(t("use_city_center"), key=f"center_{eid}")

                    if st.form_submit_button(f"💾 {t('save')}", use_container_width=True):
                        for i, e in enumerate(events):
                            if e["id"] == eid:
                                events[i].update({
                                    "title": e_title, "venue": e_venue, "city": e_city,
                                    "category": e_cat, "price": e_price, "popularity": e_pop,
                                    "description": e_desc,
                                })
                                if use_center:
                                    lat, lon = CITY_COORDS.get(e_city, (37.9601, 58.3261))
                                else:
                                    lat, lon = e_lat, e_lon
                                events[i]["lat"] = lat
                                events[i]["lon"] = lon
                                break
                        save_events(events)
                        st.success(f"✅ {t('save')}")
                        st.rerun()

                # ── Compact image upload ──
                iup1, iup2, iup3 = st.columns([3, 1, 1])
                with iup1:
                    evt_img = st.file_uploader(
                        t("upload_image"), type=["jpg", "jpeg", "png", "webp"],
                        key=f"img_upload_{eid}", label_visibility="collapsed"
                    )
                with iup2:
                    if evt_img:
                        st.image(evt_img, width=80)
                with iup3:
                    if evt_img:
                        if st.button(f"💾 🖼️", key=f"save_img_{eid}", use_container_width=True):
                            IMG_DIR.mkdir(parents=True, exist_ok=True)
                            img_filename = f"{eid}.jpg"
                            img_path = IMG_DIR / img_filename
                            with open(img_path, "wb") as fimg:
                                fimg.write(evt_img.getbuffer())
                            try:
                                from PIL import Image as PILImage
                                pil_img = PILImage.open(img_path)
                                if pil_img.mode in ("RGBA", "P"):
                                    pil_img = pil_img.convert("RGB")
                                pil_img.thumbnail((400, 400), PILImage.LANCZOS)
                                pil_img.save(img_path, "JPEG", quality=80, optimize=True)
                            except Exception:
                                pass
                            from utils.data_loader import _image_cache
                            old_image = event.get("image", "")
                            _image_cache.pop(old_image, None)
                            _image_cache.pop(f"images/{img_filename}", None)
                            st.cache_data.clear()
                            for i, e in enumerate(events):
                                if e["id"] == eid:
                                    events[i]["image"] = f"images/{img_filename}"
                                    break
                            save_events(events)
                            st.rerun()

    # --- Add New Event form ---
    st.divider()
    st.markdown(f"#### ➕ {t('add_event')}")

    with st.form("add_event"):
        nc1, nc2, nc3, nc4 = st.columns([3, 3, 2, 2])
        with nc1:
            new_title = st.text_input(f"{t('title_field')} *", placeholder="Event name")
        with nc2:
            new_venue = st.text_input(f"{t('venue_label')} *", placeholder="Location name")
        with nc3:
            new_city = st.selectbox(f"{t('event_city')} *", CITIES, key="new_city")
        with nc4:
            new_cat = st.selectbox(f"{t('event_category')} *", CATEGORIES, key="new_cat")

        nd1, nd2, nd3, nd4, nd5, nd6 = st.columns(6)
        with nd1:
            new_date_start = st.date_input(t("start_date"),
                                           value=datetime.now().date() + timedelta(days=7))
        with nd2:
            new_time_start = st.time_input(t("start_time"),
                                           value=datetime.strptime("18:00", "%H:%M").time())
        with nd3:
            new_date_end = st.date_input(t("end_date"),
                                         value=datetime.now().date() + timedelta(days=7))
        with nd4:
            new_time_end = st.time_input(t("end_time"),
                                         value=datetime.strptime("21:00", "%H:%M").time())
        with nd5:
            new_price = st.number_input(t("price_label"), min_value=0.0, step=5.0, value=0.0)
        with nd6:
            new_pop = st.slider(t("popularity"), 1, 100, 50, key="new_pop")

        nl1, nl2, nl3, nl4 = st.columns([3, 1, 1, 1])
        with nl1:
            new_desc = st.text_input(t("event_description"), placeholder="Short description...", key="new_desc")
        with nl2:
            new_lat = st.number_input("Lat", value=37.9601, format="%.6f", step=0.001, key="new_lat")
        with nl3:
            new_lon = st.number_input("Lon", value=58.3261, format="%.6f", step=0.001, key="new_lon")
        with nl4:
            new_use_center = st.checkbox(t("use_city_center"), value=True, key="new_center")

        submit = st.form_submit_button(f"➕ {t('add_event')}", use_container_width=True, type="primary")
        if submit:
            if not new_title or not new_venue:
                st.error(f"⚠️ {t('fill_required')}")
            else:
                if new_use_center:
                    lat, lon = CITY_COORDS.get(new_city, (37.9601, 58.3261))
                else:
                    lat, lon = new_lat, new_lon
                new_event = {
                    "id": generate_id(),
                    "title": new_title,
                    "category": new_cat,
                    "city": new_city,
                    "venue": new_venue,
                    "date_start": datetime.combine(new_date_start, new_time_start).isoformat(),
                    "date_end": datetime.combine(new_date_end, new_time_end).isoformat(),
                    "price": new_price,
                    "popularity": new_pop,
                    "lat": lat,
                    "lon": lon,
                    "image": "images/event_default.jpg",
                    "icon": "",
                    "description": new_desc,
                }
                events.append(new_event)
                save_events(events)
                st.success(f"✅ {t('event_added')}")
                st.balloons()

# ═════════════════ TAB 2: Settings ═════════════════
with tab_settings:
    col_exp, col_imp = st.columns(2)

    with col_exp:
        st.markdown(f"#### 📤 {t('export_events')}")
        if events:
            json_str = json.dumps(events, indent=2, ensure_ascii=False)
            st.download_button(
                f"⬇️ {t('download_json')}",
                data=json_str,
                file_name=f"events_{datetime.now().strftime('%Y%m%d')}.json",
                mime="application/json",
                use_container_width=True
            )
            st.caption(f"{len(events)} {t('events_found')}")
        else:
            st.info(t("no_events"))

    with col_imp:
        st.markdown(f"#### 📥 {t('import_events')}")
        uploaded = st.file_uploader(t("upload_json"), type=["json"])

        if uploaded:
            try:
                content = uploaded.read().decode("utf-8")
                new_events = json.loads(content)
                if isinstance(new_events, list):
                    st.success(f"{len(new_events)} {t('events_found')}")
                    if st.button(f"📥 {t('import_btn')}", use_container_width=True,
                                 type="primary"):
                        existing_ids = {e.get("id") for e in events}
                        added = 0
                        for e in new_events:
                            if e.get("id") not in existing_ids:
                                events.append(e)
                                added += 1
                        save_events(events)
                        st.success(f"✅ +{added}")
                        st.rerun()
                else:
                    st.error("Invalid format — expected array")
            except Exception as ex:
                st.error(f"Error: {ex}")

    st.divider()

    # ─── Danger Zone ──────────────────────────────
    st.markdown(f"#### ⚠️ {t('danger_zone')}")
    with st.expander(f"🗑️ {t('delete_all')}"):
        st.warning(t("cannot_be_undone"))
        confirm = st.text_input(t("confirm_delete"))
        if st.button(f"🗑️ {t('delete_all')}", type="secondary"):
            if confirm == "DELETE":
                save_events([])
                st.success("✅")
                st.rerun()
            else:
                st.error(t("confirm_delete"))

# Footer
st.divider()
st.caption(f"🛡️ {t('super_admin')} v3.0")
