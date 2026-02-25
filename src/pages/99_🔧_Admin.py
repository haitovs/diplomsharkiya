# 🔧 Admin Panel - Event Discovery
# Completely separate from user app

import streamlit as st
import pandas as pd
import pathlib
import json
from datetime import datetime, timedelta
import uuid

st.set_page_config(
    page_title="Admin - Local Events",
    page_icon="🔧",
    layout="wide"
)

from components.styles import inject_custom_css
from utils.i18n import t, render_language_selector
inject_custom_css()
render_language_selector()

# ============ Config ============
DATA_PATH = pathlib.Path(__file__).parent.parent.parent / "data" / "events.json"
ADMIN_PASSWORD = "admin123"

CITIES = ["Ashgabat", "Mary", "Türkmenabat", "Dashoguz", "Balkanabat", "Awaza"]
CATEGORIES = ["Music", "Tech", "Sports", "Food", "Art", "Market", "Film", "Wellness", "Business", "Science", "Kids", "Travel", "Community"]

CITY_COORDS = {
    "Ashgabat": (37.9601, 58.3261),
    "Mary": (37.6005, 61.8302),
    "Türkmenabat": (39.0733, 63.5786),
    "Dashoguz": (41.8387, 59.9650),
    "Balkanabat": (39.5104, 54.3672),
    "Awaza": (40.0224, 52.9693),
}

# ============ Auth ============
def check_auth():
    if "admin_auth" not in st.session_state:
        st.session_state.admin_auth = False
    
    if st.session_state.admin_auth:
        return True
    
    st.markdown(f"# 🔐 {t('admin_login')}")
    
    with st.form("login"):
        username = st.text_input("Username")
        password = st.text_input(t("password"), type="password")
        submit = st.form_submit_button(t("login"), use_container_width=True)
        
        if submit:
            if username == "admin" and password == ADMIN_PASSWORD:
                st.session_state.admin_auth = True
                st.session_state.admin_user = username
                st.rerun()
            else:
                st.error("❌ Invalid credentials")
    
    return False

# ============ Data Functions ============
def load_events():
    if not DATA_PATH.exists():
        return []
    try:
        with open(DATA_PATH, "r", encoding="utf-8") as f:
            return json.load(f)
    except:
        return []

def save_events(events):
    with open(DATA_PATH, "w", encoding="utf-8") as f:
        json.dump(events, f, indent=2, ensure_ascii=False)

def generate_id():
    return f"evt{uuid.uuid4().hex[:6]}"

# ============ Main App ============
if not check_auth():
    st.stop()

# Custom CSS
st.markdown("""
<style>
.admin-stat {
    background: linear-gradient(135deg, #1E293B, #334155);
    padding: 20px;
    border-radius: 12px;
    text-align: center;
    color: white;
}
.admin-stat h2 { color: #10B981; margin: 0; }
.admin-stat p { color: #94A3B8; margin: 0; }
</style>
""", unsafe_allow_html=True)

# Load data
events = load_events()
df = pd.DataFrame(events) if events else pd.DataFrame()

# Header
col1, col2, col3 = st.columns([2, 1, 1])
with col1:
    st.markdown(f"# 🔧 {t('admin_title')}")
with col2:
    st.caption(f"👤 Logged in as: **{st.session_state.get('admin_user', 'admin')}**")
with col3:
    if st.button(f"🚪 {t('logout')}", use_container_width=True):
        st.session_state.admin_auth = False
        st.rerun()

st.divider()

# Tabs
tabs = st.tabs(["📊 Dashboard", "📝 Manage Events", "➕ Add Event", "📥 Import/Export"])

