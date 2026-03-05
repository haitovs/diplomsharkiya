import streamlit as st
from components.styles import inject_custom_css, render_hero
from utils.i18n import t, t_cat, render_language_selector, get_lang
from utils.data_loader import load_data
from config import CATEGORY_CONFIG

st.set_page_config(page_title="About | Event Discovery", page_icon="ℹ️", layout="wide")

inject_custom_css()
render_language_selector()

render_hero(
    title=t("about_title"),
    subtitle=t("about_description"),
    icon="ℹ️"
)

lang = get_lang()
df = load_data()

# ─── Platform Statistics ──────────────────────────
_ev_count = len(df)
_city_count = df["city"].nunique() if not df.empty else 0
_cat_count = df["category"].nunique() if not df.empty else 0
_free_count = len(df[df["price"] == 0]) if not df.empty else 0

st.markdown(f"""
<div style="display:flex;gap:1rem;margin:1.5rem 0;">
    <div style="flex:1;background:linear-gradient(135deg,#141B34,#1A2238);
        border:1px solid rgba(99,102,241,0.15);border-radius:12px;padding:1.25rem;text-align:center;">
        <p style="font-size:2rem;margin:0;">🎉</p>
        <p style="color:#F8FAFC;font-weight:700;font-size:1.5rem;margin:0.25rem 0 0 0;">{_ev_count}</p>
        <p style="color:#94A3B8;font-size:0.85rem;margin:0;">{t('total_events')}</p>
    </div>
    <div style="flex:1;background:linear-gradient(135deg,#141B34,#1A2238);
        border:1px solid rgba(99,102,241,0.15);border-radius:12px;padding:1.25rem;text-align:center;">
        <p style="font-size:2rem;margin:0;">🏙️</p>
        <p style="color:#F8FAFC;font-weight:700;font-size:1.5rem;margin:0.25rem 0 0 0;">{_city_count}</p>
        <p style="color:#94A3B8;font-size:0.85rem;margin:0;">{t('cities_covered')}</p>
    </div>
    <div style="flex:1;background:linear-gradient(135deg,#141B34,#1A2238);
        border:1px solid rgba(99,102,241,0.15);border-radius:12px;padding:1.25rem;text-align:center;">
        <p style="font-size:2rem;margin:0;">🏷️</p>
        <p style="color:#F8FAFC;font-weight:700;font-size:1.5rem;margin:0.25rem 0 0 0;">{_cat_count}</p>
        <p style="color:#94A3B8;font-size:0.85rem;margin:0;">{t('categories_count')}</p>
    </div>
    <div style="flex:1;background:linear-gradient(135deg,#141B34,#1A2238);
        border:1px solid rgba(99,102,241,0.15);border-radius:12px;padding:1.25rem;text-align:center;">
        <p style="font-size:2rem;margin:0;">🆓</p>
        <p style="color:#F8FAFC;font-weight:700;font-size:1.5rem;margin:0.25rem 0 0 0;">{_free_count}</p>
        <p style="color:#94A3B8;font-size:0.85rem;margin:0;">{t('free_events')}</p>
    </div>
</div>
""", unsafe_allow_html=True)

# ─── About Text ───────────────────────────────────
ABOUT_INTRO = {
    "en": """
### 🎯 What is Event Discovery?

**Event Discovery** is a modern, full-featured platform that connects people with local events
across **Turkmenistan**. From concerts and tech meetups to food festivals, art exhibitions,
sports competitions, and community gatherings — discover, explore, and attend events happening
in your city. The platform covers **6 major cities** and supports **13 event categories**
with real-time filtering, interactive maps, ticket purchasing, and multilingual support.
""",
    "ru": """
### 🎯 Что такое Event Discovery?

**Event Discovery** — это современная полнофункциональная платформа, которая связывает людей
с местными событиями по всему **Туркменистану**. От концертов и IT-встреч до фестивалей еды,
художественных выставок, спортивных соревнований и общественных мероприятий — находите,
исследуйте и посещайте события в вашем городе. Платформа охватывает **6 крупных городов**
и поддерживает **13 категорий событий** с фильтрацией в реальном времени, интерактивными
картами, покупкой билетов и многоязычной поддержкой.
""",
    "tk": """
### 🎯 Event Discovery näme?

**Event Discovery** — Türkmenistanyň çäginde adamlary ýerli çäreler bilen birleşdirýän
döwrebap, doly aýratynlykly platforma. Konsertlerden we IT duşuşyklaryndan nahar
festiwallaryna, sungat sergilerine, sport ýaryşlaryna we jemgyýetçilik çärelerine çenli —
şäheriňizde bolýan çäreleri tapyň, öwreniň we gatnaşyň. Platforma **6 esasy şäheri**
öz içine alýar we **13 çäre kategoriýasyny** real wagt süzgüçlemesi, interaktiw kartalar,
bilet satyn almak we köp dilli goldaw bilen üpjün edýär.
""",
}

