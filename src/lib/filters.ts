import { Event, FilterState } from "@/types/event";
import { startOfDay, addDays, startOfMonth, addMonths } from "date-fns";

export function filterByDate(events: Event[], preset: string): Event[] {
  if (preset === "All") return events;

  const today = startOfDay(new Date());

  switch (preset) {
    case "Today":
      return events.filter(e => {
        const d = new Date(e.date_start);
        return d >= today && d < addDays(today, 1);
      });
    case "This Week":
      return events.filter(e => {
        const d = new Date(e.date_start);
        return d >= today && d < addDays(today, 7);
      });
    case "This Month": {
      const nextMonth = startOfMonth(addMonths(today, 1));
      return events.filter(e => {
        const d = new Date(e.date_start);
        return d >= today && d < nextMonth;
      });
    }
    default:
      return events;
  }
}

export function applyFilters(events: Event[], filters: FilterState): Event[] {
  let filtered = events;

  // City
  if (filters.city && filters.city !== "All Cities") {
    filtered = filtered.filter(e => e.city === filters.city);
  }

  // Categories
  if (filters.categories.length > 0) {
    filtered = filtered.filter(e => filters.categories.includes(e.category));
  }

  // Date
  filtered = filterByDate(filtered, filters.datePreset);

  // Price
  if (filters.maxPrice < 200) {
    filtered = filtered.filter(e => e.price <= filters.maxPrice);
  }

  // Search
  if (filters.searchQuery) {
    const q = filters.searchQuery.toLowerCase();
    filtered = filtered.filter(
      e =>
        e.title.toLowerCase().includes(q) ||
        e.venue.toLowerCase().includes(q)
    );
  }

  return filtered;
}

export function sortEvents(events: Event[], sortBy: string): Event[] {
  const sorted = [...events];
  switch (sortBy) {
    case "Date (Soonest)":
      return sorted.sort((a, b) => new Date(a.date_start).getTime() - new Date(b.date_start).getTime());
    case "Price (Low to High)":
      return sorted.sort((a, b) => a.price - b.price);
    case "Price (High to Low)":
      return sorted.sort((a, b) => b.price - a.price);
    case "Popularity":
      return sorted.sort((a, b) => b.popularity - a.popularity);
    default:
      return sorted;
  }
}