# ============ Tab 1: Dashboard ============
with tabs[0]:
    st.subheader("📊 Dashboard")
    
    # Stats
    total = len(events)
    cities = len(set(e.get("city", "") for e in events)) if events else 0
    free = len([e for e in events if e.get("price", 0) == 0])
    categories = len(set(e.get("category", "") for e in events)) if events else 0
    
    cols = st.columns(4)
    with cols[0]:
        st.metric("Total Events", total)
    with cols[1]:
        st.metric("Cities", cities)
    with cols[2]:
        st.metric("Free Events", free)
    with cols[3]:
        st.metric("Categories", categories)
    
    st.divider()
    
    # Events by category (simple bar)
    if events:
        st.markdown("#### 📊 Events by Category")
        cat_counts = {}
        for e in events:
            cat = e.get("category", "Other")
            cat_counts[cat] = cat_counts.get(cat, 0) + 1
        
        for cat, count in sorted(cat_counts.items(), key=lambda x: -x[1]):
            st.progress(count / total, text=f"{cat}: {count}")
        
        st.divider()
        
        # Events by city
        st.markdown("#### 📍 Events by City")
        city_counts = {}
        for e in events:
            city = e.get("city", "Unknown")
            city_counts[city] = city_counts.get(city, 0) + 1
        
        for city, count in sorted(city_counts.items(), key=lambda x: -x[1]):
            st.progress(count / total, text=f"{city}: {count}")
    else:
        st.info("No events yet. Add some events to see statistics.")

# ============ Tab 2: Manage Events ============
with tabs[1]:
    st.subheader("📝 Manage Events")
    
    # Filters
    col1, col2, col3 = st.columns(3)
    with col1:
        admin_city = st.selectbox("Filter City", ["All"] + CITIES, key="admin_filter_city")
    with col2:
        admin_cat = st.selectbox("Filter Category", ["All"] + CATEGORIES, key="admin_filter_cat")
    with col3:
        admin_search = st.text_input("Search", key="admin_search")
    
    # Filter events
    # Default Sort: Latest first (Reverse order of list)
    # We create a display list, reversing the original events list which is usually chronological if appended
    display_events = events[::-1]
    
    if admin_city != "All":
        display_events = [e for e in display_events if e.get("city") == admin_city]
    if admin_cat != "All":
        display_events = [e for e in display_events if e.get("category") == admin_cat]
    if admin_search:
        display_events = [e for e in display_events if admin_search.lower() in e.get("title", "").lower()]
    
    st.caption(f"Showing {len(display_events)} of {len(events)} events")
    
    if not display_events:
        st.info("No events found")
    else:
        for event in display_events:
            with st.expander(f"📌 {event.get('title', 'Untitled')} — {event.get('city', '')} ({event.get('category', '')})"):
                col1, col2 = st.columns(2)
                
                with col1:
                    st.markdown(f"**ID:** `{event.get('id', 'N/A')}`")
                    st.markdown(f"**Venue:** {event.get('venue', 'N/A')}")
                    st.markdown(f"**Date:** {event.get('date_start', 'N/A')}")
                    st.markdown(f"**Price:** {event.get('price', 0)} TMT")
                    st.markdown(f"**Popularity:** {event.get('popularity', 50)}%")
                
                with col2:
                    st.markdown("**Description:**")
                    st.write(event.get("description", "No description"))
                    if event.get("lat") and event.get("lon"):
                        st.caption(f"📍 {event['lat']:.4f}, {event['lon']:.4f}")
                
                # Actions
                act_cols = st.columns(3)
                with act_cols[0]:
                    if st.button("📋 Duplicate", key=f"dup_{event['id']}", use_container_width=True):
                        new_event = event.copy()
                        new_event["id"] = generate_id()
                        new_event["title"] = f"{event['title']} (Copy)"
                        events.append(new_event)
                        save_events(events)
                        st.success("✅ Duplicated!")
                        st.rerun()
                
                with act_cols[1]:
                    with st.expander("✏️ Edit"):
                        with st.form(key=f"edit_{event['id']}"):
                            e_title = st.text_input("Title", value=event.get("title", ""))
                            e_venue = st.text_input("Venue", value=event.get("venue", ""))
                            e_price = st.number_input("Price", value=float(event.get("price", 0)))
                            e_desc = st.text_area("Description", value=event.get("description", ""))
                            
                            # Icon edit
                            e_icon = st.selectbox("Icon", ["Default", "music", "art", "tech", "sports", "business"], 
                                                index=["Default", "music", "art", "tech", "sports", "business"].index(event.get("icon", "Default")) if event.get("icon") in ["music", "art", "tech", "sports", "business"] else 0)
                            
                            if st.form_submit_button("💾 Save"):
                                for i, e in enumerate(events):
                                    if e["id"] == event["id"]:
                                        events[i]["title"] = e_title
                                        events[i]["venue"] = e_venue
                                        events[i]["price"] = e_price
                                        events[i]["description"] = e_desc
                                        if e_icon != "Default":
                                            events[i]["icon"] = e_icon
                                        break
                                save_events(events)
                                st.success("Saved!")
                                st.rerun()
                
                with act_cols[2]:
                    if st.button("🗑️ Delete", key=f"del_{event['id']}", use_container_width=True, type="secondary"):
                        events = [e for e in events if e.get("id") != event["id"]]
                        save_events(events)
                        st.success("🗑️ Deleted!")
                        st.rerun()

