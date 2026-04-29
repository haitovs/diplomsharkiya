export interface EventTranslation {
  title?: string;
  description?: string;
  venue?: string;
}

export interface Event {
  id: string;
  title: string;
  category: string;
  city: string;
  venue: string;
  date_start: string;
  date_end: string;
  price: number;
  popularity: number;
  lat: number;
  lon: number;
  image: string;
  description: string;
  icon?: string;
  i18n?: {
    en?: EventTranslation;
    ru?: EventTranslation;
    tk?: EventTranslation;
  };
}

export interface FilterState {
  city: string;
  categories: string[];
  datePreset: string;
  maxPrice: number;
  searchQuery: string;
  sortBy: string;
}

export interface Transaction {
  id: string;
  eventId: string;
  title: string;
  amount: number;
  name: string;
  cardLast4: string;
  date: string;
}

export type Locale = "en" | "ru" | "tk";