st.markdown(ABOUT_INTRO.get(lang, ABOUT_INTRO["en"]))

st.divider()

# ─── Core Features ────────────────────────────────
FEATURES_TITLE = {
    "en": "### ✨ Platform Features",
    "ru": "### ✨ Возможности Платформы",
    "tk": "### ✨ Platformanyň Aýratynlyklary",
}

st.markdown(FEATURES_TITLE.get(lang, FEATURES_TITLE["en"]))

FEATURES = {
    "en": [
        ("📋", "Smart Event Browsing",
         "Browse all events with powerful filters — search by keyword, filter by city, category, "
         "date range (Today / This Week / This Month), and price slider. Full-text search across "
         "event titles and descriptions. Results update instantly as you adjust filters."),
        ("🗺️", "Interactive Map",
         "Explore events geographically on a Folium-powered interactive map with OpenStreetMap "
         "and CartoDB tile layers. Each event is marked with its category emoji. Click any marker "
         "to see a rich popup with event details, photos, pricing, and a Buy Ticket button."),
        ("🎫", "Ticket Purchase",
         "Buy tickets for paid events through a secure simulated checkout dialog. Enter card "
         "details, see a smooth progress bar during processing, and receive a transaction receipt "
         "with a unique ID. Purchase multiple tickets for the same event. View all your tickets "
         "in the My Tickets section."),
        ("⭐", "Save & Bookmark",
         "Save your favorite events with the heart button. All bookmarked events appear on the "
         "dedicated Saved Events page where you can review and manage your collection. "
         "Plan your schedule by saving events you want to attend."),
        ("🌐", "Multilingual Support",
         "Full interface translation in three languages: English, Russian (Русский), and "
         "Turkmen (Türkmen). All labels, buttons, categories, navigation, and content seamlessly "
         "switch between languages using the sidebar language selector."),
        ("🔧", "Admin Panel",
         "A password-protected Super Admin panel for event management. Create, edit, duplicate, "
         "and delete events. Upload event images with automatic optimization. Export/import events "
         "as JSON. Dashboard with real-time statistics — total events, cities, free events, "
         "and category counts."),
    ],
    "ru": [
        ("📋", "Умный Обзор Событий",
         "Просматривайте все события с мощными фильтрами — поиск по ключевому слову, фильтр "
         "по городу, категории, диапазону дат (Сегодня / Эта неделя / Этот месяц) и слайдер цен. "
         "Полнотекстовый поиск по названиям и описаниям событий. Результаты обновляются мгновенно."),
        ("🗺️", "Интерактивная Карта",
         "Исследуйте события на интерактивной карте Folium с поддержкой слоёв OpenStreetMap "
         "и CartoDB. Каждое событие отмечено эмодзи своей категории. Нажмите на маркер, чтобы "
         "увидеть всплывающее окно с деталями события, фотографиями, ценами и кнопкой покупки."),
        ("🎫", "Покупка Билетов",
         "Покупайте билеты на платные события через безопасный симулированный диалог оплаты. "
         "Введите данные карты, наблюдайте плавную обработку и получите чек транзакции "
         "с уникальным ID. Можно купить несколько билетов. Все билеты отображаются в разделе "
         "Мои Билеты."),
        ("⭐", "Сохранение и Закладки",
         "Сохраняйте понравившиеся события кнопкой с сердечком. Все закладки отображаются "
         "на специальной странице Сохранённых Событий, где можно управлять вашей коллекцией. "
         "Планируйте расписание, сохраняя события, которые хотите посетить."),
        ("🌐", "Многоязычная Поддержка",
         "Полный перевод интерфейса на три языка: Английский, Русский и Туркменский. Все надписи, "
         "кнопки, категории, навигация и контент плавно переключаются между языками через "
         "селектор в боковой панели."),
        ("🔧", "Панель Администратора",
         "Защищённая паролем панель Супер Администратора. Создание, редактирование, дублирование "
         "и удаление событий. Загрузка изображений с автоматической оптимизацией. Экспорт/импорт "
         "событий в JSON. Панель со статистикой — общее количество событий, городов, бесплатных "
         "событий и категорий."),
    ],
    "tk": [
        ("📋", "Akylly Çäre Brauzeri",
         "Ähli çärelere güýçli süzgüçler bilen göz aýlaň — açar söz boýunça gözleg, şäher, "
         "kategoriýa, sene aralygy (Şu gün / Şu hepde / Şu aý) we baha slaýderi boýunça süzgüç. "
         "Çäre atlaryny we beýanlaryny doly tekst gözlegi. Netijeler derrew täzelenýär."),
        ("🗺️", "Interaktiw Karta",
         "Folium esasly interaktiw kartada OpenStreetMap we CartoDB gatlak goldawy bilen "
         "çäreleri öwreniň. Her çäre kategoriýa emojisi bilen bellenýär. Islendik bellige "
         "basyp, çäre jikme-jiklikleri, suratlar, baha we Bilet satyn al düwmesini görüň."),
        ("🎫", "Bilet Satyn Almak",
         "Tölegli çärelere howpsuz simulýasiýa edilen töleg dialogynyň üsti bilen bilet satyn "
         "alyň. Kart maglumatlaryny giriziň, tekiz ilerleme zolagyny görüň we üýtgeşik belgili "
         "amal kwitansiýasyny alyň. Birmeňzeş çäre üçin birnäçe bilet satyn alyp bilersiňiz. "
         "Ähli biletleriňizi Meniň Biletlerim bölüminde görüň."),
        ("⭐", "Ýatda Saklamak",
         "Halaýan çäreleriňizi ýürek düwmesi bilen ýatda saklaň. Ähli bellikler Saklanan Çäreler "
         "sahypasynda görkezilýär, ol ýerde ýygyndyňyzy dolandyryp bilersiňiz. Gatnaşmak isleýän "
         "çäreleriňizi saklap, tertipnamaňyzy meýilleşdiriň."),
        ("🌐", "Köp Dilli Goldaw",
         "Interfeýs üç dilde doly terjime edildi: Iňlis, Rus we Türkmen. Ähli ýazgylar, "
         "düwmeler, kategoriýalar, nawigasiýa we mazmun gapdal paneldäki dil saýlaýjy arkaly "
         "diller arasynda üznüksiz geçýär."),
        ("🔧", "Dolandyryjy Paneli",
         "Parol bilen goralýan Baş Dolandyryjy paneli. Çäreleri döretmek, redaktirlemek, "
         "göçürmek we pozmak. Awtomatiki optimizasiýa bilen surat ýüklemek. Çäreleri JSON "
         "formatynda eksport/import etmek. Statistikaly dolandyryş paneli — jemi çäreler, "
         "şäherler, mugt çäreler we kategoriýa sanlary."),
    ],
}