# ============ Tab 3: Add Event ============
with tabs[2]:
    st.subheader("➕ Add New Event")
    
    with st.form("add_event"):
        col1, col2 = st.columns(2)
        
        with col1:
            title = st.text_input("Title *", placeholder="Event name")
            category = st.selectbox("Category *", CATEGORIES)
            city = st.selectbox("City *", CITIES)
            venue = st.text_input("Venue *", placeholder="Location name")
            price = st.number_input("Price (TMT)", min_value=0.0, step=5.0, value=0.0)
        
        with col2:
            date_start = st.date_input("Start Date *", value=datetime.now().date() + timedelta(days=7))
            time_start = st.time_input("Start Time *", value=datetime.strptime("18:00", "%H:%M").time())
            date_end = st.date_input("End Date *", value=datetime.now().date() + timedelta(days=7))
            time_end = st.time_input("End Time *", value=datetime.strptime("21:00", "%H:%M").time())
            popularity = st.slider("Popularity", 1, 100, 50)
        
        # Location
        st.markdown("**📍 Location Coordinates**")
        loc_cols = st.columns(3)
        with loc_cols[0]:
            use_city_coords = st.checkbox("Use city center", value=True)
        with loc_cols[1]:
            default_lat = CITY_COORDS.get(city, (37.9601, 58.3261))[0]
            lat = st.number_input("Latitude", value=default_lat if use_city_coords else 37.9601, format="%.4f")
        with loc_cols[2]:
            default_lon = CITY_COORDS.get(city, (37.9601, 58.3261))[1]
            lon = st.number_input("Longitude", value=default_lon if use_city_coords else 58.3261, format="%.4f")
        
        
        # Icon Selection
        # CWD is src/, so path is assets/icons
        icon_path = pathlib.Path("assets/icons")
        available_icons = ["Default"]
        if icon_path.exists():
            available_icons += [f.stem for f in icon_path.glob("*.png")]
            
        icon_choice = st.selectbox("Select Icon", available_icons)
        
        description = st.text_area(t("event_description"), placeholder="Event description...")
        
        submit = st.form_submit_button(f"➕ {t('add_event')}", use_container_width=True, type="primary")
        
        if submit:
            if not title or not venue:
                st.error("⚠️ Please fill in required fields")
            else:
                layout_icon = ""
                if icon_choice != "Default":
                    layout_icon = icon_choice
                
                new_event = {
                    "id": generate_id(),
                    "title": title,
                    "category": category,
                    "city": city,
                    "venue": venue,
                    "date_start": datetime.combine(date_start, time_start).isoformat(),
                    "date_end": datetime.combine(date_end, time_end).isoformat(),
                    "price": price,
                    "popularity": popularity,
                    "lat": lat,
                    "lon": lon,
                    "image": "",
                    "icon": layout_icon, 
                    "description": description,
                }
                
                events.append(new_event)
                save_events(events)
                st.success(f"✅ Event '{title}' added successfully!")
                st.balloons()

    # ─── Image Upload (outside form) ─────────────────────────
    st.divider()
    st.markdown(f"### 🖼️ {t('upload_image')}")
    st.caption("Upload images for events. They will be saved in data/images/ and linked to the selected event.")

    if events:
        event_titles = {e["id"]: e.get("title", "Untitled") for e in events}
        selected_event_id = st.selectbox(
            "Select event to add image",
            options=list(event_titles.keys()),
            format_func=lambda x: event_titles[x],
            key="img_event_select"
        )

        uploaded_img = st.file_uploader(
            t("upload_image"),
            type=["jpg", "jpeg", "png", "webp"],
            key="event_img_upload"
        )

        if uploaded_img and selected_event_id:
            if st.button(f"💾 {t('save')}", key="save_img", type="primary"):
                img_dir = pathlib.Path(__file__).parent.parent.parent / "data" / "images"
                img_dir.mkdir(parents=True, exist_ok=True)

                ext = uploaded_img.name.split(".")[-1]
                img_filename = f"{selected_event_id}.{ext}"
                img_path = img_dir / img_filename

                with open(img_path, "wb") as f:
                    f.write(uploaded_img.getbuffer())

                # Update event in the list
                for e in events:
                    if e["id"] == selected_event_id:
                        e["image"] = f"images/{img_filename}"
                        break

                save_events(events)
                st.success(f"✅ Image saved for event: {event_titles[selected_event_id]}")
                st.image(str(img_path), width=300)
    else:
        st.info(t("no_events"))

