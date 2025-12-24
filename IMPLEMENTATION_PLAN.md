# 🎟️ Sharkiya Event Discovery - Comprehensive Upgrade Plan

## Project Overview

**Current State:** Streamlit-based event discovery app with Turkmen language interface, map functionality using Folium, and basic filtering capabilities.

**Target State:** Full-featured English event discovery platform with premium UI, robust map integration, complete admin panel, and modern user experience. Default location set to Ashgabat, Turkmenistan.

---

## Phase 1: Foundation & Architecture Refactor

### 1.1 Project Structure Reorganization
```
sharkiya-event-discovery/
├── app/
│   ├── __init__.py
│   ├── main.py                 # Main Streamlit entry point
│   ├── config.py               # Configuration constants
│   ├── database.py             # SQLite/JSON data management
│   ├── models.py               # Data models with validation
│   └── utils.py                # Helper functions
├── pages/
│   ├── 1_🏠_Home.py            # Landing/dashboard page
│   ├── 2_🗺️_Map.py             # Interactive map view
│   ├── 3_📋_Events.py          # Event list/grid view
│   ├── 4_⭐_Saved.py           # Saved events page
│   └── 5_🔧_Admin.py           # Admin panel (protected)
├── components/
│   ├── event_card.py           # Reusable event card component
│   ├── filters.py              # Filter sidebar components
│   ├── map_view.py             # Map rendering component
│   ├── auth.py                 # Authentication component
│   └── stats.py                # Statistics widgets
├── data/
│   ├── events.json             # Event data (fallback)
│   └── events.db               # SQLite database
├── assets/
│   ├── images/                 # Event images
│   ├── icons/                  # Category icons
│   └── styles/                 # Custom CSS
├── .streamlit/
│   └── config.toml             # Streamlit configuration
├── requirements.txt
└── README.md
```

### 1.2 Configuration Updates
- **Default Location:** Ashgabat (37.9601, 58.3261)
- **Language:** English (full translation)
- **Time Zone:** Asia/Ashgabat (UTC+5)
- **Currency:** TMT (Turkmen Manat)

---

## Phase 2: Language Translation (Turkmen → English)

### 2.1 UI Text Translation
| Turkmen | English |
|---------|---------|
| Mähallik Çäreler | Local Events |
| Şäher | City |
| Sene | Date |
| Görnüşi | Category |
| Gözleg | Search |
| Süzgüçler | Filters |
| Ählisi | All |
| Şu gün | Today |
| Ertir | Tomorrow |
| Şu hepdäniň ahyry | This Weekend |
| 7 günüň içinde | Within 7 Days |
| Ýakynda başlaýanlar | Starting Soon |
| Baha | Price |
| Meşhurlygy | Popularity |
| Saýlananlar | Saved |
| Jikme-jik | Details |
| Biletler | Tickets |
| Paýlaş | Share |
| Aralygy | Distance |
| Arassala | Clear |

### 2.2 Event Data Translation
- Translate all event titles, descriptions, and venue names
- Keep original Turkmen names in parentheses for cultural context
- Update date formats to international standard (YYYY-MM-DD)

---

## Phase 3: Map Functionality Complete Rewrite

### 3.1 Map Improvements
```python
# New Map Features
- Interactive clustering for dense event areas
- Custom category-based markers with icons
- Smooth zoom and pan animations
- Click-to-filter by map region
- Draw tools for radius/polygon selection
- Real-time event count overlay
- Street/Satellite view toggle
- Fullscreen mode
- Location search/geocoding
- Current location detection (with permission)
```

### 3.2 Enhanced Marker System
```python
CATEGORY_ICONS = {
    "Music": {"icon": "music", "color": "purple"},
    "Tech": {"icon": "laptop", "color": "blue"},
    "Sports": {"icon": "futbol", "color": "green"},
    "Food": {"icon": "utensils", "color": "orange"},
    "Art": {"icon": "palette", "color": "pink"},
    "Market": {"icon": "shopping-bag", "color": "cadetblue"},
    "Film": {"icon": "film", "color": "darkred"},
    "Wellness": {"icon": "spa", "color": "lightgreen"},
    "Business": {"icon": "briefcase", "color": "navy"},
    "Science": {"icon": "flask", "color": "darkblue"},
    "Kids": {"icon": "child", "color": "yellow"},
    "Travel": {"icon": "plane", "color": "lightblue"},
    "Community": {"icon": "users", "color": "gray"},
}
```

### 3.3 Map Interaction Improvements
- **Radius Filter:** Draggable circle with real-time update
- **Popup Cards:** Rich event preview with image, time, price
- **Route Planning:** "Get Directions" integration with Google Maps
- **Heat Map:** Event density visualization option
- **Cluster Groups:** Expandable clusters for close events

