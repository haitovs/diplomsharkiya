"""
Event Discovery — Custom Styles
Centralized CSS injection for premium Streamlit UI.
"""

import html as _html
import streamlit as st


def _esc(text: str) -> str:
    """Escape text for safe HTML embedding."""
    return _html.escape(str(text)) if text else ""

_CSS = """
    <style>
    /* ── Google Font (preconnect for speed) ───── */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');

    /* ── Single animation (fadeIn only, no infinite loops) ── */
    @keyframes fadeInUp {
        from { opacity: 0; transform: translateY(12px); }
        to   { opacity: 1; transform: translateY(0); }
    }

    /* ── Global Overrides ──────────────────────── */
    html, body, [class*="css"] { font-family: 'Inter', sans-serif !important; }
    html { scroll-behavior: smooth; }

    /* ── Sidebar Branding ──────────────────────── */
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #0A0E27 0%, #141B34 100%) !important;
    }
    [data-testid="stSidebar"] [data-testid="stMarkdown"] { color: #F8FAFC; }
    [data-testid="stSidebar"]::before {
        content: "🎟️ EventHub";
        display: block; padding: 1.5rem 1rem 0.5rem;
        font-size: 1.5rem; font-weight: 700;
        background: linear-gradient(135deg, #6366F1, #10B981);
        -webkit-background-clip: text; -webkit-text-fill-color: transparent;
        background-clip: text; letter-spacing: -0.02em;
    }
    [data-testid="stSidebarNav"] { display: none !important; }

    /* ── Typography ────────────────────────────── */
    h1 {
        font-weight: 700 !important; letter-spacing: -0.03em !important;
        background: linear-gradient(135deg, #6366F1, #10B981);
        -webkit-background-clip: text; -webkit-text-fill-color: transparent; background-clip: text;
    }
    h2, h3 { font-weight: 600 !important; letter-spacing: -0.02em !important; }
    .hero-banner h1 {
        background: none !important; -webkit-text-fill-color: white !important; color: white !important;
    }

    /* ── Metric Cards ──────────────────────────── */
    [data-testid="stMetric"] {
        background: linear-gradient(135deg, #141B34 0%, #1A2238 100%);
        border: 1px solid rgba(99,102,241,0.15); border-radius: 12px;
        padding: 1rem 1.25rem; box-shadow: 0 4px 6px -1px rgba(0,0,0,0.3);
    }
    [data-testid="stMetric"]:hover {
        border-color: rgba(99,102,241,0.4); transform: translateY(-2px);
    }
    [data-testid="stMetric"] label {
        color: #94A3B8 !important; font-weight: 500; font-size: 0.85rem;
        text-transform: uppercase; letter-spacing: 0.05em;
    }
    [data-testid="stMetric"] [data-testid="stMetricValue"] { color: #F8FAFC !important; font-weight: 700; font-size: 1.75rem; }
    [data-testid="stMetric"] [data-testid="stMetricDelta"] { color: #10B981 !important; }
    [data-testid="column"] [data-testid="stMetric"] {
        min-height: 110px; display: flex; flex-direction: column; justify-content: center;
    }

    /* ── Containers ────────────────────────────── */
    [data-testid="stVerticalBlock"] > div[data-testid="stExpander"],
    div[data-testid="stVerticalBlockBorderWrapper"] {
        border-radius: 12px !important; border-color: rgba(99,102,241,0.12) !important;
    }
    div[data-testid="stVerticalBlockBorderWrapper"]:hover {
        border-color: rgba(99,102,241,0.35) !important;
        box-shadow: 0 4px 12px rgba(99,102,241,0.1);
    }

    /* ── Event Card ────────────────────────────── */
    .evt-card { animation: fadeInUp 0.35s ease both; }
    .evt-card:hover {
        transform: translateY(-3px);
        border-color: rgba(99,102,241,0.45) !important;
        box-shadow: 0 12px 28px -4px rgba(99,102,241,0.18);
    }
    .cat-badge {
        background: rgba(99,102,241,0.15); color: #818CF8;
        padding: 0.15rem 0.6rem; border-radius: 20px;
        font-size: 0.75rem; font-weight: 600; text-transform: uppercase; letter-spacing: 0.05em;
    }
    .price-free { box-shadow: 0 0 8px 1px rgba(16,185,129,0.2); }

    /* ── Buttons ────────────────────────────────── */
    .stButton > button {
        border-radius: 8px !important; font-weight: 600 !important;
        font-family: 'Inter', sans-serif !important;
        transition: all 0.2s ease !important;
    }
    .stButton > button:hover { transform: translateY(-1px); box-shadow: 0 4px 12px rgba(99,102,241,0.25); }
    .stButton > button:active { transform: scale(0.98); }
    .stButton > button[kind="primary"] {
        background: linear-gradient(135deg, #6366F1, #8B5CF6) !important; border: none !important;
    }
    .stButton > button[kind="primary"]:hover {
        background: linear-gradient(135deg, #818CF8, #A78BFA) !important;
    }

    /* ── Inputs ─────────────────────────────────── */
    .stSelectbox > div > div, .stMultiSelect > div > div,
    .stTextInput > div > div > input {
        border-radius: 8px !important; border-color: rgba(99,102,241,0.2) !important;
    }
    .stSelectbox > div > div:focus-within, .stMultiSelect > div > div:focus-within,
    .stTextInput > div > div > input:focus {
        border-color: #6366F1 !important; box-shadow: 0 0 0 2px rgba(99,102,241,0.15) !important;
    }

    /* ── Tabs ───────────────────────────────────── */
    .stTabs [data-baseweb="tab-list"] { gap: 0.5rem; }
    .stTabs [data-baseweb="tab"] { border-radius: 8px; padding: 0.5rem 1rem; font-weight: 500; }

    /* ── Misc ───────────────────────────────────── */
    .stProgress > div > div > div > div { background: linear-gradient(90deg, #6366F1, #10B981) !important; border-radius: 6px; }
    .stAlert { border-radius: 10px !important; }
    hr { border-color: rgba(99,102,241,0.12) !important; }
    .block-container { padding-bottom: 3rem; }

    /* ── Event row layout ──────────────────────── */
    .evt-row { display: flex; align-items: stretch; margin-bottom: 0.75rem; gap: 0; }
    .evt-row > div:first-child { flex: 1; min-width: 0; }
    .evt-row > div:first-child .evt-card { border-radius: 12px 0 0 12px !important; margin-bottom: 0 !important; height: 100%; }
    .evt-actions {
        flex: 0 0 80px; background: #141B34; border: 1px solid rgba(99,102,241,0.12);
        border-left: none; border-radius: 0 12px 12px 0;
        display: flex; flex-direction: column; align-items: center; justify-content: center;
        gap: 0.35rem; padding: 0.5rem 0.4rem;
    }

    /* ── Payment Dialog ──────────────────────────── */
    div[data-testid="stDialog"] .pay-btn button {
        background: linear-gradient(135deg, #10B981, #059669) !important;
        color: white !important; border: none !important; font-weight: 700 !important;
        font-size: 1rem !important; padding: 0.6rem 1.5rem !important; border-radius: 10px !important;
    }
    div[data-testid="stDialog"] .pay-btn button:hover {
        background: linear-gradient(135deg, #34D399, #10B981) !important;
        box-shadow: 0 6px 18px rgba(16,185,129,0.3) !important;
    }
    </style>
    """


