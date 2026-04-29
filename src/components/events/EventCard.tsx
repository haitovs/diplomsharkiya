"use client";

import Image from "next/image";
import { CATEGORIES } from "@/config/categories";
import { useTranslation } from "@/i18n/config";
import { useUIStore } from "@/store/useUIStore";
import { usePaymentStore } from "@/store/usePaymentStore";
import { formatDate, formatTime, formatPrice } from "@/lib/utils";
import type { Event } from "@/types/event";

interface EventCardProps {
  event: Event;
  onBuyTicket?: (event: Event) => void;
}

export function EventCard({ event, onBuyTicket }: EventCardProps) {
  const { t, tCat, tCity, tEvent } = useTranslation();
  const { isSaved, toggleSave } = useUIStore();
  const { getEventPurchaseCount } = usePaymentStore();
  const saved = isSaved(event.id);
  const purchaseCount = getEventPurchaseCount(event.id);
  const config = CATEGORIES[event.category];
  const catIcon = config?.icon || "📌";
  const catHex = config?.hex || "#6366F1";
  const isFree = event.price === 0;
  const title = tEvent(event, "title");
  const venue = tEvent(event, "venue");
  const description = tEvent(event, "description");

  return (
    <div className="evt-card" style={{ borderLeft: `4px solid ${catHex}` }}>
      <div className="flex">
        {/* Image */}
        <div className="relative w-[28%] min-h-[110px] shrink-0">
          <Image
            src={`/images/${event.image.replace("images/", "")}`}
            alt={title}
            fill
            className="object-cover"
            sizes="200px"
          />
        </div>

        {/* Content */}
        <div className="flex-1 p-4 flex flex-col justify-center min-w-0">
          <div className="flex items-center justify-between gap-2 mb-1">
            <div className="flex items-center gap-2">
              <span className="text-xl">{catIcon}</span>
              <span className="cat-badge">{tCat(event.category)}</span>
            </div>
            <span className={`price-badge shrink-0 ${isFree ? "price-free" : "price-paid"}`}>
              {formatPrice(event.price, t("free"))}
            </span>
          </div>

          <h4 className="text-lg font-semibold text-text-primary truncate">{title}</h4>
          <p className="text-sm text-text-secondary mt-1 truncate">
            📍 {venue} · {tCity(event.city)} &nbsp; 📅 {formatDate(event.date_start)} · {formatTime(event.date_start)}
          </p>
          {description && (
            <p className="text-sm text-text-secondary mt-1 line-clamp-2">{description}</p>
          )}

          {/* Action buttons */}
          <div className="flex items-center gap-2 mt-3">
            {event.price > 0 && (
              <button
                onClick={() => onBuyTicket?.(event)}
                className="btn-primary text-sm px-3 py-1.5"
              >
                🎫 {t("buy_ticket")}
              </button>
            )}
            {purchaseCount > 0 && (
              <span className="text-xs text-accent-secondary font-semibold">
                ✅ ×{purchaseCount}
              </span>
            )}
            <button
              onClick={() => toggleSave(event.id)}
              className="ml-auto text-2xl transition-transform hover:scale-110"
              title={saved ? t("remove") : t("save")}
            >
              {saved ? "❤️" : "🤍"}
            </button>
          </div>
        </div>
      </div>
    </div>
  );
}
