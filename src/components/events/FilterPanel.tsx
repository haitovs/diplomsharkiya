"use client";

import { useTranslation } from "@/i18n/config";
import { useFilterStore } from "@/store/useFilterStore";
import { CATEGORY_NAMES } from "@/config/categories";
import { CITY_NAMES } from "@/config/cities";
import { DATE_PRESETS, SORT_OPTIONS, PRICE_RANGE } from "@/config/constants";

export function FilterPanel() {
  const { t, tCat, tCity } = useTranslation();
  const {
    city, categories, datePreset, maxPrice, searchQuery, sortBy,
    setCity, toggleCategory, setDatePreset, setMaxPrice, setSearchQuery, setSortBy, resetFilters,
  } = useFilterStore();

  return (
    <div className="space-y-5">
      {/* Search */}
      <div>
        <label className="block text-sm font-medium text-text-secondary mb-1.5">{t("search")}</label>
        <input
          type="text"
          value={searchQuery}
          onChange={(e) => setSearchQuery(e.target.value)}
          placeholder={t("search_events")}
          className="input"
        />
      </div>

      {/* City */}
      <div>
        <label className="block text-sm font-medium text-text-secondary mb-1.5">{t("filter_by_city")}</label>
        <select
          value={city}
          onChange={(e) => setCity(e.target.value)}
          className="select"
        >
          <option value="All Cities">{t("all_cities")}</option>
          {CITY_NAMES.map((c) => (
            <option key={c} value={c}>{tCity(c)}</option>
          ))}
        </select>
      </div>

      {/* Categories */}
      <div>
        <label className="block text-sm font-medium text-text-secondary mb-1.5">{t("filter_by_category")}</label>
        <div className="flex flex-wrap gap-1.5">
          {CATEGORY_NAMES.map((cat) => (
            <button
              key={cat}
              onClick={() => toggleCategory(cat)}
              className={`text-xs px-2.5 py-1 rounded-full font-medium transition-colors ${
                categories.includes(cat)
                  ? "bg-accent-primary/20 text-accent-primary border border-accent-primary/40"
                  : "bg-bg-card text-text-secondary border border-border-subtle hover:border-accent-primary/30"
              }`}
            >
              {tCat(cat)}
            </button>
          ))}
        </div>
      </div>

      {/* Date Preset */}
      <div>
        <label className="block text-sm font-medium text-text-secondary mb-1.5">{t("event_date")}</label>
        <div className="flex flex-wrap gap-1.5">
          {DATE_PRESETS.map((preset) => (
            <button
              key={preset}
              onClick={() => setDatePreset(preset)}
              className={`text-xs px-3 py-1.5 rounded-lg font-medium transition-colors ${
                datePreset === preset
                  ? "bg-accent-primary text-white"
                  : "bg-bg-card text-text-secondary hover:bg-accent-primary/10"
              }`}
            >
              {t(preset.toLowerCase().replace(/ /g, "_"))}
            </button>
          ))}
        </div>
      </div>

      {/* Price */}
      <div>
        <label className="block text-sm font-medium text-text-secondary mb-1.5">
          {t("event_price")}: {maxPrice} TMT
        </label>
        <input
          type="range"
          min={PRICE_RANGE.min}
          max={PRICE_RANGE.max}
          value={maxPrice}
          onChange={(e) => setMaxPrice(Number(e.target.value))}
          className="w-full accent-accent-primary"
        />
      </div>

      {/* Sort */}
      <div>
        <label className="block text-sm font-medium text-text-secondary mb-1.5">{t("sort_by")}</label>
        <select
          value={sortBy}
          onChange={(e) => setSortBy(e.target.value)}
          className="select"
        >
          {SORT_OPTIONS.map((opt) => {
            const keyMap: Record<string, string> = {
              "Date (Soonest)": "date_soonest",
              "Price (Low to High)": "price_low_high",
              "Price (High to Low)": "price_high_low",
              "Popularity": "popularity",
            };
            return <option key={opt} value={opt}>{t(keyMap[opt] || opt)}</option>;
          })}
        </select>
      </div>

      {/* Reset */}
      <button onClick={resetFilters} className="btn-ghost w-full text-sm">
        🗑️ {t("reset_filters")}
      </button>
    </div>
  );
}
