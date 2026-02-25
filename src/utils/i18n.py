"""
Internationalization (i18n) module for Sharkiya Event Discovery.
Supports English (en), Russian (ru), and Turkmen (tk).
"""

import streamlit as st

LANGUAGES = {
    "en": "🇬🇧 English",
    "ru": "🇷🇺 Русский",
    "tk": "🇹🇲 Türkmen",
}

TRANSLATIONS = {
    # ─── Home Page ─────────────────────────────────
    "app_title": {
        "en": "Event Discovery",
        "ru": "Открытие Событий",
        "tk": "Çäreleri Tapyň",
    },
    "app_subtitle": {
        "en": "Your Gateway to Local Events in Turkmenistan",
        "ru": "Ваш путеводитель по событиям Туркменистана",
        "tk": "Türkmenistanda Ýerli Çärelere Girelge",
    },
    "upcoming_events": {
        "en": "Upcoming Events",
        "ru": "Предстоящие события",
        "tk": "Ýakynlaşýan Çäreler",
    },
    "cities_covered": {
        "en": "Cities Covered",
        "ru": "Города",
        "tk": "Şäherler",
    },
    "community": {
        "en": "Community",
        "ru": "Сообщество",
        "tk": "Jemgyýet",
    },
    "growing": {
        "en": "Growing",
        "ru": "Растёт",
        "tk": "Ösýär",
    },
    "live_now": {
        "en": "Live now",
        "ru": "Сейчас",
        "tk": "Häzir",
    },
    "quick_navigation": {
        "en": "🧭 Quick Navigation",
        "ru": "🧭 Быстрая Навигация",
        "tk": "🧭 Çalt Nawigasiýa",
    },
    "jump_to_section": {
        "en": "Jump to any section",
        "ru": "Перейти к любому разделу",
        "tk": "Islendik bölüme geçiň",
    },
    "browse_events": {
        "en": "📋 Browse Events",
        "ru": "📋 Обзор Событий",
        "tk": "📋 Çärelere Göz Aýlaň",
    },
    "browse_events_desc": {
        "en": "Find concerts, workshops, and more in your city.",
        "ru": "Найдите концерты, мастерклассы и многое другое в вашем городе.",
        "tk": "Şäheriňizde konsertleri, seminarlary we başgalary tapyň.",
    },
    "go_to_events": {
        "en": "Go to Events →",
        "ru": "К Событиям →",
        "tk": "Çärelere Git →",
    },
    "interactive_map": {
        "en": "🗺️ Interactive Map",
        "ru": "🗺️ Интерактивная Карта",
        "tk": "🗺️ Interaktiw Karta",
    },
    "interactive_map_desc": {
        "en": "Explore events near you on an interactive map.",
        "ru": "Исследуйте события рядом с вами на интерактивной карте.",
        "tk": "Interaktiw kartada golaýyňyzdaky çäreleri öwreniň.",
    },
    "open_map": {
        "en": "Open Map →",
        "ru": "Открыть Карту →",
        "tk": "Kartany Aç →",
    },
    "saved_events": {
        "en": "⭐ Saved Events",
        "ru": "⭐ Сохранённые",
        "tk": "⭐ Saklanan Çäreler",
    },
    "saved_events_desc": {
        "en": "Manage your bookmarked events.",
        "ru": "Управляйте избранными событиями.",
        "tk": "Belliklenen çäreleriňizi dolandyryň.",
    },
    "view_saved": {
        "en": "View Saved →",
        "ru": "Просмотр →",
        "tk": "Saklananlary Gör →",
    },
    "featured_events": {
        "en": "🔥 Featured Events",
        "ru": "🔥 Избранные События",
        "tk": "🔥 Saýlanan Çäreler",
    },
    "featured_events_desc": {
        "en": "Most popular events right now",
        "ru": "Самые популярные события сейчас",
        "tk": "Häzirki wagtda iň meşhur çäreler",
    },
    "no_events": {
        "en": "No events to display.",
        "ru": "Нет событий для показа.",
        "tk": "Görkezmek üçin çäre ýok.",
    },

    # ─── Events Page ───────────────────────────────
    "events_page_title": {
        "en": "Event Browser",
        "ru": "Обзор Событий",
        "tk": "Çäreler Brauzeri",
    },
    "events_page_subtitle": {
        "en": "Discover what's happening in Turkmenistan",
        "ru": "Узнайте, что происходит в Туркменистане",
        "tk": "Türkmenistanda nämeleriň bolýandygyny biliň",
    },
    "search_events": {
        "en": "Search events...",
        "ru": "Поиск событий...",
        "tk": "Çäreleri gözle...",
    },
    "filter_by_city": {
        "en": "Filter by City",
        "ru": "Фильтр по городу",
        "tk": "Şäher boýunça süzgüç",
    },
    "filter_by_category": {
        "en": "Filter by Category",
        "ru": "Фильтр по категории",
        "tk": "Kategoriýa boýunça süzgüç",
    },
    "sort_by": {
        "en": "Sort by",
        "ru": "Сортировать",
        "tk": "Tertiple",
    },
    "all_cities": {
        "en": "All Cities",
        "ru": "Все города",
        "tk": "Ähli Şäherler",
    },
    "all_categories": {
        "en": "All Categories",
        "ru": "Все категории",
        "tk": "Ähli Kategoriýalar",
    },
    "events_found": {
        "en": "events found",
        "ru": "событий найдено",
        "tk": "çäre tapyldy",
    },
    "free": {
        "en": "Free",
        "ru": "Бесплатно",
        "tk": "Mugt",
    },

    # ─── Map Page ──────────────────────────────────
    "map_page_title": {
        "en": "Event Map",
        "ru": "Карта Событий",
        "tk": "Çäre Kartasy",
    },
    "map_page_subtitle": {
        "en": "Find events near you",
        "ru": "Найдите события рядом с вами",
        "tk": "Golaýyňyzdaky çäreleri tapyň",
    },
    "showing_events": {
        "en": "Showing events",
        "ru": "Показаны события",
        "tk": "Çäreler görkezilýär",
    },

    # ─── Saved Events Page ─────────────────────────
    "saved_page_title": {
        "en": "Saved Events",
        "ru": "Сохранённые События",
        "tk": "Saklanan Çäreler",
    },
    "saved_page_subtitle": {
        "en": "Your bookmarked events",
        "ru": "Ваши избранные события",
        "tk": "Belliklenen çäreler",
    },
    "no_saved_events": {
        "en": "You haven't saved any events yet.",
        "ru": "Вы ещё не сохранили ни одного события.",
        "tk": "Siz entek hiç hili çäre saklamadyňyz.",
    },
    "remove": {
        "en": "Remove",
        "ru": "Удалить",
        "tk": "Aýyr",
    },

    # ─── About Page ────────────────────────────────
    "about_title": {
        "en": "About",
        "ru": "О приложении",
        "tk": "Hakynda",
    },
    "about_description": {
        "en": "Event Discovery helps you find and explore local events across Turkmenistan.",
        "ru": "Приложение помогает находить и исследовать местные события по всему Туркменистану.",
        "tk": "Çäre Tapyjy Türkmenistanyň çäginde ýerli çäreleri tapmaga we öwrenmäge kömek edýär.",
    },

    # ─── Admin Page ────────────────────────────────
    "admin_title": {
        "en": "Admin Panel",
        "ru": "Панель Администратора",
        "tk": "Dolandyryjy Paneli",
    },
    "admin_login": {
        "en": "Admin Login",
        "ru": "Вход Администратора",
        "tk": "Dolandyryjy Girişi",
    },
    "password": {
        "en": "Password",
        "ru": "Пароль",
        "tk": "Açar söz",
    },
    "login": {
        "en": "Login",
        "ru": "Войти",
        "tk": "Giriş",
    },
    "logout": {
        "en": "Logout",
        "ru": "Выход",
        "tk": "Çykyş",
    },
    "add_event": {
        "en": "Add Event",
        "ru": "Добавить событие",
        "tk": "Çäre goş",
    },
    "edit_event": {
        "en": "Edit Event",
        "ru": "Редактировать",
        "tk": "Redaktirle",
    },
    "delete_event": {
        "en": "Delete Event",
        "ru": "Удалить событие",
        "tk": "Çäräni pozmak",
    },
    "event_title": {
        "en": "Event Title",
        "ru": "Название события",
        "tk": "Çäräniň ady",
    },
    "event_description": {
        "en": "Description",
        "ru": "Описание",
        "tk": "Beýany",
    },
    "event_venue": {
        "en": "Venue",
        "ru": "Место проведения",
        "tk": "Ýer",
    },
    "event_city": {
        "en": "City",
        "ru": "Город",
        "tk": "Şäher",
    },
    "event_category": {
        "en": "Category",
        "ru": "Категория",
        "tk": "Kategoriýa",
    },
    "event_price": {
        "en": "Price (TMT)",
        "ru": "Цена (TMT)",
        "tk": "Baha (TMT)",
    },
    "event_date": {
        "en": "Date",
        "ru": "Дата",
        "tk": "Sene",
    },
    "save": {
        "en": "Save",
        "ru": "Сохранить",
        "tk": "Sakla",
    },
    "cancel": {
        "en": "Cancel",
        "ru": "Отмена",
        "tk": "Ýatyr",
    },
    "import_json": {
        "en": "Import JSON Data",
        "ru": "Импорт JSON данных",
        "tk": "JSON Maglumatyny Getir",
    },
    "export_json": {
        "en": "Export JSON Data",
        "ru": "Экспорт JSON данных",
        "tk": "JSON Maglumatyny Çykar",
    },
    "manage_events": {
        "en": "Manage Events",
        "ru": "Управление событиями",
        "tk": "Çäreleri Dolandyr",
    },
    "upload_image": {
        "en": "Upload Event Image",
        "ru": "Загрузить изображение",
        "tk": "Surat Ýükle",
    },

    # ─── Common / Shared ──────────────────────────
    "language": {
        "en": "Language",
        "ru": "Язык",
        "tk": "Dil",
    },
    "settings": {
        "en": "Settings",
        "ru": "Настройки",
        "tk": "Sazlamalar",
    },
    "date_soonest": {
        "en": "Date (Soonest)",
        "ru": "Дата (ближайшие)",
        "tk": "Sene (iň ýakyn)",
    },
    "price_low_high": {
        "en": "Price (Low to High)",
        "ru": "Цена (по возрастанию)",
        "tk": "Baha (arzandan gymmat)",
    },
    "price_high_low": {
        "en": "Price (High to Low)",
        "ru": "Цена (по убыванию)",
        "tk": "Baha (gymmatdan arzan)",
    },
    "popularity": {
        "en": "Popularity",
        "ru": "Популярность",
        "tk": "Meşhurlyk",
    },
}


def get_lang() -> str:
    """Get current language from session state."""
    return st.session_state.get("lang", "en")


def t(key: str) -> str:
    """Translate a key to the current language."""
    lang = get_lang()
    entry = TRANSLATIONS.get(key, {})
    return entry.get(lang, entry.get("en", key))


def render_language_selector():
    """Render language selector in sidebar."""
    current = get_lang()
    options = list(LANGUAGES.keys())
    labels = list(LANGUAGES.values())
    idx = options.index(current) if current in options else 0

    with st.sidebar:
        st.markdown("---")
        selected = st.selectbox(
            "🌐 " + t("language"),
            options=options,
            format_func=lambda x: LANGUAGES[x],
            index=idx,
            key="lang_selector",
        )
        if selected != current:
            st.session_state["lang"] = selected
            st.rerun()