features = FEATURES.get(lang, FEATURES["en"])
for i in range(0, len(features), 3):
    cols = st.columns(3)
    for j, col in enumerate(cols):
        if i + j < len(features):
            icon, title, desc = features[i + j]
            with col:
                st.markdown(f"""
<div style="background:#141B34;border:1px solid rgba(99,102,241,0.15);
    border-radius:12px;padding:1.5rem;height:100%;min-height:220px;">
    <p style="font-size:2rem;margin:0 0 0.5rem 0;">{icon}</p>
    <h4 style="color:#F8FAFC;margin:0 0 0.5rem 0;font-size:1rem;font-weight:600;">{title}</h4>
    <p style="color:#94A3B8;font-size:0.85rem;line-height:1.5;margin:0;">{desc}</p>
</div>
""", unsafe_allow_html=True)

st.divider()

# ─── Event Categories ─────────────────────────────
CAT_SECTION_TITLE = {
    "en": "### 🏷️ Event Categories",
    "ru": "### 🏷️ Категории Событий",
    "tk": "### 🏷️ Çäre Kategoriýalary",
}

st.markdown(CAT_SECTION_TITLE.get(lang, CAT_SECTION_TITLE["en"]))

cat_items = list(CATEGORY_CONFIG.items())
for i in range(0, len(cat_items), 4):
    cols = st.columns(4)
    for j, col in enumerate(cols):
        if i + j < len(cat_items):
            cat_key, cat_cfg = cat_items[i + j]
            cat_name = t_cat(cat_key)
            cat_icon = cat_cfg.get("icon", "📌")
            with col:
                st.markdown(f"""
<div style="background:#141B34;border:1px solid rgba(99,102,241,0.1);
    border-radius:10px;padding:1rem;text-align:center;margin-bottom:0.75rem;">
    <p style="font-size:1.8rem;margin:0;">{cat_icon}</p>
    <p style="color:#F8FAFC;font-weight:600;font-size:0.9rem;margin:0.25rem 0 0 0;">{cat_name}</p>
</div>
""", unsafe_allow_html=True)

