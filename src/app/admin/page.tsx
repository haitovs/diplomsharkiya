"use client";

import { useState, useEffect, useCallback, useRef } from "react";
import { StatCard } from "@/components/ui/StatCard";
import { useTranslation } from "@/i18n/config";
import { useAdminStore } from "@/store/useAdminStore";
import { ADMIN_USERNAME, ADMIN_PASSWORD } from "@/config/constants";
import { CATEGORIES, CATEGORY_NAMES } from "@/config/categories";
import { CITY_NAMES, CITY_COORDS } from "@/config/cities";
import type { Event } from "@/types/event";
import toast from "react-hot-toast";

export default function AdminPage() {
  const { t, tCat, tCity } = useTranslation();
  const { isAuthenticated, login, logout } = useAdminStore();
  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");
  const [events, setEvents] = useState<Event[]>([]);
  const [tab, setTab] = useState<"manage" | "add" | "settings">("manage");
  const [filterCity, setFilterCity] = useState("All");
  const [filterCat, setFilterCat] = useState("All");
  const [searchText, setSearchText] = useState("");
  const [editingEvent, setEditingEvent] = useState<Event | null>(null);

  const [newTitle, setNewTitle] = useState("");
  const [newVenue, setNewVenue] = useState("");
  const [newCity, setNewCity] = useState("Ashgabat");
  const [newCat, setNewCat] = useState("Music");
  const [newPrice, setNewPrice] = useState(0);
  const [newPop, setNewPop] = useState(50);
  const [newDesc, setNewDesc] = useState("");
  const [newDateStart, setNewDateStart] = useState("");
  const [newDateEnd, setNewDateEnd] = useState("");
  const [newUseCityCenter, setNewUseCityCenter] = useState(true);
  const [newImage, setNewImage] = useState<File | null>(null);
  const [newTitleTk, setNewTitleTk] = useState("");
  const [newVenueTk, setNewVenueTk] = useState("");
  const [newDescTk, setNewDescTk] = useState("");
  const [newTitleRu, setNewTitleRu] = useState("");
  const [newVenueRu, setNewVenueRu] = useState("");
  const [newDescRu, setNewDescRu] = useState("");

  const fetchEvents = useCallback(async () => {
    const res = await fetch("/api/events");
    const data = await res.json();
    setEvents(data);
  }, []);

  useEffect(() => {
    if (isAuthenticated) fetchEvents();
  }, [isAuthenticated, fetchEvents]);

  function handleLogin(e: React.FormEvent) {
    e.preventDefault();
    if (username === ADMIN_USERNAME && password === ADMIN_PASSWORD) {
      login(username);
    } else {
      toast.error(t("invalid_credentials"));
    }
  }

  async function uploadImage(file: File, eventId: string): Promise<string> {
    const formData = new FormData();
    formData.append("file", file);
    formData.append("eventId", eventId);
    const res = await fetch("/api/upload", { method: "POST", body: formData });
    const data = await res.json();
    return data.image;
  }

  async function handleAddEvent(e: React.FormEvent) {
    e.preventDefault();
    if (!newTitle || !newVenue) {
      toast.error(t("fill_required"));
      return;
    }
    const coords = newUseCityCenter ? CITY_COORDS[newCity] || { lat: 37.9601, lon: 58.3261 } : { lat: 37.9601, lon: 58.3261 };
    const buildLocale = (tt: string, vv: string, dd: string) => {
      const obj: { title?: string; venue?: string; description?: string } = {};
      if (tt.trim()) obj.title = tt.trim();
      if (vv.trim()) obj.venue = vv.trim();
      if (dd.trim()) obj.description = dd.trim();
      return Object.keys(obj).length ? obj : undefined;
    };
    const tkBlock = buildLocale(newTitleTk, newVenueTk, newDescTk);
    const ruBlock = buildLocale(newTitleRu, newVenueRu, newDescRu);
    const i18n = (tkBlock || ruBlock) ? { ...(tkBlock ? { tk: tkBlock } : {}), ...(ruBlock ? { ru: ruBlock } : {}) } : undefined;
    const body: Record<string, unknown> = {
      title: newTitle, venue: newVenue, city: newCity, category: newCat,
      price: newPrice, popularity: newPop, description: newDesc,
      date_start: newDateStart || new Date(Date.now() + 7 * 86400000).toISOString().slice(0, 16),
      date_end: newDateEnd || new Date(Date.now() + 7 * 86400000 + 10800000).toISOString().slice(0, 16),
      lat: coords.lat, lon: coords.lon,
      image: `images/cat_${newCat.toLowerCase()}.jpg`,
      ...(i18n ? { i18n } : {}),
    };
    const res = await fetch("/api/events", { method: "POST", headers: { "Content-Type": "application/json" }, body: JSON.stringify(body) });
    if (res.ok) {
      const created = await res.json();
      if (newImage && created.id) {
        const imagePath = await uploadImage(newImage, created.id);
        await fetch(`/api/events/${created.id}`, {
          method: "PUT",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({ ...created, image: imagePath }),
        });
      }
      toast.success(t("event_added"));
      setNewTitle(""); setNewVenue(""); setNewDesc(""); setNewImage(null);
      setNewTitleTk(""); setNewVenueTk(""); setNewDescTk("");
      setNewTitleRu(""); setNewVenueRu(""); setNewDescRu("");
      fetchEvents();
    }
  }

  async function handleDelete(id: string) {
    await fetch(`/api/events/${id}`, { method: "DELETE" });
    fetchEvents();
    toast.success(t("event_deleted"));
  }

  async function handleDuplicate(event: Event) {
    const body = { ...event, id: undefined, title: `${event.title} (Copy)` };
    await fetch("/api/events", { method: "POST", headers: { "Content-Type": "application/json" }, body: JSON.stringify(body) });
    fetchEvents();
    toast.success(t("duplicate"));
  }

  async function handleSaveEdit(event: Event, formData: Partial<Event>, imageFile?: File | null) {
    let imagePath = formData.image || event.image;
    if (imageFile) {
      imagePath = await uploadImage(imageFile, event.id);
    }
    await fetch(`/api/events/${event.id}`, {
      method: "PUT",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ ...event, ...formData, image: imagePath }),
    });
    setEditingEvent(null);
    fetchEvents();
    toast.success(t("save"));
  }

  async function handleDeleteAll() {
    const confirmed = prompt(t("confirm_delete"));
    if (confirmed === "DELETE") {
      await fetch("/api/events", { method: "DELETE" });
      fetchEvents();
      toast.success(t("all_events_deleted"));
    }
  }

  async function handleImport(file: File) {
    const text = await file.text();
    try {
      const imported = JSON.parse(text);
      if (Array.isArray(imported)) {
        for (const ev of imported) {
          const existing = events.find(e => e.id === ev.id);
          if (!existing) {
            await fetch("/api/events", { method: "POST", headers: { "Content-Type": "application/json" }, body: JSON.stringify(ev) });
          }
        }
        fetchEvents();
        toast.success(t("events_imported", { count: String(imported.length) }));
      }
    } catch {
      toast.error(t("invalid_json_format"));
    }
  }

  let displayEvents = [...events].reverse();
  if (filterCity !== "All") displayEvents = displayEvents.filter(e => e.city === filterCity);
  if (filterCat !== "All") displayEvents = displayEvents.filter(e => e.category === filterCat);
  if (searchText) displayEvents = displayEvents.filter(e => e.title.toLowerCase().includes(searchText.toLowerCase()));

  const totalEvents = events.length;
  const citiesCount = new Set(events.map(e => e.city)).size;
  const freeCount = events.filter(e => e.price === 0).length;
  const catCount = new Set(events.map(e => e.category)).size;

  const CATEGORY_COLORS: Record<string, string> = {
    Music: "#6366F1", Tech: "#3B82F6", Sports: "#EF4444", Food: "#F59E0B",
    Art: "#EC4899", Market: "#8B5CF6", Film: "#06B6D4", Wellness: "#10B981",
    Business: "#64748B", Science: "#14B8A6", Kids: "#F97316", Travel: "#0EA5E9",
    Community: "#22C55E",
  };

  if (!isAuthenticated) {
    return (
      <div className="max-w-md mx-auto mt-16">
        <div className="card p-8 text-center">
          <p className="text-5xl mb-2">🔐</p>
          <h2 className="text-2xl font-bold mb-1">{t("super_admin")}</h2>
          <p className="text-text-secondary text-sm mb-6">{t("admin_access_desc")}</p>
          <form onSubmit={handleLogin} className="space-y-4 text-left">
            <div>
              <label className="block text-sm font-medium text-text-secondary mb-1">{t("username")}</label>
              <input value={username} onChange={e => setUsername(e.target.value)} className="input" placeholder="admin" />
            </div>
            <div>
              <label className="block text-sm font-medium text-text-secondary mb-1">{t("password")}</label>
              <input type="password" value={password} onChange={e => setPassword(e.target.value)} className="input" />
            </div>
            <button type="submit" className="btn-primary w-full">🔑 {t("login")}</button>
          </form>
        </div>
      </div>
    );
  }

  // Edit page view — replaces the entire admin content
  if (editingEvent) {
    return (
      <>
        <div className="flex items-center gap-3 mb-6">
          <button onClick={() => setEditingEvent(null)} className="btn-ghost text-sm px-3 py-1.5">
            ← {t("back")}
          </button>
          <h2 className="text-xl font-bold text-text-primary">✏️ {t("edit_event")}</h2>
        </div>
        <EditPage
          event={editingEvent}
          onSave={handleSaveEdit}
          onCancel={() => setEditingEvent(null)}
          t={t}
          tCat={tCat}
        />
      </>
    );
  }

  return (
    <>
      <div className="flex items-center justify-between mb-6">
        <h2 className="text-xl font-bold text-text-primary">🛡️ {t("super_admin")} — {t("event_management_system")}</h2>
        <button onClick={logout} className="btn-ghost text-sm">🚪 {t("logout")}</button>
      </div>

      <div className="inline-flex rounded-lg border border-border-subtle bg-bg-secondary p-1 mb-6">
        {(["manage", "add", "settings"] as const).map((key) => {
          const icons = { manage: "📋", add: "➕", settings: "⚙️" };
          const labels = { manage: t("manage_events_tab"), add: t("add_event_tab"), settings: t("settings_tab") };
          return (
            <button
              key={key}
              onClick={() => setTab(key)}
              className={`px-4 py-2 rounded-md text-sm font-medium transition-all ${
                tab === key
                  ? "bg-accent-primary text-white shadow-sm"
                  : "text-text-secondary hover:text-text-primary"
              }`}
            >
              {icons[key]} {labels[key]}
            </button>
          );
        })}
      </div>

      <div className="grid grid-cols-2 sm:grid-cols-4 gap-4 mb-6">
        <StatCard icon="📊" value={totalEvents} label={t("total_events")} />
        <StatCard icon="🏙️" value={citiesCount} label={t("cities_covered")} />
        <StatCard icon="🆓" value={freeCount} label={t("free_events")} />
        <StatCard icon="🏷️" value={catCount} label={t("categories_count")} />
      </div>

      {tab === "manage" && (
        <>
          <div className="grid grid-cols-1 sm:grid-cols-3 gap-3 mb-4">
            <select value={filterCity} onChange={e => setFilterCity(e.target.value)} className="select">
              <option value="All">{t("all_cities")}</option>
              {CITY_NAMES.map(c => <option key={c} value={c}>{tCity(c)}</option>)}
            </select>
            <select value={filterCat} onChange={e => setFilterCat(e.target.value)} className="select">
              <option value="All">{t("all_categories")}</option>
              {CATEGORY_NAMES.map(c => <option key={c} value={c}>{tCat(c)}</option>)}
            </select>
            <input value={searchText} onChange={e => setSearchText(e.target.value)} placeholder={t("search_events")} className="input" />
          </div>

          <p className="text-sm text-text-secondary mb-4">
            {t("showing_of", { count: String(displayEvents.length), total: String(events.length) })}
          </p>

          {displayEvents.length === 0 ? (
            <p className="text-center text-text-secondary py-12">{t("no_events_found")}</p>
          ) : (
            <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-4 mb-8">
              {displayEvents.map(event => {
                const catColor = CATEGORY_COLORS[event.category] || "#6366F1";
                const catConfig = CATEGORIES[event.category];
                return (
                  <div key={event.id} className="card overflow-hidden flex flex-col">
                    <div className="h-1" style={{ background: catColor }} />
                    <div className="p-4 flex-1 flex flex-col">
                      <h4 className="font-semibold text-text-primary truncate mb-1">
                        {catConfig?.icon} {event.title}
                      </h4>
                      <p className="text-sm text-text-secondary truncate mb-2">
                        📍 {event.venue} · {event.city}
                      </p>
                      <div className="flex flex-wrap gap-1.5 mb-3">
                        <span className="cat-badge" style={{ background: `${catColor}15`, color: catColor }}>
                          {tCat(event.category)}
                        </span>
                        <span className={`text-xs px-2 py-0.5 rounded-full font-semibold ${
                          event.price === 0 ? "bg-emerald-50 text-emerald-600" : "bg-indigo-50 text-indigo-600"
                        }`}>
                          {event.price === 0 ? t("free") : `${event.price} TMT`}
                        </span>
                      </div>
                      {event.description && (
                        <p className="text-xs text-text-muted truncate mb-3">{event.description}</p>
                      )}
                      <div className="flex-1" />
                      <div className="flex gap-2 pt-3 border-t border-border-subtle">
                        <button onClick={() => setEditingEvent(event)} className="btn-ghost text-xs px-2.5 py-1.5 flex-1">
                          ✏️ {t("edit")}
                        </button>
                        <button onClick={() => handleDuplicate(event)} className="btn-ghost text-xs px-2.5 py-1.5 flex-1">
                          📋 {t("duplicate")}
                        </button>
                        <button onClick={() => handleDelete(event.id)} className="btn-ghost text-xs px-2.5 py-1.5 flex-1 text-error border-error/20 hover:bg-error/5">
                          🗑️ {t("delete")}
                        </button>
                      </div>
                    </div>
                  </div>
                );
              })}
            </div>
          )}
        </>
      )}

      {tab === "add" && (
        <div className="max-w-2xl mx-auto">
          <div className="card p-6">
            <h3 className="text-lg font-semibold mb-5">➕ {t("add_event")}</h3>
            <form onSubmit={handleAddEvent} className="space-y-5">
              <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
                <div>
                  <label className="block text-sm font-medium text-text-secondary mb-1.5">{t("title_field")} *</label>
                  <input value={newTitle} onChange={e => setNewTitle(e.target.value)} className="input" />
                </div>
                <div>
                  <label className="block text-sm font-medium text-text-secondary mb-1.5">{t("venue_label")} *</label>
                  <input value={newVenue} onChange={e => setNewVenue(e.target.value)} className="input" />
                </div>
                <div>
                  <label className="block text-sm font-medium text-text-secondary mb-1.5">{t("event_city")}</label>
                  <select value={newCity} onChange={e => setNewCity(e.target.value)} className="select">
                    {CITY_NAMES.map(c => <option key={c} value={c}>{c}</option>)}
                  </select>
                </div>
                <div>
                  <label className="block text-sm font-medium text-text-secondary mb-1.5">{t("event_category")}</label>
                  <select value={newCat} onChange={e => setNewCat(e.target.value)} className="select">
                    {CATEGORY_NAMES.map(c => <option key={c} value={c}>{tCat(c)}</option>)}
                  </select>
                </div>
                <div>
                  <label className="block text-sm font-medium text-text-secondary mb-1.5">{t("start_date")}</label>
                  <input type="datetime-local" value={newDateStart} onChange={e => setNewDateStart(e.target.value)} className="input" />
                </div>
                <div>
                  <label className="block text-sm font-medium text-text-secondary mb-1.5">{t("end_date")}</label>
                  <input type="datetime-local" value={newDateEnd} onChange={e => setNewDateEnd(e.target.value)} className="input" />
                </div>
                <div>
                  <label className="block text-sm font-medium text-text-secondary mb-1.5">{t("price_label")} (TMT)</label>
                  <input type="number" value={newPrice} onChange={e => setNewPrice(Number(e.target.value))} min={0} step={5} className="input" />
                </div>
                <div>
                  <label className="block text-sm font-medium text-text-secondary mb-1.5">{t("popularity")}: {newPop}</label>
                  <input type="range" value={newPop} onChange={e => setNewPop(Number(e.target.value))} min={1} max={100} className="w-full accent-accent-primary mt-2" />
                </div>
              </div>
              <div>
                <label className="block text-sm font-medium text-text-secondary mb-1.5">{t("event_description")}</label>
                <textarea value={newDesc} onChange={e => setNewDesc(e.target.value)} className="input min-h-[100px] resize-y" />
              </div>
              <div className="border-t border-border-subtle pt-5">
                <div className="mb-3">
                  <h3 className="text-sm font-semibold text-text-primary">🌐 {t("translations")}</h3>
                  <p className="text-xs text-text-muted mt-0.5">{t("translations_hint")}</p>
                </div>
                <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
                  <div>
                    <label className="block text-sm font-medium text-text-secondary mb-1.5">{t("title_tk")}</label>
                    <input value={newTitleTk} onChange={e => setNewTitleTk(e.target.value)} className="input" />
                  </div>
                  <div>
                    <label className="block text-sm font-medium text-text-secondary mb-1.5">{t("title_ru")}</label>
                    <input value={newTitleRu} onChange={e => setNewTitleRu(e.target.value)} className="input" />
                  </div>
                  <div>
                    <label className="block text-sm font-medium text-text-secondary mb-1.5">{t("venue_tk")}</label>
                    <input value={newVenueTk} onChange={e => setNewVenueTk(e.target.value)} className="input" />
                  </div>
                  <div>
                    <label className="block text-sm font-medium text-text-secondary mb-1.5">{t("venue_ru")}</label>
                    <input value={newVenueRu} onChange={e => setNewVenueRu(e.target.value)} className="input" />
                  </div>
                  <div className="sm:col-span-2">
                    <label className="block text-sm font-medium text-text-secondary mb-1.5">{t("description_tk")}</label>
                    <textarea value={newDescTk} onChange={e => setNewDescTk(e.target.value)} className="input min-h-[80px] resize-y" />
                  </div>
                  <div className="sm:col-span-2">
                    <label className="block text-sm font-medium text-text-secondary mb-1.5">{t("description_ru")}</label>
                    <textarea value={newDescRu} onChange={e => setNewDescRu(e.target.value)} className="input min-h-[80px] resize-y" />
                  </div>
                </div>
              </div>
              <div>
                <label className="block text-sm font-medium text-text-secondary mb-1.5">{t("upload_image")}</label>
                <ImageDropZone file={newImage} onFile={setNewImage} t={t} />
              </div>
              <label className="flex items-center gap-2 text-sm text-text-secondary">
                <input type="checkbox" checked={newUseCityCenter} onChange={e => setNewUseCityCenter(e.target.checked)} className="accent-accent-primary" />
                {t("use_city_center")}
              </label>
              <button type="submit" className="btn-primary w-full py-2.5">➕ {t("add_event")}</button>
            </form>
          </div>
        </div>
      )}

      {tab === "settings" && (
        <div className="grid grid-cols-1 sm:grid-cols-2 gap-6">
          <div className="card p-6">
            <h4 className="font-semibold mb-4">📤 {t("export_events")}</h4>
            <p className="text-sm text-text-secondary mb-4">{events.length} {t("events_found")}</p>
            <button
              onClick={() => {
                const blob = new Blob([JSON.stringify(events, null, 2)], { type: "application/json" });
                const url = URL.createObjectURL(blob);
                const a = document.createElement("a");
                a.href = url; a.download = `events_${new Date().toISOString().slice(0, 10)}.json`;
                a.click(); URL.revokeObjectURL(url);
              }}
              className="btn-primary w-full"
            >⬇️ {t("download_json")}</button>
          </div>
          <div className="card p-6">
            <h4 className="font-semibold mb-4">📥 {t("import_events")}</h4>
            <input type="file" accept=".json" onChange={e => e.target.files?.[0] && handleImport(e.target.files[0])} className="input" />
          </div>
          <div className="card p-6 sm:col-span-2 border-error/30">
            <h4 className="font-semibold text-error mb-4">⚠️ {t("danger_zone")}</h4>
            <p className="text-sm text-text-secondary mb-4">{t("cannot_be_undone")}</p>
            <button onClick={handleDeleteAll} className="btn-ghost text-error border-error/30 hover:bg-error/5 w-full">🗑️ {t("delete_all")}</button>
          </div>
        </div>
      )}

      <hr className="border-border-subtle mt-8 mb-4" />
      <p className="text-xs text-text-muted">🛡️ {t("super_admin")} v3.0</p>
    </>
  );
}

