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
    "event_discovery_platform": {
        "en": "Event Discovery Platform",
        "ru": "Платформа Открытия Событий",
        "tk": "Çäreleri Tapyş Platformasy",
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

    # ─── Date Filter Presets ─────────────────────
    "all": {
        "en": "All",
        "ru": "Все",
        "tk": "Hemmesi",
    },
    "today": {
        "en": "Today",
        "ru": "Сегодня",
        "tk": "Şu gün",
    },
    "this_week": {
        "en": "This Week",
        "ru": "Эта неделя",
        "tk": "Şu hepde",
    },
    "this_month": {
        "en": "This Month",
        "ru": "Этот месяц",
        "tk": "Şu aý",
    },

    # ─── Admin Panel Extras ──────────────────────
    "super_admin": {
        "en": "Super Admin",
        "ru": "Супер Админ",
        "tk": "Baş Dolandyryjy",
    },
    "event_management_system": {
        "en": "Event Management System",
        "ru": "Система управления событиями",
        "tk": "Çäreleri dolandyryş ulgamy",
    },
    "admin_access_desc": {
        "en": "Administrative access for event management",
        "ru": "Административный доступ для управления событиями",
        "tk": "Çäreleri dolandyrmak üçin dolandyryjy girişi",
    },
    "dashboard": {
        "en": "Dashboard",
        "ru": "Панель",
        "tk": "Dolandyryş paneli",
    },
    "manage_events_tab": {
        "en": "Manage Events",
        "ru": "Управление",
        "tk": "Dolandyr",
    },
    "add_event_tab": {
        "en": "Add Event",
        "ru": "Добавить",
        "tk": "Goş",
    },
    "settings_tab": {
        "en": "Settings",
        "ru": "Настройки",
        "tk": "Sazlamalar",
    },
    "total_events": {
        "en": "Total Events",
        "ru": "Всего событий",
        "tk": "Jemi çäreler",
    },
    "free_events": {
        "en": "Free Events",
        "ru": "Бесплатные",
        "tk": "Mugt çäreler",
    },
    "categories_count": {
        "en": "Categories",
        "ru": "Категории",
        "tk": "Kategoriýalar",
    },
    "events_by_category": {
        "en": "Events by Category",
        "ru": "События по категориям",
        "tk": "Kategoriýa boýunça çäreler",
    },
    "events_by_city": {
        "en": "Events by City",
        "ru": "События по городам",
        "tk": "Şäher boýunça çäreler",
    },
    "duplicate": {
        "en": "Duplicate",
        "ru": "Дублировать",
        "tk": "Göçür",
    },
    "edit": {
        "en": "Edit",
        "ru": "Редактировать",
        "tk": "Üýtget",
    },
    "delete": {
        "en": "Delete",
        "ru": "Удалить",
        "tk": "Poz",
    },
    "delete_all": {
        "en": "Delete All Events",
        "ru": "Удалить все события",
        "tk": "Ähli çäreleri poz",
    },
    "confirm_delete": {
        "en": "Type 'DELETE' to confirm",
        "ru": "Введите 'DELETE' для подтверждения",
        "tk": "Tassyklamak üçin 'DELETE' ýazyň",
    },
    "danger_zone": {
        "en": "Danger Zone",
        "ru": "Опасная зона",
        "tk": "Howply zona",
    },
    "title_field": {
        "en": "Title",
        "ru": "Название",
        "tk": "Ady",
    },
    "venue_label": {
        "en": "Venue",
        "ru": "Место",
        "tk": "Ýer",
    },
    "price_label": {
        "en": "Price",
        "ru": "Цена",
        "tk": "Baha",
    },
    "start_date": {
        "en": "Start Date",
        "ru": "Дата начала",
        "tk": "Başlanýan senesi",
    },
    "end_date": {
        "en": "End Date",
        "ru": "Дата окончания",
        "tk": "Gutarýan senesi",
    },
    "start_time": {
        "en": "Start Time",
        "ru": "Время начала",
        "tk": "Başlanýan wagty",
    },
    "end_time": {
        "en": "End Time",
        "ru": "Время окончания",
        "tk": "Gutarýan wagty",
    },
    "showing_of": {
        "en": "Showing {count} of {total} events",
        "ru": "Показано {count} из {total} событий",
        "tk": "{total} çäreden {count} görkezilýär",
    },
    "filter_city": {
        "en": "Filter City",
        "ru": "Фильтр по городу",
        "tk": "Şäher süzgüji",
    },
    "filter_category": {
        "en": "Filter Category",
        "ru": "Фильтр по категории",
        "tk": "Kategoriýa süzgüji",
    },
    "search": {
        "en": "Search",
        "ru": "Поиск",
        "tk": "Gözleg",
    },
    "no_events_found": {
        "en": "No events found",
        "ru": "События не найдены",
        "tk": "Çäre tapylmady",
    },
    "logged_in_as": {
        "en": "Logged in as",
        "ru": "Вошли как",
        "tk": "Girildi",
    },
    "invalid_credentials": {
        "en": "Invalid credentials",
        "ru": "Неверные данные",
        "tk": "Nädogry maglumatlar",
    },
    "event_added": {
        "en": "Event added successfully!",
        "ru": "Событие успешно добавлено!",
        "tk": "Çäre üstünlikli goşuldy!",
    },
    "fill_required": {
        "en": "Please fill in required fields",
        "ru": "Заполните обязательные поля",
        "tk": "Zerur meýdanlary dolduryň",
    },
    "use_city_center": {
        "en": "Use city center",
        "ru": "Центр города",
        "tk": "Şäher merkezi",
    },
    "location_coords": {
        "en": "Location Coordinates",
        "ru": "Координаты",
        "tk": "Koordinatalar",
    },
    "export_events": {
        "en": "Export Events",
        "ru": "Экспорт событий",
        "tk": "Çäreleri eksport et",
    },
    "import_events": {
        "en": "Import Events",
        "ru": "Импорт событий",
        "tk": "Çäreleri import et",
    },
    "download_json": {
        "en": "Download JSON",
        "ru": "Скачать JSON",
        "tk": "JSON ýükle",
    },
    "upload_json": {
        "en": "Upload JSON",
        "ru": "Загрузить JSON",
        "tk": "JSON ýükle",
    },
    "import_btn": {
        "en": "Import",
        "ru": "Импорт",
        "tk": "Import",
    },
    "cannot_be_undone": {
        "en": "This cannot be undone!",
        "ru": "Это действие необратимо!",
        "tk": "Bu hereketi yzyna gaýtaryp bolmaýar!",
    },
    "username": {
        "en": "Username",
        "ru": "Имя пользователя",
        "tk": "Ulanyjy ady",
    },
    "map_note": {
        "en": "Map data from OpenStreetMap",
        "ru": "Данные карты: OpenStreetMap",
        "tk": "Karta maglumatlary: OpenStreetMap",
    },
    "reset_filters": {
        "en": "Reset Filters",
        "ru": "Сбросить фильтры",
        "tk": "Süzgüçleri arassala",
    },
    "clear_saved": {
        "en": "Clear All Saved",
        "ru": "Очистить сохранённые",
        "tk": "Hemmesini arassala",
    },

    # ─── Sidebar Navigation ──────────────────────
    "nav_home": {
        "en": "🏠 Home",
        "ru": "🏠 Главная",
        "tk": "🏠 Baş sahypa",
    },
    "nav_events": {
        "en": "📋 Events",
        "ru": "📋 События",
        "tk": "📋 Çäreler",
    },
    "nav_map": {
        "en": "🗺️ Map",
        "ru": "🗺️ Карта",
        "tk": "🗺️ Karta",
    },
    "nav_saved": {
        "en": "⭐ Saved Events",
        "ru": "⭐ Сохранённые",
        "tk": "⭐ Saklananlar",
    },
    "nav_about": {
        "en": "ℹ️ About",
        "ru": "ℹ️ О приложении",
        "tk": "ℹ️ Hakynda",
    },
    "nav_admin": {
        "en": "🔧 Admin",
        "ru": "🔧 Админ",
        "tk": "🔧 Dolandyryjy",
    },
}

