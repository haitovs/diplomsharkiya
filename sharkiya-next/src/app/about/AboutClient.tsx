"use client";

import { Hero } from "@/components/ui/Hero";
import { StatCard } from "@/components/ui/StatCard";
import { useTranslation } from "@/i18n/config";
import { CATEGORIES } from "@/config/categories";
import type { Event } from "@/types/event";

interface AboutClientProps {
  events: Event[];
}

const ABOUT_INTRO: Record<string, string> = {
  en: "**Event Discovery** is a modern, full-featured platform that connects people with local events across **Turkmenistan**. From concerts and tech meetups to food festivals, art exhibitions, sports competitions, and community gatherings — discover, explore, and attend events happening in your city. The platform covers **6 major cities** and supports **13 event categories** with real-time filtering, interactive maps, ticket purchasing, and multilingual support.",
  ru: "**Event Discovery** — это современная полнофункциональная платформа, которая связывает людей с местными событиями по всему **Туркменистану**. От концертов и IT-встреч до фестивалей еды, художественных выставок, спортивных соревнований и общественных мероприятий — находите, исследуйте и посещайте события в вашем городе. Платформа охватывает **6 крупных городов** и поддерживает **13 категорий событий** с фильтрацией в реальном времени, интерактивными картами, покупкой билетов и многоязычной поддержкой.",
  tk: "**Event Discovery** — Türkmenistanyň çäginde adamlary ýerli çäreler bilen birleşdirýän döwrebap, doly aýratynlykly platforma. Konsertlerden we IT duşuşyklaryndan nahar festiwallaryna, sungat sergilerine, sport ýaryşlaryna we jemgyýetçilik çärelerine çenli — şäheriňizde bolýan çäreleri tapyň, öwreniň we gatnaşyň. Platforma **6 esasy şäheri** öz içine alýar we **13 çäre kategoriýasyny** real wagt süzgüçlemesi, interaktiw kartalar, bilet satyn almak we köp dilli goldaw bilen üpjün edýär.",
};

const FEATURES: Record<string, [string, string, string][]> = {
  en: [
    ["📋", "Smart Event Browsing", "Browse all events with powerful filters — search by keyword, filter by city, category, date range, and price slider. Results update instantly."],
    ["🗺️", "Interactive Map", "Explore events geographically on an interactive map with OpenStreetMap tiles. Each event is marked with its category emoji."],
    ["🎫", "Ticket Purchase", "Buy tickets for paid events through a simulated checkout dialog. Enter card details and receive a transaction receipt with a unique ID."],
    ["⭐", "Save & Bookmark", "Save your favorite events with the heart button. All bookmarked events appear on the dedicated Saved Events page."],
    ["🌐", "Multilingual Support", "Full interface translation in three languages: English, Russian, and Turkmen. All content seamlessly switches between languages."],
    ["🔧", "Admin Panel", "A password-protected Super Admin panel for event management. Create, edit, duplicate, and delete events. Import/export as JSON."],
  ],
  ru: [
    ["📋", "Умный Обзор Событий", "Просматривайте все события с мощными фильтрами — поиск по ключевому слову, фильтр по городу, категории, диапазону дат и слайдер цен."],
    ["🗺️", "Интерактивная Карта", "Исследуйте события на интерактивной карте с поддержкой слоёв OpenStreetMap. Каждое событие отмечено эмодзи своей категории."],
    ["🎫", "Покупка Билетов", "Покупайте билеты на платные события через симулированный диалог оплаты. Введите данные карты и получите чек транзакции."],
    ["⭐", "Сохранение и Закладки", "Сохраняйте понравившиеся события кнопкой с сердечком. Все закладки отображаются на странице Сохранённых Событий."],
    ["🌐", "Многоязычная Поддержка", "Полный перевод интерфейса на три языка: Английский, Русский и Туркменский. Контент плавно переключается между языками."],
    ["🔧", "Панель Администратора", "Защищённая паролем панель Супер Администратора. Создание, редактирование, дублирование и удаление событий. Экспорт/импорт в JSON."],
  ],
  tk: [
    ["📋", "Akylly Çäre Brauzeri", "Ähli çärelere güýçli süzgüçler bilen göz aýlaň — açar söz boýunça gözleg, şäher, kategoriýa, sene aralygy we baha slaýderi."],
    ["🗺️", "Interaktiw Karta", "OpenStreetMap gatlak goldawy bilen interaktiw kartada çäreleri öwreniň. Her çäre kategoriýa emojisi bilen bellenýär."],
    ["🎫", "Bilet Satyn Almak", "Tölegli çärelere simulýasiýa edilen töleg dialogynyň üsti bilen bilet satyn alyň. Kart maglumatlaryny giriziň we amal kwitansiýasyny alyň."],
    ["⭐", "Ýatda Saklamak", "Halaýan çäreleriňizi ýürek düwmesi bilen ýatda saklaň. Ähli bellikler Saklanan Çäreler sahypasynda görkezilýär."],
    ["🌐", "Köp Dilli Goldaw", "Interfeýs üç dilde doly terjime edildi: Iňlis, Rus we Türkmen. Mazmun diller arasynda üznüksiz geçýär."],
    ["🔧", "Dolandyryjy Paneli", "Parol bilen goralýan Baş Dolandyryjy paneli. Çäreleri döretmek, redaktirlemek, göçürmek we pozmak. JSON formatynda eksport/import."],
  ],
};

