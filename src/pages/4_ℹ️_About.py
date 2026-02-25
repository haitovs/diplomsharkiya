import streamlit as st
from components.styles import inject_custom_css, render_hero
from utils.i18n import t, render_language_selector

st.set_page_config(page_title="About | Event Discovery", page_icon="ℹ️")

inject_custom_css()
render_language_selector()

render_hero(
    title=t("about_title"),
    subtitle=t("about_description"),
    icon="ℹ️"
)

# About content — bilingual via i18n
ABOUT_CONTENT = {
    "en": """
### 🎯 What is Event Discovery?

Event Discovery is a modern platform that connects people with local events
across Turkmenistan. From concerts and tech meetups to food festivals and art exhibitions
— discover what's happening in your city.

### ✨ Key Features
""",
    "ru": """
### 🎯 Что такое Event Discovery?

Event Discovery — это современная платформа, которая связывает людей с местными событиями
по всему Туркменистану. От концертов и IT-встреч до фестивалей еды и художественных выставок
— узнайте, что происходит в вашем городе.

### ✨ Основные Функции
""",
    "tk": """
### 🎯 Çäre Tapyjy näme?

Çäre Tapyjy — Türkmenistanyň çäginde adamlary ýerli çäreler bilen birleşdirýän
döwrebap platforma. Konsertlerden we IT duşuşyklaryndan nahar festiwallaryna we çeperçilik
sergilerine çenli — şäheriňizde nämeleriň bolýandygyny biliň.

### ✨ Esasy Aýratynlyklar
""",
}

FEATURES = {
    "en": [
        ("### 📋 Smart Browsing", "Filter events by city, category, date, and price. Full-text search included."),
        ("### 🗺️ Interactive Map", "Explore events geographically with rich popups showing all event details."),
        ("### ⭐ Save & Plan", "Bookmark your favorite events to build your personal event calendar."),
    ],
    "ru": [
        ("### 📋 Умный Поиск", "Фильтруйте события по городу, категории, дате и цене. Полнотекстовый поиск."),
        ("### 🗺️ Интерактивная Карта", "Исследуйте события на карте с подробными всплывающими окнами."),
        ("### ⭐ Сохранение", "Добавляйте избранные события в личный календарь."),
    ],
    "tk": [
        ("### 📋 Akylly Gözleg", "Çäreleri şäher, kategoriýa, sene we baha boýunça süzgüçläň. Doly tekst gözlegi."),
        ("### 🗺️ Interaktiw Karta", "Çäreleri kartada giňişleýin maglumatlary bolan pop-uplar bilen öwreniň."),
        ("### ⭐ Saklamak", "Halaýan çäreleriňizi bellikläp, şahsy çäre senenamany dörediň."),
    ],
}

from utils.i18n import get_lang
lang = get_lang()

st.markdown(ABOUT_CONTENT.get(lang, ABOUT_CONTENT["en"]))

col1, col2, col3 = st.columns(3)
features = FEATURES.get(lang, FEATURES["en"])
for col, (title, desc) in zip([col1, col2, col3], features):
    with col:
        with st.container(border=True):
            st.markdown(title)
            st.markdown(desc)

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

st.markdown("---")
st.markdown("*Version 5.0 • Built with Streamlit • Event Discovery*")
