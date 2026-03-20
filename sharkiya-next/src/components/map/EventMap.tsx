"use client";

import { useEffect, useRef } from "react";
import { CATEGORIES } from "@/config/categories";
import { DEFAULT_CENTER, DEFAULT_ZOOM } from "@/config/cities";
import { formatDate, formatTime, formatPrice } from "@/lib/utils";
import type { Event } from "@/types/event";

interface EventMapProps {
  events: Event[];
  onBuyTicket?: (event: Event) => void;
}

declare global {
  interface Window {
    L: any;
    __mapBuyTicket?: (eventId: string) => void;
  }
}

export function EventMap({ events, onBuyTicket }: EventMapProps) {
  const mapRef = useRef<HTMLDivElement>(null);
  const mapInstanceRef = useRef<any>(null);
  const markersRef = useRef<any[]>([]);

  useEffect(() => {
    // Load Leaflet CSS
    if (!document.getElementById("leaflet-css")) {
      const link = document.createElement("link");
      link.id = "leaflet-css";
      link.rel = "stylesheet";
      link.href = "https://unpkg.com/leaflet@1.9.4/dist/leaflet.css";
      document.head.appendChild(link);
    }

    // Load Leaflet JS
    function loadScript(): Promise<void> {
      if (window.L) return Promise.resolve();
      return new Promise((resolve) => {
        if (document.getElementById("leaflet-js")) {
          const check = setInterval(() => {
            if (window.L) { clearInterval(check); resolve(); }
          }, 50);
          return;
        }
        const script = document.createElement("script");
        script.id = "leaflet-js";
        script.src = "https://unpkg.com/leaflet@1.9.4/dist/leaflet.js";
        script.onload = () => resolve();
        document.head.appendChild(script);
      });
    }

    loadScript().then(() => {
      if (!mapRef.current || mapInstanceRef.current) return;

      const L = window.L;
      const map = L.map(mapRef.current).setView(
        [DEFAULT_CENTER.lat, DEFAULT_CENTER.lon],
        DEFAULT_ZOOM
      );

      const osm = L.tileLayer("https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png", {
        attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a>',
      }).addTo(map);

      const carto = L.tileLayer("https://{s}.basemaps.cartocdn.com/light_all/{z}/{x}/{y}{r}.png", {
        attribution: '&copy; <a href="https://carto.com/">CARTO</a>',
      });

      const satellite = L.tileLayer("https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}", {
        attribution: "Esri",
      });

      L.control.layers({
        "OpenStreetMap": osm,
        "Light Mode": carto,
        "Satellite": satellite,
      }).addTo(map);

      mapInstanceRef.current = map;
    });

    return () => {
      if (mapInstanceRef.current) {
        mapInstanceRef.current.remove();
        mapInstanceRef.current = null;
      }
    };
  }, []);

  // Register global callback for popup buy buttons
  useEffect(() => {
    window.__mapBuyTicket = (eventId: string) => {
      const event = events.find(e => e.id === eventId);
      if (event && onBuyTicket) onBuyTicket(event);
    };
    return () => { delete window.__mapBuyTicket; };
  }, [events, onBuyTicket]);

  // Update markers when events change
  useEffect(() => {
    if (!mapInstanceRef.current || !window.L) return;

    const L = window.L;
    const map = mapInstanceRef.current;

    // Clear existing markers
    markersRef.current.forEach(m => map.removeLayer(m));
    markersRef.current = [];

    const bounds: [number, number][] = [];

    events.forEach(event => {
      if (!event.lat || !event.lon) return;

      const config = CATEGORIES[event.category];
      const icon = config?.icon || "📌";

      const divIcon = L.divIcon({
        html: `<span style="font-size:24px;filter:drop-shadow(0 2px 4px rgba(0,0,0,0.5))">${icon}</span>`,
        className: "",
        iconSize: [30, 30],
        iconAnchor: [15, 15],
      });

      const buyBtn = event.price > 0 && onBuyTicket
        ? `<button onclick="window.__mapBuyTicket('${event.id}')" style="margin-top:8px;width:100%;padding:6px 0;background:linear-gradient(135deg,#6366F1,#8B5CF6);color:#fff;border:none;border-radius:6px;font-size:12px;font-weight:600;cursor:pointer">🎫 Buy Ticket — ${formatPrice(event.price)}</button>`
        : event.price === 0
          ? `<div style="margin-top:8px;text-align:center;padding:4px 0;background:#ECFDF5;color:#059669;border-radius:6px;font-size:12px;font-weight:600">Free</div>`
          : "";

      const popupHtml = `
        <div style="font-family:Inter,sans-serif;min-width:200px;">
          <h4 style="margin:0 0 6px;font-size:14px;font-weight:600;color:#1E293B">${event.title}</h4>
          <p style="margin:2px 0;color:#64748B;font-size:12px">📍 ${event.venue}</p>
          <p style="margin:2px 0;color:#64748B;font-size:12px">📅 ${formatDate(event.date_start)} ${formatTime(event.date_start)}</p>
          <div style="display:flex;align-items:center;gap:6px;margin-top:6px;font-size:12px">
            <span style="background:#E2E8F0;padding:2px 8px;border-radius:4px">${event.category}</span>
            <span style="font-weight:bold;color:#6366F1">${formatPrice(event.price)}</span>
          </div>
          ${buyBtn}
        </div>
      `;

      const marker = L.marker([event.lat, event.lon], { icon: divIcon })
        .bindPopup(popupHtml, { maxWidth: 300 })
        .bindTooltip(event.title)
        .addTo(map);

      markersRef.current.push(marker);
      bounds.push([event.lat, event.lon]);
    });

    if (bounds.length > 1) {
      map.fitBounds(bounds, { padding: [30, 30] });
    } else if (bounds.length === 1) {
      map.setView(bounds[0], 13);
    }
  }, [events, onBuyTicket]);

  return (
    <div
      ref={mapRef}
      className="w-full h-[600px] rounded-xl overflow-hidden border border-border-subtle"
      style={{ zIndex: 1 }}
    />
  );
}