const HOW_STEPS: Record<string, [string, string, string][]> = {
  en: [
    ["1️⃣", "Browse & Filter", "Open Events page and use filters to narrow down events by city, category, date, and price."],
    ["2️⃣", "Explore the Map", "Switch to the Map view to see events pinned geographically. Click markers for details."],
    ["3️⃣", "Save Favorites", "Tap the heart icon on any event to bookmark it. Find all saved events on the Saved page."],
    ["4️⃣", "Buy Tickets", "For paid events, click the ticket button to open checkout. Enter payment details and get your receipt."],
  ],
  ru: [
    ["1️⃣", "Просматривайте и Фильтруйте", "Откройте страницу Событий и используйте фильтры: город, категория, дата и цена."],
    ["2️⃣", "Исследуйте Карту", "Переключитесь на Карту, чтобы увидеть события на карте. Нажмите на маркер для подробностей."],
    ["3️⃣", "Сохраняйте Избранное", "Нажмите на сердечко у любого события. Все сохранённые события на странице Избранного."],
    ["4️⃣", "Покупайте Билеты", "Для платных событий нажмите кнопку билета. Введите данные оплаты и получите квитанцию."],
  ],
  tk: [
    ["1️⃣", "Göz Aýlaň we Süzgüçläň", "Çäreler sahypasyny açyň we süzgüçleri ulanyň: şäher, kategoriýa, sene we baha."],
    ["2️⃣", "Kartany Öwreniň", "Çäreleri kartada görmek üçin Karta geçiň. Jikme-jiklikler üçin belgilere basyň."],
    ["3️⃣", "Halanlaryňyzy Saklaň", "Islendik çäredäki ýürek nyşanyna basyň. Saklanan çäreler Saklananlar sahypasynda."],
    ["4️⃣", "Bilet Satyn Alyň", "Tölegli çäreler üçin bilet düwmesine basyň. Töleg maglumatlaryny giriziň we kwitansiýaňyzy alyň."],
  ],
};

