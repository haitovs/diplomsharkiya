# Local Events Discovery — Streamlit Template (No Backend)

A quick, fully-clickable **template** to showcase how a *Local Events Discovery* app would work — using **static data only**.
It includes search, filters (date/city/category), sorting, an interactive map, a **Favorites** view, and a
details panel for each event. Everything runs locally — no backend or database.

## 🧰 Quickstart

```bash
# 1) Create a virtual environment (folder name: venv — not .venv)
python -m venv venv

# 2) Activate it
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate

# 3) Install deps
pip install -r requirements.txt

# 4) Run
streamlit run app.py
```

The app uses static sample data in `data/events.json`. Edit it to change events.

## 📦 What’s inside

- `app.py` — the Streamlit UI
- `data/events.json` — sample events (Warsaw-centric)
- `assets/` — place images here if you want to reference local files later
- `requirements.txt` — pinned deps
- `README.md` — this file

## 🧭 Features you can click

- **Top bar**: city, quick dates (Today / Weekend / 7 days / All), category chips, search box
- **Sorting**: soonest / price / popularity
- **Event cards**: Details, Save, Share (simulated), Tickets (stub)
- **Map**: toggle the Map tab to see event pins
- **Favorites**: saved events via session state (no login)

## 🛠️ Customize

- Add/edit events in `data/events.json` (title, time, price, coords)
- Tweak the UI quickly in `app.py` (tabs, filters, layout)
- Replace placeholder images/emoji with your own assets in `assets/`

Enjoy!
