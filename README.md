# 🎟️ Sharkiya Event Discovery

A modern event discovery platform for Turkmenistan. Find, explore, and save local events with an interactive map, powerful filters, and a full-featured admin panel.

![Version](https://img.shields.io/badge/version-2.0.0-blue)
![Python](https://img.shields.io/badge/python-3.9+-green)
![Streamlit](https://img.shields.io/badge/streamlit-1.31+-red)

## ✨ Features

### User Features
- **🗺️ Interactive Map** - Explore events on a Leaflet map with clustering, category-colored markers, and draw tools for radius filtering
- **📋 Event List** - Browse events with rich cards showing all details
- **🔍 Smart Filters** - Filter by city, category, date, price, and search
- **📍 Location-Based Search** - Draw a circle on the map to find nearby events
- **⭐ Save Events** - Save your favorite events for quick access
- **📤 Share** - Share events with friends (coming soon)

### Admin Features
- **📊 Dashboard** - Overview with statistics and charts
- **📝 Event Management** - Create, edit, duplicate, and delete events
- **📍 Map Location Picker** - Set event coordinates visually
- **📥 Import/Export** - Bulk import from JSON, export for backup
- **🔐 Secure Login** - Password-protected admin access

## 🚀 Quick Start

### Prerequisites
- Python 3.9 or higher
- pip package manager

### Installation

1. **Clone or navigate to the project:**
   ```bash
   cd sharkiya-event-discovery
   ```

2. **Create a virtual environment (recommended):**
   ```bash
   python -m venv venv
   venv\Scripts\activate  # Windows
   source venv/bin/activate  # macOS/Linux
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Run the application:**
   ```bash
   streamlit run main.py
   ```

5. **Access the app:**
   - Main App: http://localhost:8501
   - Admin Panel: Run `streamlit run admin.py` separately

### Quick Run (Windows)
Double-click `run.bat` to start the application.

## 📁 Project Structure

```
sharkiya-event-discovery/
├── app/                        # Core application modules
│   ├── __init__.py
│   ├── config.py               # Configuration & constants
│   ├── models.py               # Pydantic data models
│   ├── database.py             # Database operations
│   └── utils.py                # Helper functions
├── components/                 # Reusable UI components
│   ├── __init__.py
│   ├── ui_components.py        # Event cards, filters, etc.
│   └── map_view.py             # Map rendering
├── data/                       # Data storage
│   └── events.db               # SQLite database (auto-created)
├── main.py                     # Main application entry
├── admin.py                    # Admin panel
├── events.json                 # Event data (JSON)
├── requirements.txt            # Python dependencies
├── run.bat                     # Windows launcher
└── README.md                   # This file
```

## 🎯 Default Settings

- **Location:** Ashgabat, Turkmenistan (37.9601, 58.3261)
- **Language:** English
- **Currency:** TMT (Turkmen Manat)

## 🔧 Configuration

Edit `app/config.py` to customize:

```python
# Change default location
DEFAULT_LAT = 37.9601  # Ashgabat
DEFAULT_LON = 58.3261

# Add cities
CITIES = ["Ashgabat", "Mary", "Türkmenabat", ...]

# Customize categories
CATEGORIES = {
    "Music": {"icon": "🎵", "color": "#8B5CF6"},
    ...
}
```

## 🔐 Admin Access

Default credentials:
- **Username:** `admin`
- **Password:** `admin123`

⚠️ **Change the password in production!** Edit `ADMIN_PASSWORD` in `admin.py`.

## 📊 API/Data Format

Events are stored in JSON format:

```json
{
    "id": "evt001",
    "title": "Jazz Night at Riverside",
    "category": "Music",
    "city": "Ashgabat",
    "venue": "Magtymguly Avenue — Riverside Park",
    "date_start": "2025-12-28T19:30:00",
    "date_end": "2025-12-28T22:00:00",
    "price": 60,
    "popularity": 84,
    "lat": 37.9647,
    "lon": 58.3409,
    "image": "",
    "description": "An outdoor evening with local jazz ensembles."
}
```

## 🛠️ Technologies

- **Frontend:** Streamlit
- **Maps:** Folium, Leaflet
- **Data:** Pandas, Pydantic
- **Charts:** Plotly
- **Database:** SQLite (optional)

## 📝 License

MIT License - feel free to use for your diploma project!

## 👨‍💻 Author

Made with ❤️ in Turkmenistan

---

*Version 2.0.0 - December 2024*