const CITIES_TABLE: Record<string, { headers: string[]; rows: string[][] }> = {
  en: {
    headers: ["City", "Region", "Status"],
    rows: [
      ["Ashgabat", "Ahal", "Active"], ["Mary", "Mary", "Active"],
      ["Türkmenabat", "Lebap", "Active"], ["Dashoguz", "Dashoguz", "Active"],
      ["Balkanabat", "Balkan", "Active"], ["Awaza", "Turkmenbashi", "Active"],
    ],
  },
  ru: {
    headers: ["Город", "Регион", "Статус"],
    rows: [
      ["Ашхабад", "Ахал", "Активен"], ["Мары", "Мары", "Активен"],
      ["Туркменабат", "Лебап", "Активен"], ["Дашогуз", "Дашогуз", "Активен"],
      ["Балканабат", "Балкан", "Активен"], ["Аваза", "Туркменбаши", "Активен"],
    ],
  },
  tk: {
    headers: ["Şäher", "Welaýat", "Ýagdaýy"],
    rows: [
      ["Aşgabat", "Ahal", "Işjeň"], ["Mary", "Mary", "Işjeň"],
      ["Türkmenabat", "Lebap", "Işjeň"], ["Daşoguz", "Daşoguz", "Işjeň"],
      ["Balkanabat", "Balkan", "Işjeň"], ["Awaza", "Türkmenbaşy", "Işjeň"],
    ],
  },
};

const SECTION_TITLES: Record<string, Record<string, string>> = {
  what: { en: "🎯 What is Event Discovery?", ru: "🎯 Что такое Event Discovery?", tk: "🎯 Event Discovery näme?" },
  features: { en: "✨ Platform Features", ru: "✨ Возможности Платформы", tk: "✨ Platformanyň Aýratynlyklary" },
  categories: { en: "🏷️ Event Categories", ru: "🏷️ Категории Событий", tk: "🏷️ Çäre Kategoriýalary" },
  how: { en: "🔄 How It Works", ru: "🔄 Как Это Работает", tk: "🔄 Nähili Işleýär" },
  cities: { en: "🏙️ Cities Covered", ru: "🏙️ Города", tk: "🏙️ Şäherler" },
  tech: { en: "⚙️ Technology Stack", ru: "⚙️ Технологический Стек", tk: "⚙️ Tehnologiýa Steýki" },
};

const TECH_ITEMS = [
  ["⚡", "Next.js + React", "Core framework"],
  ["🗺️", "Leaflet", "Interactive maps"],
  ["🎨", "Tailwind CSS", "Modern styling"],
  ["📦", "Zustand", "State management"],
  ["💾", "JSON", "Data storage"],
  ["🌐", "i18n", "EN / RU / TK"],
];