// ── Image drop zone ──────────────────────────────────────────────
function ImageDropZone({ file, onFile, currentImage, t }: {
  file: File | null;
  onFile: (f: File | null) => void;
  currentImage?: string;
  t: (key: string) => string;
}) {
  const inputRef = useRef<HTMLInputElement>(null);
  const [dragging, setDragging] = useState(false);
  const preview = file ? URL.createObjectURL(file) : currentImage ? `/${currentImage}` : null;

  function handleDrop(e: React.DragEvent) {
    e.preventDefault();
    setDragging(false);
    const f = e.dataTransfer.files[0];
    if (f && f.type.startsWith("image/")) onFile(f);
  }

  return (
    <div
      onDragOver={e => { e.preventDefault(); setDragging(true); }}
      onDragLeave={() => setDragging(false)}
      onDrop={handleDrop}
      onClick={() => inputRef.current?.click()}
      className={`relative border-2 border-dashed rounded-xl p-4 text-center cursor-pointer transition-colors ${
        dragging
          ? "border-accent-primary bg-accent-primary/5"
          : "border-border-subtle hover:border-accent-primary/40"
      }`}
    >
      <input
        ref={inputRef}
        type="file"
        accept="image/*"
        className="hidden"
        onChange={e => {
          const f = e.target.files?.[0];
          if (f) onFile(f);
        }}
      />
      {preview ? (
        <div className="relative">
          {/* eslint-disable-next-line @next/next/no-img-element */}
          <img src={preview} alt="Preview" className="max-h-48 mx-auto rounded-lg object-cover" />
          <button
            type="button"
            onClick={e => { e.stopPropagation(); onFile(null); }}
            className="absolute top-1 right-1 bg-white/90 hover:bg-white rounded-full w-6 h-6 flex items-center justify-center text-xs text-error shadow"
          >✕</button>
        </div>
      ) : (
        <div className="py-6">
          <p className="text-3xl mb-2">📷</p>
          <p className="text-sm text-text-secondary">{t("drag_drop_image")}</p>
          <p className="text-xs text-text-muted mt-1">{t("or_click_to_browse")}</p>
        </div>
      )}
    </div>
  );
}