---

## Phase 4: Admin Panel Implementation

### 4.1 Authentication System
```python
# Admin authentication with session management
- Username/password authentication
- Session timeout (30 minutes)
- Password hashing (bcrypt)
- Admin activity logging
- Multiple admin accounts support
```

### 4.2 Admin Dashboard Features
```
┌─────────────────────────────────────────────────────────────┐
│                    📊 Admin Dashboard                        │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌──────────┐   │
│  │ 43       │  │ 12       │  │ 8        │  │ 85%      │   │
│  │ Total    │  │ This     │  │ Cities   │  │ Fill     │   │
│  │ Events   │  │ Week     │  │ Covered  │  │ Rate     │   │
│  └──────────┘  └──────────┘  └──────────┘  └──────────┘   │
│                                                             │
│  📈 Events by Category          📍 Events by City          │
│  ─────────────────────         ─────────────────────       │
│  [Bar Chart]                   [Pie Chart]                 │
│                                                             │
│  📅 Upcoming Events Preview                                │
│  ─────────────────────────────                             │
│  [Event List with Quick Actions]                           │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

### 4.3 Event Management (CRUD)
```python
# Event CRUD Operations
class EventManager:
    def create_event(data: EventCreate) -> Event
    def read_event(event_id: str) -> Event
    def update_event(event_id: str, data: EventUpdate) -> Event
    def delete_event(event_id: str) -> bool
    def list_events(filters: EventFilters) -> List[Event]
    def bulk_import(file: UploadFile) -> ImportResult
    def bulk_export(format: str) -> FileResponse
```

### 4.4 Admin Event Form
```
┌─────────────────────────────────────────────────────────────┐
│                    ✏️ Create/Edit Event                     │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  Title *          [___________________________________]     │
│                                                             │
│  Category *       [Dropdown: Music ▼]                       │
│                                                             │
│  City *           [Dropdown: Ashgabat ▼]                    │
│                                                             │
│  Venue *          [___________________________________]     │
│                                                             │
│  Date & Time *                                              │
│  Start: [📅 2025-01-15] [🕐 18:00]                         │
│  End:   [📅 2025-01-15] [🕐 21:00]                         │
│                                                             │
│  Location (Map Picker or Coordinates)                       │
│  ┌─────────────────────────────────┐                       │
│  │  [Interactive Map]              │  Lat: [37.9601]       │
│  │  Click to set location          │  Lon: [58.3261]       │
│  └─────────────────────────────────┘                       │
│                                                             │
│  Price (TMT)      [___50___]  ☐ Free Event                 │
│                                                             │
│  Description *    [                                   ]     │
│                   [          Multiline text area      ]     │
│                   [___________________________________]     │
│                                                             │
│  Image            [📁 Upload Image] or [🔗 Image URL]      │
│                                                             │
│  Popularity (1-100) [Slider: ████████░░ 75]                │
│                                                             │
│  ┌────────────┐  ┌────────────┐  ┌────────────┐           │
│  │  💾 Save   │  │ 👁️ Preview │  │  ❌ Cancel │           │
│  └────────────┘  └────────────┘  └────────────┘           │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

### 4.5 Bulk Operations
- **Import:** CSV/JSON file upload with validation
- **Export:** Download events as CSV/JSON
- **Duplicate:** Clone events with date offset
- **Archive:** Soft-delete past events
- **Restore:** Recover archived events

---

## Phase 5: User Interface Redesign

### 5.1 Premium Theme
```css
/* Color Palette */
:root {
    --primary: #6366F1;        /* Indigo */
    --primary-dark: #4F46E5;
    --secondary: #10B981;      /* Emerald */
    --accent: #F59E0B;         /* Amber */
    --background: #F8FAFC;
    --surface: #FFFFFF;
    --text-primary: #1E293B;
    --text-secondary: #64748B;
    --border: #E2E8F0;
    --success: #22C55E;
    --warning: #EAB308;
    --error: #EF4444;
}
```

### 5.2 Event Card Design
```
┌─────────────────────────────────────────┐
│  ┌─────────────────────────────────┐   │
│  │                                 │   │
│  │      [Event Image/Gradient]     │   │
│  │                                 │   │
│  │  🟣 Music                       │   │
│  └─────────────────────────────────┘   │
│                                         │
│  Jazz Night at Riverside                │
│  📍 Ashgabat • Magtymguly Avenue       │
│  📅 Dec 25, 2025 • 7:30 PM             │
│  💰 60 TMT • ⭐ 84% popularity         │
│                                         │
│  ┌──────────┐ ┌──────────┐ ┌────────┐ │
│  │ Details  │ │ ❤️ Save  │ │ Share  │ │
│  └──────────┘ └──────────┘ └────────┘ │
└─────────────────────────────────────────┘
```