export function AboutClient({ events }: AboutClientProps) {
  const { t, tCat, locale } = useTranslation();
  const lang = locale;

  const evCount = events.length;
  const cityCount = new Set(events.map(e => e.city)).size;
  const catCount = new Set(events.map(e => e.category)).size;
  const freeCount = events.filter(e => e.price === 0).length;

  const features = FEATURES[lang] || FEATURES.en;
  const steps = HOW_STEPS[lang] || HOW_STEPS.en;
  const citiesTable = CITIES_TABLE[lang] || CITIES_TABLE.en;

  return (
    <>
      <Hero title={t("about_title")} subtitle={t("about_description")} icon="ℹ️" />

      {/* Stats */}
      <div className="grid grid-cols-2 sm:grid-cols-4 gap-4 mb-8">
        <StatCard icon="🎉" value={evCount} label={t("total_events")} />
        <StatCard icon="🏙️" value={cityCount} label={t("cities_covered")} />
        <StatCard icon="🏷️" value={catCount} label={t("categories_count")} />
        <StatCard icon="🆓" value={freeCount} label={t("free_events")} />
      </div>

      {/* What is */}
      <h3 className="text-xl font-semibold mb-3">{SECTION_TITLES.what[lang] || SECTION_TITLES.what.en}</h3>
      <p className="text-text-secondary leading-relaxed mb-8">{ABOUT_INTRO[lang] || ABOUT_INTRO.en}</p>

      <hr className="border-border-subtle mb-8" />

      {/* Features */}
      <h3 className="text-xl font-semibold mb-4">{SECTION_TITLES.features[lang] || SECTION_TITLES.features.en}</h3>
      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-4 mb-8">
        {features.map(([icon, title, desc], i) => (
          <div key={i} className="feature-card">
            <p className="text-3xl mb-3">{icon}</p>
            <h4 className="text-base font-semibold text-text-primary mb-2">{title}</h4>
            <p className="text-sm text-text-secondary leading-relaxed">{desc}</p>
          </div>
        ))}
      </div>

      <hr className="border-border-subtle mb-8" />

      {/* Categories */}
      <h3 className="text-xl font-semibold mb-4">{SECTION_TITLES.categories[lang] || SECTION_TITLES.categories.en}</h3>
      <div className="grid grid-cols-2 sm:grid-cols-4 gap-3 mb-8">
        {Object.entries(CATEGORIES).map(([key, cfg]) => (
          <div key={key} className="bg-bg-secondary border border-border-subtle rounded-xl p-4 text-center">
            <p className="text-3xl mb-1">{cfg.icon}</p>
            <p className="text-sm font-semibold">{tCat(key)}</p>
          </div>
        ))}
      </div>

      <hr className="border-border-subtle mb-8" />

      {/* How it works */}
      <h3 className="text-xl font-semibold mb-4">{SECTION_TITLES.how[lang] || SECTION_TITLES.how.en}</h3>
      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4 mb-8">
        {steps.map(([num, title, desc], i) => (
          <div key={i} className="bg-bg-secondary border border-border-subtle rounded-xl p-5 text-center min-h-[180px]">
            <p className="text-3xl mb-2">{num}</p>
            <h4 className="text-sm font-semibold mb-2">{title}</h4>
            <p className="text-xs text-text-secondary leading-relaxed">{desc}</p>
          </div>
        ))}
      </div>

      <hr className="border-border-subtle mb-8" />

      {/* Cities */}
      <h3 className="text-xl font-semibold mb-4">{SECTION_TITLES.cities[lang] || SECTION_TITLES.cities.en}</h3>
      <div className="overflow-x-auto mb-8">
        <table className="w-full text-sm">
          <thead>
            <tr className="border-b border-border-subtle">
              {citiesTable.headers.map((h, i) => (
                <th key={i} className="text-left py-2 px-4 text-text-secondary font-medium">{h}</th>
              ))}
            </tr>
          </thead>
          <tbody>
            {citiesTable.rows.map((row, i) => (
              <tr key={i} className="border-b border-border-subtle/50">
                <td className="py-2 px-4 font-medium">{row[0]}</td>
                <td className="py-2 px-4 text-text-secondary">{row[1]}</td>
                <td className="py-2 px-4 text-accent-secondary">✅ {row[2]}</td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>

      <hr className="border-border-subtle mb-8" />

      {/* Tech Stack */}
      <h3 className="text-xl font-semibold mb-4">{SECTION_TITLES.tech[lang] || SECTION_TITLES.tech.en}</h3>
      <div className="grid grid-cols-2 sm:grid-cols-3 lg:grid-cols-6 gap-3 mb-8">
        {TECH_ITEMS.map(([icon, name, desc], i) => (
          <div key={i} className="bg-bg-secondary border border-border-subtle rounded-xl p-4 text-center">
            <p className="text-2xl mb-1">{icon}</p>
            <p className="text-xs font-semibold">{name}</p>
            <p className="text-xs text-text-muted">{desc}</p>
          </div>
        ))}
      </div>

      {/* Footer */}
      <hr className="border-border-subtle mb-4" />
      <p className="text-sm text-text-muted italic">
        {lang === "ru" ? "Версия 1.0 — Создано на Next.js — Платформа Открытия Событий Туркменистана" :
         lang === "tk" ? "Wersiýa 1.0 — Next.js bilen döredildi — Türkmenistan üçin Çäre Tapyş Platformasy" :
         "Version 1.0 — Built with Next.js — Event Discovery Platform for Turkmenistan"}
      </p>
    </>
  );
}