def inject_custom_css():
    """Inject the pre-built CSS string. Must run every page render."""
    st.markdown(_CSS, unsafe_allow_html=True)


def render_hero(title: str, subtitle: str, icon: str = "🎟️", badge: str = "Event Discovery Platform"):
    """Render a premium gradient hero banner."""
    st.markdown(f"""
    <div class="hero-banner" style="
        background: linear-gradient(135deg, #6366F1 0%, #4F46E5 40%, #10B981 100%);
        padding: 3rem 2.5rem; border-radius: 16px; margin-bottom: 2rem;
        text-align: center; color: white; position: relative; overflow: hidden;
        box-shadow: 0 20px 40px -12px rgba(99,102,241,0.35);
    ">
        <p style="
            display: inline-block; padding: 0.3rem 1rem;
            background: rgba(255,255,255,0.15);
            border: 1px solid rgba(255,255,255,0.25);
            border-radius: 20px; font-size: 0.85rem; font-weight: 500;
            margin-bottom: 0.75rem;
        ">{icon} {badge}</p>
        <h1 style="
            color: white !important; margin: 0 0 0.5rem 0;
            font-size: 2.25rem; font-weight: 700; letter-spacing: -0.03em;
            background: none; -webkit-text-fill-color: white;
        ">{title}</h1>
        <p style="
            color: rgba(255,255,255,0.85) !important; font-size: 1.1rem;
            font-weight: 400; max-width: 500px; margin: 0 auto;
        ">{subtitle}</p>
    </div>
    """, unsafe_allow_html=True)