### 5.3 Responsive Layout
- **Desktop:** 3-column grid with sidebar filters
- **Tablet:** 2-column grid with collapsible filters
- **Mobile:** Single column with bottom sheet filters

---

## Phase 6: Feature Enhancements

### 6.1 Enhanced Filtering System
```python
FILTER_OPTIONS = {
    "city": ["All", "Ashgabat", "Mary", "Türkmenabat", "Dashoguz", "Balkanabat", "Awaza"],
    "category": ["Music", "Tech", "Sports", "Food", "Art", "Market", "Film", "Wellness", "Business", "Science", "Kids", "Travel", "Community"],
    "date_preset": ["All", "Today", "Tomorrow", "This Weekend", "This Week", "This Month"],
    "price_range": [(0, 0), (1, 50), (51, 100), (101, 200), (200, None)],  # Free, Under 50, 50-100, etc.
    "time_of_day": ["Morning (6-12)", "Afternoon (12-17)", "Evening (17-22)", "Night (22-6)"],
    "sort_by": ["Relevance", "Date (Soonest)", "Price (Low to High)", "Price (High to Low)", "Popularity"],
}
```

### 6.2 Search Improvements
- Fuzzy search with typo tolerance
- Search history (last 5 searches)
- Search suggestions/autocomplete
- Voice search (if browser supports)

### 6.3 Event Details Page
```
┌─────────────────────────────────────────────────────────────┐
│  [Hero Image Gallery - Carousel]                            │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  🟣 Music                                    ❤️ Save | 📤  │
│                                                             │
│  Jazz Night at Riverside                                    │
│  ═══════════════════════════════════════                   │
│                                                             │
│  📍 Magtymguly Avenue — Riverside Park, Ashgabat           │
│  📅 December 25, 2025 • 7:30 PM - 10:00 PM                 │
│  💰 60 TMT per person                                       │
│  ⭐ 84% popularity rating                                   │
│                                                             │
│  ─────────────────────────────────────────────────────     │
│                                                             │
│  An outdoor evening of local jazz ensembles. Bring your    │
│  own blanket or rent seating on-site. Food vendors         │
│  available. Perfect for couples and music enthusiasts.     │
│                                                             │
│  ─────────────────────────────────────────────────────     │
│                                                             │
│  📍 Event Location                                          │
│  ┌───────────────────────────────────────────────────┐     │
│  │                                                    │     │
│  │              [Mini Map with Marker]                │     │
│  │                                                    │     │
│  └───────────────────────────────────────────────────┘     │
│                                                             │
│  ┌─────────────────┐  ┌─────────────────────────────┐     │
│  │  🎫 Get Tickets │  │  🗺️ Open in Google Maps    │     │
│  └─────────────────┘  └─────────────────────────────┘     │
│                                                             │
│  ─────────────────────────────────────────────────────     │
│                                                             │
│  Similar Events You Might Like                              │
│  ┌────────┐ ┌────────┐ ┌────────┐                         │
│  │ Event  │ │ Event  │ │ Event  │                         │
│  │  Card  │ │  Card  │ │  Card  │                         │
│  └────────┘ └────────┘ └────────┘                         │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

### 6.4 Notifications & Reminders
- Browser push notifications for saved events
- Email reminders (optional)
- Calendar export (ICS format)

---

## Phase 7: Technical Improvements

### 7.1 Data Management
```python
# SQLite Database Schema
CREATE TABLE events (
    id TEXT PRIMARY KEY,
    title TEXT NOT NULL,
    category TEXT NOT NULL,
    city TEXT NOT NULL,
    venue TEXT NOT NULL,
    date_start DATETIME NOT NULL,
    date_end DATETIME NOT NULL,
    price REAL DEFAULT 0,
    popularity INTEGER DEFAULT 50,
    lat REAL,
    lon REAL,
    image TEXT,
    description TEXT,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    is_active BOOLEAN DEFAULT 1
);

CREATE TABLE admins (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT UNIQUE NOT NULL,
    password_hash TEXT NOT NULL,
    email TEXT,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    last_login DATETIME
);

CREATE TABLE saved_events (
    session_id TEXT,
    event_id TEXT,
    saved_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (session_id, event_id),
    FOREIGN KEY (event_id) REFERENCES events(id)
);

