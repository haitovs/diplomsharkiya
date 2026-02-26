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
col_title, col_user, col_logout = st.columns([3, 1, 1])
with col_title:
    st.markdown(f"# 🛡️ {t('super_admin')} — {t('event_management_system')}")
with col_user:
    st.caption(f"👤 {t('logged_in_as')}: **{st.session_state.get('admin_user', 'admin')}**")
with col_logout:
    if st.button(f"🚪 {t('logout')}", use_container_width=True):
        st.session_state.admin_auth = False
        st.rerun()

st.divider()

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

            with st.expander(
                f"{cat_display} · **{event.get('title', 'Untitled')}** — "
                f"{event.get('city', '')} · {price_str}"
            ):
                col_info, col_actions = st.columns([3, 1])

                with col_info:
                    st.markdown(f"**ID:** `{event.get('id', 'N/A')}`")
                    st.markdown(f"**{t('venue_label')}:** {event.get('venue', 'N/A')}")
                    st.markdown(f"**{t('event_date')}:** {event.get('date_start', 'N/A')}")
                    st.markdown(f"**{t('price_label')}:** {price_str}")
                    if event.get("description"):
                        st.markdown(f"**{t('event_description')}:** {event['description'][:200]}")

                with col_actions:
                    if st.button(f"📋 {t('duplicate')}", key=f"dup_{event['id']}",
                                 use_container_width=True):
                        new_event = event.copy()
                        new_event["id"] = generate_id()
                        new_event["title"] = f"{event['title']} (Copy)"
                        events.append(new_event)
                        save_events(events)
                        st.rerun()

                    if st.button(f"🗑️ {t('delete')}", key=f"del_{event['id']}",
                                 use_container_width=True):
                        events = [e for e in events if e.get("id") != event["id"]]
                        save_events(events)
                        st.rerun()

                # Edit form (clean, flat)
                st.markdown(f"##### ✏️ {t('edit')}")
                with st.form(key=f"edit_{event['id']}"):
                    ec1, ec2 = st.columns(2)
                    with ec1:
                        e_title = st.text_input(t("title_field"), value=event.get("title", ""))
                        e_venue = st.text_input(t("venue_label"), value=event.get("venue", ""))
                        e_city = st.selectbox(t("event_city"), CITIES,
                                              index=CITIES.index(event.get("city", "Ashgabat"))
                                              if event.get("city") in CITIES else 0)
                        e_cat = st.selectbox(t("event_category"), CATEGORIES,
                                             index=CATEGORIES.index(event.get("category", "Music"))
                                             if event.get("category") in CATEGORIES else 0)
                    with ec2:
                        e_price = st.number_input(t("price_label"), value=float(event.get("price", 0)),
                                                  min_value=0.0, step=5.0)
                        e_pop = st.slider(t("popularity"), 1, 100,
                                          int(event.get("popularity", 50)))
                        e_desc = st.text_area(t("event_description"),
                                              value=event.get("description", ""), height=100)

                    if st.form_submit_button(f"💾 {t('save')}", use_container_width=True):
                        for i, e in enumerate(events):
                            if e["id"] == event["id"]:
                                events[i]["title"] = e_title
                                events[i]["venue"] = e_venue
                                events[i]["city"] = e_city
                                events[i]["category"] = e_cat
                                events[i]["price"] = e_price
                                events[i]["popularity"] = e_pop
                                events[i]["description"] = e_desc
                                lat, lon = CITY_COORDS.get(e_city, (37.9601, 58.3261))
                                events[i]["lat"] = lat
                                events[i]["lon"] = lon
                                break
                        save_events(events)
                        st.success(f"✅ {t('save')}")
                        st.rerun()

                # Image upload per event (outside form — file_uploader can't be in st.form)
                st.markdown(f"###### 🖼️ {t('upload_image')}")
                img_col_preview, img_col_upload = st.columns([1, 2])
                with img_col_preview:
                    # Show current image or new upload preview
                    evt_img = st.file_uploader(
                        t("upload_image"),
                        type=["jpg", "jpeg", "png", "webp"],
                        key=f"img_upload_{event['id']}"
                    )
                with img_col_upload:
                    if evt_img:
                        st.image(evt_img, width=180, caption="New")
                    elif event.get("image"):
                        cur_img_path = pathlib.Path(__file__).parent.parent.parent / "data" / event["image"]
                        if cur_img_path.exists():
                            st.image(str(cur_img_path), width=180, caption="Current")

                if evt_img:
                    if st.button(f"💾 {t('save')}", key=f"save_img_{event['id']}",
                                 type="primary"):
                        IMG_DIR.mkdir(parents=True, exist_ok=True)

                        # Always save as .jpg for consistency
                        img_filename = f"{event['id']}.jpg"
                        img_path = IMG_DIR / img_filename

                        # Write uploaded bytes to disk
                        with open(img_path, "wb") as fimg:
                            fimg.write(evt_img.getbuffer())

                        # Resize to thumbnail for performance
                        try:
                            from PIL import Image as PILImage
                            pil_img = PILImage.open(img_path)
                            if pil_img.mode in ("RGBA", "P"):
                                pil_img = pil_img.convert("RGB")
                            pil_img.thumbnail((400, 400), PILImage.LANCZOS)
                            pil_img.save(img_path, "JPEG", quality=80, optimize=True)
                        except Exception:
                            pass

                        # Clear old image path from cache if it changed
                        from utils.data_loader import _image_cache
                        old_image = event.get("image", "")
                        _image_cache.pop(old_image, None)
                        _image_cache.pop(f"images/{img_filename}", None)

                        # Also clear streamlit's data cache so load_data() refreshes
                        st.cache_data.clear()

                        # Update event record
                        new_image_path = f"images/{img_filename}"
                        for i, e in enumerate(events):
                            if e["id"] == event["id"]:
                                events[i]["image"] = new_image_path
                                break
                        save_events(events)
                        st.success(f"✅ {t('save')}")
                        st.rerun()

    # --- Add New Event form ---
    st.divider()
    st.markdown(f"### ➕ {t('add_event')}")

    with st.form("add_event"):
        ac1, ac2 = st.columns(2)

        with ac1:
            new_title = st.text_input(f"{t('title_field')} *", placeholder="Event name")
            new_cat = st.selectbox(f"{t('event_category')} *", CATEGORIES, key="new_cat")
            new_city = st.selectbox(f"{t('event_city')} *", CITIES, key="new_city")
            new_venue = st.text_input(f"{t('venue_label')} *", placeholder="Location name")
            new_price = st.number_input(t("event_price"), min_value=0.0, step=5.0, value=0.0)

        with ac2:
            new_date_start = st.date_input(f"{t('start_date')} *",
                                           value=datetime.now().date() + timedelta(days=7))
            new_time_start = st.time_input(f"{t('start_time')} *",
                                           value=datetime.strptime("18:00", "%H:%M").time())
            new_date_end = st.date_input(f"{t('end_date')} *",
                                         value=datetime.now().date() + timedelta(days=7))
            new_time_end = st.time_input(f"{t('end_time')} *",
                                         value=datetime.strptime("21:00", "%H:%M").time())
            new_pop = st.slider(t("popularity"), 1, 100, 50, key="new_pop")

        new_desc = st.text_area(t("event_description"), placeholder="...", key="new_desc")

        submit = st.form_submit_button(f"➕ {t('add_event')}", use_container_width=True,
                                       type="primary")
        if submit:
            if not new_title or not new_venue:
                st.error(f"⚠️ {t('fill_required')}")
            else:
                lat, lon = CITY_COORDS.get(new_city, (37.9601, 58.3261))
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