def render_section_header(title: str, subtitle: str = ""):
    """Render a styled section header."""
    sub_html = f'<p style="color: #94A3B8; margin-top: 0.25rem;">{subtitle}</p>' if subtitle else ""
    st.markdown(f"""
    <div style="margin: 1.5rem 0 1rem 0;">
        <h3 style="margin: 0; font-weight: 600;">{title}</h3>
        {sub_html}
    </div>
    """, unsafe_allow_html=True)


def render_event_card_html(title: str, venue: str, city: str, date_str: str,
                           price: float, category: str, cat_icon: str,
                           cat_color: str = "#6366F1", description: str = "",
                           free_text: str = "Free", image_data_uri: str = ""):
    """Render a premium styled event card using HTML."""
    # Escape all user-provided text to prevent broken HTML
    title = _esc(title)
    venue = _esc(venue)
    city = _esc(city)
    date_str = _esc(date_str)
    category = _esc(category)
    description = _esc(description)

    price_str = _esc(free_text) if price == 0 else f"{int(price)} TMT"
    price_bg = "rgba(16, 185, 129, 0.15)" if price == 0 else "rgba(99, 102, 241, 0.15)"
    price_fg = "#10B981" if price == 0 else "#818CF8"
    desc_html = f'<p style="color: #94A3B8; font-size: 0.85rem; margin: 0.5rem 0 0 0; line-height: 1.5;">{description[:120]}{"..." if len(description) > 120 else ""}</p>' if description else ""

    img_html = ""
    if image_data_uri:
        img_html = f'''<img src="{image_data_uri}" style="
            width: 100%; height: 100%; object-fit: cover; border-radius: 8px;
        " alt="{title}"/>'''

    price_class = "price-free" if price == 0 else ""

    return f"""
    <div class="evt-card" style="
        background: #141B34; border: 1px solid rgba(99, 102, 241, 0.12);
        border-left: 4px solid {cat_color}; border-radius: 12px;
        overflow: hidden; margin-bottom: 1rem;
    ">
        <div style="display: flex; align-items: stretch;">
            <div style="flex: 0 0 28%; max-width: 28%; min-height: 110px;">
                {img_html}
            </div>
            <div style="flex: 1; padding: 1rem 1.25rem; display: flex; flex-direction: column; justify-content: center;">
                <div style="display: flex; align-items: center; justify-content: space-between; margin-bottom: 0.4rem;">
                    <div style="display: flex; align-items: center; gap: 0.5rem;">
                        <span style="font-size: 1.25rem;">{cat_icon}</span>
                        <span class="cat-badge" style="
                            color: #818CF8;
                            padding: 0.15rem 0.6rem; border-radius: 20px;
                            font-size: 0.75rem; font-weight: 600; text-transform: uppercase;
                            letter-spacing: 0.05em;
                        ">{category}</span>
                    </div>
                    <div class="{price_class}" style="
                        background: {price_bg}; color: {price_fg};
                        padding: 0.35rem 0.85rem; border-radius: 8px;
                        font-weight: 700; font-size: 0.9rem; white-space: nowrap;
                    ">{price_str}</div>
                </div>
                <h4 style="margin: 0; font-size: 1.1rem; font-weight: 600; color: #F8FAFC;">{title}</h4>
                <p style="color: #94A3B8; font-size: 0.85rem; margin: 0.35rem 0 0 0;">
                    📍 {venue} · {city}&nbsp;&nbsp;📅 {date_str}
                </p>
                {desc_html}
            </div>
        </div>
    </div>
    """


# Color mapping for categories → actual hex values
CATEGORY_COLORS = {
    "Music": "#A855F7",
    "Tech": "#3B82F6",
    "Sports": "#22C55E",
    "Food": "#F97316",
    "Art": "#EC4899",
    "Market": "#5F9EA0",
    "Film": "#EF4444",
    "Wellness": "#4ADE80",
    "Business": "#1E40AF",
    "Science": "#8B5CF6",
    "Kids": "#FBBF24",
    "Travel": "#38BDF8",
    "Community": "#94A3B8",
}

def get_category_color_hex(category: str) -> str:
    """Get hex color for a category."""
    return CATEGORY_COLORS.get(category, "#6366F1")