CREATE TABLE analytics (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    event_id TEXT,
    action TEXT,  -- 'view', 'save', 'share', 'directions'
    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
);
```

### 7.2 Performance Optimizations
- Lazy loading for images
- Pagination for event lists (20 per page)
- Caching with TTL for static content
- Debounced search input
- Map tile caching

### 7.3 Error Handling
- Graceful fallbacks for missing data
- User-friendly error messages
- Automatic retry for network failures
- Offline mode for viewed events

---

## Phase 8: Testing & Quality Assurance

### 8.1 Test Coverage
- Unit tests for data processing functions
- Integration tests for CRUD operations
- UI tests for critical user flows
- Map interaction tests
- Mobile responsiveness tests

### 8.2 Validation Rules
```python
VALIDATION_RULES = {
    "title": {"min_length": 3, "max_length": 100, "required": True},
    "category": {"choices": CATEGORIES, "required": True},
    "city": {"choices": CITIES, "required": True},
    "venue": {"min_length": 5, "max_length": 200, "required": True},
    "date_start": {"type": "datetime", "min": "now", "required": True},
    "date_end": {"type": "datetime", "after": "date_start", "required": True},
    "price": {"type": "number", "min": 0, "max": 10000},
    "lat": {"type": "float", "min": 35, "max": 43},  # Turkmenistan bounds
    "lon": {"type": "float", "min": 52, "max": 67},
    "popularity": {"type": "int", "min": 1, "max": 100},
}
```

---

## Implementation Timeline

### Week 1: Foundation
- [ ] Project structure reorganization
- [ ] Configuration and constants setup
- [ ] Database schema implementation
- [ ] Language translation (UI)

### Week 2: Core Features
- [ ] Map rewrite with new features
- [ ] Enhanced filtering system
- [ ] Event card components
- [ ] Event details page

### Week 3: Admin Panel
- [ ] Authentication system
- [ ] Admin dashboard
- [ ] Event CRUD operations
- [ ] Bulk import/export

### Week 4: Polish & Testing
- [ ] UI/UX refinements
- [ ] Performance optimization
- [ ] Testing and bug fixes
- [ ] Documentation

---

## Dependencies

```txt
# requirements.txt
streamlit>=1.31.0
streamlit-folium>=0.18.0
folium>=0.15.0
pandas>=2.1.0
numpy>=1.24.0
Pillow>=10.0.0
bcrypt>=4.1.0
python-dateutil>=2.8.0
pydantic>=2.5.0
```

---

## Default Configuration

```python
# config.py
class Config:
    APP_TITLE = "Local Events"
    APP_ICON = "🎟️"
    
    # Default location: Ashgabat, Turkmenistan
    DEFAULT_LAT = 37.9601
    DEFAULT_LON = 58.3261
    DEFAULT_ZOOM = 12
    
    # Cities
    CITIES = [
        "Ashgabat",
        "Mary", 
        "Türkmenabat",
        "Dashoguz",
        "Balkanabat",
        "Awaza",
    ]
    
    # Categories with icons and colors
    CATEGORIES = {
        "Music": {"icon": "🎵", "color": "#8B5CF6"},
        "Tech": {"icon": "💻", "color": "#3B82F6"},
        "Sports": {"icon": "⚽", "color": "#22C55E"},
        "Food": {"icon": "🍽️", "color": "#F97316"},
        "Art": {"icon": "🎨", "color": "#EC4899"},
        "Market": {"icon": "🛍️", "color": "#14B8A6"},
        "Film": {"icon": "🎬", "color": "#DC2626"},
        "Wellness": {"icon": "🧘", "color": "#84CC16"},
        "Business": {"icon": "💼", "color": "#1E40AF"},
        "Science": {"icon": "🔬", "color": "#6366F1"},
        "Kids": {"icon": "👶", "color": "#FBBF24"},
        "Travel": {"icon": "✈️", "color": "#06B6D4"},
        "Community": {"icon": "👥", "color": "#6B7280"},
    }
    
    # Admin
    ADMIN_SESSION_TIMEOUT = 1800  # 30 minutes
    
    # Pagination
    EVENTS_PER_PAGE = 20
```

---

## Success Metrics

1. **User Engagement**
   - Average session duration > 3 minutes
   - Events saved per session > 2
   - Direction requests > 10% of views

2. **Admin Efficiency**
   - Event creation time < 2 minutes
   - Bulk import success rate > 95%

3. **Technical Performance**
   - Page load time < 3 seconds
   - Map render time < 1 second
   - Zero critical bugs in production

---

*Last Updated: December 24, 2024*
*Project Version: 2.0.0*