# ─── Category name translations ─────────────────
CATEGORY_TRANSLATIONS = {
    "Music": {"en": "Music", "ru": "Музыка", "tk": "Saz"},
    "Tech": {"en": "Tech", "ru": "Технологии", "tk": "Tehnologiýa"},
    "Sports": {"en": "Sports", "ru": "Спорт", "tk": "Sport"},
    "Food": {"en": "Food", "ru": "Еда", "tk": "Tagam"},
    "Art": {"en": "Art", "ru": "Искусство", "tk": "Sungat"},
    "Market": {"en": "Market", "ru": "Рынок", "tk": "Bazar"},
    "Film": {"en": "Film", "ru": "Кино", "tk": "Film"},
    "Wellness": {"en": "Wellness", "ru": "Здоровье", "tk": "Saglyk"},
    "Business": {"en": "Business", "ru": "Бизнес", "tk": "Işewürlik"},
    "Science": {"en": "Science", "ru": "Наука", "tk": "Ylym"},
    "Kids": {"en": "Kids", "ru": "Дети", "tk": "Çagalar"},
    "Travel": {"en": "Travel", "ru": "Путешествия", "tk": "Syýahat"},
    "Community": {"en": "Community", "ru": "Сообщество", "tk": "Jemgyýet"},
}


def get_lang() -> str:
    """Get current language from session state."""
    return st.session_state.get("lang", "en")


def t(key: str, **kwargs) -> str:
    """Translate a key to the current language. Supports {placeholder} formatting."""
    lang = get_lang()
    entry = TRANSLATIONS.get(key, {})
    text = entry.get(lang, entry.get("en", key))
    if kwargs:
        try:
            text = text.format(**kwargs)
        except (KeyError, IndexError):
            pass
    return text


def t_cat(category: str) -> str:
    """Translate a category name to the current language."""
    lang = get_lang()
    entry = CATEGORY_TRANSLATIONS.get(category, {})
    return entry.get(lang, category)


def render_language_selector():
    """Render language selector and translated navigation in sidebar."""
    current = get_lang()
    options = list(LANGUAGES.keys())
    idx = options.index(current) if current in options else 0

    with st.sidebar:
        # Translated navigation links (replaces the hidden default nav)
        st.page_link("0_🏠_Home.py", label=t("nav_home"))
        st.page_link("pages/1_📋_Events.py", label=t("nav_events"))
        st.page_link("pages/2_🗺️_Map.py", label=t("nav_map"))
        st.page_link("pages/3_⭐_Saved_Events.py", label=t("nav_saved"))
        st.page_link("pages/4_ℹ️_About.py", label=t("nav_about"))
        st.page_link("pages/99_🔧_Admin.py", label=t("nav_admin"))

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
