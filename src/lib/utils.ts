import { format, parseISO } from "date-fns";

export function formatPrice(price: number, freeText: string = "Free"): string {
  return price === 0 ? freeText : `${Math.round(price)} TMT`;
}

export function formatDate(dateStr: string): string {
  try {
    return format(parseISO(dateStr), "MMM d, yyyy");
  } catch {
    return "TBD";
  }
}

export function formatTime(dateStr: string): string {
  try {
    return format(parseISO(dateStr), "HH:mm");
  } catch {
    return "";
  }
}

export function formatDateRange(start: string, end: string): string {
  const startDate = formatDate(start);
  const startTime = formatTime(start);
  const endTime = formatTime(end);
  return `${startDate} · ${startTime} – ${endTime}`;
}

export function cn(...classes: (string | boolean | undefined | null)[]): string {
  return classes.filter(Boolean).join(" ");
}