// ── Full edit page ───────────────────────────────────────────────
function EditPage({ event, onSave, onCancel, t, tCat }: {
  event: Event;
  onSave: (event: Event, data: Partial<Event>, imageFile?: File | null) => void;
  onCancel: () => void;
  t: (key: string) => string;
  tCat: (cat: string) => string;
}) {
  const [title, setTitle] = useState(event.title);
  const [venue, setVenue] = useState(event.venue);
  const [city, setCity] = useState(event.city);
  const [category, setCategory] = useState(event.category);
  const [price, setPrice] = useState(event.price);
  const [popularity, setPopularity] = useState(event.popularity);
  const [description, setDescription] = useState(event.description);
  const [dateStart, setDateStart] = useState(event.date_start?.slice(0, 16) || "");
  const [dateEnd, setDateEnd] = useState(event.date_end?.slice(0, 16) || "");
  const [useCityCenter, setUseCityCenter] = useState(false);
  const [imageFile, setImageFile] = useState<File | null>(null);

  const [titleTk, setTitleTk] = useState(event.i18n?.tk?.title || "");
  const [venueTk, setVenueTk] = useState(event.i18n?.tk?.venue || "");
  const [descTk, setDescTk] = useState(event.i18n?.tk?.description || "");
  const [titleRu, setTitleRu] = useState(event.i18n?.ru?.title || "");
  const [venueRu, setVenueRu] = useState(event.i18n?.ru?.venue || "");
  const [descRu, setDescRu] = useState(event.i18n?.ru?.description || "");

  function handleSubmit(e: React.FormEvent) {
    e.preventDefault();
    const coords = useCityCenter ? CITY_COORDS[city] || { lat: event.lat, lon: event.lon } : { lat: event.lat, lon: event.lon };
    const buildLocale = (tt: string, vv: string, dd: string) => {
      const obj: { title?: string; venue?: string; description?: string } = {};
      if (tt.trim()) obj.title = tt.trim();
      if (vv.trim()) obj.venue = vv.trim();
      if (dd.trim()) obj.description = dd.trim();
      return Object.keys(obj).length ? obj : undefined;
    };
    const tkBlock = buildLocale(titleTk, venueTk, descTk);
    const ruBlock = buildLocale(titleRu, venueRu, descRu);
    const i18n = (tkBlock || ruBlock) ? { ...(tkBlock ? { tk: tkBlock } : {}), ...(ruBlock ? { ru: ruBlock } : {}) } : undefined;
    onSave(event, {
      title, venue, city, category, price, popularity, description,
      date_start: dateStart || event.date_start,
      date_end: dateEnd || event.date_end,
      lat: coords.lat, lon: coords.lon,
      i18n,
    }, imageFile);
  }

  return (
    <div className="max-w-3xl mx-auto">
      <div className="card p-6">
        <form onSubmit={handleSubmit} className="space-y-5">
          {/* Image */}
          <div>
            <label className="block text-sm font-medium text-text-secondary mb-1.5">{t("upload_image")}</label>
            <ImageDropZone file={imageFile} onFile={setImageFile} currentImage={event.image} t={t} />
          </div>

          <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
            <div>
              <label className="block text-sm font-medium text-text-secondary mb-1.5">{t("title_field")}</label>
              <input value={title} onChange={e => setTitle(e.target.value)} className="input" />
            </div>
            <div>
              <label className="block text-sm font-medium text-text-secondary mb-1.5">{t("venue_label")}</label>
              <input value={venue} onChange={e => setVenue(e.target.value)} className="input" />
            </div>
            <div>
              <label className="block text-sm font-medium text-text-secondary mb-1.5">{t("event_city")}</label>
              <select value={city} onChange={e => setCity(e.target.value)} className="select">
                {CITY_NAMES.map(c => <option key={c} value={c}>{c}</option>)}
              </select>
            </div>
            <div>
              <label className="block text-sm font-medium text-text-secondary mb-1.5">{t("event_category")}</label>
              <select value={category} onChange={e => setCategory(e.target.value)} className="select">
                {CATEGORY_NAMES.map(c => <option key={c} value={c}>{tCat(c)}</option>)}
              </select>
            </div>
            <div>
              <label className="block text-sm font-medium text-text-secondary mb-1.5">{t("start_date")}</label>
              <input type="datetime-local" value={dateStart} onChange={e => setDateStart(e.target.value)} className="input" />
            </div>
            <div>
              <label className="block text-sm font-medium text-text-secondary mb-1.5">{t("end_date")}</label>
              <input type="datetime-local" value={dateEnd} onChange={e => setDateEnd(e.target.value)} className="input" />
            </div>
            <div>
              <label className="block text-sm font-medium text-text-secondary mb-1.5">{t("price_label")} (TMT)</label>
              <input type="number" value={price} onChange={e => setPrice(Number(e.target.value))} min={0} step={5} className="input" />
            </div>
            <div>
              <label className="block text-sm font-medium text-text-secondary mb-1.5">{t("popularity")}: {popularity}</label>
              <input type="range" value={popularity} onChange={e => setPopularity(Number(e.target.value))} min={1} max={100} className="w-full accent-accent-primary mt-2" />
            </div>
          </div>

          <div>
            <label className="block text-sm font-medium text-text-secondary mb-1.5">{t("event_description")}</label>
            <textarea value={description} onChange={e => setDescription(e.target.value)} className="input min-h-[120px] resize-y" />
          </div>

          {/* Per-language translations */}
          <div className="border-t border-border-subtle pt-5">
            <div className="mb-3">
              <h3 className="text-sm font-semibold text-text-primary">🌐 {t("translations")}</h3>
              <p className="text-xs text-text-muted mt-0.5">{t("translations_hint")}</p>
            </div>
            <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
              <div>
                <label className="block text-sm font-medium text-text-secondary mb-1.5">{t("title_tk")}</label>
                <input value={titleTk} onChange={e => setTitleTk(e.target.value)} className="input" />
              </div>
              <div>
                <label className="block text-sm font-medium text-text-secondary mb-1.5">{t("title_ru")}</label>
                <input value={titleRu} onChange={e => setTitleRu(e.target.value)} className="input" />
              </div>
              <div>
                <label className="block text-sm font-medium text-text-secondary mb-1.5">{t("venue_tk")}</label>
                <input value={venueTk} onChange={e => setVenueTk(e.target.value)} className="input" />
              </div>
              <div>
                <label className="block text-sm font-medium text-text-secondary mb-1.5">{t("venue_ru")}</label>
                <input value={venueRu} onChange={e => setVenueRu(e.target.value)} className="input" />
              </div>
              <div className="sm:col-span-2">
                <label className="block text-sm font-medium text-text-secondary mb-1.5">{t("description_tk")}</label>
                <textarea value={descTk} onChange={e => setDescTk(e.target.value)} className="input min-h-[100px] resize-y" />
              </div>
              <div className="sm:col-span-2">
                <label className="block text-sm font-medium text-text-secondary mb-1.5">{t("description_ru")}</label>
                <textarea value={descRu} onChange={e => setDescRu(e.target.value)} className="input min-h-[100px] resize-y" />
              </div>
            </div>
          </div>

          <label className="flex items-center gap-2 text-sm text-text-secondary">
            <input type="checkbox" checked={useCityCenter} onChange={e => setUseCityCenter(e.target.checked)} className="accent-accent-primary" />
            {t("use_city_center")}
          </label>

          <div className="flex gap-3 pt-2">
            <button type="submit" className="btn-primary flex-1 py-2.5">💾 {t("save")}</button>
            <button type="button" onClick={onCancel} className="btn-ghost flex-1 py-2.5">{t("cancel")}</button>
          </div>
        </form>
      </div>
    </div>
  );
}
