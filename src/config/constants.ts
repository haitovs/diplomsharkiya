export const APP_TITLE = "Event Discovery";
export const APP_ICON = "🎟️";
export const VERSION = "1.0.0";
export const CURRENCY = "TMT";
export const TIMEZONE = "Asia/Ashgabat";
export const EVENTS_PER_PAGE = 20;

export const DATE_PRESETS = ["All", "Today", "This Week", "This Month"] as const;
export const SORT_OPTIONS = [
  "Date (Soonest)",
  "Price (Low to High)",
  "Price (High to Low)",
  "Popularity",
] as const;

export const PRICE_RANGE = { min: 0, max: 200 };

export const ADMIN_USERNAME = "admin";
export const ADMIN_PASSWORD = "admin";