st.divider()

# ─── How It Works ─────────────────────────────────
HOW_IT_WORKS_TITLE = {
    "en": "### 🔄 How It Works",
    "ru": "### 🔄 Как Это Работает",
    "tk": "### 🔄 Nähili Işleýär",
}

HOW_STEPS = {
    "en": [
        ("1️⃣", "Browse & Filter", "Open the Events page and use the sidebar filters to narrow down events by city, category, date, and price."),
        ("2️⃣", "Explore the Map", "Switch to the Map view to see events pinned geographically. Click markers for detailed event popups."),
        ("3️⃣", "Save Favorites", "Tap the heart icon on any event to bookmark it. Find all saved events on the Saved Events page."),
        ("4️⃣", "Buy Tickets", "For paid events, click the ticket button to open the secure checkout. Enter payment details and get your receipt."),
    ],
    "ru": [
        ("1️⃣", "Просматривайте и Фильтруйте", "Откройте страницу Событий и используйте фильтры в боковой панели: город, категория, дата и цена."),
        ("2️⃣", "Исследуйте Карту", "Переключитесь на Карту, чтобы увидеть события на карте. Нажмите на маркер для подробностей."),
        ("3️⃣", "Сохраняйте Избранное", "Нажмите на сердечко у любого события. Все сохранённые события на странице Избранного."),
        ("4️⃣", "Покупайте Билеты", "Для платных событий нажмите кнопку билета. Введите данные оплаты и получите квитанцию."),
    ],
    "tk": [
        ("1️⃣", "Göz Aýlaň we Süzgüçläň", "Çäreler sahypasyny açyň we gapdal paneldäki süzgüçleri ulanyň: şäher, kategoriýa, sene we baha."),
        ("2️⃣", "Kartany Öwreniň", "Çäreleri kartada görmek üçin Karta geçiň. Jikme-jiklikler üçin belgilere basyň."),
        ("3️⃣", "Halanlaryňyzy Saklaň", "Islendik çäredäki ýürek nyşanyna basyň. Saklanan çäreler Saklananlar sahypasynda."),
        ("4️⃣", "Bilet Satyn Alyň", "Tölegli çäreler üçin bilet düwmesine basyň. Töleg maglumatlaryny giriziň we kwitansiýaňyzy alyň."),
    ],
}

st.markdown(HOW_IT_WORKS_TITLE.get(lang, HOW_IT_WORKS_TITLE["en"]))

