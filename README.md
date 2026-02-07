# 🎟️ Sharkiya Event Discovery

**A modern event discovery platform for Turkmenistan**  
Find, explore, and manage local events with an interactive map, powerful filters, and admin panel.

![Version](https://img.shields.io/badge/version-2.1.0-blue)
![Python](https://img.shields.io/badge/python-3.9+-green)
![Streamlit](https://img.shields.io/badge/streamlit-1.31+-red)

---

## ✨ Features

### 🎯 User Features
- **🗺️ Interactive Map** - Leaflet map with category-colored markers and radius filtering
- **📋 Event Browsing** - Beautiful event cards with category badges and styled pricing  
- **🔍 Smart Filters** - Filter by city, category, date range, and price
- **📍 Radius Search** - Draw circles on map to find nearby events
- **⭐ Save Events** - Bookmark favorites for quick access
- **📤 Share** - Share event locations via Google Maps link
- **🎨 Modern UI** - Professional design with color-coded categories

### 🔧 Admin Features  
- **📝 Event Management** - Full CRUD operations
- **🗺️ Map Location Picker** - Visual coordinate selection
- **📊 Dashboard** - Statistics and analytics (planned)
- **📥 Import/Export** - JSON data management

---

## 🚀 Quick Start

### Prerequisites
- Python 3.9+
- pip package manager

### Installation

1. **Navigate to  project:**
   ```bash
   cd sharkiya-event-discovery
   ```

2. **Create virtual environment (recommended):**
   ```bash
   python -m venv venv
   venv\\Scripts\\activate  # Windows
   source venv/bin/activate  # macOS/Linux
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Run the application:**
   ```bash
   streamlit run app.py --server.port 8502
   ```

5. **Access at:** [http://localhost:8502](http://localhost:8502)

### Quick Run (Windows)
Double-click `start.bat` to launch automatically.

---

## 📁 Project Structure

```
sharkiya-event-discovery/
├── app.py                  # Main Streamlit application
├── admin.py                # Admin panel (separate)
├── config.py               # Configuration settings
├── state_manager.py        # Session state management
├── events.json             # Event data storage
├── requirements.txt        # Python dependencies
├── start.bat               # Windows launcher
└── README.md               # This file
```

---

## 🎯 Recent Updates (v2.1.0)

### Sprint 1: Critical Fixes ✅
- Fixed session state warnings
- Improved button layout (no more vertical text wrapping)
- Moved search to top of sidebar
- Added bordered event card containers
- Enhanced visual hierarchy with headings and emojis

### Sprint 2: Visual Polish ✅
- **Category Color Badges** - 8 distinct colors for easy identification
- **Enhanced Price Display** - "MUGT" for free, gold styling for paid
- **Modal Dialogs** - Professional `@st.dialog` implementation for event details
- **Larger Tab Buttons** - 50px height, bold text, active state highlighting
- **Working Share Button** - Generates Google Maps links with coordinates

### Final Enhancements ✅
- Map loading spinner and error handling
- Improved tab navigation with bigger, more prominent buttons
- Share functionality now shows clickable links

---

## 🎨 Category Colors

| Category | Color | Badge |
|----------|-------|-------|
| Wellness | Green (#10b981) | 🎫 |
| Music | Purple (#8b5cf6) | 🎵 |
| Art | Pink (#ec4899) | 🎨 |
| Sports | Blue (#3b82f6) | ⚽ |
| Tech | Indigo (#6366f1) | 💻 |
| Business | Amber (#f59e0b) | 💼 |
| Food | Orange (#f97316) | 🍽️ |
| Market | Teal (#14b8a6) | 🛍️ |

---

## 🗺️ Default Settings

- **Location:** Ashgabat, Turkmenistan (37.9601, 58.3261)
- **Language:** Turkmen (UI), English event support
- **Currency:** TMT (Turkmen Manat)
- **Map:** OpenStreetMap tiles via Folium

---

## 🔐 Admin Access

Run admin panel separately:
```bash
streamlit run admin.py
```

Default credentials:
- **Username:** `admin`
- **Password:** `admin123`

⚠️ **Change password in production!**

---

## 🛠️ Technologies

- **Frontend:** Streamlit 1.31+
- **Maps:** Folium, Leaflet, streamlit-folium
- **Data:** Pandas, Pydantic
- **Database:** JSON (future: SQLite)

---

## 📦 Distribution

For portable distribution without Python installation, see distribution strategies:

### Option A: Python + Launcher (Recommended)
- Size: ~50KB (before dependencies)
- User needs: Python 3.8+
- Install time: 2 minutes (auto-installs packages)
- Total disk: ~150MB

### Option B: PyInstaller Executable
- Size: 3+ GB
- User needs: Nothing
- Distribution: Copy folder
- Total disk: 3+ GB

**Recommendation:** Use Option A for 60x smaller size and easier maintenance!

---

## 📝 Event Data Format

Events stored in `events.json`:

```json
{
    "id": "evt001",
    "title": "Yoga in the Park (All Levels)",
    "category": "Wellness",
    "city": "Ashgabat",
    "venue": "Bagtyýarlyk Park",
    "date_start": "2025-12-25T10:00:00",
    "date_end": "2025-12-25T11:15:00",
    "price": 18,
    "popularity": 56,
    "lat": 37.9647,
    "lon": 58.3409,
    "image": "",
    "description": "Bring your mat, relax in nature..."
}
```

---

## 🐛 Troubleshooting

### Map doesn't load
- Check internet connection (map tiles require online access)
- Wait for loading spinner
- Check browser console for errors

### Share button doesn't work
- Ensure event has valid coordinates (lat/lon)
- Check if coordinates are within Turkmenistan bounds

### Search doesn't work
- Verify `events.json` is not corrupted
- Check search box is at top of sidebar
- Try clearing browser cache

---

## 📄 License

MIT License - Feel free to use for educational/diploma projects!

---

## 👨‍💻 Author

Made with ❤️ for Turkmenistan diploma project  
*Version 2.1.0 - January 2026*