# ============ Tab 4: Import/Export ============
with tabs[3]:
    st.subheader("📥 Import / Export")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("#### 📤 Export Events")
        
        if events:
            json_str = json.dumps(events, indent=2, ensure_ascii=False)
            st.download_button(
                "⬇️ Download JSON",
                data=json_str,
                file_name=f"events_{datetime.now().strftime('%Y%m%d')}.json",
                mime="application/json",
                use_container_width=True
            )
            st.caption(f"{len(events)} events ready for export")
        else:
            st.info("No events to export")
    
    with col2:
        st.markdown("#### 📥 Import Events")
        
        uploaded = st.file_uploader("Upload JSON", type=["json"])
        
        if uploaded:
            try:
                content = uploaded.read().decode("utf-8")
                new_events = json.loads(content)
                
                if isinstance(new_events, list):
                    st.success(f"Found {len(new_events)} events")
                    
                    if st.button("📥 Import", use_container_width=True, type="primary"):
                        existing_ids = {e.get("id") for e in events}
                        added = 0
                        for e in new_events:
                            if e.get("id") not in existing_ids:
                                events.append(e)
                                added += 1
                        
                        save_events(events)
                        st.success(f"✅ Imported {added} new events!")
                        st.rerun()
                else:
                    st.error("Invalid format - expected array")
            except Exception as e:
                st.error(f"Error: {e}")
    
    st.divider()
    
    # ============ Maintenance ============
    st.markdown("#### 🛠️ Maintenance")
    with st.expander("🎨 Auto-Assign Icons"):
        st.info("This will assign icons to events based on their category (e.g., 'Music' -> 'music.png').")
        if st.button("🚀 Run Auto-Assign", type="primary"):
            updated_count = 0
            icon_path = pathlib.Path("assets/icons")
            if not icon_path.exists():
                st.error("Assets folder not found!")
            else:
                available_icons = {f.stem.lower(): f.stem for f in icon_path.glob("*.png")}
                
                for e in events:
                    cat = e.get("category", "").lower()
                    current_icon = e.get("icon", "")
                    
                    # Mapping logic
                    assigned = ""
                    if cat in available_icons:
                        assigned = available_icons[cat]
                    elif "music" in cat: assigned = "music"
                    elif "art" in cat: assigned = "art"
                    elif "tech" in cat: assigned = "tech"
                    elif "sport" in cat: assigned = "sports"
                    
                    if assigned and not current_icon:
                        e["icon"] = assigned
                        updated_count += 1
                
                if updated_count > 0:
                    save_events(events)
                    st.success(f"✅ Assigned icons to {updated_count} events!")
                    st.rerun()
                else:
                    st.warning("No events needed updates (or no matching icons found).")
    
    # Danger zone
    st.markdown("#### ⚠️ Danger Zone")
    with st.expander("🗑️ Delete All Events"):
        st.warning("This cannot be undone!")
        confirm = st.text_input("Type 'DELETE' to confirm")
        
        if st.button("🗑️ Delete All", type="secondary"):
            if confirm == "DELETE":
                save_events([])
                st.success("All events deleted")
                st.rerun()
            else:
                st.error("Type 'DELETE' to confirm")

# Footer
st.divider()
st.caption("🔧 Admin Panel v2.0")