steps = HOW_STEPS.get(lang, HOW_STEPS["en"])
step_cols = st.columns(4)
for i, col in enumerate(step_cols):
    if i < len(steps):
        num, title, desc = steps[i]
        with col:
            st.markdown(f"""
<div style="background:#141B34;border:1px solid rgba(99,102,241,0.12);
    border-radius:12px;padding:1.25rem;text-align:center;min-height:180px;">
    <p style="font-size:1.8rem;margin:0;">{num}</p>
    <h4 style="color:#F8FAFC;font-size:0.95rem;font-weight:600;margin:0.5rem 0;">{title}</h4>
    <p style="color:#94A3B8;font-size:0.82rem;line-height:1.5;margin:0;">{desc}</p>
</div>
""", unsafe_allow_html=True)

st.divider()

# ─── Cities Covered ───────────────────────────────
CITIES_TABLE = {
    "en": """
### 🏙️ Cities Covered

| City | Region | Status |
|------|--------|--------|
| Ashgabat | Ahal | ✅ Active |
| Mary | Mary | ✅ Active |
| Türkmenabat | Lebap | ✅ Active |
| Dashoguz | Dashoguz | ✅ Active |
| Balkanabat | Balkan | ✅ Active |
| Awaza | Turkmenbashi | ✅ Active |
""",
    "ru": """
### 🏙️ Города

| Город | Регион | Статус |
|-------|--------|--------|
| Ашхабад | Ахал | ✅ Активен |
| Мары | Мары | ✅ Активен |
| Туркменабат | Лебап | ✅ Активен |
| Дашогуз | Дашогуз | ✅ Активен |
| Балканабат | Балкан | ✅ Активен |
| Аваза | Туркменбаши | ✅ Активен |
""",
    "tk": """
### 🏙️ Şäherler

| Şäher | Welaýat | Ýagdaýy |
|-------|---------|---------|
| Aşgabat | Ahal | ✅ Işjeň |
| Mary | Mary | ✅ Işjeň |
| Türkmenabat | Lebap | ✅ Işjeň |
| Daşoguz | Daşoguz | ✅ Işjeň |
| Balkanabat | Balkan | ✅ Işjeň |
| Awaza | Türkmenbaşy | ✅ Işjeň |
""",
}

st.markdown(CITIES_TABLE.get(lang, CITIES_TABLE["en"]))

st.divider()

# ─── Tech Stack ───────────────────────────────────
TECH_TITLE = {
    "en": "### ⚙️ Technology Stack",
    "ru": "### ⚙️ Технологический Стек",
    "tk": "### ⚙️ Tehnologiýa Steýki",
}

st.markdown(TECH_TITLE.get(lang, TECH_TITLE["en"]))

TECH_ITEMS = [
    ("🐍", "Python / Streamlit", "Core framework"),
    ("🗺️", "Folium + Leaflet", "Interactive maps"),
    ("📊", "Pandas", "Data processing"),
    ("🎨", "Custom CSS", "Premium UI/UX"),
    ("💾", "JSON", "Data storage"),
    ("🌐", "i18n", "EN / RU / TK"),
]

tech_cols = st.columns(6)
for i, col in enumerate(tech_cols):
    icon, name, desc = TECH_ITEMS[i]
    with col:
        st.markdown(f"""
<div style="background:#141B34;border:1px solid rgba(99,102,241,0.1);
    border-radius:10px;padding:1rem;text-align:center;">
    <p style="font-size:1.5rem;margin:0;">{icon}</p>
    <p style="color:#F8FAFC;font-weight:600;font-size:0.8rem;margin:0.25rem 0 0 0;">{name}</p>
    <p style="color:#64748B;font-size:0.7rem;margin:0;">{desc}</p>
</div>
""", unsafe_allow_html=True)

st.markdown("")

# ─── Footer ──────────────────────────────────────
st.markdown("---")
FOOTER = {
    "en": "*Version 6.0 — Built with Streamlit — Event Discovery Platform for Turkmenistan*",
    "ru": "*Версия 6.0 — Создано на Streamlit — Платформа Открытия Событий Туркменистана*",
    "tk": "*Wersiýa 6.0 — Streamlit bilen döredildi — Türkmenistan üçin Çäre Tapyş Platformasy*",
}
st.markdown(FOOTER.get(lang, FOOTER["en"]))
